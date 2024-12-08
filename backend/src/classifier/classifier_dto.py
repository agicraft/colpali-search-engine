from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from .mime_types import MimeType


class BaseDtoModel(BaseModel):
    model_config = ConfigDict(
        strict=True,
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class DocumentDto(BaseDtoModel):
    id: int
    name: str
    mime: str
    created_at: int
    indexed: bool
    num_pages: Optional[int] = 1
    num_chunks: Optional[int] = 1


class SearchRequestDto(BaseDtoModel):
    query: str


class ChunkInterpretRequestDto(BaseDtoModel):
    query: str


class SearchDocumentDto(BaseDtoModel):
    doc_id: int
    name: str
    mime: str
    created_at: int
    chunk_id: int
    page_id: int


class RagRequestDto(BaseDtoModel):
    request_id: int
    query: str
    chunks: List[int]


class RagResponseDto(BaseDtoModel):
    request_id: int
    answer: str


class DocPreviewDto(BaseDtoModel):
    id: int
    name: str
    pages: List[int]


class SearchResponseDto(BaseDtoModel):
    documents: List[SearchDocumentDto]
