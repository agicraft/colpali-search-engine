from enum import StrEnum


class MimeType(StrEnum):
    PDF = "application/pdf"
    MD = "text/markdown"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    JPEG = "image/jpeg"
    PNG = "image/png"
