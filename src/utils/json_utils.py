import json
import re


def parse_json(response: str):
    """
    Robust JSON parser for LLM responses.

    Handles:
    - ```json ... ```
    - ``` ... ```
    - Leading/trailing whitespace
    - JSON objects
    - JSON arrays (returns first element)
    - Extra text before/after JSON
    """

    if response is None:
        raise ValueError("LLM returned None")

    response = response.strip()

    # -----------------------------------
    # Remove markdown fences
    # -----------------------------------

    response = re.sub(r"^```json", "", response, flags=re.IGNORECASE)
    response = re.sub(r"^```", "", response)
    response = re.sub(r"```$", "", response)

    response = response.strip()

    # -----------------------------------
    # Try direct parse
    # -----------------------------------

    try:

        data = json.loads(response)

        if isinstance(data, list):

            if len(data) == 0:
                raise ValueError("Empty JSON array")

            return data[0]

        return data

    except Exception:
        pass

    # -----------------------------------
    # Extract JSON object
    # -----------------------------------

    match = re.search(r"\{.*\}", response, re.DOTALL)

    if match:

        candidate = match.group(0)

        try:

            data = json.loads(candidate)

            if isinstance(data, list):

                return data[0]

            return data

        except Exception:
            pass

    # -----------------------------------
    # Extract JSON array
    # -----------------------------------

    match = re.search(r"\[.*\]", response, re.DOTALL)

    if match:

        candidate = match.group(0)

        try:

            data = json.loads(candidate)

            if len(data) == 0:
                raise ValueError("Empty JSON array")

            return data[0]

        except Exception:
            pass

    # -----------------------------------
    # Debug
    # -----------------------------------

    print("\n========== INVALID JSON ==========")
    print(response)
    print("==================================\n")

    raise ValueError("Unable to parse JSON response.")