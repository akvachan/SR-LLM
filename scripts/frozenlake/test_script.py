from frozenlake.prompt import (
    TaskDecompositionBasePrompt,
    MultiPlanSelectionBasePrompt,
    MultiPlanSelectionTreeLvl1Prompt,
    MultiPlanSelectionTreeLvl2Prompt,
    MultiPlanSelectionTreeLvl3Prompt,
    MultiPlanSelectionTreeLvl4Prompt
)

variables = {
    "SIZE": "1blablabla",
    "GOAL": "2blablabla",
    "MAX_TOKENS": "3blablabla",
    "ORIGIN": "4blablabla",
    "OBSTACLES": "5blablabla",
    "LOWER_BOUND": "6blablabla",
    "UPPER_BOUND": "7blablabla",
}


task_decomposition_base_prompt = TaskDecompositionBasePrompt(
    variables=variables,
    has_output_scheme=True,
)
print(task_decomposition_base_prompt.content)

print("\n\n\n")

multi_plan_selection_base_prompt = MultiPlanSelectionBasePrompt(
    variables=variables,
)
print(multi_plan_selection_base_prompt.content)

print("\n\n\n")

variables = {
    "FEEDBACK": "feedmeblabla"
}

multi_plan_selection_tree_lvl1_prompt = MultiPlanSelectionTreeLvl1Prompt(
    variables=variables,
    has_output_scheme=True,
)

print(multi_plan_selection_tree_lvl1_prompt.content)

print("\n\n\n")

multi_plan_selection_tree_lvl2_prompt = MultiPlanSelectionTreeLvl2Prompt(
    has_output_scheme=True
)

print(multi_plan_selection_tree_lvl2_prompt.content)

print("\n\n\n")

multi_plan_selection_tree_lvl3_prompt = MultiPlanSelectionTreeLvl3Prompt(
    has_output_scheme=True
)

print(multi_plan_selection_tree_lvl3_prompt.content)

print("\n\n\n")

multi_plan_selection_tree_lvl4_prompt = MultiPlanSelectionTreeLvl4Prompt(
    has_output_scheme=True
)

print(multi_plan_selection_tree_lvl4_prompt.content)

