from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import BYTEA
from .. import database


class BaseOrmModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Document(BaseOrmModel):
    __tablename__ = "document"

    name: Mapped[str] = mapped_column()
    mime: Mapped[str] = mapped_column()
    created_at: Mapped[int] = mapped_column(BigInteger)
    indexed: Mapped[bool] = mapped_column()
    content: Mapped["DocumentContent"] = relationship(back_populates="document")
    chunks: Mapped[List["DocumentChunk"]] = relationship(back_populates="document")
    pages: Mapped[List["DocumentPage"]] = relationship(back_populates="document")


class DocumentContent(BaseOrmModel):
    __tablename__ = "document_content"

    doc_id: Mapped[int] = mapped_column(ForeignKey("document.id"))
    content: Mapped[bytes] = mapped_column(BYTEA)
    document: Mapped["Document"] = relationship(back_populates="content")


class DocumentPage(BaseOrmModel):
    __tablename__ = "document_page"

    doc_id: Mapped[int] = mapped_column(ForeignKey("document.id"))
    number: Mapped[int] = mapped_column()
    image: Mapped[bytes] = mapped_column(BYTEA)
    document: Mapped["Document"] = relationship(back_populates="pages")


class DocumentChunk(BaseOrmModel):
    __tablename__ = "document_chunk"

    doc_id: Mapped[int] = mapped_column(ForeignKey("document.id"))
    page_id: Mapped[int] = mapped_column(ForeignKey("document_page.id"))
    image: Mapped[bytes] = mapped_column(BYTEA)
    page: Mapped["DocumentPage"] = relationship()
    document: Mapped["Document"] = relationship(back_populates="chunks")


def create_all_tables():
    BaseOrmModel.metadata.create_all(bind=database.engine)
