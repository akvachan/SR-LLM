from language_model import LanguageModel
from oshandler import OSHandler
from frozenlake.prompt import TaskDecompositionBasePrompt, MultiPlanSelectionBasePrompt, \
    MultiPlanSelectionTreeLvl1Prompt, MultiPlanSelectionTreeLvl2Prompt, MultiPlanSelectionTreeLvl3Prompt, \
    MultiPlanSelectionTreeLvl4Prompt
from frozenlake.map import FrozenLakeMap, MAPS_DIR, PROJECT_ROOT
from frozenlake.intel import FrozenLakeIntel
from frozenlake.logger import ChatLogger
from language_models.gpt4 import GPT4LanguageModel
from prompt import Prompt

import gymnasium as gym
import os
import math
import numpy as np

MAP_NAME = "FrozenLake-v1"
MAPS_DIR = MAPS_DIR
EXPERIMENTS_DIR = "experiments"
LOG_DIR = "logs"
MAX_TOKENS = 2000
MAPS = OSHandler.get_file_list(MAPS_DIR)  # Not immutable, just global!
MAX_ITERATIONS = len(MAPS)


class Experiment:

    def __init__(self, curr_map: FrozenLakeMap, base_prompt):

        self.curr_map = curr_map

        self.logger = ChatLogger(
            location=os.path.join(
                PROJECT_ROOT,
                LOG_DIR,
                MAP_NAME,
                base_prompt.name,
                "0-shot",
                GPT4LanguageModel.model_name,
            ),
            name="chat" + "_" + curr_map.name
        )

        self.variables = {
            "SIZE": curr_map.size,
            "ORIGIN": curr_map.origin,
            "GOAL": curr_map.goals[0],
            "OBSTACLES": curr_map.obstacles,
            "LOWER_BOUND": -1,
            "UPPER_BOUND": curr_map.size + 1,
            "MAX_TOKENS": MAX_TOKENS
        }

        self.system_message = base_prompt(
            variables=self.variables,
            has_output_scheme=True,
        )

        self.logger.put(
            extra={
                "role": "system",
                "content": self.system_message.content.replace("\n", " ")
            }
        )

        self.language_model = GPT4LanguageModel(
            agent_name="FrozenLakeAgent_1",
            system_message=self.system_message,
        )

        self.intel = FrozenLakeIntel(
            map_size=curr_map.size,
            map_name=curr_map.name,
            num_obstacles=len(curr_map.obstacles),
            horizon=math.ceil(len(curr_map.solution) * 1.5)
        )

    def task_decomposition_run(self):
        environment = gym.make(MAP_NAME, is_slippery=False, render_mode="human", desc=self.curr_map.strarr)
        _ = environment.reset()
        curr_pos = self.curr_map.origin
        prev_pos = None

        terminated = False
        while not terminated:
            feedback = Prompt(
                content=f"You are now at {tuple(curr_pos)}."
            )

            response = self.language_model.generate_response(feedback)

            user_request, user_role = dict(self.language_model.last_request)["content"], \
                dict(self.language_model.last_request)[
                    "role"]
            assistant_response, assistant_role = dict(self.language_model.last_response)["content"], \
                dict(self.language_model.last_response)["role"]

            self.logger.put({"role": user_role, "content": user_request.replace("\n", " ")})
            self.logger.put({"role": assistant_role, "content": assistant_response.replace("\n", " ")})

            direction = response["step_3"]
            action = self.curr_map.direction_to_action(direction)
            observation, reward, terminated, _, info = environment.step(action)
            curr_pos = self.curr_map.determine_position(observation)
            self.intel.gather_intel(self.curr_map, curr_pos, prev_pos)
            prev_pos = curr_pos

            if self.intel.num_actions == self.intel.horizon:
                terminated = True

        self.intel.serialize(
            location=os.path.join(
                PROJECT_ROOT,
                EXPERIMENTS_DIR,
                "STP",
                TaskDecompositionBasePrompt.name,
                "0-shot",
                GPT4LanguageModel.model_name,
            ),
            name="intel" + "_" + self.curr_map.name
        )

        environment.close()

    def multi_plan_selection_run(self):
        pass


def task_decomposition():
    np.random.shuffle(MAPS)

    for i in range(MAX_ITERATIONS):
        experiment = Experiment(
            curr_map=FrozenLakeMap.deserialize(os.path.join(MAPS_DIR, MAPS[i])),
            base_prompt=TaskDecompositionBasePrompt,
        )
        experiment.task_decomposition_run()

        print(f"Task Decomposition 0-shot: {i} of {MAX_ITERATIONS} completed.")


def multi_plan_selection():
    np.random.shuffle(MAPS)

    for i in range(MAX_ITERATIONS):
        experiment = Experiment(
            curr_map=FrozenLakeMap.deserialize(os.path.join(MAPS_DIR, MAPS[i])),
            base_prompt=MultiPlanSelectionBasePrompt
        )
        experiment.multi_plan_selection_run()

        print(f"Multi-Plan Selection 0-shot: {i} of {MAX_ITERATIONS} completed.")


if __name__ == "__main__":
    task_decomposition()
    # multi_plan_selection()

