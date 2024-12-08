import json
import logging
from typing import Iterable, List, Optional, TypeVar

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel
import openai
import time

logger = logging.getLogger(__name__)
BM = TypeVar("BM", bound=BaseModel)


def llm_chat_completion(
    *,
    messages: Iterable[ChatCompletionMessageParam],
    model: str,
    temperature: Optional[float] | openai.NotGiven = openai.NOT_GIVEN,
) -> str:
    client = openai.OpenAI()
    attempts = 5
    for attempt in range(attempts):
        try:
            response = client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content or ""
        except:
            logger.exception(f"Request to LLM attept {attempt+1} failed")
            time.sleep(1.0)
    raise RuntimeError(f"Request to LLM failed after {attempts} attempts")


def llm_chat_request(
    *,
    messages: Iterable[ChatCompletionMessageParam],
    model: str,
    output_class: type[BM],
    temperature: Optional[float] | openai.NotGiven = openai.NOT_GIVEN,
) -> BM:
    client = openai.OpenAI()
    attempts = 5
    for attempt in range(attempts):
        try:
            response = client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return parse_llm_response_json(
                response.choices[0].message.content, output_class
            )
        except:
            logger.exception(f"Request to LLM attept {attempt+1} failed")
            time.sleep(1.0)
    raise RuntimeError(f"Request to LLM failed after {attempts} attempts")


def extract_json_from_text(text: str) -> List[str]:
    start_json_char = "{"
    decoder = json.JSONDecoder(strict=False)
    pos = 0
    ret: List[str] = []
    while True:
        start_char_pos = text.find(start_json_char, pos)
        if start_char_pos < 0:
            break
        try:
            result, index = decoder.raw_decode(text[start_char_pos:])
            pos = start_char_pos + index
            ret.append(json.dumps(result, ensure_ascii=False))
        except ValueError:
            pos = start_char_pos + 1
    return ret


def parse_llm_response_json(text: Optional[str], output_class: type[BM]):
    if not text:
        raise RuntimeError("Empty LLM response")

    json_strs = extract_json_from_text(text)
    if not json_strs:
        raise RuntimeError("No JSONs found in LLM response")

    for json_str in json_strs:
        try:
            return output_class.model_validate_json(json_str)
        except:
            ...

    raise RuntimeError("Failed to parse JSON from LLM according to model")
