from prompt import Prompt
from language_models.gpt4 import GPT4LanguageModel
from frozenlake.prompt import SystemPromptGeneratorGPT, SystemPromptMistralInference
from oshandler import OSHandler
from frozenlake.map import FrozenLakeMap

import math
import gymnasium as gym
import os
import numpy as np
import json

ENV_NAME = "FrozenLake-v1"
FINE_TUNING_DATA_PATH = os.path.join(OSHandler.get_project_root(), "fine_tuning_data", ENV_NAME)
TRAINING_MAPS_PATH = os.path.join(OSHandler.get_project_root(), "maps", ENV_NAME, "train-v2")
TRAINING_MAPS_NAMES = OSHandler.get_file_list(TRAINING_MAPS_PATH)
MAX_TOKENS = 1000


def main():
    np.random.shuffle(TRAINING_MAPS_NAMES)
    for map_name in TRAINING_MAPS_NAMES:
        full_path = os.path.join(TRAINING_MAPS_PATH, map_name)
        fl_map = FrozenLakeMap.deserialize(full_path)
        env = gym.make(
            ENV_NAME,
            is_slippery=False,
            render_mode="human",
            desc=fl_map.strarr
        )
        _ = env.reset()
        curr_pos = fl_map.origin

        variables = {
            "SIZE": fl_map.size,
            "ORIGIN": fl_map.origin,
            "GOAL": fl_map.goals[0],
            "OBSTACLES": fl_map.obstacles,
            "LOWER_BOUND": -1,
            "UPPER_BOUND": fl_map.size + 1,
            "MAX_TOKENS": MAX_TOKENS
        }

        sys_prompt_generator = SystemPromptGeneratorGPT(
            variables=variables,
            has_output_scheme=True
        )

        sys_prompt_inference = SystemPromptMistralInference(
            variables=variables,
            has_output_scheme=True
        )

        qa_arr = []

        num_actions = 0
        horizon = math.ceil(len(fl_map.solution) * 1.5)
        terminated = False
        success = False
        while not terminated:
            feedback = Prompt(content=f"You are now at {curr_pos}.")

            language_model = GPT4LanguageModel(
                agent_name="GeneratorAgent",
                system_message=sys_prompt_generator,
            )

            response = language_model.generate_response(feedback, in_json=True)
            move = response["move"]
            action = fl_map.direction_to_action(move)

            observation, reward, terminated, _, info = env.step(action)
            num_actions += 1
            curr_pos = fl_map.determine_position(observation)

            system = sys_prompt_inference.content
            question = feedback.content
            answer = json.dumps(response)
            qa_arr.append({
                "S": system,
                "Q": question,
                "A": answer
            })

            if num_actions == horizon:
                terminated = True

            if terminated and curr_pos == fl_map.goals[0]:
                success = True

        if success:
            OSHandler.write_to_json(qa_arr,
                                    os.path.join(FINE_TUNING_DATA_PATH, fl_map.name + "_" + "finetune" + ".json"))


if __name__ == '__main__':
    main()
