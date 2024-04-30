from openai import OpenAI

import tools

client = OpenAI()


def give_response(task, feedback):
    return client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": task},
            {"role": "user", "content": feedback},
        ]
    )

def tot(prompt_templates_path):
    tot_prompt_templates = []
    for root, dirs, files in os.walk(prompt_templates_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                prompt_template = read_task(file_path)
                tot_prompt_templates.append(prompt_template)
