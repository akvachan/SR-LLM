# Custom modules import
from astar import AStar
from map import MapGenerator, MapSolver, MapManipulator
from oshandler import OSHandler

# Site modules import
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import re
import random
import gymnasium as gym
from typing import Callable

PROJECT_ROOT = OSHandler.get_project_root()


class FrozenLakeMapGenerator(MapGenerator):
    """
    Class responsible for generating the frozenlake map
    """

    maps_dir: str = "maps"
    map_name: str = "FrozenLake-v1"

    @classmethod
    def generate_batch(cls, map_sizes_classes: list[int], proportions: list[float], total_count: int) -> None:
        """
        Generates a map batch of various sizes and saves it in the project root directory.

        :param map_sizes_classes: Map sizes, e.g. [5, 10, 15, 20]
        :param proportions: Percentage of maps with the corresponding size in the final batch, must sum up to 1, e.g. [0.25, 0.25, 0.25, 0.25]
        :param total_count: Total number of maps to generate, e.g. 200
        :return:
        """
        if not OSHandler.check_path(PROJECT_ROOT, cls.maps_dir, cls.map_name):
            OSHandler.make_dir(PROJECT_ROOT, cls.maps_dir, cls.map_name)
        map_sizes = cls.generate_random_map_sizes(map_sizes_classes, proportions, total_count)
        for _id, map_size in enumerate(map_sizes):
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
        gym_mk = gym.make(cls.map_name, render_mode=render_mode, desc=generate_random_map(size=size))
        gym_mk.env.reset()
        rendered_map = gym_mk.env.render()
        gym_mk.close()

        cleaned_map = FrozenLakeMapManipulator.remove_ansi(rendered_map)
        randomized_map = FrozenLakeMapManipulator.randomize(cleaned_map)
        map_data = FrozenLakeMapManipulator.gather_data(randomized_map, _id)

        OSHandler.write_to_json(map_data, PROJECT_ROOT, cls.maps_dir, cls.map_name, f"fl{_id}_{size}.json")

    @staticmethod
    def generate_random_map_sizes(map_sizes_classes, proportions, total_count) -> list[int]:
        """
        Generates a list of numbers representing different sizes of the maps.

        :param map_sizes_classes: Map sizes, only these numbers will be in a final list
        :param proportions: Percentage of maps with the corresponding size
        :param total_count: Length of the final list
        :return: A list of integers
        """
        counts = [round(p * total_count) for p in proportions]
        counts[-1] = total_count - sum(counts[:-1])

        sizes = []
        for size, count in zip(map_sizes_classes, counts):
            sizes.extend([size] * count)

        return sizes


