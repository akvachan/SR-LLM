import random
import time

from oshandler import OSHandler
from frozenlake.prompt import TaskDecompositionBasePrompt, MultiPlanSelectionBasePrompt, \
    MultiPlanSelectionTreeLvl1Prompt, MultiPlanSelectionTreeLvl2Prompt, MultiPlanSelectionTreeLvl3Prompt, \
    MultiPlanSelectionTreeLvl4Prompt, ReflectionRefinementActorBasePrompt, ReflectionRefinementCriticBasePrompt, \
    ReflectionRefinementActorRetryPrompt, ReflectionRefinementCriticPrompt
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
MAX_TOKENS = 1000
MAPS = OSHandler.get_file_list(MAPS_DIR)  # Not immutable, just global!
MAX_ITERATIONS = len(MAPS)
ACTOR_RETRIES = 3


class Experiment:

    def __init__(self, curr_map: FrozenLakeMap, base_prompt, examples=0):

        self.curr_map = curr_map
        self.base_prompt = base_prompt
        self.examples = examples

        self.logger = ChatLogger(
            location=os.path.join(
                PROJECT_ROOT,
                LOG_DIR,
                MAP_NAME,
                base_prompt.name,
                f"{examples}-shot",
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
            examples=examples
        )

        self.logger.put(
            extra={
                "role": "system",
                "content": self.system_message.content.replace("\n", " ")
            }
        )

        self.intel = FrozenLakeIntel(
            map_size=curr_map.size,
            map_name=curr_map.name,
            num_obstacles=len(curr_map.obstacles),
            horizon=math.ceil(len(curr_map.solution) * 1.5)
        )

    def task_decomposition_run(self):
        """
        1. Initialize language model agent without memory (history)
        2. Initialize gym environment
        3. Iterate until environment terminates:
            1. Give feedback to agent about its current position
            2. Generate response of agent regarding its next move
            3. Log both the feedback and the response
            4. Extract direction and map it to an action in the environment
            5. Collect observations and termination status
            6. Determine new position of the agent
            7. Collect all necessary information regarding state of the agent and environment for evaluation
            8. Check if maximum number of allows steps (horizon) is reached
        4. When terminated save evaluation information in json file on disk
        5. Close the environment
        """

        language_model = GPT4LanguageModel(
            agent_name="FrozenLakeAgent_1",
            system_message=self.system_message,
        )

        environment = gym.make(MAP_NAME, is_slippery=False, render_mode="human", desc=self.curr_map.strarr)
        _ = environment.reset()
        curr_pos = self.curr_map.origin
        prev_pos = None

        terminated = False
        while not terminated:
            feedback = Prompt(content=f"You are now at {tuple(curr_pos)}.")

            response = language_model.generate_response(feedback, in_json=True)

            lm_last_request = dict(language_model.last_request)
            user_request, user_role = lm_last_request["content"], lm_last_request["role"]

            lm_last_response = dict(language_model.last_response)
            assistant_response, assistant_role = lm_last_response["content"], lm_last_response["role"]

            self.logger.put({"role": user_role, "content": user_request.replace("\n", " ")})
            self.logger.put({"role": assistant_role, "content": assistant_response.replace("\n", " ")})

            try:
                direction = response["step_3"]
                action = self.curr_map.direction_to_action(direction)
            except KeyError as e:
                print(e)
                action = environment.action_space.sample()

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
                self.base_prompt.name,
                f"{self.examples}-shot",
                GPT4LanguageModel.model_name,
            ),
            name="intel" + "_" + self.curr_map.name
        )

        environment.close()

    def multi_plan_selection_run(self):
        """
        1. Initialize language model agent with memory (history)
        2. Initialize gym environment
        3. Iterate until environment terminates:
            1. Create feedback prompt for agent about its current position
            2. Initialize Tree of Thought Prompts for future use
            3. Iterate over each Tree of Thought prompt:
                1. Generate response of agent regarding the Tree of Thought prompt
                2. Log both the feedback and the response
            4. Extract direction and map it to an action in the environment
            5. Collect observations and termination status
            6. Determine new position of the agent
            7. Collect all necessary information regarding state of the agent and environment for evaluation
            8. Check if maximum number of allows steps (horizon) is reached
        4. When terminated save evaluation information in json file on disk
        5. Close the environment
        """
        environment = gym.make(MAP_NAME, is_slippery=False, render_mode="human", desc=self.curr_map.strarr)
        _ = environment.reset()
        curr_pos = self.curr_map.origin
        prev_pos = None

        terminated = False
        while not terminated:
            language_model = GPT4LanguageModel(
                agent_name="FrozenLakeAgent_2",
                system_message=self.base_prompt(
                    variables=self.variables,
                ),
                with_history=True
            )

            feedback = Prompt(content=f"You are now at {tuple(curr_pos)}.")

            prompt_lvl_1 = MultiPlanSelectionTreeLvl1Prompt(
                variables={
                    "FEEDBACK": feedback.content
                },
                examples=self.examples
            )

            prompt_lvl_2 = MultiPlanSelectionTreeLvl2Prompt(examples=self.examples)
            prompt_lvl_3 = MultiPlanSelectionTreeLvl3Prompt(examples=self.examples)
            prompt_lvl_4 = MultiPlanSelectionTreeLvl4Prompt(has_output_scheme=True, examples=self.examples)

            for prompt in [prompt_lvl_1, prompt_lvl_2, prompt_lvl_3, prompt_lvl_4]:
                time.sleep(3)
                try:
                    response = language_model.generate_response(prompt, in_json=prompt.has_output_scheme)
                except ValueError as e:
                    print(e)
                    response = {}

                lm_last_request = dict(language_model.last_request)
                user_request, user_role = lm_last_request["content"], lm_last_request["role"]

                lm_last_response = dict(language_model.last_response)
                assistant_response, assistant_role = lm_last_response["content"][0].text.value, "assistant"

                self.logger.put({"role": user_role, "content": user_request.replace("\n", " ")})
                self.logger.put({"role": assistant_role, "content": assistant_response.replace("\n", " ")})

            try:
                direction = response["rank_1"]["move"]
                action = self.curr_map.direction_to_action(direction)
            except KeyError as e:
                print(e)
                action = environment.action_space.sample()

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
                self.base_prompt.name,
                f"{self.examples}-shot",
                GPT4LanguageModel.model_name,
            ),
            name="intel" + "_" + self.curr_map.name
        )

        environment.close()

    def reflection_refinement_run(self):
        """
        1. Initialize gym environment
        2. Initialize base actor prompt (system prompt for actor)
        3. Initialize base critic prompt (system prompt for critic)
        4. Iterate until environment terminates:
            1. Create a new instance of actor model with memory (history)
            2. Create a new instance of critic model with memory (history)
            3. Create a feedback prompt for actor about its current position
            4. Initialize move ratings dict
            5. Iterate 3 times or until rating for actor's move is above 4:
                1. Generate response of actor
                2. Log both the feedback and the response
                3. Initialize critic prompt with all the variables necessary
                4. Generate response of critic to actor's move
                5. Log both the feedback and the response
                6. If rating for actor's move is above 4, break
                7. Else initialize actor retry prompt with all the variables necessary
                8. Save the move with the best rating
            6. Extract the best move from move rating dict and map it to an action in the environment
            7. Collect observations and termination status
            8. Determine new position of the agent
            9. Collect all necessary information regarding state of the agent and environment for evaluation
            10. Check if maximum number of allows steps (horizon) is reached
        5. When terminated save evaluation information in json file on disk
        6. Close the environment
        """

        environment = gym.make(MAP_NAME, is_slippery=False, render_mode="human", desc=self.curr_map.strarr)
        _ = environment.reset()
        curr_pos = self.curr_map.origin
        prev_pos = None

        base_actor_prompt = ReflectionRefinementActorBasePrompt(
            variables=self.variables,
            has_output_scheme=True,
            examples=self.examples
        )

        base_critic_prompt = ReflectionRefinementCriticBasePrompt(
            variables=self.variables,
            examples=self.examples
        )

        terminated = False

        self.logger.put({"role": "system", "content": base_critic_prompt.content.replace("\n", "")})

        while not terminated:

            actor = GPT4LanguageModel(
                agent_name="actor",
                system_message=base_actor_prompt,
                with_history=True
            )

            critic = GPT4LanguageModel(
                agent_name="critic",
                system_message=base_critic_prompt,
                with_history=True
            )

            actor_prompt = Prompt(content=f"You are now at {tuple(curr_pos)}.")

            move_to_rating = {}

            for _ in range(1, ACTOR_RETRIES):
                response = actor.generate_response(actor_prompt, in_json=base_actor_prompt.has_output_scheme)

                actor_last_request = dict(actor.last_request)
                user_request, user_role = actor_last_request["content"], actor_last_request["role"]

                actor_last_response = dict(actor.last_response)
                assistant_response, assistant_role = actor_last_response["content"][0].text.value, "actor"

                self.logger.put({"role": user_role, "content": user_request.replace("\n", " ")})
                self.logger.put({"role": assistant_role, "content": assistant_response.replace("\n", " ")})

                try:
                    actor_explanation = response["explanation"]
                except KeyError as e:
                    actor_explanation = e

                try:
                    direction = response["move"]
                except KeyError as e:
                    direction = random.choice(["up", "down", "left", "right"])

                critic_prompt = ReflectionRefinementCriticPrompt(
                    variables={
                        "EXPLANATION": actor_explanation,
                        "DIRECTION": direction
                    },
                    has_output_scheme=True,
                    examples=self.examples
                )

                critique = critic.generate_response(critic_prompt, in_json=critic_prompt.has_output_scheme)

                critic_last_request = dict(critic.last_request)
                user_request, user_role = critic_last_request["content"], critic_last_request["role"]

                critic_last_response = dict(critic.last_response)
                assistant_response, assistant_role = critic_last_response["content"][0].text.value, "critic"

                self.logger.put({"role": user_role, "content": user_request.replace("\n", " ")})
                self.logger.put({"role": assistant_role, "content": assistant_response.replace("\n", " ")})

                try:
                    critic_explanation = critique["explanation"]
                except KeyError as e:
                    critic_explanation = e

                try:
                    ranking = critique["rating"]
                except KeyError as e:
                    ranking = random.randint(0, 5)

                move_to_rating[direction] = ranking

                if int(ranking) >= 4:
                    break

                actor_prompt = ReflectionRefinementActorRetryPrompt(
                    variables={
                        "EXPLANATION": critic_explanation,
                        "DIRECTION": direction
                    }
                )

            best_move = sorted(list(move_to_rating), key=lambda x: x[1], reverse=True)[0]

            action = self.curr_map.direction_to_action(best_move)
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
                self.base_prompt.name,
                f"{self.examples}-shot",
                GPT4LanguageModel.model_name,
            ),
            name="intel" + "_" + self.curr_map.name
        )

        environment.close()


