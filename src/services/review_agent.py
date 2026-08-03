from utils.json_utils import parse_json
from services.base_agent import BaseAgent
from utils.prompt_loader import load_prompt
from core.llm_client import LLMClient
from models.review_result import ReviewResult


class ReviewAgent(BaseAgent):

    def __init__(self):
        self.llm = LLMClient()

    def execute(self, code: str):

        prompt = load_prompt("review_prompt.txt")

        final_prompt = f"""
{prompt}

{code}
"""

        response = self.llm.generate(final_prompt)

        data = parse_json(response)

        if data is None:
            raise ValueError("Invalid JSON returned from LLM.")

        return ReviewResult(
            severity=data["severity"],
            issue=data["issue"],
            explanation=data["explanation"],
            suggestion=data["suggestion"]
        )