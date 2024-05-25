from language_model import LanguageModel
from prompt import Prompt
import tools
import tiktoken
import time
from openai import OpenAI


class GPT4LanguageModel(LanguageModel):
    model_name: str = "gpt-4o"
    description: str = "Powerful LLM from OpenAI"
    temperature: float = 0.6

    def __init__(self, agent_name, system_message: Prompt, examples: list[Prompt] = None, with_history: bool = False):
        self.messages = None
        self.last_response = None
        self.last_request = None
        self.thread = None
        self.assistant = None
        self.agent_name = agent_name
        self.client = OpenAI()
        self.system_message = system_message
        self.with_history = with_history
        self.examples = examples or []
        if self.with_history:
            self.setup_assistant()

    def setup_assistant(self):
        self.assistant = self.client.beta.assistants.create(
            name=self.agent_name,
            instructions=self.system_message.content,
            model=self.model_name,
        )
        self.thread = self.client.beta.threads.create()

    def generate_response(self, user_message: Prompt, in_json: bool = True):
        self.log_request(user_message)
        if self.with_history:
            return self.handle_response_with_history(user_message, in_json)
        else:
            return self.handle_standard_response(in_json)

    def log_request(self, user_message: Prompt):
        self.last_request = {"role": "user", "content": user_message.content}

    def handle_response_with_history(self, user_message: Prompt, in_json: bool):
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=user_message.content
        )
        run = self.client.beta.threads.runs.create(
            temperature=self.temperature,
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )
        out = self.wait_for_response(run)
        if in_json:
            if not tools.is_json(out):
                raise ValueError("Output format is not JSON:\n{}".format(out))
            return tools.to_json(out)
        return out

    def wait_for_response(self, run):
        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id, run_id=run.id)
            if run_status.status == "completed":
                self.messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
                self.last_response = self.messages.data[0]
                return self.last_response.content[0].text.value
            elif run_status.status == "failed":
                print("Run failed:", run_status.last_error)
                break
            time.sleep(0.5)

    def handle_standard_response(self, in_json: bool):
        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": self.system_message.content}, self.last_request]
        )
        self.last_response = response.choices[0].message
        out = self.last_response.content
        if in_json:
            if not tools.is_json(out):
                raise ValueError("Output format is not JSON")
            return tools.to_json(out)
        return out

    @staticmethod
    def encode(string: str) -> list[int]:
        try:
            return tiktoken.encoding_for_model(GPT4LanguageModel.model_name).encode(string)
        except KeyError:
            return tiktoken.get_encoding("cl100k_base").encode(string)

    @staticmethod
    def decode(tokens: list[int]) -> str:
        # Implement decoding logic based on the token list
        return tiktoken.decode(tokens)

    def flush_thread(self):
        # Implement if needed for cleaning thread resources
        pass

    def create_thread(self):
        # Create a thread if needed for initializing or restarting conversation threads
        pass

    def set_examples(self, examples):
        self.examples = examples

    def set_with_history(self, with_history):
        self.with_history = with_history
        if with_history:
            self.setup_assistant()
