import logging
from typing import Annotated, List
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Path,
    Request,
    Response,
    UploadFile,
)
import httpx
from sqlalchemy.orm import Session
from ..utils.data_table import (
    apply_filtering_result_to_response,
    create_filter_from_request,
)
from ..database import get_db
from .classifier_service import (
    get_classifier_service,
    get_doc_indexer_service,
    get_doc_processor_service,
    get_rag_service,
)
from .classifier_dto import (
    DocPreviewDto,
    DocumentDto,
    RagRequestDto,
    RagResponseDto,
    SearchDocumentDto,
    SearchRequestDto,
    SearchResponseDto,
)
from urllib.parse import quote

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents")


@router.post("/search", response_model=SearchResponseDto)
async def search(
    request: Request, body: SearchRequestDto, db: Session = Depends(get_db)
):
    service = get_classifier_service(request.state)
    doc_indexer = get_doc_indexer_service(request.state)

    results = service.find_documents_by_query(db, body.query, doc_indexer)

    return SearchResponseDto(
        documents=[SearchDocumentDto(**res.model_dump()) for res in results],
    )


@router.post("/rag", response_model=RagResponseDto)
async def rag_request(
    request: Request, body: RagRequestDto, db: Session = Depends(get_db)
):
    service = get_classifier_service(request.state)
    rag = get_rag_service(request.state)

    answer = service.rag_query(db, body.query, body.chunks, rag)

    return RagResponseDto(answer=answer, request_id=body.request_id)


@router.get("", response_model=List[DocumentDto])
async def get_all(request: Request, response: Response, db: Session = Depends(get_db)):
    filtering_query = create_filter_from_request(request)
    service = get_classifier_service(request.state)
    return apply_filtering_result_to_response(
        service.get_documents(db, filtering_query), response
    )


@router.delete("/{entityId}")
async def delete(
    request: Request,
    entity_id: Annotated[int, Path(alias="entityId")],
    db: Session = Depends(get_db),
):
    service = get_classifier_service(request.state)
    doc_indexer = get_doc_indexer_service(request.state)
    service.delete_document(db, entity_id, doc_indexer)


@router.get("/chunk/{entityId}/interpret")
async def chunk_interpret(
    request: Request,
    q: str,
    entity_id: Annotated[int, Path(alias="entityId")],
    db: Session = Depends(get_db),
):
    service = get_classifier_service(request.state)
    doc_indexer = get_doc_indexer_service(request.state)
    info = service.get_chunk_interpret_info(
        db, entity_id, query=q, doc_indexer=doc_indexer
    )
    return Response(content=info.image, media_type=info.mime)


@router.get("/chunk/{entityId}/image")
async def chunk_image(
    request: Request,
    entity_id: Annotated[int, Path(alias="entityId")],
    db: Session = Depends(get_db),
):
    service = get_classifier_service(request.state)
    info = service.get_chunk_render_info(db, entity_id)

    return Response(content=info.image, media_type=info.mime)


@router.get("/page/{entityId}/image")
async def page_image(
    request: Request,
    entity_id: Annotated[int, Path(alias="entityId")],
    db: Session = Depends(get_db),
):
    service = get_classifier_service(request.state)
    info = service.get_page_render_info(db, entity_id)

    return Response(content=info.image, media_type=info.mime)


@router.get("/{entityId}/preview", response_model=DocPreviewDto)
async def preview_document(
    request: Request,
    entity_id: Annotated[int, Path(alias="entityId")],
    db: Session = Depends(get_db),
):
    service = get_classifier_service(request.state)
    return service.get_doc_preview_info(db, entity_id)


@router.get("/{entityId}/download")
async def download_document(
    request: Request,
    entity_id: Annotated[int, Path(alias="entityId")],
    db: Session = Depends(get_db),
):
    service = get_classifier_service(request.state)
    info = service.get_doc_download_info(db, entity_id)

    return Response(
        content=info.content,
        media_type=info.mime,
        headers={
            "Content-Disposition": f'''attachment; filename*=UTF-8''"{quote(info.name)}"'''
        },
    )


@router.post("/upload", response_model=bool)
async def upload(
    request: Request,
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    service = get_classifier_service(request.state)
    doc_processor = get_doc_processor_service(request.state)
    doc_indexer = get_doc_indexer_service(request.state)

    if not file.content_type:
        raise HTTPException(httpx.codes.BAD_REQUEST, detail="Unknown content type")
    if not file.filename:
        raise HTTPException(httpx.codes.BAD_REQUEST, detail="Name not provided")

    if not service.is_mime_supported(file.content_type):
        raise HTTPException(httpx.codes.BAD_REQUEST, detail="Invalid file format")
    service.create_document(
        db,
        name=file.filename,
        mime=file.content_type,
        content=await file.read(),
        doc_processor=doc_processor,
    )
    background_tasks.add_task(service.index_documents, db, doc_indexer=doc_indexer)

    return True


# @router.get("/wip")
# async def wip(request: Request, db: Session = Depends(get_db)):
#     service = get_classifier_service(request.state)
#     doc = service.get_document(db, 2)
#     doc_indexer = get_doc_indexer_service(request.state)
#     doc_indexer.index(doc)
#     return "OK"
