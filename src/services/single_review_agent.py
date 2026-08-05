from core.llm_client import LLMClient
from utils.prompt_loader import load_prompt
from utils.json_utils import parse_json


class SingleReviewAgent:

    def __init__(self):
        self.client = LLMClient()

    def execute(self, code):

        prompt = load_prompt("single_review_prompt.txt")

        prompt = prompt.replace("{code}", code)

        response = self.client.generate(prompt)

        print("\n================ RAW RESPONSE ================")
        print(response)
        print("==============================================\n")

        return parse_json(response)