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

def normality_test(vector: np.ndarray, alpha: float = 0.05) -> list:
    """
    Performs the Shapiro-Wilk test for normality on a given array.
    
    Args:
        vector: A numpy array of numerical data.
        alpha: The significance level to evaluate normality. Defaults to 0.05.
        
    Returns:
        A list containing the test statistic, the p-value, and a boolean 
        indicating if the data is considered normal (p-value > alpha).
    """
    # Convert the input to a numpy array with float data type to ensure mathematical precision
    vector = np.asarray(vector, dtype=float)
    
    # Execute the Shapiro-Wilk test returning the test statistic and p-value
    stat, p = stats.shapiro(vector)
    
    # Evaluate if the p-value is strictly greater than the significance level
    # A higher p-value indicates we fail to reject the null hypothesis of normality
    is_normal = p > alpha
    
    # Return the rounded statistic, rounded p-value, and the evaluated normality boolean
    return [round(stat, 6), round(p, 6), bool(is_normal)]

def anova_test(*vectors: np.ndarray, alpha: float = 0.05) -> list:
    """
    Performs a one-way ANOVA test to check for significant differences between group means.
    
    Args:
        *vectors: Variable number of numpy arrays representing different groups.
        alpha: The significance level to evaluate the hypothesis. Defaults to 0.05.
        
    Returns:
        A list containing the F-statistic, the p-value, and a boolean 
        indicating if the null hypothesis is rejected (p-value < alpha).
    """
    # Comprehension list to convert all input arguments into float-typed numpy arrays
    groups = [np.asarray(v, dtype=float) for v in vectors]
    
    # Perform the one-way ANOVA across all provided algorithmic groups
    f_stat, p = stats.f_oneway(*groups)
    
    # Determine if the differences are statistically significant based on the alpha threshold
    # A smaller p-value rejects the null hypothesis of equal means
    reject_h0 = p < alpha
    
    # Return the rounded test statistic, rounded p-value, and the rejection boolean
    return [round(f_stat, 6), round(float(p), 6), bool(reject_h0)]

def kruskal_test(*vectors: np.ndarray, alpha: float = 0.05) -> list:
    """
    Performs the Kruskal-Wallis H-test for independent samples.
    
    Args:
        *vectors: Variable number of numpy arrays representing different groups.
        alpha: The significance level to evaluate the hypothesis. Defaults to 0.05.
        
    Returns:
        A list containing the H-statistic, the p-value, and a boolean 
        indicating if the null hypothesis is rejected (p-value < alpha).
    """
    # Ensure all incoming groups are standardized as float numpy arrays
    groups = [np.asarray(v, dtype=float) for v in vectors]
    
    # Execute the non-parametric Kruskal-Wallis test on the provided groups
    h_stat, p = stats.kruskal(*groups)
    
    # Check if the calculated p-value falls below the chosen significance level
    reject_h0 = p < alpha
    
    # Return the computed statistic, exact p-value, and the significance conclusion
    return [round(h_stat, 6), round(float(p), 6), bool(reject_h0)]


def analyze(func_name: str, result_list: list, algorithm_names: list, alpha: float = 0.05) -> dict:
    """
    Analyzes the fitness results of multiple optimization algorithms.

    Calculates descriptive statistics and evaluates data distributions to
    determine and execute the appropriate statistical hypothesis test. 
    Allows customization of the statistical significance threshold.

    Args:
        func_name: The name of the optimization function evaluated.
        result_list: A list containing lists or arrays of fitness values.
        algorithm_names: A list of strings with the names of the algorithms.
        alpha: The significance level for hypothesis testing. Defaults to 0.05.

    Returns:
        A dictionary containing the function name, calculated statistics,
        hypothesis test results, significance evaluation, and the alpha used.
    """
    # Convert raw fitness lists into numpy arrays for vectorized calculations
    algorithm_results = [np.asarray(vec, dtype=float) for vec in result_list]
    # Convert each list of results into a NumPy float array for statistical tests.

    # Initialize dictionary to store descriptive metrics
    stats = {}

    # Iterate to calculate and store metrics per algorithm
    for name, vec in zip(algorithm_names, algorithm_results):
        stats[name] = {
            'mean': np.mean(vec),
            'std': np.std(vec, ddof=1),
            'best': np.min(vec)
        }

    # Perform normality tests and check if all distributions are normal
    normality_results = [normality_test(vec, alpha=alpha) for vec in algorithm_results]
    all_normal = all(result[2] for result in normality_results)
    # Determine whether every algorithm sample passed normality.

    # Select and apply hypothesis test based on normality
    if all_normal:
        hypothesis = anova_test(*algorithm_results, alpha=alpha)
        test_used = "ANOVA"
        stat_name = "F-statistic"
    else:
        hypothesis = kruskal_test(*algorithm_results, alpha=alpha)
        test_used = "Kruskal-Wallis"
        stat_name = "H-statistic"

    # Extract the p-value from the hypothesis test result tuple
    p_val = hypothesis[1]
    
    # Calculate significance dynamically using the provided alpha parameter
    is_significant = p_val < alpha

    # Return the comprehensive results dictionary
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

def stat_report(result_data: dict) -> None:
    """
    Generates and prints a formatted, color-coded statistical report.

    Args:
        result_data: A dictionary containing the statistical analysis results.
    """
    # Define ANSI escape codes for terminal colors
    color_green = '\033[92m'
    color_red = '\033[91m'
    color_reset = '\033[0m'

    # Extract the function name to build the report header
    func_name = result_data['func_name']
    title = f"Algorithm Performance on {func_name}"
    
    print(f"\n>>> {title}")

    # Extract and print descriptive statistics
    descriptive_stats = result_data["stats"]
    for algo, stats in descriptive_stats.items():
        print(f"\n{algo}:")
        print(f"  Mean fitness:     {stats['mean']:.2e}")
        print(f"  Std deviation:    {stats['std']:.2e}")
        print(f"  Best result:      {stats['best']:.2e}")

    # Extract test details to prepare the hypothesis section
    test_used = result_data['test_used']
    print(f"\n>> [{test_used} Test Results]")
    
    stat_name = result_data['stat_name']
    stat_val = result_data['stat_val']
    p_val = result_data['p_val']
    is_significant = result_data['significant']
    alpha = result_data['alpha']

    # Print the statistic value and p-value
    stat_label = f"{stat_name}:"
    print(f"  {stat_label:<18}{stat_val:.3f}")
    print(f"  {'p-value:':<18}{p_val:.2e}")
    
    # Apply color codes based on the dynamic significance calculation
    if is_significant:
        sig_str = f"{color_green}Yes{color_reset}"
    else:
        sig_str = f"{color_red}No{color_reset}"
    
    # Print the conclusion displaying the specific alpha used for evaluation
    print(f"  {'Significant:':<18}{sig_str} (α={alpha})\n")