def word_to_action(word):
    return {
        "turn left": 0,
        "turn right": 1,
        "move forward": 2,
        "move back": 3,
        "pick up": 4,
        "drop": 5,
        "toggle / activate an object": 6,
        "complete task": 7
    }[word]