def task_decomposition(examples, iterations=MAX_ITERATIONS):
    np.random.shuffle(MAPS)

    for i in range(iterations):
        experiment = Experiment(
            curr_map=FrozenLakeMap.deserialize(os.path.join(MAPS_DIR, MAPS[i])),
            base_prompt=TaskDecompositionBasePrompt,
            examples=examples
        )
        experiment.task_decomposition_run()

        print(f"Task Decomposition {examples}-shot: {i+1} of {iterations} completed.")


def multi_plan_selection(examples, iterations=MAX_ITERATIONS):
    np.random.shuffle(MAPS)

    for i in range(iterations):
        experiment = Experiment(
            curr_map=FrozenLakeMap.deserialize(os.path.join(MAPS_DIR, MAPS[i])),
            base_prompt=MultiPlanSelectionBasePrompt,
            examples=examples
        )
        experiment.multi_plan_selection_run()

        print(f"Multi-Plan Selection {examples}-shot: {i+1} of {iterations} completed.")


def reflection_refinement(examples, iterations=MAX_ITERATIONS):
    np.random.shuffle(MAPS)
    for i in range(iterations):
        experiment = Experiment(
            curr_map=FrozenLakeMap.deserialize(os.path.join(MAPS_DIR, MAPS[i])),
            base_prompt=ReflectionRefinementActorBasePrompt,
            examples=examples
        )
        experiment.reflection_refinement_run()

        print(f"Reflection Refinement {examples}-shot: {i+1} of {iterations} completed.")


def main():
    # Zero-shot
    # task_decomposition(0)
    # multi_plan_selection(0)
    # reflection_refinement(0)

    # One-shot
    # task_decomposition(1, iterations=math.ceil(MAX_ITERATIONS/2))
    # multi_plan_selection(1, iterations=math.ceil(MAX_ITERATIONS/2))
    # reflection_refinement(1, iterations=math.ceil(MAX_ITERATIONS/2))

    # Four-shot
    # task_decomposition(4, iterations=math.ceil(MAX_ITERATIONS/2))
    # multi_plan_selection(4, iterations=math.ceil(MAX_ITERATIONS/2))
    reflection_refinement(4, iterations=math.ceil(MAX_ITERATIONS/2))


if __name__ == "__main__":
    main()

