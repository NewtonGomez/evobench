"""
Core statistical tests for evaluating optimization algorithm results.

This module provides wrappers for various statistical tests from SciPy,
standardizing their outputs for use in the analysis pipeline.
"""

import numpy as np
from scipy import stats
from typing import List, Union, Tuple


def normality_test(
    vector: Union[np.ndarray, List[float]], 
    alpha: float = 0.05, 
    test_type: str = "shapiro"
) -> List[Union[float, bool]]:
    """
    Performs a normality test on a given array.

    Args:
        vector (Union[np.ndarray, List[float]]): The sample data to test.
        alpha (float, optional): The significance level. Defaults to 0.05.
        test_type (str, optional): The type of normality test to perform. 
                                   Options: 'shapiro', 'ks', 'dagostino'. 
                                   Defaults to "shapiro".

    Returns:
        List[Union[float, bool]]: A list containing [statistic, p-value, is_normal_boolean].

    Raises:
        ValueError: If an unsupported test_type is provided.
    """
    vector = np.asarray(vector, dtype=float)

    if test_type == "shapiro":
        stat, p = stats.shapiro(vector)
    elif test_type == "ks":
        # Standardize the data for Kolmogorov-Smirnov test against a normal distribution
        vector_norm = (vector - np.mean(vector)) / (np.std(vector, ddof=1) + 1e-8)
        stat, p = stats.kstest(vector_norm, 'norm')
    elif test_type == "dagostino":
        stat, p = stats.normaltest(vector)
    else:
        raise ValueError(f"Unsupported normality test type: '{test_type}'")

    is_normal = p > alpha
    return [round(stat, 6), round(float(p), 6), bool(is_normal)]


def parametric_test(
    *vectors: Union[np.ndarray, List[float]], 
    alpha: float = 0.05, 
    test_type: str = "anova"
) -> Tuple[float, float, bool, str, str]:
    """
    Performs a global parametric test to check for significant differences.

    Args:
        *vectors (Union[np.ndarray, List[float]]): Multiple arrays of sample data.
        alpha (float, optional): The significance level. Defaults to 0.05.
        test_type (str, optional): The type of parametric test to perform. 
                                   Options: 'anova'. Defaults to "anova".

    Returns:
        Tuple[float, float, bool, str, str]: A tuple containing:
            (statistic, p_value, reject_h0_boolean, stat_name, test_used_name)

    Raises:
        ValueError: If an unsupported test_type is provided.
    """
    groups = [np.asarray(v, dtype=float) for v in vectors]

    if test_type == "anova":
        stat, p = stats.f_oneway(*groups)
        stat_name = "F-statistic"
        test_used = "ANOVA"
    else:
        raise ValueError(f"Unsupported parametric test type: '{test_type}'")

    reject_h0 = p < alpha
    return round(stat, 6), round(float(p), 6), bool(reject_h0), stat_name, test_used


def nonparametric_test(
    *vectors: Union[np.ndarray, List[float]], 
    alpha: float = 0.05, 
    test_type: str = "kruskal"
) -> Tuple[float, float, bool, str, str]:
    """
    Performs a global non-parametric test for independent samples.

    Args:
        *vectors (Union[np.ndarray, List[float]]): Multiple arrays of sample data.
        alpha (float, optional): The significance level. Defaults to 0.05.
        test_type (str, optional): The type of non-parametric test to perform. 
                                   Options: 'kruskal', 'mood'. Defaults to "kruskal".

    Returns:
        Tuple[float, float, bool, str, str]: A tuple containing:
            (statistic, p_value, reject_h0_boolean, stat_name, test_used_name)

    Raises:
        ValueError: If an unsupported test_type is provided.
    """
    groups = [np.asarray(v, dtype=float) for v in vectors]

    if test_type == "kruskal":
        stat, p = stats.kruskal(*groups)
        stat_name = "H-statistic"
        test_used = "Kruskal-Wallis"
    elif test_type == "mood":
        stat, p, _, _ = stats.median_test(*groups)
        stat_name = "Pearson's chi-squared"
        test_used = "Mood's Median Test"
    else:
        raise ValueError(f"Unsupported non-parametric test type: '{test_type}'")

    reject_h0 = p < alpha
    return round(stat, 6), round(float(p), 6), bool(reject_h0), stat_name, test_used


# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================
# Aliases for test compatibility with expected names
anova_test = parametric_test
kruskal_test = nonparametric_test
