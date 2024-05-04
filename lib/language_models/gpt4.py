# Custom modules
import tools
from language_model import LanguageModel
from prompt import Prompt

# Site modules
import tiktoken
from openai import OpenAI
from typing import Callable, Optional

'''
messages = [
  {"role": "system", "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
  {"role": "system", "name":"example_user", "content": "New synergies will help drive top-line growth."},
  {"role": "system", "name": "example_assistant", "content": "Things working well together will increase revenue."},
  {"role": "system", "name":"example_user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
  {"role": "system", "name": "example_assistant", "content": "Let's talk later when we're less busy about how to do better."},
  {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
  {"role": "assistant", "content": "ANTWORT AUF OBEN"}
]
'''


class GPT4LanguageModel(LanguageModel):
    name: str = "gpt-4-turbo"
    description: str = "Powerful LLM from OpenAI"

    # Language model specific hyperparameters
    temperature: float = 0.6
    max_tokens: int = 2000
    response_format: dict = {
        "type": "json_object"
    }
    retry: int = 1
    client = OpenAI()

    def __init__(self, system_message: Prompt):
        self.system_message = system_message
        self.messages = [{
            "role": "system",
            "content": system_message.content
        }]

    def generate_response(self, user_message: Prompt, retry: Optional[int] = retry) -> str:

        self.messages.append({
            "role": "user",
            "content": user_message.content
        })

        response = self.client.chat.completions.create(
            model=self.name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format=self.response_format,
            messages=self.messages,
        )

        assistant_message = dict(response.choices[0].message)
        self.messages.append(assistant_message)

        response_string = assistant_message["content"]

        if not tools.is_json(response_string) and self.retry:
            self.generate_response(
                Prompt(content="You gave invalid JSON response. Please try again."),
                retry=retry-1
            )
        elif not tools.is_json(response_string) and not self.retry:
            return ""

        return response_string

    @staticmethod
    def encode(string: str) -> list[int]:
        try:
            encoding = tiktoken.encoding_for_model(GPT4LanguageModel.name)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return encoding.encode(string)

    @staticmethod
    def decode(tokens: list[int]) -> str:
        # TODO
        pass

