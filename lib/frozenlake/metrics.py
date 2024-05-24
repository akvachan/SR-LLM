import numpy as np

from metrics import Metrics


class FrozenLakeMetrics(Metrics):

    @staticmethod
    def success_rate(num_runs, num_successful_runs):
        return num_successful_runs / num_runs if num_runs > 0 else 0

    @staticmethod
    def optimal_rate(num_runs, num_optimal_runs):
        return num_optimal_runs / num_runs if num_runs > 0 else 0

    @staticmethod
    def feasible_rate(num_runs, num_feasible_runs):
        return num_feasible_runs / num_runs if num_runs > 0 else 0

    @staticmethod
    def mean_goal_distance(goal_distances):
        return np.mean(goal_distances) if len(goal_distances) > 0 else -1

    @staticmethod
    def mean_traps_escaped(traps_escaped):
        return np.mean(traps_escaped) if len(traps_escaped) > 0 else -1
