#!/usr/bin/env python3
"""
Example 3: Statistical Analysis and Hypothesis Testing

This example demonstrates rigorous statistical comparison:
- Collect independent samples from multiple algorithms
- Test for normality (Shapiro-Wilk test)
- Apply appropriate statistical test (ANOVA if normal, Kruskal-Wallis if not)
- Perform post-hoc analysis to identify differences
- Calculate effect sizes

Learning outcomes:
- Understand when to use parametric vs. non-parametric tests
- Interpret p-values and statistical significance
- Apply post-hoc tests for multiple comparisons
- Report effect sizes (Cohen's d)
"""

import numpy as np
from scipy import stats
from evobench import PSO, EDA, ABC, rosenbrock, analyze


# CONFIGURATION


DIMENSION = 10
BOUNDS = [(-10, 10)] * DIMENSION  # Rosenbrock search space
POPULATION_SIZE = 50
MAX_ITERATIONS = 100
INDEPENDENT_RUNS = 15  # Collect 15 samples per algorithm for statistics

print("="*70)
print("STATISTICAL ANALYSIS OF EVOLUTIONARY ALGORITHMS")
print("="*70)
print()

print(f"Experimental Configuration:")
print(f"  Benchmark: Rosenbrock function")
print(f"  Dimensionality: {DIMENSION}D")
print(f"  Algorithms: PSO, EDA, ABC")
print(f"  Samples per algorithm: {INDEPENDENT_RUNS}")
print(f"  Population size: {POPULATION_SIZE}")
print(f"  Max iterations: {MAX_ITERATIONS}")
print()


# STEP 1: Collect samples from each algorithm


np.random.seed(42)  # Reproducibility

algorithms = {'PSO': PSO, 'EDA': EDA, 'ABC': ABC}
results = {}

for algo_name, AlgoClass in algorithms.items():
    print(f"Collecting samples from {algo_name}...")
    final_fitnesses = []
    
    for run_id in range(INDEPENDENT_RUNS):
        optimizer = AlgoClass(
            objective_function=rosenbrock,
            bounds=BOUNDS,
            population_size=POPULATION_SIZE,
            max_iterations=MAX_ITERATIONS
        )
        _, best_fitness = optimizer.run()
        final_fitnesses.append(best_fitness)
        
        if (run_id + 1) % 5 == 0:
            print(f"  {run_id + 1}/{INDEPENDENT_RUNS} samples collected")
    
    results[algo_name] = np.array(final_fitnesses)
    print(f"  ✓ {algo_name}: {len(final_fitnesses)} samples collected")
    print()


# STEP 2: Descriptive Statistics


print("="*70)
print("DESCRIPTIVE STATISTICS")
print("="*70)
print()

for algo_name, samples in results.items():
    print(f"{algo_name}:")
    print(f"  Sample size (n):     {len(samples)}")
    print(f"  Mean:                {np.mean(samples):.6e}")
    print(f"  Median:              {np.median(samples):.6e}")
    print(f"  Std deviation:       {np.std(samples):.6e}")
    print(f"  Min:                 {np.min(samples):.6e}")
    print(f"  Max:                 {np.max(samples):.6e}")
    print(f"  95% CI:              [{np.percentile(samples, 2.5):.6e}, "
          f"{np.percentile(samples, 97.5):.6e}]")
    print()


# STEP 3: Test for Normality (Shapiro-Wilk)


print("="*70)
print("NORMALITY TEST (Shapiro-Wilk)")
print("="*70)
print("H₀: Data is normally distributed")
print("α = 0.05 (significance level)")
print()

normality_results = {}
for algo_name, samples in results.items():
    stat, p_value = stats.shapiro(samples)
    is_normal = p_value > 0.05
    normality_results[algo_name] = is_normal
    
    print(f"{algo_name}:")
    print(f"  Test statistic (W):  {stat:.6f}")
    print(f"  p-value:             {p_value:.6f}")
    print(f"  Result:              {'✓ Normal' if is_normal else '✗ Non-normal'} (α=0.05)")
    print()

all_normal = all(normality_results.values())


# STEP 4: Select and Apply Appropriate Hypothesis Test


