import os
import json
from prompt import Prompt
from oshandler import OSHandler

FROZENLAKE_PROMPTS = "FrozenLake-v1"


class TaskDecompositionBasePrompt(Prompt):
    name = "task_decomposition"
    description = "Custom chain of thought (CoT) prompt template"
    output_scheme = {
        "step_1": "",
        "step_2": "",
        "step_3": "up/down/left/right"
    }
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "task_decomposition", "base.txt")


class MultiPlanSelectionBasePrompt(Prompt):
    name = "multi_plan_selection_base"
    description = "Tree of Thought (ToT) Base prompt template"
    output_scheme = None
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "base.txt")


class MultiPlanSelectionTreeLvl1Prompt(Prompt):
    name = "multi_plan_selection_tree_lvl1"
    description = "Tree of Thought (ToT) Lvl1 prompt template"
    output_scheme = {
        "up": "",
        "down": "",
        "left": "",
        "right": ""
    }
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_1.txt")


class MultiPlanSelectionTreeLvl2Prompt(Prompt):
    name = "multi_plan_selection_tree_lvl2"
    description = "Tree of Thought (ToT) Lvl2 prompt template"
    output_scheme = {
        "up": {
            "new_coordinates": "",
            "is_in_obstacles": "",
            "is_in_boundaries": "",
            "goal_distance": ""
        },
        "down": {
            "new_coordinates": "",
            "is_in_obstacles": "",
            "is_in_boundaries": "",
            "goal_distance": ""
        },
        "left": {
            "new_coordinates": "",
            "is_in_obstacles": "",
            "is_in_boundaries": "",
            "goal_distance": ""
        },
        "right": {
            "new_coordinates": "",
            "is_in_obstacles": "",
            "is_in_boundaries": "",
            "goal_distance": ""
        },
        "success_probabilities": {
            "up": "float[0..1]",
            "down": "float[0..1]",
            "left": "float[0..1]",
            "right": "float[0..1]"
        }
    }
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_2.txt")


class MultiPlanSelectionTreeLvl3Prompt(Prompt):
    name = "multi_plan_selection_tree_lvl3"
    description = "Tree of Thought (ToT) Lvl3 prompt template"
    output_scheme = {
        "up": {
            "scenarios": "",
            "scenarios_safe": "boolean"
        },
        "down": {
            "scenarios": "",
            "scenarios_safe": "boolean"
        },
        "left": {
            "scenarios": "",
            "scenarios_safe": "boolean"
        },
        "right": {
            "scenarios": "",
            "scenarios_safe": "boolean"
        }
    }
    prompt_path = os.path.join(FROZENLAKE_PROMPTS, "multi_plan_selection", "tree_lvl_3.txt")


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
