from abc import ABC, abstractmethod
from prompt import Prompt


class LanguageModel(ABC):
    """
    Abstract base class for custom implementation of a language model.
    """

    @property
    def name(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    def __init__(self, system_message: Prompt):
        self.system_message = system_message

    @abstractmethod
    def generate_response(self, user_message: Prompt) -> str:
        ...

    @staticmethod
    def encode(string: str) -> list[int]:
        ...

    @staticmethod
    def decode(tokens: list[int]) -> str:
        ...




