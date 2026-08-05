import time

from ollama import chat
from logger.file_logger import logger


class LLMClient:
    """
    Generic LLM Client using Ollama
    """

    def __init__(self):

        # Use the model installed on your system
        # Change this only if you install another model.
        self.model = "qwen2.5:7b"

    def generate(self, prompt: str) -> str:

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
                    ],
                    options={
                        # Deterministic responses for benchmarking
                        "temperature": 0,

                        # Large enough to avoid truncated JSON
                        "num_predict": 700,

                        # Keep responses focused
                        "top_p": 0.9
                    }
                )

                return response["message"]["content"]

            except Exception as ex:

                logger.warning(
                    f"Retry {attempt + 1}/{MAX_RETRIES} failed: {str(ex)}"
                )

                if attempt == MAX_RETRIES - 1:

                    logger.error(
                        "Maximum retry limit reached."
                    )

                    raise ex

                time.sleep(2)