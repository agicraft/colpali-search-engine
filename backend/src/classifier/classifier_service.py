from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging
from typing import Any, List, Optional, Tuple

import pydantic
from sqlalchemy import func

from ..utils.dates import timestamp_ms
from .mime_types import MimeType

from ..utils.strings import to_snake_case

from ..utils.data_table import FilteringQuery, FilteringResult, apply_filter_to_db_query

from .classifier_models import Document, DocumentChunk, DocumentContent, DocumentPage
from sqlalchemy.orm import Query, Session

logger = logging.getLogger(__name__)

CLASSIFIER_SERVICE_NAME = "classifier_service"
DOC_INDEXER_SERVICE_NAME = "doc_indexer_service"
RAG_SERVICE_NAME = "rag_service"
DOC_PROCESSOR_SERVICE_NAME = "doc_processor_service"
MAX_IMAGES = 2


class DocInfo(pydantic.BaseModel):
    id: int
    name: str
    mime: str
    created_at: int
    indexed: bool
    num_pages: Optional[int] = 1
    num_chunks: Optional[int] = 1


class SearchResult(pydantic.BaseModel):
    name: str
    mime: str
    created_at: int
    doc_id: int
    page_id: int
    chunk_id: int


class RenderImageInfo(pydantic.BaseModel):
    mime: str
    image: bytes


class DocDownloadInfo(pydantic.BaseModel):
    mime: str
    name: str
    content: bytes


class DocPreviewInfo(pydantic.BaseModel):
    id: int
    name: str
    pages: List[int]


class DocProcessor(ABC):
    @abstractmethod
    def extract_pages(
        self, doc: Document, doc_content: DocumentContent
    ) -> List[bytes]: ...

    @abstractmethod
    def chunk_pages(
        self, pages: List[DocumentPage]
    ) -> List[Tuple[DocumentPage, bytes]]: ...


class DocIndexer(ABC):
    @abstractmethod
    def index(self, doc: Document): ...

    @abstractmethod
    def query(self, query: str) -> List[int]: ...

    @abstractmethod
    def interpret(self, query: str, image: bytes) -> bytes: ...

    @abstractmethod
    def delete(self, doc: Document): ...


class RagService(ABC):
    @abstractmethod
    def question(self, prompt: str, images: List[bytes]) -> str: ...


scanning_doc_ids = set()