class FrozenLakeMapManipulator(MapManipulator):
    """
    Class responsible for various manipulations with the frozenlake map.
    """

    @staticmethod
    def remove_ansi(_map: str) -> str:
        """
        Removes ansi color codes from the map string.

        :param _map: Map string to remove ansi from
        :return: Map string without ansi and trailing whitespaces
        """
        _map = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', _map)
        return _map.strip()

    @staticmethod
    def randomize(_map: str) -> str:
        """
        Randomizes the map string by placing the origin tile 'S' on a non-obstacle, non-goal tile.
        There is a 35% chance that the goal tile 'G' and the origin tile 'S' will swap positions.

        :param _map: A string representation of the map where 'S' is the start, 'G' is the goal, 'H' is an obstacle.
        :return: A randomized map string with updated 'S' and potentially swapped 'S' and 'G'.
        """
        map_list = [list(row) for row in _map.split('\n')]
        origin_pos = None
        goal_pos = None
        non_obstacle_positions = []

        for row_idx, row in enumerate(map_list):
            for col_idx, char in enumerate(row):
                if char == 'S':
                    origin_pos = (row_idx, col_idx)
                elif char == 'G':
                    goal_pos = (row_idx, col_idx)
                if char not in ('H', 'G'):
                    non_obstacle_positions.append((row_idx, col_idx))

        if origin_pos and non_obstacle_positions:
            map_list[origin_pos[0]][origin_pos[1]] = 'F'
            new_origin = random.choice(non_obstacle_positions)
            map_list[new_origin[0]][new_origin[1]] = 'S'

            if goal_pos and random.random() < 0.35:
                map_list[new_origin[0]][new_origin[1]], map_list[goal_pos[0]][goal_pos[1]] = \
                    map_list[goal_pos[0]][goal_pos[1]], 'S'

        return '\n'.join(''.join(row) for row in map_list)

    @staticmethod
    def gather_data(_map: str, _id: int):
        """
        Gathers data from map string.
        Data includes its size, origin position, goal position and obstacles positions.
        Additional information will be added, such as map name and map in binary list representation.

        :param _map: Map string to gather data from
        :param _id: Map number/identifier
        :return: Dictionary containing necessary data
        """
        map_list = _map.split('\n')
        map_size = len(map_list[0])
        map_name = f"fl{_id}_{map_size}.json"

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

    @staticmethod
    def has_escaped_trap(_map: list[str], prev_pos: tuple[int, int], curr_pos: tuple[int, int]) -> bool:
        """
        Method that checks if the agent escaped the trap.
        Trap is defined as a position from which there is only one exit.
        Escaping the trap means previously being in a trap and then not anymore.

        :param _map: A map in list of string format
        :param prev_pos: Coordinates of the previous position on the map
        :param curr_pos: Coordinates of the current position on the map
        :return: Boolean value indicating if trap was escaped
        """
        def count_exits(map_grid, row, col):
            rows = len(map_grid)
            cols = len(map_grid[0])
            exit_count = 0
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for d in directions:
                new_row, new_col = row + d[0], col + d[1]
                if 0 <= new_row < rows and 0 <= new_col < cols:
                    if map_grid[new_row][new_col] != 'H':
                        exit_count += 1
            return exit_count

        def is_trapped(map_grid, row, col):
            return count_exits(map_grid, row, col) == 1

        prev_row, prev_col = prev_pos
        curr_row, curr_col = curr_pos

        was_trapped = is_trapped(_map, prev_row, prev_col)
        is_not_trapped = not is_trapped(_map, curr_row, curr_col)

        return was_trapped and is_not_trapped


class FrozenLakeMapSolver(MapSolver):
    """
    Class responsible for solving the frozenlake map.
    """

    maps_dir: str = "maps"
    map_name: str = "FrozenLake-v1"
    algorithm: Callable = AStar

    @classmethod
    def solve_batch(cls) -> None:
        """
        Solves a map batch that was previously generated by MapGenerator.

        :return:
        """
        map_files = OSHandler.get_file_list(PROJECT_ROOT, cls.maps_dir, cls.map_name)
        for map_file in map_files:
            cls.solve_single(map_file)

    @classmethod
    def solve_single(cls, map_file) -> None:
        """
        Solves a single map that was previously generated by MapGenerator.

        :param map_file: Name of the map file in the dedicated maps directory at project root
        :return:
        """
        cls.check_json_map(map_file)

        map_dict = OSHandler.read_from_json(PROJECT_ROOT, cls.maps_dir, cls.map_name, map_file)
        algorithm = cls.algorithm(map_bin=map_dict["map_bin"], origin=map_dict["origin"], goal=map_dict["goal"])

        optimal_path = algorithm.search()
        map_dict["map_solution"] = optimal_path

        OSHandler.write_to_json(map_dict, PROJECT_ROOT, cls.maps_dir, cls.map_name, map_file)

    @classmethod
    def check_json_map(cls, map_file) -> None:
        """
        Checks if the map file is a valid json file with all the necessary information to solve the map.

        :param map_file: Name of the map file in the dedicated maps directory at project root
        :return:
        """
        if not map_file.endswith(".json"):
            raise ValueError("Only .json files are supported")

        if not OSHandler.check_path(PROJECT_ROOT, cls.maps_dir, cls.map_name, map_file):
            raise FileNotFoundError(
                f"Map {PROJECT_ROOT}/{cls.maps_dir}/{cls.map_name}/{map_file} does not exist.")

        map_dict = OSHandler.read_from_json(PROJECT_ROOT, cls.maps_dir, cls.map_name, map_file)

        if map_dict.get("map_bin", None) is None:
            raise KeyError(f"Map {map_file} does not contain a valid map_bin array.")

        if map_dict.get("origin", None) is None:
            raise KeyError(f"Map {map_file} does not contain a valid origin.")

        if map_dict.get("goal", None) is None:
            raise KeyError(f"Map {map_file} does not contain a valid goal.")
