import os
from prompt import Prompt

FROZENLAKE_PROMPTS = "FrozenLake-v1"
FROZENLAKE_FINETUNING_PROMPTS = "FrozenLake-v1-Fine-Tuning"


class NaiveBasePrompt(Prompt):
    name = "naive_prompt"
    description = "Naive prompt template"
    output_scheme = {
        "explanation": "",
        "step_3": "up/down/left/right"
    }
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "naive", "base.txt")


class TaskDecompositionBasePrompt(Prompt):
    name = "task_decomposition"
    description = "Custom chain of thought (CoT) prompt template"
    output_scheme = {
        "step_1": "",
        "step_2": "",
        "step_3": "up/down/left/right"
    }
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "task_decomposition", "base.txt")
    examples_paths = [
        os.path.join(FROZENLAKE_PROMPTS, "task_decomposition", "base_example_1.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "task_decomposition", "base_example_2.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "task_decomposition", "base_example_3.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "task_decomposition", "base_example_4.txt")
    ]


class MultiPlanSelectionBasePrompt(Prompt):
    name = "multi_plan_selection_base"
    description = "Tree of Thought (ToT) Base prompt template"
    output_scheme = None
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "base.txt")
    examples_paths = None


class MultiPlanSelectionTreeLvl1Prompt(Prompt):
    name = "multi_plan_selection_tree_lvl1"
    description = "Tree of Thought (ToT) Lvl1 prompt template"
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_1.txt")
    examples_paths = [
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_1_example_1.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_1_example_2.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_1_example_3.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_1_example_4.txt")
    ]


class MultiPlanSelectionTreeLvl2Prompt(Prompt):
    name = "multi_plan_selection_tree_lvl2"
    description = "Tree of Thought (ToT) Lvl2 prompt template"
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_2.txt")
    examples_paths = [
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_2_example_1.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_2_example_2.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_2_example_3.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_2_example_4.txt")
    ]


class MultiPlanSelectionTreeLvl3Prompt(Prompt):
    name = "multi_plan_selection_tree_lvl3"
    description = "Tree of Thought (ToT) Lvl3 prompt template"
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_3.txt")
    examples_paths = [
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_3_example_1.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_3_example_2.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_3_example_3.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_3_example_4.txt")
    ]


class MultiPlanSelectionTreeLvl4Prompt(Prompt):
    name = "multi_plan_selection_tree_lvl4"
    description = "Tree of Thought (ToT) Lvl4 prompt template"
    output_scheme = {
        "rank_1": {
            "move": "up/down/left/right",
            "explanation": ""
        },
        "rank_2": {
            "move": "up/down/left/right",
            "explanation": ""
        },
        "rank_3": {
            "move": "up/down/left/right",
            "explanation": ""
        },
        "rank_4": {
            "move": "up/down/left/right",
            "explanation": ""
        }
    }
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_4.txt")
    examples_paths = [
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_4_example_1.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_4_example_2.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_4_example_3.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_4_example_4.txt")
    ]


class ReflectionRefinementActorBasePrompt(Prompt):
    name = "base_actor"
    description = "Prompt with Actor-Critic Editing (PACE) Actor Base prompt template"
    output_scheme = {
        "explanation": "",
        "move": "up/down/left/right"
    }
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "base_actor.txt")
    examples_paths = [
        os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "base_actor_example_1.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "base_actor_example_2.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "base_actor_example_3.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "base_actor_example_4.txt")
    ]


class ReflectionRefinementCriticBasePrompt(Prompt):
    name = "base_critic"
    description = "Prompt with Actor-Critic Editing (PACE) Critic Base prompt template"
    output_scheme = None
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "base_critic.txt")
    examples_paths = None


class ReflectionRefinementCriticPrompt(Prompt):
    name = "critic"
    description = "Prompt with Actor-Critic Editing (PACE) Critic prompt template"
    output_scheme = {
        "explanation": "",
        "rating": "int[0..5]"
    }
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "critic.txt")
    examples_paths = [
        os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "critic_example_1.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "critic_example_2.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "critic_example_3.txt"),
        os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "critic_example_4.txt")
    ]


class ReflectionRefinementActorRetryPrompt(Prompt):
    name = "actor_retry"
    description = "Prompt with Actor-Critic Editing (PACE) Critic prompt template"
    output_scheme = None
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "reflection_refinement", "actor_retry.txt")
    examples_paths = None


class SystemPromptGeneratorGPT(Prompt):
    name = "system_prompt_gpt_generation"
    description = "System prompt for generating training data with GPT"
    output_scheme = {
        "explanation": "",
        "move": "up/down/left/right"
    }
    prompt_path = os.path.join(FROZENLAKE_FINETUNING_PROMPTS, "system_prompt_gpt_generation.txt")
    examples_paths = None


class SystemPromptMistralInference(Prompt):
    name = "system_prompt_mistral_inference"
    description = "System prompt for inference using Mistral"
    output_scheme = {
        "explanation": "",
        "move": "up/down/left/right"
    }
    prompt_path = os.path.join(FROZENLAKE_FINETUNING_PROMPTS, "system_prompt_mistral_inference.txt")
    examples_paths = None
