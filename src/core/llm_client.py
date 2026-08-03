import time

from ollama import chat
from logger.file_logger import logger


class LLMClient:
    """
    Generic LLM Client using Ollama
    """

    def __init__(self):
        self.model = "qwen2.5:7b"

    def generate(self, prompt):

        MAX_RETRIES = 3

        for attempt in range(MAX_RETRIES):

            try:

                response = chat(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                return response["message"]["content"]

            except Exception as ex:

                logger.warning(
                    f"Retry {attempt + 1}/{MAX_RETRIES} failed: {str(ex)}"
                )

                if attempt == MAX_RETRIES - 1:
                    logger.error("Maximum retry limit reached.")
                    raise ex

                time.sleep(2)