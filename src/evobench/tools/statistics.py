import numpy as np
from scipy import stats

"""
Statistical Analysis Module for Evolutionary Benchmarking
This module provides the statistical infrastructure to compare the performance
of multiple evolutionary algorithms across benchmark functions.
    1. Shapiro-Wilk normality test to decide which parametric path to take
    2. ANOVA parametric test (assumes normality)
    3. Kruskal-Wallis H-test non-parametric to ANOVA
"""
def normality_test(vector: np.ndarray) -> list:
    """
    Evaluate whether a single sample follows a normal distribution.

    The Shapiro-Wilk test is used to determine if the sample data is
    consistent with normality. The result includes the test statistic,
    the p-value, and a boolean flag indicating whether normality is
    accepted at the 0.05 significance level.

    Args:
        vector (np.ndarray): Sample values for one algorithm.

    Returns:
        list: [statistic, p-value, is_normal]
    """
    vector = np.asarray(vector, dtype=float)
    stat, p = stats.shapiro(vector)
    return [round(stat, 6), round(p, 6), bool(p > 0.05)]

def anova_test(*vectors: np.ndarray) -> list:
    """
    Perform a one-way ANOVA test across multiple groups.

    ANOVA is a parametric test used when each group is assumed to follow a
    normal distribution. It compares the group means to determine whether
    at least one algorithm performs differently from the others.

    Args:
        *vectors (np.ndarray): One-dimensional sample arrays for each algorithm.

    Returns:
        list: [statistic, p-value, reject_h0]
    """
    groups = [np.asarray(v, dtype=float) for v in vectors]
    f_stat, p = stats.f_oneway(*groups)
    return [round(f_stat, 6), round(float(p), 6), bool(p < 0.05)]

def kruskal_test(*vectors: np.ndarray) -> list:
    """
    Perform the Kruskal-Wallis H-test across multiple groups.

    This non-parametric alternative to ANOVA is used when the normality
    assumption does not hold. It tests whether the distribution of
    ranks differs between algorithms.

    Args:
        *vectors (np.ndarray): One-dimensional sample arrays for each algorithm.

    Returns:
        list: [statistic, p-value, reject_h0]
    """
    groups = [np.asarray(v, dtype=float) for v in vectors]
    h_stat, p = stats.kruskal(*groups)
    return [round(h_stat, 6), round(float(p), 6), bool(p < 0.05)]

def analyze(func_name: str, result_list: list, algorithm_names: list) -> list:
    """
    Analyze benchmark results and decide the appropriate statistical test.

    This function checks normality for each algorithm's result vector and
    chooses either ANOVA or Kruskal-Wallis based on that conclusion.
    The returned list contains the function name, algorithm labels,
    normality test summaries, selected test name, and hypothesis result.

    Args:
        func_name (str): Name of the benchmark function.
        result_list (list): One-dimensional result arrays for each algorithm.
        algorithm_names (list): Names of the algorithms being compared.

    Returns:
        list: [func_name, algorithm_names, normality_results, test_used, hypothesis]
    """

    algorithm_results = [np.asarray(vec, dtype=float) for vec in result_list]
    # Convert each list of results into a NumPy float array for statistical tests.

    normality_results = [normality_test(vec) for vec in algorithm_results]
    # Run normality tests for every algorithm dataset.

    all_normal = all(result[2] for result in normality_results)
    # Determine whether every algorithm sample passed normality.

    if all_normal:
        hypothesis = anova_test(*algorithm_results)
        test_used = "ANOVA"
    else:
        hypothesis = kruskal_test(*algorithm_results)
        test_used = "Kruskal-Wallis"
    # Choose the correct hypothesis test based on normality.

    return [func_name, algorithm_names, normality_results, test_used, hypothesis]

def stat_report(result_data: list) -> None:
    """
    Print a formatted statistical summary report.

    The report extracts values from the result payload and prints the
    normality test outcomes for each algorithm, followed by the selected
    hypothesis test and its decision.

    Args:
        result_data (list): Output from analyze() containing all test results.

    Returns:
        None
    """
    func_name = result_data[0]
    algorithm_names = result_data[1]
    normality_results = result_data[2]
    test_used = result_data[3]
    hypothesis = result_data[4]

    print(f"\nFunction: {func_name.upper()}")

    print("\nNormality Test Results:")
    for i in range(len(algorithm_names)):
        algorithm = algorithm_names[i]
        norm = normality_results[i]
        status = "Normal" if norm[2] else "Not Normal"
        print(f"{algorithm:<8} W={norm[0]:.4f} p={norm[1]:.4f} -> {status}")
    # Display normality status for each algorithm.

    print(f"\n  [Hypothesis Test — {test_used}]")
    stat_letter = "F" if test_used == "ANOVA" else "H"
    print(f"    {stat_letter}={hypothesis[0]:.4f}  p={hypothesis[1]:.4f}", end="  ")
    print("-> H0 REJECTED (Differences exist)" if hypothesis[2] else "-> H0 NOT rejected (They perform equally)")
    # Print the hypothesis test result and decision.

