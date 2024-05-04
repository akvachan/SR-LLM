from oshandler import OSHandler

from abc import ABC, abstractmethod
import json
import os


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
    def output_scheme(self) -> str:
        ...

    @property
    def prompt_path(self) -> str:
        ...

    def __init__(self, content: str = None, variables: dict[str, str] = None, has_output_scheme: bool = False) -> None:
        """
        Prompt is created from prompt txt-file from prompt_templates.
        Give variables dictionary in case your prompt has variables that need to be defined.
        Set has_output_scheme to True if you have a specific output scheme for your prompt.
        Content of the prompt is populated automatically on creation and injection.
        :param variables: A variable-value dictionary
        :param has_output_scheme: A boolean indicating whether there is a specific output scheme, and you want to use it
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

    def inject_variables(self):
        self.content = self.content.format(**self.variables)

    def inject_output_scheme(self):
        header = "## Output Format ##"
        instruction = "Generate JSON response to the prompt in following format:"
        json_str = json.dumps(self.output_scheme, indent=4)
        self.content = self.content + "\n" + header + "\n" + instruction + "\n" + json_str
