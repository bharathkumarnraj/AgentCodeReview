from utils.json_utils import parse_json

from services.base_agent import BaseAgent
from core.llm_client import LLMClient
from utils.prompt_loader import load_prompt
from models.review_result import ReviewResult


class PerformanceAgent(BaseAgent):

    def __init__(self):
        self.llm = LLMClient()

    def execute(self, code: str):

        prompt = load_prompt("performance_prompt.txt")

        final_prompt = f"""
{prompt}

{code}
"""

        response = self.llm.generate(final_prompt)

        data = parse_json(response)

        return ReviewResult(
            severity=data["severity"],
            issue=data["issue"],
            explanation=data["explanation"],
            suggestion=data["suggestion"]
        )