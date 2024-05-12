# Custom modules
from language_model import LanguageModel
from prompt import Prompt
import tools

# Site modules
from typing_extensions import override
from openai.lib.streaming import AssistantEventHandler
import tiktoken
import time
from openai import OpenAI


class GPT4LanguageModel(LanguageModel):
    model_name: str = "gpt-4-turbo"
    description: str = "Powerful LLM from OpenAI"
    temperature: float = 0.6

    def __init__(self, agent_name, system_message: Prompt, examples: list[Prompt] = None, with_history: bool = False):
        self.agent_name = agent_name
        self.client = OpenAI()
        self.system_message = system_message
        self.with_history = with_history
        self.examples = examples
        self.messages = None
        self.last_request = None
        self.last_response = None
        if self.with_history:
            self.assistant = self.client.beta.assistants.create(
                name=self.agent_name,
                instructions=self.system_message.content,
                model=self.model_name,
            )
            self.thread = self.client.beta.threads.create()

    def generate_response(self, user_message: Prompt):

        self.last_request = {
            "role": "user",
            "content": user_message.content,
        }

        if self.with_history:
            # Create a new message and add it to the messages of the thread
            _ = self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=user_message.content
            )

            # Create a new request in a specific thread to a specific assistant
            run = self.client.beta.threads.runs.create(
                temperature=self.temperature,
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
            )

            # Wait until assistant generates the message
            while True:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id)
                if run_status.status == "completed":
                    break
                elif run_status.status == "failed":
                    print("Run failed:", run_status.last_error)
                    break
                time.sleep(1)

            # Update messages in the thread
            self.messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )

            self.last_response = self.messages.data[0]
            out = self.last_response.content[0].text.value
        else:
            response = self.client.chat.completions.create(
                model=self.model_name,
                temperature=self.temperature,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": self.system_message.content
                    },
                    self.last_request
                ],
            )
            self.last_response = response.choices[0].message
            out = self.last_response.content

        if not tools.is_json(out):
            raise ValueError("Output format is not JSON:\n{}".format(out))

        return tools.to_json(out)

    def flush_thread(self):
        pass

    def create_thread(self):
        pass

    def set_examples(self, examples):
        self.examples = examples

    def set_with_history(self, with_history):
        self.with_history = with_history

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
