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
ALGORITHM_COLORS = ["cadetblue", "slategray", "midnightblue", "steelblue"]


def plot_histograms(func_name: str, algorithm_names: list, result_list: list) -> None:
    """
    Plot one histogram per algorithm in a shared figure.

    Each subplot visualizes the distribution of best fitness values for a
    single algorithm, allowing direct comparison across all algorithms
    on the same benchmark function.

    Args:
        func_name (str): Name of the objective function (e.g. "Ackley").
        algorithm_names (list): Names of the algorithms to plot.
        result_list (list): One 1D array of best fitness values per algorithm.

    Returns:
        None
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
    #plt.savefig(f"histogram_{func_name}.png", dpi=300, bbox_inches='tight') # download the histogram images from the "results" folder instead of saving them here
    plt.show()
    plt.close(fig)


def plot_boxplot(func_name: str, algorithm_names: list, result_list: list) -> None:
    """
    Draw a grouped boxplot comparing algorithm fitness distributions.

    Each boxplot displays the median, interquartile range, and outliers for a
    given algorithm on the specified benchmark function.

    Args:
        func_name (str): Name of the objective function (e.g. "sphere").
        algorithm_names (list): List of algorithm name strings.
        result_list (list): One 1D array of best fitness values per algorithm.

    Returns:
        None
    """
    data = [np.asarray(v, dtype=float) for v in result_list]
    fig, ax = plt.subplots(figsize=(8, 5))

    bp = ax.boxplot(
        data,
        patch_artist=True,   # fills boxes with color
        notch=False,
        vert=True,
        widths=0.5,
        showfliers=True,
        flierprops=dict(marker="o", color="red", alpha=0.6, markersize=4)   
    )

    # Apply consistent colors to each box
    for patch, color in zip(bp["boxes"], ALGORITHM_COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)

    if func_name.lower() == "trid":
        ax.set_yscale("linear")
    else:
        min_val = min([np.min(d) for d in data])
        if min_val > 0:
            ax.set_yscale("log")    
        else:
            #max_abs = max([np.max(np.abs(d)) for d in data])
            #umbral = max_abs * 0.01 if max_abs > 0 else 1e-4

            #umbral= max(umbral, 1e-2)
            ax.set_yscale("symlog", linthresh=1e-8)


    ax.set_title(f"Fitness Boxplot — {func_name.capitalize()}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Algorithm", fontsize=11)
    ax.set_ylabel("Best Fitness", fontsize=11)
    ax.set_xticks(range(1, len(algorithm_names) + 1))
    ax.set_xticklabels(algorithm_names, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    #plt.savefig(f"boxplot_{func_name}.png", dpi=300, bbox_inches='tight') #download the boxplot images from the "results" folder instead of saving them here
    plt.show()
    plt.close(fig)


def plot_all(func_name: str, algorithm_names: list, result_list: list) -> None:
    """
    Generate both histogram and boxplot visualizations for a benchmark.

    This function is the primary entry point after collecting best fitness
    results for each algorithm on a given objective function.

    Args:
        func_name (str): Name of the objective function (e.g. "sphere").
        algorithm_names (list): List of algorithm name strings.
        result_list (list): One 1D array of best fitness values per algorithm.

    Example:
        from evobench.tools.plotter import plot_all

        plot_all(
            func_name       = "ackley",
            algorithm_names = ["EDA", "PSO", "ABC"],
            result_list     = [eda_results, pso_results, abc_results]
        )

    Returns:
        None
    """
    plot_histograms(func_name, algorithm_names, result_list)
    plot_boxplot(func_name, algorithm_names, result_list)