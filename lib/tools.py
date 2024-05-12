import json

def is_json(json_string: str) -> bool:
    try:
        json.loads(json_string)
    except ValueError as e:
        return False
    return True


def to_json(json_string: str) -> str:
    return json.loads(json_string)