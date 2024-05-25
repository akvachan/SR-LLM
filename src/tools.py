import json
from typing import Any


def is_json(json_string: str) -> bool:
    try:
        json.loads(remove_header(json_string))
    except ValueError:
        return False
    return True


def to_json(json_string: str) -> Any:
    return json.loads(remove_header(json_string))


def remove_header(json_string: str) -> str:
    return json_string.replace("```json\n", "").replace("```", "")