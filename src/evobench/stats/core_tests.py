import numpy as np
from scipy import stats

def normality_test(vector: np.ndarray, alpha: float = 0.05) -> list:
    """Performs the Shapiro-Wilk test for normality on a given array."""
    vector = np.asarray(vector, dtype=float)
    stat, p = stats.shapiro(vector)
    is_normal = p > alpha
    return [round(stat, 6), round(p, 6), bool(is_normal)]

def anova_test(*vectors: np.ndarray, alpha: float = 0.05) -> list:
    """Performs a one-way ANOVA test to check for significant differences."""
    groups = [np.asarray(v, dtype=float) for v in vectors]
    f_stat, p = stats.f_oneway(*groups)
    reject_h0 = p < alpha
    return [round(f_stat, 6), round(float(p), 6), bool(reject_h0)]

def kruskal_test(*vectors: np.ndarray, alpha: float = 0.05) -> list:
    """Performs the Kruskal-Wallis H-test for independent samples."""
    groups = [np.asarray(v, dtype=float) for v in vectors]
    h_stat, p = stats.kruskal(*groups)
    reject_h0 = p < alpha
    return [round(h_stat, 6), round(float(p), 6), bool(reject_h0)]