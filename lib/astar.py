import heapq
from collections import deque


class AStar:
    def __init__(self, map_bin: list[int], origin: list[int], goal: list[int]):
        self.map = map_bin
        self.origin = origin
        self.goal = goal
        self.path = deque()

    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        while current in came_from:
            self.path.appendleft(current)
            current = came_from[current]
        return self.path

    def search(self):
        open_set = []
        heapq.heappush(open_set, (0, self.origin))
        came_from = {}
        g_score = {self.origin: 0}
        f_score = {self.origin: self.heuristic(self.origin, self.goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == self.goal:
                return self.reconstruct_path(came_from, current)
            neighbors = [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                         (current[0], current[1] + 1), (current[0], current[1] - 1)]
            for neighbor in neighbors:
                if 0 <= neighbor[0] < len(self.map) and 0 <= neighbor[1] < len(self.map[0]) and not \
                        self.map[neighbor[0]][neighbor[1]]:
                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score.get(neighbor, float("inf")):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return None
