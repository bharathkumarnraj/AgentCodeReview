import json
import re


def parse_json(response: str):
    """
    Parse JSON returned by the LLM.

    Removes markdown code fences if present.
    """

    response = response.strip()

    # Remove ```json
    response = re.sub(r"^```json", "", response)

    # Remove ```
    response = re.sub(r"```$", "", response)

    response = response.strip()

    return json.loads(response)