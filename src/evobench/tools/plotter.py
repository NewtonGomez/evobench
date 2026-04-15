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


def plot_histograms(func_name: str, algorithm_names: list, result_list: list) -> None:
    """
    Plots one histogram per algorithm, all in the same window as subplots.
 
    Each subplot shows the fitness distribution of a single algorithm,
    making it easy to read without overlapping bars.
 
    Args:
        func_name       : Name of the objective function (e.g. "Ackley").
        algorithm_names : List of algorithm names (e.g. ["EDA", "PSO", "BEE"]).
        result_list     : List of 1D arrays, one per algorithm, with best_fitness values.
    """
    n_algos = len(algorithm_names)
    fig, axes = plt.subplots(1, n_algos, figsize=(5 * n_algos, 4), sharey=True)
 
    # sharey=True keeps the Y axis scale consistent across all subplots
 
    if n_algos == 1:
        axes = [axes]
 
    for i, (ax, name, data) in enumerate(zip(axes, algorithm_names, result_list)):
        data   = np.asarray(data, dtype=float)
        n_bins = int(np.ceil(np.log2(len(data)) + 1))  # Sturges rule
 
        ax.hist(
            data,
            bins=n_bins,
            color=ALGORITHM_COLORS[i % len(ALGORITHM_COLORS)],
            edgecolor="white",
            alpha=0.85
        )
 
        ax.set_title(name, fontsize=12, fontweight="bold")
        ax.set_xlabel("Best Fitness", fontsize=10)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
 
    axes[0].set_ylabel("Frequency", fontsize=10)
 
    fig.suptitle(
        f"Fitness Distribution — {func_name.capitalize()}",
        fontsize=14,
        fontweight="bold"
    )
 
    plt.tight_layout()
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
        patch.set_alpha(0.75)

    if func_name.lower() == "trid":
        ax.set_yscale("linear")
    else:
        ax.set_yscale("symlog", linthresh=1e-5)  # Log scale helps visualize wide fitness ranges
    ax.set_title(f"Fitness Boxplot — {func_name.capitalize()}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Algorithm", fontsize=11)
    ax.set_ylabel("Best Fitness", fontsize=11)
    ax.set_xticks(range(1, len(algorithm_names) + 1))
    ax.set_xticklabels(algorithm_names, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
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
    plot_histograms(func_name, algorithm_names, result_list)
    plot_boxplot(func_name, algorithm_names, result_list)