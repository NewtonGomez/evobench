import numpy as np
import pytest
from typing import List
 
from evobench.tools.statistics import normality_test, anova_test, kruskal_test, analyze
 
"""
Unit testing module for the Statistical Analysis functions.
 
This suite verifies the correctness of the statistical pipeline by using
synthetic data with known properties (normality, non-normality, equal/different
distributions). A fixed random seed guarantees reproducibility across runs.
"""
 
# Fixtures and test cases validate statistical helper behavior and analysis choice logic.
# FIXTURES
 
@pytest.fixture
def normal_vector() -> np.ndarray:
    """
    Create a synthetic Gaussian data sample.

    This fixture provides normal data for the Shapiro-Wilk normality test.

    Returns:
        np.ndarray: A normally distributed sample of size 30.
    """
    # Use a fixed seed so the fixture remains deterministic.
    rng = np.random.default_rng(42)
    # Generate a standard normal sample of size 30.
    return rng.normal(loc=0.0, scale=1.0, size=30)
 
 
@pytest.fixture
def non_normal_vector() -> np.ndarray:
    """
    Create a synthetic non-normal data sample.

    This fixture provides skewed exponential data for the Shapiro-Wilk test.

    Returns:
        np.ndarray: A non-normally distributed sample of size 30.
    """
    # Use a fixed seed so the fixture remains deterministic.
    rng = np.random.default_rng(42)
    # Generate a skewed exponential sample for non-normality.
    return rng.exponential(scale=1.0, size=30)
 
 
@pytest.fixture
def equal_groups() -> List[np.ndarray]:
    """
    Create equal-distribution groups for hypothesis testing.

    The generated groups should all come from the same Gaussian distribution.

    Returns:
        List[np.ndarray]: Three groups with identical statistical properties.
    """
    rng = np.random.default_rng(42)
    # Create three groups that share the same underlying distribution.
    return [rng.normal(0.0, 1.0, 30) for _ in range(3)]
 
 
@pytest.fixture
def different_groups() -> List[np.ndarray]:
    """
    Create groups with clearly different means.

    These groups are designed to produce significant differences in tests.

    Returns:
        List[np.ndarray]: Three groups with distinct mean values.
    """
    rng = np.random.default_rng(42)
    group_a = rng.normal(0.0,   1.0, 30)
    group_b = rng.normal(50.0,  1.0, 30)
    group_c = rng.normal(100.0, 1.0, 30)
    # Return groups with strong mean differences for hypothesis testing.
    return [group_a, group_b, group_c]
 
 
# NORMALITY TEST
 
def test_normality_detects_normal_data(normal_vector: np.ndarray) -> None:
    """
    Verify that normal data passes the normality test.

    Args:
        normal_vector (np.ndarray): A sample generated from a normal distribution.

    Returns:
        None
    """
    # Run the normality check on a Gaussian sample.
    result = normality_test(normal_vector)
 
    assert isinstance(result, list), "normality_test must return a list."
    assert len(result) == 3, "Result must have 3 elements: [statistic, p_value, is_normal]."
    assert isinstance(result[2], bool), "Third element must be a boolean."
    assert result[2] == True, "Normal data must be detected as normal (p > 0.05)."
 
 
def test_normality_detects_non_normal_data(non_normal_vector: np.ndarray) -> None:
    """
    Verify that non-normal data fails the normality test.

    Args:
        non_normal_vector (np.ndarray): A skewed exponential sample.

    Returns:
        None
    """
    # Run the normality check on a skewed exponential sample.
    result = normality_test(non_normal_vector)
 
    assert result[2] == False, "Non-normal data must be detected as not normal (p <= 0.05)."
 
 
def test_normality_accepts_any_sample_size() -> None:
    """
    Verify that normality_test supports various sample sizes.

    The test covers vector sizes of 10, 30, 50, and 100.

    Returns:
        None
    """
    rng = np.random.default_rng(0)
    for size in [10, 30, 50, 100]:
        # Test the normality helper for different sample sizes.
        vec = rng.normal(0.0, 1.0, size)
        result = normality_test(vec)
        assert len(result) == 3, f"Failed for sample size {size}."
 
 
# ANOVA TEST
 
 
def test_anova_does_not_reject_equal_groups(equal_groups: List[np.ndarray]) -> None:
    """
    Verify that ANOVA does not reject the null hypothesis for equal groups.

    Args:
        equal_groups (List[np.ndarray]): Three groups drawn from the same distribution.

    Returns:
        None
    """
    # Run ANOVA on groups drawn from the same distribution.
    result = anova_test(*equal_groups)
 
    assert isinstance(result, list), "anova_test must return a list."
    assert len(result) == 3, "Result must have 3 elements: [f_statistic, p_value, reject_h0]."
    assert result[2] == False, "H0 must NOT be rejected when groups are equal."
 
 
