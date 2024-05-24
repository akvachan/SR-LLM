#!/usr/bin/env python
import time

from frozenlake.map import FrozenLakeMap
from oshandler import OSHandler
import gymnasium as gym

import os
import argparse

MAP_NAME = "FrozenLake-v1"


def main(name, render_mode):
    path = os.path.join(OSHandler.get_project_root(), "maps", MAP_NAME, name)
    _map = FrozenLakeMap.deserialize(path)
    strarr = _map.strarr

    print("Origin: ", _map.origin)
    print("Goal: ", _map.goals[0])
    print("Obstacles: ", _map.obstacles)

    env = gym.make(MAP_NAME, is_slippery=False, render_mode=render_mode, desc=strarr)
    _ = env.reset()
    done = False
    while not done:
        time.sleep(10)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=f"Visualize {MAP_NAME} map according to name passed"
    )
    parser.add_argument('--name', type=str)
    parser.add_argument('--render_mode', type=str, default='human', choices=['human', 'rgb_array', 'ansi'])
    args = parser.parse_args()

    main(name=args.name, render_mode=args.render_mode)
