from prompt import Prompt
from openai import OpenAI
import tools
import re


class Mistral7bInstructLanguageModel:
    model_name = "Mistral-7B-Instruct"
    # model_name = "Mistral-7B-Instruct (non-finetuned)"
    description = "Mistral 7B Instruct smaller LLM"
    temperature = 0.6
    max_tokens = 1000

    def __init__(self, agent_name, system_message: Prompt):
        self.agent_name = agent_name
        self.system_message = system_message
        self.last_response = None
        self.last_request = None
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    def generate_response(self, feedback: Prompt, in_json=True):
        self.last_request = {"role": "user", "content": feedback.content}
        # Point to the local server
        response = self.client.chat.completions.create(
            model="arseniikvachan/FrozenLake-Mistral_merged-GGUF",
            # model="RichardErkhov/mistralai_-_Mistral-7B-Instruct-v0.2-gguf",
            messages=[
                {"role": "system", "content": self.system_message.content},
                {"role": "user", "content": feedback.content}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stop="}"
        )
        self.last_response = response.choices[0].message
        out = self.last_response.content + "}" if self.last_response.content[-1] == '"' or self.last_response.content[-1] == '\n' else self.last_response.content + '"}'
        json_match = re.search(r'\{.*?\}', out, re.DOTALL)
        json_str = ""
        if json_match:
            json_str = json_match.group()
        print(json_str)
        if in_json:
            if not tools.is_json(json_str):
                raise ValueError("Output format is not JSON or does not have JSON:\n{}".format(out))
            return tools.to_json(json_str)
        return out
