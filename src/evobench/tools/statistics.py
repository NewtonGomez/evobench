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
    Returns: [statistic, p-value, is_normal]
    """
    vector = np.asarray(vector, dtype=float)
    stat, p = stats.shapiro(vector)
    return[round(stat,6), round(p,6), bool(p > 0.05)]

def anova_test(*vectors: np.ndarray) -> list:
    """
    Returns: [statistic, p-value, reject_h0]
    """
    groups = [np.asarray(v, dtype=float) for v in vectors]
    f_stat, p = stats.f_oneway(*groups)
    return [round(f_stat,6), round(float(p),6), bool(p < 0.05)]

def kruskal_test(*vectors: np.ndarray) -> list:
    """
    Returns: [statistic, p-value, reject_h0]
    """
    groups = [np.asarray(v, dtype=float) for v in vectors]
    h_stat, p = stats.kruskal(*groups)
    return [round(h_stat,6), round(float(p),6), bool(p < 0.05)] 

def analyze(func_name: str, result_list: list, algorithm_names: list) -> list:

    """
    Returns a main list containig all the information:
    0. Function name
    1. Algorithm names
    2. Normality test results for each algorithm
    3. ANOVA test results or Kruskal-Wallis test results depending on normality
    4. Hypothesis test results
    """

    algorithm_results = [np.asarray(vec, dtype=float) for vec in result_list]

    #First we must check the normality of each algorithm's results
    normality_results = [normality_test(vec) for vec in algorithm_results]

    #Second, we check the index 2 of each result (which is the boolean)
    all_normal = all(result[2] for result in normality_results)

    #Third, Set the hypothesis test
    if all_normal:
        hypothesis = anova_test(*algorithm_results)
        test_used = "ANOVA"
    else:
        hypothesis = kruskal_test(*algorithm_results)
        test_used = "Kruskal-Wallis"

    #Finally, we return the result
    return [func_name, algorithm_names, normality_results, test_used, hypothesis]   

def stat_report(result_data:list) -> None:
    """
    Prints the report by extracting the list index
    """
    func_name=result_data[0]    
    algorithm_names=result_data[1]
    normality_results=result_data[2]
    test_used=result_data[3]
    hypothesis=result_data[4]

    print(f"\nFunction: {func_name.upper()}")

    print("\nNormality Test Results:")
    for i in range(len(algorithm_names)):
        algorithm = algorithm_names[i]
        norm = normality_results[i]
        status = "Normal" if norm[2] else "Not Normal"
        print(f"{algorithm:<8} W={norm[0]:.4f} p={norm[1]:.4f} -> {status}")

    print(f"\n  [Hypothesis Test — {test_used}]")
    stat_letter = "F" if test_used == "ANOVA" else "H"
    print(f"    {stat_letter}={hypothesis[0]:.4f}  p={hypothesis[1]:.4f}", end="  ")
    print("-> H0 REJECTED (Differences exist)" if hypothesis[2] else "-> H0 NOT rejected (They perform equally)")   

