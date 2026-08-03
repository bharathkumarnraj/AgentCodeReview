import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = "AgentCodeReview"
    VERSION = "0.1.0"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    DEFAULT_MODEL = "gpt-5"


settings = Settings()