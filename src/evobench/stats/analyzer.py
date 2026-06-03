"""
Statistical analyzer for optimization algorithms.

This module processes the fitness results of multiple algorithms,
performs normality tests to decide the appropriate global statistical test,
and conducts post-hoc analysis if the global test shows significance.
"""

import numpy as np
from typing import List, Dict, Any

# Import tests from our own module
from evobench.stats.core_tests import normality_test, parametric_test, nonparametric_test
from evobench.stats.post_hoc import dunn_test, tukeyHSD_test


def analyze(
    func_name: str, 
    result_list: List[List[float]], 
    algorithm_names: List[str], 
    alpha: float = 0.05,
    norm_test: str = "shapiro",
    param_test: str = "anova",
    nonparam_test: str = "kruskal"
) -> Dict[str, Any]:
    """
    Analyzes the fitness results of multiple optimization algorithms.
    Automatically handles switching between parametric and non-parametric 
    global tests based on data normality, and includes post-hoc tests 
    when the global test is significant.

    Args:
        func_name (str): The name of the benchmark function evaluated.
        result_list (List[List[float]]): A list where each element contains the fitness results.
        algorithm_names (List[str]): Names corresponding to each algorithm in `result_list`.
        alpha (float, optional): The significance level. Defaults to 0.05.
        norm_test (str, optional): The normality test to use. Defaults to "shapiro".
        param_test (str, optional): The parametric test to use if data is normal. Defaults to "anova".
        nonparam_test (str, optional): The non-parametric test to use if data isn't normal. Defaults to "kruskal".

    Returns:
        Dict[str, Any]: A dictionary containing statistical descriptive data,
                        test results, p-values, and post-hoc analysis if applicable.
    """
    algorithm_results = [np.asarray(vec, dtype=float) for vec in result_list]
    stats_desc = {}

    # Calculate descriptive statistics
    for name, vec in zip(algorithm_names, algorithm_results):
        stats_desc[name] = {
            'mean': float(np.mean(vec)),
            'std': float(np.std(vec, ddof=1)),
            'best': float(np.min(vec))
        }

    # Execute selected normality test
    normality_results = [
        normality_test(vec, alpha=alpha, test_type=norm_test) 
        for vec in algorithm_results
    ]
    all_normal = all(result[2] for result in normality_results)

    # Execute selected global statistical test based on normality
    if all_normal:
        stat_val, p_val, is_significant, stat_name, test_used = parametric_test(
            *algorithm_results, alpha=alpha, test_type=param_test
        )
        post_hoc_test_name = "Tukey HSD"
    else:
        stat_val, p_val, is_significant, stat_name, test_used = nonparametric_test(
            *algorithm_results, alpha=alpha, test_type=nonparam_test
        )
        post_hoc_test_name = "Dunn's Test"

    # Perform post-hoc test if the global test is significant
    post_hoc_results = None
    if is_significant and len(algorithm_results) > 2:
        if all_normal:
            post_hoc_results = tukeyHSD_test(
                *algorithm_results, algorithm_names=algorithm_names, alpha=alpha
            )
        else:
            post_hoc_results = dunn_test(
                *algorithm_results, algorithm_names=algorithm_names, alpha=alpha
            )

    return {
        "func_name": func_name,
        "stats": stats_desc,
        "test_used": test_used,
        "stat_name": stat_name,
        "stat_val": stat_val,
        "p_val": p_val,
        "significant": is_significant,
        "alpha": alpha,
        "all_normal": all_normal,
        "post_hoc_test": post_hoc_test_name,
        "post_hoc_results": post_hoc_results,
        "normality_results": {
            name: result[2] for name, result in zip(algorithm_names, normality_results)
        }
    }
