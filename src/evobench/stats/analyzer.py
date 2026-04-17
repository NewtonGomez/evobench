import numpy as np

# Importamos las pruebas de nuestro propio modulo
from evobench.stats.core_tests import normality_test, anova_test, kruskal_test

def analyze(func_name: str, result_list: list, algorithm_names: list, alpha: float = 0.05) -> dict:
    """
    Analyzes the fitness results of multiple optimization algorithms.
    """
    algorithm_results = [np.asarray(vec, dtype=float) for vec in result_list]
    stats = {}

    for name, vec in zip(algorithm_names, algorithm_results):
        stats[name] = {
            'mean': np.mean(vec),
            'std': np.std(vec, ddof=1),
            'best': np.min(vec)
        }

    normality_results = [normality_test(vec, alpha=alpha) for vec in algorithm_results]
    all_normal = all(result[2] for result in normality_results)

    if all_normal:
        hypothesis = anova_test(*algorithm_results, alpha=alpha)
        test_used = "ANOVA"
        stat_name = "F-statistic"
    else:
        hypothesis = kruskal_test(*algorithm_results, alpha=alpha)
        test_used = "Kruskal-Wallis"
        stat_name = "H-statistic"

    p_val = hypothesis[1]
    is_significant = p_val < alpha

    return {
        "func_name": func_name,
        "stats": stats,
        "test_used": test_used,
        "stat_name": stat_name,
        "stat_val": hypothesis[0],
        "p_val": p_val,
        "significant": is_significant,
        "alpha": alpha
    }