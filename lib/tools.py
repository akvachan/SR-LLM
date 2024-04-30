import json


def is_json(json_string: str) -> bool:
    try:
        json.loads(json_string)
    except ValueError as e:
        return False
    return True

def extract_words(string):
    return word_tokenize(string)


def extract_chars(string):
    return list(string)

def extract_freqs(_list):
    return dict(Counter(_list))


def determine_position(observation, size):
    return observation // size, observation % size


def extract_direction(text):
    pattern = r'\b(down|up|left|right)\b'
    directions = re.findall(pattern, text)
    return directions[-1] if directions else None


def direction_to_action(direction):
    mapping = {
        "up": 3,
        "down": 1,
        "left": 0,
        "right": 2
    }
    return mapping[direction]

