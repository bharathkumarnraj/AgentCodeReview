from pathlib import Path


def load_prompt(file_name: str) -> str:

    prompt_path = Path("prompts") / file_name

    return prompt_path.read_text(encoding="utf-8")