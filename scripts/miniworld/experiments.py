import argparse
import miniworld
from miniworld.envs.putnext import PutNext
from language_models.gpt4_vision import GPT4VisionLanguageModel
from prompt import Prompt
from map import word_to_action

MAX_ITERATIONS = 64


class Experiment:
    def __init__(self, system_message):
        self.system_message = system_message

    def naive_run(self):
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

        language_model = GPT4VisionLanguageModel(
            agent_name="FrozenLakeAgent_1",
            system_message=self.system_message,
        )

        environment = PutNext(size=12, render_mode="human")
        obs, reward, termination, truncation, info = environment.reset()

        terminated = False
        while not terminated:
            feedback = Prompt(content=f"Choose the next action.")

            response = language_model.generate_response(feedback, obs)

            try:
                word = response["word_action"]
                action = word_to_action(word)
            except KeyError as e:
                print(e)
                action = environment.action_space.sample()

            observation, reward, terminated, _, info = environment.step(action)

        environment.close()


def naive(iterations):
    for i in range(iterations):
        experiment = Experiment()
        experiment.naive_run()

        print(f"Multi-Plan Selection 0-shot: {i + 1} of {iterations} completed.")


def main(iterations: int):
    naive(iterations)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Conducts experiment on a PutNext map",
        epilog="""Example usage: python experiments.py --iter 64"""
    )
    parser.add_argument("--iter", type=int, default=MAX_ITERATIONS, help="Number of iterations/maps to experiment on")
    args = parser.parse_args()
    main(args.iterations)
