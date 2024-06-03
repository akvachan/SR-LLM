from openai import OpenAI

from prompt import Prompt
import tools


class GPT4VisionLanguageModel:
    model_name: str = "gpt-4o"
    description: str = "Powerful LLM from OpenAI"
    temperature: float = 0.6

    def __init__(self, agent_name, system_message: Prompt):
        self.agent_name = agent_name
        self.client = OpenAI()
        self.system_message = system_message

    def generate_response(self, user_message: Prompt, image) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": self.system_message.content
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_message.content
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{tools.encode_image(image)}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300,
        )
        return response
