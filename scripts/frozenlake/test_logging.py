import logging
import random

from frozenlake.prompt import Prompt
from language_models.gpt4 import GPT4LanguageModel

logger = logging.getLogger(__name__)


def main():

    system_prompt = Prompt(
        content="Let's play Rock Paper Scissors. Please output your answer in JSON: {'play': 'rock/paper/scissors'}"
    )

    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("logfile.log")
    formatter = logging.Formatter("{asctime} : {role} : {content}", style="{")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    gpt4 = GPT4LanguageModel(system_message=system_prompt)
    logger.info("", extra=gpt4.messages[-1]) # Log system message

    for _ in range(5):
        user_prompt = Prompt(random.choice(["rock", "paper", "scissors"]))
        gpt4.generate_response(user_message=user_prompt, retry=0)
        gpt4.messages[-1]["content"] = gpt4.messages[-1]["content"].replace("\n", " ")
        logger.info("", extra=gpt4.messages[-2]) # Log user message
        logger.info("", extra=gpt4.messages[-1]) # Log assistant message


if __name__ == '__main__':
    main()
