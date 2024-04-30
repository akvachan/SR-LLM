from abc import ABC, abstractmethod


class Prompt(ABC):

    @property
    def name(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    @property
    def output_scheme(self) -> str:
        ...

    def __init__(self, content: str, variables: list[str], system: bool = False) -> None:
        self.content = content
        self.variables = variables
        self.system = system
        self.inject_variables()

    def __init__(self, content: str, system: bool = False) -> None:
        self.content = content
        self.system = system

    @abstractmethod
    def inject_variables(self) -> None:
        ...

