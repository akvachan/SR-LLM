from frozenlake.metrics import FrozenLakeMetrics
from frozenlake.intel import FrozenLakeIntel
from oshandler import OSHandler

import os

EXPERIMENTS_PATH = os.path.join(OSHandler.get_project_root(), "experiments", "STP")


def main():
    evaluation = {}
    for experiment_name in os.listdir(EXPERIMENTS_PATH):
        intel_path = os.path.join(EXPERIMENTS_PATH, experiment_name, "0-shot", "gpt-4o")
        intels = OSHandler.get_file_list(intel_path)

        num_runs = len(intels)
        num_successful_runs = 0
        num_optimal_runs = 0
        num_feasible_runs = 0
        goal_distances = []
        traps_escaped = []

        for intel in intels:
            _intel = FrozenLakeIntel.deserialize(os.path.join(intel_path, intel))
            num_successful_runs += 1 if _intel.goal_reached else 0
            num_optimal_runs += 1 if _intel.goal_reached_optimal else 0
            num_feasible_runs += 1 if not _intel.goal_reached and _intel.num_actions == _intel.horizon else 0
            goal_distances.append(_intel.goal_distance)
            traps_escaped.append(_intel.traps_escaped)

        success_rate = FrozenLakeMetrics.success_rate(num_runs, num_successful_runs)
        optimal_rate = FrozenLakeMetrics.optimal_rate(num_runs, num_optimal_runs)
        feasible_rate = FrozenLakeMetrics.feasible_rate(num_runs, num_feasible_runs)
        mean_goal_distance = FrozenLakeMetrics.mean_goal_distance(goal_distances)
        mean_traps_escaped = FrozenLakeMetrics.mean_traps_escaped(traps_escaped)

        evaluation[experiment_name] = {
            "success_rate": success_rate,
            "optimal_rate": optimal_rate,
            "feasible_rate": feasible_rate,
            "mean_goal_distance": mean_goal_distance,
            "mean_traps_escaped": mean_traps_escaped
        }
    print(evaluation)


if __name__ == "__main__":
    main()