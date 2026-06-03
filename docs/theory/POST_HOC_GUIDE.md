# Post-Hoc Tests for Statistical Analysis of Algorithms

## General Description

The `post_hoc.py` module provides two advanced statistical tests to determine exactly which pairs of algorithms have significantly different performances:

1. **Dunn's Test**: For **non-normal** data (following Kruskal-Wallis)
2. **Tukey's HSD Test**: For **normal** data (following ANOVA)

## Automatic Integration

Post-hoc tests are executed **automatically** when:
- The global test is **significant** (p < α)
- There are **more than 2 algorithms** to compare

### Workflow

```
1. analyzer.analyze() executes:
   ├─ Normality test (Shapiro-Wilk)
   ├─ Global test (ANOVA or Kruskal-Wallis)
   └─ Post-hoc test (if significant)
       ├─ Dunn's Test (if NOT normal)
       └─ Tukey HSD (if normal)

2. reporter.stat_report() displays:
   ├─ Descriptive statistics
   ├─ Normality results
   ├─ Global test results
   ├─ Post-hoc test results
   └─ Algorithm ranking with medals
```

## Usage

### Basic Example

```python
from src.evobench.stats import analyze, stat_report

# Results from 3 algorithms
pso_results = [2.5, 3.1, 2.8, ...]
eda_results = [4.2, 3.9, 4.5, ...]
abc_results = [6.5, 6.2, 6.8, ...]

# Analysis (automatic post-hoc)
result = analyze(
    func_name="Sphere Function",
    result_list=[pso_results, eda_results, abc_results],
    algorithm_names=["PSO", "EDA", "ABC"],
    alpha=0.05
)

# Display visual report
stat_report(result)
```

### Direct Usage of Post-Hoc Tests

```python
from src.evobench.stats import dunn_test, tukeyHSD_test
import numpy as np

data1 = np.array([1.2, 1.5, 1.3, 1.4])
data2 = np.array([2.1, 2.3, 2.2, 2.4])
data3 = np.array([3.5, 3.7, 3.6, 3.8])

# Dunn's test (for non-normal data)
results_dunn = dunn_test(data1, data2, data3, 
                         algorithm_names=["Algo1", "Algo2", "Algo3"],
                         alpha=0.05)

# Tukey HSD test (for normal data)
results_tukey = tukeyHSD_test(data1, data2, data3,
                              algorithm_names=["Algo1", "Algo2", "Algo3"],
                              alpha=0.05)
```

## Result Interpretation

### Output Example

```
[Dunn's Test]
Correction method: Bonferroni (α_corrected=0.0167)

Algorithm 1     Algorithm 2     Different?      p-value     
  ----------------------------------------------------------
  PSO             EDA             ✓ YES           0.001234    BETTER: PSO
  PSO             ABC             ✓ YES           0.000089    BETTER: PSO
  EDA             ABC             ✓ YES           0.034567    BETTER: EDA

[Algorithm Ranking by Mean Fitness]
  🥇 PSO             → 2.35e+00
  🥈 EDA             → 4.05e+00
  🥉 ABC             → 6.52e+00
```

### Visual Symbols

- **✓ YES**: Significant difference (these algorithms are different)
- **✗ NO**: No significant difference (similar performance)
- **BETTER**: Indicates which algorithm is better (lower fitness is better)
- **Medals**: 🥇 1st place, 🥈 2nd place, 🥉 3rd place

## Displayed Statistics

### Dunn's Test
- `z_stat`: Test z-statistic
- `p_value`: Original p-value
- `p_value_corrected`: P-value with Bonferroni correction
- `mean_rank_diff`: Difference of averaged ranks
- `significant`: Whether significant difference exists after correction

### Tukey HSD Test
- `meandiff`: Mean difference
- `p_value`: Test p-value
- `lower_ci`, `upper_ci`: Confidence intervals
- `significant`: Whether significant difference exists

## Test Selection

```
┌─────────────────────────────────────┐
│  Are the data normal?               │
│  (Shapiro-Wilk Test)                │
└─────────┬───────────────────────────┘
          │
    ┌─────┴─────┐
    │           │
   YES         NO
    │           │
    ▼           ▼
 ANOVA      Kruskal-Wallis
    │           │
    ▼           ▼
Tukey HSD   Dunn's Test
```

## Dependencies

Post-hoc tests require:
- `numpy >= 1.24.0`
- `scipy >= 1.9.0`
- `pandas >= 1.5.0`
- `statsmodels >= 0.13.0`

Install with: `pip install -r requirements.txt`

## Complete Example

See `test_post_hoc_example.py` for an executable example demonstrating both types of tests.

```bash
python3 test_post_hoc_example.py
```

## References

- Dunn, O. J. (1961). "Multiple comparisons among means". Journal of the American Statistical Association, 56(293), 52-64.
- Tukey, J. W. (1949). "Comparing individual means in the analysis of variance". Biometrics, 5(2), 99-114.
- [Statsmodels Documentation](https://www.statsmodels.org/stable/generated/statsmodels.stats.multicomp.pairwise_tukeyhsd.html)
