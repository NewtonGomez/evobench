import numpy as np
from scipy import stats
import pandas as pd
from itertools import combinations


def dunn_test(*vectors: np.ndarray, algorithm_names: list = None, alpha: float = 0.05) -> dict:
    """
    Performs Dunn's test for post-hoc pairwise comparisons (for non-normal data).
    
    This test is used after Kruskal-Wallis to determine which specific pairs of
    algorithms have significantly different results.
    
    Args:
        *vectors: Multiple numpy arrays, one for each algorithm's results
        algorithm_names: List of algorithm names corresponding to the vectors
        alpha: Significance level (default 0.05)
    
    Returns:
        dict: Contains pairwise comparisons with test statistics and p-values
    """
    groups = [np.asarray(v, dtype=float) for v in vectors]
    
    if algorithm_names is None:
        algorithm_names = [f"Algorithm_{i}" for i in range(len(groups))]
    
    # Combine all data
    all_data = np.concatenate(groups)
    n_total = len(all_data)
    k = len(groups)
    
    # Rank all data
    ranks = stats.rankdata(all_data)
    
    # Assign ranks back to each group
    group_ranks = []
    idx = 0
    for group in groups:
        n_i = len(group)
        group_ranks.append(ranks[idx:idx + n_i])
        idx += n_i
    
    # Calculate average ranks for each group
    mean_ranks = [np.mean(r) for r in group_ranks]
    
    # Prepare results
    comparisons = []
    pairs = list(combinations(range(k), 2))
    
    for i, j in pairs:
        n_i = len(groups[i])
        n_j = len(groups[j])
        
        # Dunn's test statistic
        # z = (R_i - R_j) / sqrt(N(N+1)/12 * (1/n_i + 1/n_j))
        denominator = np.sqrt((n_total * (n_total + 1) / 12.0) * (1.0/n_i + 1.0/n_j))
        z_stat = abs(mean_ranks[i] - mean_ranks[j]) / denominator if denominator != 0 else 0
        
        # Two-tailed p-value
        p_value = 2 * (1 - stats.norm.cdf(z_stat))
        
        # Bonferroni correction
        n_comparisons = len(pairs)
        corrected_alpha = alpha / n_comparisons
        is_significant = p_value < corrected_alpha
        
        comparisons.append({
            "pair": (algorithm_names[i], algorithm_names[j]),
            "z_stat": round(z_stat, 6),
            "p_value": round(p_value, 6),
            "p_value_corrected": round(p_value * n_comparisons, 6),
            "significant": is_significant,
            "mean_rank_diff": round(abs(mean_ranks[i] - mean_ranks[j]), 4)
        })
    
    return {
        "test_type": "Dunn's Test",
        "alpha": alpha,
        "correction": f"Bonferroni (α_corrected={round(alpha/len(pairs), 4)})",
        "comparisons": comparisons,
        "mean_ranks": {name: round(mr, 4) for name, mr in zip(algorithm_names, mean_ranks)}
    }


def tukeyHSD_test(*vectors: np.ndarray, algorithm_names: list = None, alpha: float = 0.05) -> dict:
    """
    Performs Tukey's HSD (Honestly Significant Difference) test for post-hoc
    pairwise comparisons (for normal data).
    
    This test is used after ANOVA to determine which specific pairs of algorithms
    have significantly different results, while controlling family-wise error rate.
    
    Args:
        *vectors: Multiple numpy arrays, one for each algorithm's results
        algorithm_names: List of algorithm names corresponding to the vectors
        alpha: Significance level (default 0.05)
    
    Returns:
        dict: Contains pairwise comparisons with test statistics and p-values
    """
    try:
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
    except ImportError:
        raise ImportError("statsmodels is required for Tukey HSD test. Install with: pip install statsmodels")
    
    groups = [np.asarray(v, dtype=float) for v in vectors]
    
    if algorithm_names is None:
        algorithm_names = [f"Algorithm_{i}" for i in range(len(groups))]
    
    # Prepare data for statsmodels
    data_list = []
    groups_list = []
    
    for algo_name, group in zip(algorithm_names, groups):
        data_list.extend(group)
        groups_list.extend([algo_name] * len(group))
    
    # Perform Tukey HSD test
    tukey_result = pairwise_tukeyhsd(endog=data_list, groups=groups_list, alpha=alpha)
    
    # Parse results
    comparisons = []
    tukey_df = pd.DataFrame(data=tukey_result.summary().data[1:], columns=tukey_result.summary().data[0])
    
    for idx, row in tukey_df.iterrows():
        group1 = str(row.iloc[0])
        group2 = str(row.iloc[1])
        meandiff = float(row.iloc[2])
        p_value = float(row.iloc[4])
        is_significant = p_value < alpha
        
        comparisons.append({
            "pair": (group1, group2),
            "meandiff": round(meandiff, 6),
            "p_value": round(p_value, 6),
            "significant": is_significant,
            "lower_ci": round(float(row.iloc[3]), 6),
            "upper_ci": round(float(row.iloc[5]), 6)
        })
    
    # Calculate group means
    group_means = {name: round(np.mean(group), 6) for name, group in zip(algorithm_names, groups)}
    
    return {
        "test_type": "Tukey's HSD Test",
        "alpha": alpha,
        "correction": "Family-wise error rate controlled",
        "comparisons": comparisons,
        "group_means": group_means
    }