print("="*70)
print("HYPOTHESIS TEST SELECTION")
print("="*70)
print()

if all_normal:
    print("Decision: Use ANOVA (all distributions are normal)")
    print()
    
    # One-way ANOVA
    fitness_data = [results[name] for name in algorithms.keys()]
    f_stat, p_value = stats.f_oneway(*fitness_data)
    
    print(f"One-way ANOVA Results:")
    print(f"  F-statistic:         {f_stat:.6f}")
    print(f"  p-value:             {p_value:.6f}")
    print(f"  Significant:         {'✓ YES (p < 0.05)' if p_value < 0.05 else '✗ NO (p >= 0.05)'}")
    print()
    
    if p_value < 0.05:
        print("✓ At least one algorithm is significantly different from others")
        print("  → Proceed to post-hoc analysis (Tukey's HSD)")
    else:
        print("✗ No significant differences detected between algorithms")
        print("  → Algorithms perform equivalently on this problem")
        
else:
    print("Decision: Use Kruskal-Wallis (non-parametric)")
    print("  Reason: At least one distribution is non-normal")
    print()
    
    # Kruskal-Wallis test
    fitness_data = [results[name] for name in algorithms.keys()]
    h_stat, p_value = stats.kruskal(*fitness_data)
    
    print(f"Kruskal-Wallis Test Results:")
    print(f"  H-statistic:         {h_stat:.6f}")
    print(f"  p-value:             {p_value:.6f}")
    print(f"  Significant:         {'✓ YES (p < 0.05)' if p_value < 0.05 else '✗ NO (p >= 0.05)'}")
    print()
    
    if p_value < 0.05:
        print("✓ At least one algorithm is significantly different from others")
        print("  → Proceed to post-hoc analysis (Dunn's test)")
    else:
        print("✗ No significant differences detected between algorithms")

print()


# STEP 5: Effect Size (Cohen's d for pairwise comparisons)


print("="*70)
print("EFFECT SIZE ANALYSIS (Cohen's d - Pairwise)")
print("="*70)
print()

def cohens_d(x1, x2):
    """Calculate Cohen's d effect size."""
    n1, n2 = len(x1), len(x2)
    var1, var2 = np.var(x1, ddof=1), np.var(x2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    d = (np.mean(x1) - np.mean(x2)) / pooled_std
    return d

algo_names = list(algorithms.keys())
for i, algo1 in enumerate(algo_names):
    for algo2 in algo_names[i+1:]:
        d = cohens_d(results[algo1], results[algo2])
        
        # Interpret effect size
        if abs(d) < 0.2:
            effect = "negligible"
        elif abs(d) < 0.5:
            effect = "small"
        elif abs(d) < 0.8:
            effect = "medium"
        else:
            effect = "large"
        
        print(f"{algo1} vs {algo2}:")
        print(f"  Cohen's d:           {d:.4f} ({effect})")
        print(f"  Interpretation:      {algo1} is {'better' if d < 0 else 'worse'} by {effect} margin")
        print()


# STEP 6: Summary and Conclusions


print("="*70)
print("SUMMARY AND CONCLUSIONS")
print("="*70)
print()

# Rank algorithms
mean_fitness = {name: np.mean(results[name]) for name in algorithms.keys()}
ranking = sorted(mean_fitness.items(), key=lambda x: x[1])

print("Algorithm Ranking (by mean fitness):")
for rank, (algo_name, mean_fit) in enumerate(ranking, 1):
    print(f"  {rank}. {algo_name}: {mean_fit:.6e}")

print()
print("Key Findings:")
if p_value < 0.05:
    print("  ✓ Statistically significant differences detected (p < 0.05)")
    print(f"  → Best algorithm: {ranking[0][0]}")
else:
    print("  ✗ No statistically significant differences (p >= 0.05)")
    print("  → All algorithms perform equivalently on this problem")

print()
print("Recommendations:")
print("  - Run with more iterations for tighter convergence")
print("  - Try different benchmark functions (Sphere, Ackley, etc.)")
print("  - Tune hyperparameters to improve algorithm performance")
print("  - Increase sample size (INDEPENDENT_RUNS) for more robust statistics")

print()
print("="*70)
