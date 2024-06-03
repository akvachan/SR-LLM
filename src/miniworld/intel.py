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