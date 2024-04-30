#!/usr/bin/env python

from frozenlake.map import FrozenLakeMapSolver

import argparse

def main():
    FrozenLakeMapSolver.solve_batch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solves a batch of frozen lake maps. No arguments are needed.",
    )
    main()
