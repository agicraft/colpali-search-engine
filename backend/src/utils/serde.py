from typing import Any
from pydantic.json import pydantic_encoder
import json


def json_pydantic_dump(data: Any):
    return json.dumps(data, default=pydantic_encoder)
