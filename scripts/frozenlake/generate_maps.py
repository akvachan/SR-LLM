#!/usr/bin/env python

from frozenlake.map import FrozenLakeMapGenerator

import argparse
import numpy as np


def main(map_sizes, proportions, map_count):
    FrozenLakeMapGenerator.generate_batch(map_sizes, proportions, map_count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a batch of frozen lake maps",
        epilog="""Example usage: python generate_maps.py --map_sizes 4 8 12 --proportions 0.33 0.33 0.34 
        --map_count 128"""
    )
    parser.add_argument("--map_sizes", type=int, nargs='+', default=[4, 8, 12], help="List of map sizes")
    parser.add_argument("--proportions", type=float, nargs='+', default=[1 / 3, 1 / 3, 1 / 3],
                        help="Proportions for each map size (must sum up to 1)")
    parser.add_argument("--map_count", type=int, default=128, help="Total number of maps to generate")
    args = parser.parse_args()

    if not np.isclose(sum(args.proportions), 1):
        raise ValueError("Proportions must sum to 1")

    main(args.map_sizes, args.proportions, args.map_count)
