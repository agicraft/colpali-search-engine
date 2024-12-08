from typing import List, Tuple

from ..utils.doc_converter import convert_to
from ..utils.images import pil_to_jpeg_bytes
from .mime_types import MimeType
from pdf2image import convert_from_bytes

from .classifier_models import Document, DocumentContent, DocumentPage
from .classifier_service import DocProcessor

PDF_DPI = 100


class DefaultDocProcessor(DocProcessor):

    def extract_pages(self, doc: Document, doc_content: DocumentContent) -> List[bytes]:
        ret: List[bytes]
        if doc.mime == MimeType.PDF:
            ret = split_pdf(doc_content.content)
        elif doc.mime == MimeType.PPTX:
            pdf = to_pdf(doc_content.content, format="pptx")
            ret = split_pdf(pdf)
        elif doc.mime == MimeType.DOCX:
            pdf = to_pdf(doc_content.content, format="docx")
            ret = split_pdf(pdf)
        elif doc.mime == MimeType.XLSX:
            pdf = to_pdf(doc_content.content, format="xlsx")
            ret = split_pdf(pdf)
        elif doc.mime == MimeType.JPEG or doc.mime == MimeType.PNG:
            ret = [doc_content.content]
        else:
            raise ValueError(f"No processors for document type {doc.mime}")
        return ret

    def chunk_pages(
        self, pages: List[DocumentPage]
    ) -> List[Tuple[DocumentPage, bytes]]:
        ret = []
        for page in pages:
            ret.append((page, page.image))
        return ret


def to_pdf(source: bytes, format: str) -> bytes:
    return convert_to(source=source, from_format=format, to_format="pdf", timeout=30)


def split_pdf(pdf: bytes) -> List[bytes]:
    images = convert_from_bytes(pdf, dpi=PDF_DPI)
    return [pil_to_jpeg_bytes(img) for img in images]
