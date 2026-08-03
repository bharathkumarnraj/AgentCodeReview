import json


def parse_json(text: str):

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        return None