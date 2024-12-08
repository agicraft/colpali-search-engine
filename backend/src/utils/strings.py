import base64
from io import BytesIO
import re

snake_case_regex = re.compile(r"(?!^)([A-Z]+)")


def base64_encode(b: bytes) -> str:
    output = BytesIO()
    base64.encode(BytesIO(b), output)
    output.seek(0)
    return output.read().decode("ascii")


def base64_decode(s: str) -> bytes:
    return base64.b64decode(s)


def to_snake_case(camel_str):
    return snake_case_regex.sub(r"_\1", camel_str).lower()
