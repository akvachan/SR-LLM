from abc import ABC, abstractmethod
from typing import List
from prompt import Prompt


class LanguageModel(ABC):
    """
    Abstract base class for custom implementation of a language model.
    """

    @property
    def model_name(self) -> str:
        pass

    @property
    def description(self) -> str:
        pass

    @abstractmethod
    def generate_response(self, user_message: Prompt) -> str:
        pass

    @staticmethod
    @abstractmethod
    def encode(string: str) -> List[int]:
        pass

    @staticmethod
    @abstractmethod
    def decode(tokens: List[int]) -> str:
        pass
