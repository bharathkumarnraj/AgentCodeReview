from services.base_agent import BaseAgent
from utils.prompt_loader import load_prompt
from core.llm_client import LLMClient


class RepairAgent(BaseAgent):

    def __init__(self):
        self.llm = LLMClient()

    def execute(self, code: str):

        prompt = load_prompt("repair_prompt.txt")

        final_prompt = f"""
{prompt}

{code}
"""

        repaired_code = self.llm.generate(final_prompt)

        return repaired_code