def test_anova_rejects_different_groups(different_groups: List[np.ndarray]) -> None:
    """
    Verify that ANOVA rejects the null hypothesis for different groups.

    Args:
        different_groups (List[np.ndarray]): Three groups with distinct means.

    Returns:
        None
    """
    # Run ANOVA on groups with large mean separation.
    result = anova_test(*different_groups)
 
    assert result[2] == True, "H0 must be rejected when groups are clearly different."
 
 
def test_anova_accepts_n_groups() -> None:
    """
    Verify that anova_test supports a variable number of groups.

    Returns:
        None
    """
    rng = np.random.default_rng(1)
    for n_groups in [2, 3, 5]:
        # Ensure ANOVA handles varying numbers of groups.
        groups = [rng.normal(0.0, 1.0, 30) for _ in range(n_groups)]
        result = anova_test(*groups)
        assert len(result) == 3, f"Failed for {n_groups} groups."
 
 
# KRUSKAL-WALLIS TEST
 
 
def test_kruskal_does_not_reject_equal_groups(equal_groups: List[np.ndarray]) -> None:
    """
    Verify that Kruskal-Wallis does not reject H0 for equal groups.

    Args:
        equal_groups (List[np.ndarray]): Three groups drawn from the same distribution.

    Returns:
        None
    """
    # Run Kruskal-Wallis on groups with the same underlying distribution.
    result = kruskal_test(*equal_groups)
 
    assert isinstance(result, list), "kruskal_test must return a list."
    assert len(result) == 3, "Result must have 3 elements: [h_statistic, p_value, reject_h0]."
    assert result[2] == False, "H0 must NOT be rejected when groups are equal."
 
 
def test_kruskal_rejects_different_groups(different_groups: List[np.ndarray]) -> None:
    """
    Verify that Kruskal-Wallis rejects H0 for different groups.

    Args:
        different_groups (List[np.ndarray]): Three groups with distinct distributions.

    Returns:
        None
    """
    # Run Kruskal-Wallis on groups that should show a significant difference.
    result = kruskal_test(*different_groups)
 
    assert result[2] == True, "H0 must be rejected when groups are clearly different."
 
 
# ANALYZE FUNCTION
 
 
def test_analyze_selects_anova_when_all_normal() -> None:
    """
    Verify analyze() chooses ANOVA for all-normal groups.

    Returns:
        None
    """
    rng = np.random.default_rng(42)
    groups = [rng.normal(0.0, 1.0, 30) for _ in range(3)]
 
    # Analyze groups that should all pass the normality checks.
    result = analyze("sphere", groups, ["EDA", "PSO", "ABC"])
 
    assert result[3] == "ANOVA", "analyze() must select ANOVA when all groups are normal."
 
 
def test_analyze_selects_kruskal_when_not_normal() -> None:
    """
    Verify analyze() chooses Kruskal-Wallis when normality fails.

    Returns:
        None
    """
    rng = np.random.default_rng(42)
    normal_a  = rng.normal(0.0, 1.0, 30)
    normal_b  = rng.normal(0.0, 1.0, 30)
    skewed    = rng.exponential(1.0, 30)   # not normal
 
    # Analyze a mixture of normal and non-normal groups.
    result = analyze("ackley", [normal_a, normal_b, skewed], ["EDA", "PSO", "ABC"])
 
    assert result[3] == "Kruskal-Wallis", "analyze() must select Kruskal-Wallis when normality fails."
 
 
def test_analyze_returns_correct_structure() -> None:
    """
    Verify analyze() returns the expected result structure.

    Returns:
        None
    """
    rng = np.random.default_rng(42)
    groups = [rng.normal(0.0, 1.0, 30) for _ in range(3)]
    names  = ["EDA", "PSO", "ABC"]
 
    result = analyze("trid", groups, names)
 
    assert isinstance(result, list),       "analyze() must return a list."
    assert len(result) == 5,               "Result must have 5 elements."
    assert result[0] == "trid",            "Index 0 must be the function name."
    assert result[1] == names,             "Index 1 must be the algorithm names."
    assert isinstance(result[2], list),    "Index 2 must be the normality results list."
    assert result[3] in ("ANOVA", "Kruskal-Wallis"), "Index 3 must be the test name."
    assert isinstance(result[4], list),    "Index 4 must be the hypothesis result list."