class ClassifierService:

    def find_documents_by_query(
        self, db: Session, query: str, doc_indexer: DocIndexer
    ) -> List[SearchResult]:

        found_chunk_ids = doc_indexer.query(query)
        if not found_chunk_ids:
            return []

        docs = (
            db.query(Document, DocumentChunk.id)
            .select_from(DocumentChunk)
            .join(Document)
            .filter(DocumentChunk.id.in_(found_chunk_ids))
            .all()
        )
        chunk_doc_map = {chunk_id: doc for doc, chunk_id in docs}

        chunk_pages = (
            db.query(DocumentChunk.id, DocumentChunk.page_id)
            .filter(DocumentChunk.id.in_(found_chunk_ids))
            .all()
        )
        chunk_page_map = {chunk_id: page_id for (chunk_id, page_id) in chunk_pages}

        ret = []
        for chunk_id in found_chunk_ids:
            if not chunk_id in chunk_doc_map:
                logger.error(f"Invalid chunk id in from indeser {chunk_id=}")
                continue
            doc = chunk_doc_map[chunk_id]
            ret.append(
                SearchResult(
                    doc_id=doc.id,
                    chunk_id=chunk_id,
                    created_at=doc.created_at,
                    mime=doc.mime,
                    name=doc.name,
                    page_id=chunk_page_map[chunk_id],
                )
            )

        return ret

    def rag_query(
        self,
        db: Session,
        query: str,
        chunk_ids: List[int],
        rag: RagService,
    ) -> str:

        if not chunk_ids:
            raise ValueError("No chunks")

        chunk_ids = chunk_ids[0:MAX_IMAGES]

        chunks = db.query(DocumentChunk).filter(DocumentChunk.id.in_(chunk_ids)).all()
        chunk_map = {chunk.id: chunk.image for chunk in chunks}

        images = []
        # keep exact order as in original list of ids
        for chunk_id in chunk_ids:
            if chunk_id in chunk_map:
                images.append(chunk_map[chunk_id])

        return rag.question(query, images=images)

    def get_chunk_render_info(self, db: Session, chunk_id: int) -> RenderImageInfo:
        chunk = self.get_chunk(db, chunk_id)
        return RenderImageInfo(image=chunk.image, mime="image/jpeg")

    def get_chunk_interpret_info(
        self, db: Session, chunk_id: int, query: str, doc_indexer: DocIndexer
    ) -> RenderImageInfo:
        chunk = self.get_chunk(db, chunk_id)
        interpret_img = doc_indexer.interpret(query=query, image=chunk.image)
        return RenderImageInfo(image=interpret_img, mime="image/jpeg")

    def get_page_render_info(self, db: Session, page_id: int) -> RenderImageInfo:
        chunk = self.get_page(db, page_id)
        return RenderImageInfo(image=chunk.image, mime="image/jpeg")

    def get_doc_download_info(self, db: Session, doc_id: int) -> DocDownloadInfo:
        doc = self.get_document(db, doc_id)
        content = doc.content
        return DocDownloadInfo(content=content.content, mime=doc.mime, name=doc.name)

    def get_doc_preview_info(self, db: Session, doc_id: int) -> DocPreviewInfo:
        doc = self.get_document(db, doc_id)
        pages_res = (
            db.query(DocumentPage.id)
            .filter(DocumentPage.document == doc)
            .order_by(DocumentPage.number.asc())
        )
        return DocPreviewInfo(
            id=doc.id, name=doc.name, pages=[page_id for (page_id,) in pages_res]
        )

    def get_page(self, db: Session, entity_id: int) -> DocumentPage:
        ret = db.query(DocumentPage).filter(DocumentPage.id == entity_id).first()
        if not ret:
            raise RuntimeError(f"Page #{entity_id} not found")
        return ret

    def get_chunk(self, db: Session, entity_id: int) -> DocumentChunk:
        ret = db.query(DocumentChunk).filter(DocumentChunk.id == entity_id).first()
        if not ret:
            raise RuntimeError(f"Chunk #{entity_id} not found")
        return ret

    def get_documents(
        self, db: Session, filtering_query: FilteringQuery
    ) -> FilteringResult[DocInfo]:

        subq_pages = (
            db.query(DocumentPage.doc_id, func.count(DocumentPage.id).label("cnt"))
            .group_by(DocumentPage.doc_id)
            .subquery()
        )
        subq_chunks = (
            db.query(DocumentChunk.doc_id, func.count(DocumentChunk.id).label("cnt"))
            .group_by(DocumentChunk.doc_id)
            .subquery()
        )

        q = (
            db.query(
                Document,
                subq_pages.c.cnt.label("num_pages"),
                subq_chunks.c.cnt.label("num_chunks"),
            )
            .select_from(Document)
            .outerjoin(subq_pages, subq_pages.c.doc_id == Document.id)
            .outerjoin(subq_chunks, subq_chunks.c.doc_id == Document.id)
        )

        return apply_filter_to_db_query(
            filtering_query,
            q,
            sort_to_col=session_sort_to_col,
            apply_search=session_apply_search,
            q_total=db.query(Document),
            map_item=lambda items: [
                DocInfo(**doc.__dict__, num_pages=num_pages, num_chunks=num_chunks)
                for (doc, num_pages, num_chunks) in items
            ],
        )

    def is_mime_supported(self, mime: str) -> bool:
        return mime in MimeType

    def create_document(
        self,
        db: Session,
        name: str,
        mime: str,
        content: bytes,
        doc_processor: DocProcessor,
    ) -> Document:
        doc = Document(
            name=name,
            mime=mime,
            created_at=timestamp_ms(),
            indexed=False,
        )
        doc_content = DocumentContent(document=doc, content=content)

        pages_bytes = doc_processor.extract_pages(doc, doc_content)
        pages = []
        for idx, page_bytes in enumerate(pages_bytes):
            page = DocumentPage(document=doc, number=idx + 1, image=page_bytes)
            pages.append(page)
            db.add(page)

        chunks_bytes = doc_processor.chunk_pages(pages)

        for page, chunk_bytes in chunks_bytes:
            chunk = DocumentChunk(document=doc, page=page, image=chunk_bytes)
            db.add(chunk)

        db.add(doc)
        db.add(doc_content)
        db.commit()
        db.refresh(doc)
        return doc

    def get_document(self, db: Session, entity_id: int):
        ret = db.query(Document).filter(Document.id == entity_id).first()
        if not ret:
            raise RuntimeError(f"Document #{entity_id} not found")
        return ret

    def delete_document(self, db: Session, entity_id: int, doc_indexer: DocIndexer):
        doc = self.get_document(db, entity_id)

        doc_indexer.delete(doc)

        db.query(DocumentChunk).filter(DocumentChunk.document == doc).delete()
        db.query(DocumentPage).filter(DocumentPage.document == doc).delete()
        db.query(DocumentContent).filter(DocumentContent.document == doc).delete()

        db.delete(doc)
        db.commit()
        return doc

    def index_documents(self, db: Session, doc_indexer: DocIndexer):
        docs_for_scanning = db.query(Document).filter(Document.indexed == False).all()
        for doc in docs_for_scanning:
            # already scanning
            if doc.id in scanning_doc_ids:
                continue
            scanning_doc_ids.add(doc.id)
            try:
                doc_indexer.index(doc)

            finally:
                scanning_doc_ids.remove(doc.id)
            # if processing was successful
            doc.indexed = True
            db.commit()


def get_classifier_service(state: Any) -> ClassifierService:
    return getattr(state, CLASSIFIER_SERVICE_NAME)


def get_doc_indexer_service(state: Any) -> DocIndexer:
    return getattr(state, DOC_INDEXER_SERVICE_NAME)


def get_rag_service(state: Any) -> RagService:
    return getattr(state, RAG_SERVICE_NAME)


def get_doc_processor_service(state: Any) -> DocProcessor:
    return getattr(state, DOC_PROCESSOR_SERVICE_NAME)


def session_sort_to_col(col: str):
    return getattr(Document, to_snake_case(col))


def session_apply_search(q: Query, search: str):
    return q.filter(Document.name.like(f"%{search}%"))
