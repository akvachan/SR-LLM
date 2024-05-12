from intel import Intel


class FrozenLakeIntel(Intel):

    def __init__(
            self,
            map_size: int,
            map_name: str,
            num_obstacles: int,
            horizon: int,

    ):
        # Spatial metrics
        self.path = []
        self.goal_reached = False
        self.goal_reached_optimal = False
        self.goal_distance = -1
        self.obstacle_touched = False
        self.wall_touched = False
        self.traps_escaped = 0
        self.num_actions = 0

        # Static metrics
        self.map_size = map_size
        self.map_name = map_name
        self.num_obstacles = num_obstacles
        self.horizon = horizon

    def append_path(self, point: tuple[int, int]) -> None:
        self.path.append(point)

    def set_goal_reached(self, goal_reached: bool) -> None:
        self.goal_reached = goal_reached

    def set_goal_reached_optimal(self, goal_reached_optimal: bool) -> None:
        self.goal_reached_optimal = goal_reached_optimal

    def set_goal_distance(self, goal_distance: int) -> None:
        self.goal_distance = goal_distance

    def set_obstacle_touched(self, obstacle_touched: bool) -> None:
        self.obstacle_touched = obstacle_touched

    def set_wall_touched(self, wall_touched: bool) -> None:
        self.wall_touched = wall_touched

    def increment_traps_escaped(self) -> None:
        self.traps_escaped += 1

    def increment_num_actions(self):
        self.num_actions += 1

    def gather_intel(self, curr_map, curr_pos, prev_pos):
        self.increment_num_actions()
        self.set_goal_reached(True if curr_pos == curr_map.goals[0] else False)
        self.set_goal_reached_optimal(
            True if self.goal_reached and self.num_actions == len(curr_map.solution) else False)
        self.set_goal_distance(abs(curr_pos[0] - curr_map.goals[0][0]) + abs(curr_pos[1] - curr_map.goals[0][1]))
        self.set_obstacle_touched(curr_pos in curr_map.obstacles)
        self.set_wall_touched(curr_pos == prev_pos)
        if curr_map.has_escaped_trap(curr_pos, prev_pos):
            self.increment_traps_escaped()
        self.append_path(curr_pos)
