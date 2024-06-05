import os
import argparse
import matplotlib.pyplot as plt
from frozenlake.intel import FrozenLakeIntel
from oshandler import OSHandler

def gather_metrics(exp_dirs):
    data = []
    for exp_dir in exp_dirs:
        intels = OSHandler.get_file_list(exp_dir)
        map_size_to_runs = {}
        map_size_to_success = {}

        for intel in intels:
            _intel = FrozenLakeIntel.deserialize(os.path.join(exp_dir, intel))
            map_size = _intel.map_size
            if map_size not in map_size_to_runs:
                map_size_to_runs[map_size] = 0
                map_size_to_success[map_size] = 0
            map_size_to_runs[map_size] += 1
            if _intel.goal_reached:
                map_size_to_success[map_size] += 1

        for map_size in map_size_to_runs:
            success_rate = map_size_to_success[map_size] / map_size_to_runs[map_size]
            data.append({
                "exp_dir": exp_dir,
                "map_size": map_size,
                "success_rate": success_rate
            })

    return data

def plot_success_rate(data):
    plt.figure(figsize=(10, 6))

    exp_dirs = set([entry["exp_dir"] for entry in data])
    for exp_dir in exp_dirs:
        exp_data = [entry for entry in data if entry["exp_dir"] == exp_dir]
        exp_data = sorted(exp_data, key=lambda x: x["map_size"])  # Sort by map size
        map_sizes = [entry["map_size"] for entry in exp_data]
        success_rates = [entry["success_rate"] for entry in exp_data]

        plt.plot(map_sizes, success_rates, marker='o', label=exp_dir)

    plt.xlabel('Map Size')
    plt.ylabel('Success Rate')
    plt.title('Success Rate vs Map Size')
    plt.grid(True)
    plt.legend(loc='best')
    plt.xticks(ticks=sorted(set([entry["map_size"] for entry in data])), labels=sorted(set([entry["map_size"] for entry in data])))
    plt.show()

def main(exp_dirs):
    data = gather_metrics(exp_dirs)
    plot_success_rate(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluates experiments on FrozenLake-v1 maps and plots success rate vs map size",
        epilog="""Example usage: python plot_experiments.py --exp_dirs"""
    )
    parser.add_argument("--exp_dirs", type=str, nargs='+', required=True,
                        help="Directories with the results of experiments")
    args = parser.parse_args()
    main(args.exp_dirs)
