from map import MapGenerator, MapSolver, MapManipulator
from oshandler import OSHandler
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import re
import random
import gymnasium as gym

PROJECT_ROOT = OSHandler.get_project_root(__file__)


class FrozenLakeMapGenerator(MapGenerator):
    maps_dir: str = ""
    map_name: str = "FrozenLake-v1"

    @classmethod
    def generate_batch(cls, map_sizes_classes: list[int], proportions: list[float], total_count: int) -> None:
        """
        Generates a map batch of various sizes and saves it in the project root directory.

        :param map_sizes_classes: Map sizes, e.g. [5, 10, 15, 20]
        :param proportions: Percentage of maps with corresponding size in the final batch, must sum up to 1, e.g. [0.25, 0.25, 0.25, 0.25]
        :param total_count: Total number of maps to generate, e.g. 200
        :return:
        """
        map_sizes = cls.generate_random_map_sizes(map_sizes_classes, proportions, total_count)
        for _id, map_size in enumerate(map_sizes):
            if not OSHandler.check_path(PROJECT_ROOT, cls.maps_dir, cls.map_name):
                OSHandler.make_dir(PROJECT_ROOT, cls.maps_dir, cls.map_name)
            cls.generate_single(_id, map_size, "ansi")

    @classmethod
    def generate_single(cls, _id: int, size: int, render_mode: str = "ansi") -> None:
        """
        Generates a single map and saves it in the project root directory.

        :param _id: Map number/identifier
        :param size: Size of the map
        :param render_mode: Gymnasium specific parameter, controls final representation of the map
        :return:
        """
        map_make = gym.make(cls.map_name, render_mode=render_mode, desc=generate_random_map(size=size))
        map_make.env.reset()
        map_make = map_make.env.render()
        map_make = FrozenLakeMapManipulator.remove_ansi(map_make)
        map_make = FrozenLakeMapManipulator.randomize(map_make)
        map_data = FrozenLakeMapManipulator.gather_data(map_make, _id)
        OSHandler.write_to_json(map_data, PROJECT_ROOT, cls.maps_dir, cls.map_name, f"fl{_id}_{size}.json")

    @staticmethod
    def generate_random_map_sizes(map_sizes, proportions, total_count) -> list[int]:
        counts = [round(p * total_count) for p in proportions]
        counts[-1] = total_count - sum(counts[:-1])

        sizes = []
        for size, count in zip(map_sizes, counts):
            sizes.extend([size] * count)

        return sizes


class FrozenLakeMapManipulator(MapManipulator):
    @staticmethod
    def remove_ansi(_map: str) -> str:
        _map = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', _map)
        return _map.strip()

    @staticmethod
    def randomize(_map: str) -> str:
        map_list = [list(row) for row in _map.split('\n')]
        current_start = None
        goal_position = None
        non_h_or_g_positions = []

        for r, row in enumerate(map_list):
            for c, char in enumerate(row):
                if char == 'S':
                    current_start = (r, c)
                elif char == 'G':
                    goal_position = (r, c)
                if char not in ('H', 'G'):
                    non_h_or_g_positions.append((r, c))

        if current_start:
            map_list[current_start[0]][current_start[1]] = 'F'
            if non_h_or_g_positions:
                new_start = random.choice(non_h_or_g_positions)
                map_list[new_start[0]][new_start[1]] = 'S'
                # Swap S and G with 25% probability if both positions are set
                if random.random() < 0.25 and goal_position:
                    map_list[new_start[0]][new_start[1]], map_list[goal_position[0]][goal_position[1]] = \
                        map_list[goal_position[0]][goal_position[1]], 'S'

        return '\n'.join(''.join(row) for row in map_list)

    @staticmethod
    def gather_data(_map: str, map_id: int):
        map_list = _map.split('\n')
        map_size = len(map_list[0])
        map_name = f"fl{map_id}_{map_size}.json"

        origin = None
        goal = None
        obstacles = []
        map_bin = []

        for r, row in enumerate(map_list):
            map_bin_row = []
            for c, char in enumerate(row):
                if char == 'S':
                    origin = (r, c)
                    map_bin_row.append(0)
                elif char == 'G':
                    goal = (r, c)
                    map_bin_row.append(0)
                elif char == 'H':
                    obstacles.append((r, c))
                    map_bin_row.append(1)
                else:
                    map_bin_row.append(0)
            map_bin.append(map_bin_row)

        map_data = {
            "map_name": map_name,
            "map_size": map_size,
            "origin": origin,
            "goal": goal,
            "obstacles": obstacles,
            "map_str": map_list,
            "map_bin": map_bin
        }

        return map_data


class FrozenLakeMapSolver(MapSolver):
    maps_dir: str = ""
    map_name: str = "FrozenLake-v1"

    def __init__(self, algorithm: object) -> None:
        self.algorithm = algorithm

    def solve_batch(self, ) -> None:
        pass

    def solve_single(self, map_file) -> None:
        if not map_file.endswith(".json"):
            raise ValueError("Only .json files are supported")
        if not OSHandler.check_path(PROJECT_ROOT, FrozenLakeMapSolver.maps_dir, FrozenLakeMapSolver.map_name, map_file):
            raise FileNotFoundError(
                f"Map {PROJECT_ROOT}/{FrozenLakeMapSolver.maps_dir}/{FrozenLakeMapSolver.map_name}/{map_file} does not exist.")
        if map_bin := OSHandler.read_from_json(PROJECT_ROOT, FrozenLakeMapSolver.maps_dir, FrozenLakeMapSolver.map_name,
                                               map_file).get("map_bin", None) is None:
            raise KeyError(f"Map {map_file} does not contain a valid map_bin array.")


        return self.algorithm.search(map_bin)
