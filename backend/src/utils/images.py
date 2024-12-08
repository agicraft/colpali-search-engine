import io
from PIL.Image import Image


def pil_to_jpeg_bytes(img: Image) -> bytes:
    bytes_io = io.BytesIO()
    img.save(bytes_io, format="JPEG", subsampling=0, quality=80)
    return bytes_io.getvalue()


def pil_to_bytes(img: Image) -> bytes:
    bytes_io = io.BytesIO()
    img.save(bytes_io, format="PNG")
    return bytes_io.getvalue()
