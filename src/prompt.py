from abc import ABC, abstractmethod
import json
import os
from typing import Dict, Optional
from oshandler import OSHandler


class Prompt(ABC):
    """
    Prompt has a name, description, output scheme in dict format that is JSON-compliant and also a path to this prompt
    in prompt_templates directory.
    Each prompt should be saved as a txt-file in the prompt_templates!
    """

    @property
    def name(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    @property
    def output_scheme(self) -> Dict[str, str]:
        ...

    @property
    def prompt_path(self) -> str:
        ...

    @property
    def examples_paths(self) -> list[str]:
        ...

    def __init__(self, content: Optional[str] = None, variables: Optional[Dict[str, str]] = None,
                 has_output_scheme: bool = False, examples: int = 0) -> None:
        """
        Prompt is created from prompt txt-file from prompt_templates.
        Give variables dictionary in case your prompt has variables that need to be defined.
        Set has_output_scheme to True if you have a specific output scheme for your prompt.
        Content of the prompt is populated automatically on creation and injection.
        :param content: Optional content string
        :param variables: Optional dictionary of variables
        :param has_output_scheme: Boolean indicating whether there is a specific output scheme
        """
        if self.prompt_path:
            self.content = OSHandler.read_from_file(
                os.path.join(OSHandler.get_project_root(), "prompt_templates", self.prompt_path))
        else:
            self.content = content

        self.has_output_scheme = has_output_scheme

        if variables:
            self.variables = variables
            self.inject_variables()

        if has_output_scheme:
            self.inject_output_scheme()

        if examples > 0 and self.examples_paths:
            ex_list = []
            for i in range(examples):
                ex_list.append(
                    OSHandler.read_from_file(
                        os.path.join(OSHandler.get_project_root(), "examples", self.examples_paths[i])
                    )
                )
            self.examples = "\n\n".join(ex_list)
            self.inject_examples()

    def inject_variables(self) -> None:
        self.content = self.content.format(**self.variables)

    def inject_output_scheme(self) -> None:
        header = "## Output Format ##"
        instruction = "Generate JSON response to the prompt in following format:"
        json_str = json.dumps(self.output_scheme, indent=4)
        self.content = f"{self.content}\n\n{header}\n{instruction}\n{json_str}"

    def inject_examples(self) -> None:
        header = "## Examples ##"
        self.content = f"{self.content}\n\n{header}\n{self.examples}"
