from frozenlake.metrics import FrozenLakeMetrics
from frozenlake.intel import FrozenLakeIntel
from oshandler import OSHandler

import os
import argparse


def main(exp_dir: str):
    intels = OSHandler.get_file_list(exp_dir)
    num_runs = len(intels)
    num_successful_runs = 0
    num_optimal_runs = 0
    num_feasible_runs = 0
    goal_distances = []
    traps_escaped = []

    count = 0
    for intel in intels:
        count += 1
        _intel = FrozenLakeIntel.deserialize(os.path.join(exp_dir, intel))
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

    print(
        "success_rate", success_rate, "\n",
        "optimal_rate", optimal_rate, "\n",
        "feasible_rate", feasible_rate, "\n",
        "mean_goal_distance", mean_goal_distance, "\n",
        "mean_traps_escaped", mean_traps_escaped, "\n",
        "count", count
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluates an experiment on a FrozenLake-v1 map",
        epilog="""Example usage: python experiments.py --exp_dir"""
    )
    parser.add_argument("--exp_dir", type=str, nargs='+', default="task_decomposition",
                        help="Directory with the results of experiments")
    args = parser.parse_args()
    main(args.exp_dir[0])
