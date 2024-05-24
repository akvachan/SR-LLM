#!/usr/bin/env python

from frozenlake.map import FrozenLakeMapSolver

import argparse


def main(maps_dir):
    if maps_dir:
        FrozenLakeMapSolver.solve_batch(maps_dir)
    else:
        FrozenLakeMapSolver.solve_batch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solves a batch of frozen lake maps. No arguments are needed.",
    )
    parser.add_argument("--maps_dir", type=str, default=None, help="Path to the frozen lake maps")
    args = parser.parse_args()

    main(args.maps_dir)
