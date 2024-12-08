import logging
from typing import List
from ..utils.llm import llm_chat_completion
from ..classifier.classifier_service import RagService as IRagService
import os
import base64

logger = logging.getLogger(__name__)


class RagService(IRagService):
    def __init__(self) -> None:
        super().__init__()

    def question(self, prompt: str, images: List[bytes]) -> str:
        # return f"Dummy answer for '{prompt}' using {len(images)} chunks"
        return self.__llm_prompt(
            prompt=prompt,
            images=images,
            default_answer="К сожелению, у меня нет ответа",
        )

    def __llm_prompt(
        self, prompt: str, images: List[bytes], default_answer: str
    ) -> str:

        user_prompt = f"""
Please answer the following question using only the information visible in the provided image.
Do not use any of your own knowledge, training data, or external sources.
Base your response solely on the content depicted within the image.
If there is no relation with question and image, you can respond with "{default_answer}".
Answer in Russian language.

User's question: {prompt}
"""

        return llm_chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {
                    "role": "user",
                    "content": [
                        *[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64.b64encode(img).decode('ascii')}"
                                },
                            }
                            for img in images
                        ],
                        {
                            "type": "text",
                            "text": user_prompt,
                        },
                    ],
                },
            ],
            model=os.environ["LLM_MODEL"],
        )
