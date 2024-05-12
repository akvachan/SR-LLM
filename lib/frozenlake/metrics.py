import numpy as np

from metrics import Metrics


class FrozenLakeMetrics(Metrics):

    @staticmethod
    def success_rate(num_runs, num_successful_runs):
        return num_runs / num_successful_runs

    @staticmethod
    def optimal_rate(num_runs, num_optimal_runs):
        return num_runs / num_optimal_runs

    @staticmethod
    def feasible_rate(num_runs, num_feasible_runs):
        return num_runs / num_feasible_runs

    @staticmethod
    def mean_goal_distance(goal_distances):
        return np.mean(goal_distances)

    @staticmethod
    def mean_traps_escaped(total_traps_escaped):
        return np.mean(total_traps_escaped)