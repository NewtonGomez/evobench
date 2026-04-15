import numpy as np
import matplotlib.pyplot as plt

"""
Plotter Module for Evolutionary Benchmarking Results.

This module provides visualization tools to display the distribution
of best fitness values obtained by each algorithm across all benchmark
functions. For each objective function, two plots are generated:
    1. Histogram  — shows the frequency distribution of best fitness values
    2. Boxplot    — shows median, spread, and outliers per algorithm
"""

# Color assigned to each algorithm for visual consistency across plots
ALGORITHM_COLORS = ["steelblue", "darkorange", "mediumseagreen"]


def plot_histogram(func_name: str, algorithm_names: list, result_list: list) -> None:
    """
    Plots overlapping histograms of best_fitness distributions for each algorithm.

    One histogram per algorithm is drawn on the same figure to allow direct
    visual comparison of how results are distributed for a given function.

    Args:
        func_name       : Name of the objective function (e.g. "sphere").
        algorithm_names : List of algorithm name strings (e.g. ["EDA", "PSO", "ABC"]).
        result_list     : List of 1D arrays, one per algorithm, with best_fitness values.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    for i, (name, data) in enumerate(zip(algorithm_names, result_list)):
        data = np.asarray(data, dtype=float)

        # Sturges rule for bin count — works for any sample size
        n_bins = int(np.ceil(np.log2(len(data)) + 1))

        ax.hist(
            data,
            bins=n_bins,
            alpha=0.6,
            label=name,
            color=ALGORITHM_COLORS[i % len(ALGORITHM_COLORS)],
            edgecolor="white"
        )

    ax.set_title(f"Fitness Distribution — {func_name.capitalize()}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Best Fitness", fontsize=11)
    ax.set_ylabel("Frequency", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(f"histogram_{func_name}.png", dpi=150)
    plt.show()
    plt.close(fig)


def plot_boxplot(func_name: str, algorithm_names: list, result_list: list) -> None:
    """
    Plots a grouped boxplot comparing best_fitness distributions per algorithm.

    Each box shows the median, interquartile range, and outliers for a given
    algorithm on a specific objective function.

    Args:
        func_name       : Name of the objective function (e.g. "sphere").
        algorithm_names : List of algorithm name strings (e.g. ["EDA", "PSO", "ABC"]).
        result_list     : List of 1D arrays, one per algorithm, with best_fitness values.
    """
    data = [np.asarray(v, dtype=float) for v in result_list]

    fig, ax = plt.subplots(figsize=(8, 5))

    bp = ax.boxplot(
        data,
        patch_artist=True,   # fills boxes with color
        notch=False,
        vert=True,
        widths=0.5
    )

    # Apply consistent colors to each box
    for patch, color in zip(bp["boxes"], ALGORITHM_COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_title(f"Fitness Boxplot — {func_name.capitalize()}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Algorithm", fontsize=11)
    ax.set_ylabel("Best Fitness", fontsize=11)
    ax.set_xticks(range(1, len(algorithm_names) + 1))
    ax.set_xticklabels(algorithm_names, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(f"boxplot_{func_name}.png", dpi=150)
    plt.show()
    plt.close(fig)


def plot_all(func_name: str, algorithm_names: list, result_list: list) -> None:
    """
    Generates both histogram and boxplot for a given objective function.

    This is the main entry point called from run_experiments.py after
    collecting the best_fitness results of all algorithms on one function.

    Args:
        func_name       : Name of the objective function (e.g. "sphere").
        algorithm_names : List of algorithm name strings (e.g. ["EDA", "PSO", "ABC"]).
        result_list     : List of 1D arrays, one per algorithm, with best_fitness values.

    Example usage in run_experiments.py:
        from evobench.tools.plotter import plot_all

        plot_all(
            func_name       = "ackley",
            algorithm_names = ["EDA", "PSO", "ABC"],
            result_list     = [eda_results, pso_results, abc_results]
        )
    """
    plot_histogram(func_name, algorithm_names, result_list)
    plot_boxplot(func_name, algorithm_names, result_list)