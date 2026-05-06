# Statistical Testing and Hypothesis Testing

## Overview

Comparing evolutionary algorithms requires rigorous statistical methodology to ensure that observed performance differences are not merely artifacts of stochastic variation. This document outlines the **complete decision flow** implemented in evobench for multi-algorithm hypothesis testing.

The framework ensures:

✓ **Rigor**: Decisions based on formal statistical tests, not subjective judgment  
✓ **Reproducibility**: Consistent methodology across studies  
✓ **Interpretability**: Clear understanding of what results mean  
✓ **Validity**: Tests appropriate to data properties  

---

## Fundamental Concepts

### Parametric vs. Non-Parametric Testing

When comparing multiple algorithms, we must determine whether observed fitness differences are statistically significant.

#### Parametric Tests (ANOVA)

**Assumptions**:
- Data are normally distributed
- Variances are homogeneous across groups
- Observations are independent

**Advantages**:
- More powerful (higher probability of detecting true differences)
- Well-established theory and software support

**Disadvantages**:
- Sensitive to assumption violations
- May produce invalid conclusions if assumptions fail

**Examples**: ANOVA, t-test, Tukey's HSD

#### Non-Parametric Tests (Kruskal-Wallis)

**Assumptions**:
- Data are independent
- **No normality assumption** (more robust)
- **No homogeneity of variance assumption**

**Advantages**:
- Robust to distribution violations
- Don't assume any particular distribution form
- Based on ranks (outlier-resistant)

**Disadvantages**:
- Slightly less powerful than parametric tests when assumptions hold
- Different null hypothesis (tests medians/distributions rather than means)

**Examples**: Kruskal-Wallis, Mann-Whitney U, Dunn's test

### When to Use Which

**Use ANOVA when**:
- Data appear normally distributed
- Variances are similar across groups
- You want to test for differences in means

**Use Kruskal-Wallis when**:
- Data violate normality
- Variances are unequal
- You want a more robust test

**Best Practice**: Always check assumptions first, then choose appropriately.

---

## The evobench Decision Flow

### Complete Decision Tree

```
Start: Obtain Results from Multiple Algorithm Runs
            ↓
     Normality Testing
   (Shapiro-Wilk test)
            ↓
    ┌───────────────────────────────┐
    │                               │
All Groups        Not All Groups
    Normal?           Normal?
    │                 │
    ├─→ YES      NO ←─┤
    │                 │
    ↓                 ↓
 ANOVA          Kruskal-Wallis
(Parametric)     (Non-parametric)
    │                 │
    └─────────────────┘
           ↓
    Check p-value
    against α = 0.05
           ↓
    ┌───────────────────────────────┐
    │                               │
 Significant?             Not Significant?
 p < 0.05                   p ≥ 0.05
    │                               │
    ├─→ YES ──→ Post-Hoc Tests    NO ←─┤
    │          (Pairwise Comp.)       │
    │                                 │
    └─────────────────────────────────┘
           ↓
    Final Conclusion
```

---

## Stage 1: Normality Testing (Shapiro-Wilk Test)

### Purpose

Before applying parametric tests, we must verify that the normality assumption holds for each algorithm's results.

The **Shapiro-Wilk test** is the most powerful test for normality detection across sample sizes typical in evolutionary benchmarking (20–100 runs per algorithm).

### Mathematical Foundation

The Shapiro-Wilk statistic is defined as:

$$W = \frac{\left(\sum_{i=1}^{n} a_i x_{(i)}\right)^2}{\sum_{i=1}^{n} (x_i - \bar{x})^2}$$

where:

- $x_{(1)} \leq x_{(2)} \leq \cdots \leq x_{(n)}$ are the **order statistics** (sorted values)
- $a_i$ are **coefficients** derived from order statistic properties (dependent on $n$)
- $\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$ is the sample mean
- $n$ is the sample size

#### Interpretation

| $W$ Value | Interpretation |
|-----------|-----------------|
| $W \approx 1$ | Strong evidence for normality |
| $W \approx 0.95$ | Likely normal |
| $W < 0.90$ | Likely non-normal; investigate |
| $W < 0.85$ | Strong evidence against normality |

### Procedure

For each algorithm's fitness results (vector of 30 independent runs):

1. **Compute order statistics**: Sort values from smallest to largest
2. **Calculate Shapiro-Wilk $W$ statistic** using the formula above
3. **Determine p-value**: Use lookup tables or software
4. **Make decision**:
   - If $p > 0.05$: Fail to reject $H_0$ (assume normal)
   - If $p \leq 0.05$: Reject $H_0$ (conclude non-normal)

### Hypotheses

$$H_0: \text{The data are normally distributed}$$
$$H_1: \text{The data are not normally distributed}$$

### Example Interpretation

```python
from scipy.stats import shapiro
import numpy as np

# Fitness results from 30 PSO runs
pso_results = np.array([1.234, 1.245, ..., 1.256])

statistic, p_value = shapiro(pso_results)

print(f"W-statistic: {statistic:.4f}")
print(f"p-value: {p_value:.6f}")

if p_value > 0.05:
    print("✓ PSO results appear normally distributed")
else:
    print("✗ PSO results are NOT normally distributed")
```

### Important Caveat

With large sample sizes ($n > 50$), even tiny deviations from normality become statistically significant. **Practical significance** may matter more than statistical significance.

**Recommendation**: If $p$ is slightly below 0.05 but histogram looks reasonably normal, consider using ANOVA with caution or increasing robustness of interpretation.

---

## Stage 2: Primary Hypothesis Testing

### Case A: All Groups Are Normal → Use ANOVA

#### Purpose

Test whether the **mean fitness values** differ significantly across algorithms.

#### Hypotheses

$$H_0: \mu_1 = \mu_2 = \cdots = \mu_k \quad \text{(all algorithm means are equal)}$$
$$H_1: \text{At least one } \mu_i \text{ differs from the others}$$

#### Mathematical Formulation

ANOVA decomposes total variance into between-group and within-group components:

$$\text{Total Sum of Squares (SST)} = \sum_{i=1}^{k} \sum_{j=1}^{n_i} (x_{ij} - \bar{x})^2$$

where:
- $k$ = number of algorithms
- $n_i$ = number of runs for algorithm $i$
- $x_{ij}$ = fitness of algorithm $i$, run $j$
- $\bar{x}$ = grand mean across all runs

**Between-Group Sum of Squares (SSB)**:
$$\text{SSB} = \sum_{i=1}^{k} n_i (\bar{x}_i - \bar{x})^2$$

where $\bar{x}_i$ is the mean for algorithm $i$.

**Within-Group Sum of Squares (SSW)**:
$$\text{SSW} = \sum_{i=1}^{k} \sum_{j=1}^{n_i} (x_{ij} - \bar{x}_i)^2$$

**F-statistic**:
$$F = \frac{\text{MS}_{\text{between}}}{\text{MS}_{\text{within}}} = \frac{\text{SSB} / (k-1)}{\text{SSW} / (N-k)}$$

where:
- $\text{MS}_{\text{between}}$ = mean square between groups
- $\text{MS}_{\text{within}}$ = mean square within groups
- $N = \sum_{i=1}^{k} n_i$ = total observations
- Degrees of freedom: numerator $(k-1)$, denominator $(N-k)$

#### Interpretation

The F-statistic follows an F-distribution under $H_0$. The p-value is:

$$p\text{-value} = P(F > F_{\text{observed}} | H_0)$$

**Decision**:
- If $p < 0.05$: **Reject $H_0$** (significant difference exists)
- If $p \geq 0.05$: **Fail to reject $H_0$** (no significant difference)

#### Example

```python
from scipy.stats import f_oneway

# Fitness results: 30 runs per algorithm
pso_results = [1.234, 1.245, ..., 1.256]  # length 30
eda_results = [2.345, 2.456, ..., 2.567]  # length 30
abc_results = [3.456, 3.567, ..., 3.678]  # length 30

f_statistic, p_value = f_oneway(pso_results, eda_results, abc_results)

print(f"F-statistic: {f_statistic:.4f}")
print(f"p-value: {p_value:.6f}")

if p_value < 0.05:
    print("✓ Significant difference among algorithms")
else:
    print("✗ No significant difference")
```

---

### Case B: Not All Groups Are Normal → Use Kruskal-Wallis

#### Purpose

Test whether the **distributions** of results differ across algorithms (non-parametric alternative to ANOVA).

#### Hypotheses

$$H_0: \text{All algorithm distributions are identical}$$
$$H_1: \text{At least one algorithm's distribution differs}$$

#### Mathematical Formulation

The Kruskal-Wallis test operates on **ranks** rather than raw values.

**Step 1**: Combine all fitness values and rank them from 1 to $N$.

**Step 2**: Calculate the sum of ranks for each algorithm:

$$R_i = \sum_{j=1}^{n_i} r_{ij}$$

where $r_{ij}$ is the rank of the $j$-th observation from algorithm $i$.

**Step 3**: Compute H-statistic:

$$H = \frac{12}{N(N+1)} \sum_{i=1}^{k} \frac{R_i^2}{n_i} - 3(N+1)$$

where:
- $N = \sum n_i$ (total observations)
- $k$ = number of algorithms

#### Distribution

Under $H_0$, $H$ approximately follows a chi-squared distribution with $df = k - 1$ degrees of freedom for large $N$ (typically $N \geq 30$).

#### Example

```python
from scipy.stats import kruskal

pso_results = [1.234, 1.245, ..., 1.256]
eda_results = [2.345, 2.456, ..., 2.567]
abc_results = [3.456, 3.567, ..., 3.678]

h_statistic, p_value = kruskal(pso_results, eda_results, abc_results)

print(f"H-statistic: {h_statistic:.4f}")
print(f"p-value: {p_value:.6f}")

if p_value < 0.05:
    print("✓ Significant difference in distributions")
else:
    print("✗ No significant difference")
```

---

## Stage 3: Post-Hoc Testing

When the primary test is significant ($p < 0.05$), we conduct **pairwise comparisons** to identify which specific algorithm pairs differ significantly.

### Post-Hoc for ANOVA: Tukey's Honest Significant Difference (HSD)

#### Purpose

Compare all pairs of algorithms while controlling the **family-wise error rate** (probability of making any type I error across all comparisons).

#### Procedure

For each pair of algorithms $(i, j)$:

$$|(\bar{x}_i - \bar{x}_j)| \stackrel{?}{>} q_{\alpha,k,df} \sqrt{\frac{\text{MS}_{\text{within}}}{2} \left(\frac{1}{n_i} + \frac{1}{n_j}\right)}$$

where:

- $q_{\alpha,k,df}$ = critical value from the **studentized range distribution**
  - Depends on: significance level $\alpha$, number of groups $k$, error degrees of freedom $df = N - k$
  - Typically $\alpha = 0.05$
- $\text{MS}_{\text{within}}$ = mean square within groups (from ANOVA)
- $n_i, n_j$ = sample sizes for algorithms $i$ and $j$

#### Decision

If the inequality holds: **Algorithms $i$ and $j$ differ significantly**

#### Example

```python
from scipy.stats import tukey_hsd
import numpy as np

# Fitness results
pso = np.array([1.234, 1.245, ..., 1.256])
eda = np.array([2.345, 2.456, ..., 2.567])
abc = np.array([3.456, 3.567, ..., 3.678])

# Tukey HSD test
res = tukey_hsd(pso, eda, abc)

print(f"Pairwise p-values:\n{res.pvalue}")
# Typical output:
#        pso      eda      abc
# pso  1.000  0.000032  0.000001
# eda  0.000032  1.000  0.045267
# abc  0.000001  0.045267  1.000

print(f"Confidence intervals:\n{res.confidence_interval()}")
```

### Post-Hoc for Kruskal-Wallis: Dunn's Test

#### Purpose

Perform rank-based pairwise comparisons with Bonferroni correction to control family-wise error.

#### Procedure

For each pair of algorithms $(i, j)$:

$$\left| \bar{R}_i - \bar{R}_j \right| \stackrel{?}{>} z_{\alpha'} \sqrt{\frac{N(N+1)}{12} \left(\frac{1}{n_i} + \frac{1}{n_j}\right)}$$

where:

- $\bar{R}_i = \frac{R_i}{n_i}$ = mean rank for algorithm $i$
- $z_{\alpha'}$ = critical value from standard normal distribution
- $\alpha' = \frac{\alpha}{m}$ = Bonferroni-corrected significance level
  - $m = \binom{k}{2}$ = number of pairwise comparisons
- $N$ = total sample size

#### Bonferroni Correction

To maintain family-wise error rate $\alpha = 0.05$ across $m$ comparisons:

$$\alpha' = \frac{0.05}{m}$$

**Example**: With 3 algorithms, $m = 3$ comparisons, so $\alpha' = 0.05/3 \approx 0.0167$ for each comparison.

#### Example

```python
from scipy.stats import mannwhitneyu

pso = [1.234, 1.245, ..., 1.256]
eda = [2.345, 2.456, ..., 2.567]
abc = [3.456, 3.567, ..., 3.678]

# Bonferroni-corrected alpha for 3 comparisons
alpha_corrected = 0.05 / 3

# Pairwise Mann-Whitney U tests (rank-based)
comparisons = [
    ("PSO vs EDA", pso, eda),
    ("PSO vs ABC", pso, abc),
    ("EDA vs ABC", eda, abc)
]

for name, group1, group2 in comparisons:
    stat, p = mannwhitneyu(group1, group2)
    significant = "✓" if p < alpha_corrected else "✗"
    print(f"{name}: p={p:.6f} {significant}")
```

---

## Interpretation Guidelines

### Scenario A: All Normal + ANOVA Significant

**What It Means**:
- Data are normally distributed
- Parametric assumptions are satisfied
- At least one algorithm performs significantly differently

**What To Do**:
1. Examine Tukey HSD results to identify specific differences
2. Compare means (not medians) as summary statistics
3. Report mean ± std dev for each algorithm

**Example Report**:
```
"ANOVA revealed significant differences in performance (F = 45.32, p < 0.001).
Post-hoc Tukey HSD testing showed PSO significantly outperformed both EDA
(p < 0.001) and ABC (p = 0.002), while EDA and ABC were not significantly
different (p = 0.145)."
```

### Scenario B: Not All Normal + Kruskal-Wallis Significant

**What It Means**:
- Data violate normality assumptions
- Non-parametric methods are appropriate
- Distributions differ significantly

**What To Do**:
1. Examine Dunn's test results for pairwise differences
2. Report medians (not means) as summary statistics
3. Consider visualizing distributions (boxplots)

**Example Report**:
```
"Kruskal-Wallis test revealed significant differences (H = 38.91, p < 0.001).
Dunn's test (Bonferroni-corrected) showed PSO had significantly lower median
fitness than EDA (p < 0.001) and ABC (p = 0.003). EDA and ABC medians did
not differ significantly (p = 0.089)."
```

### Scenario C: All Normal + ANOVA Not Significant

**What It Means**:
- No statistically significant differences detected
- Algorithms are empirically equivalent (on this benchmark, this dimension)

**What To Do**:
1. Report descriptive statistics (means, std devs)
2. Calculate effect sizes (Cohen's d) for practical significance
3. Discuss computational costs (is faster algorithm better despite same fitness?)

**Example Report**:
```
"ANOVA showed no significant difference in mean fitness across algorithms
(F = 1.45, p = 0.241). PSO, EDA, and ABC achieved statistically equivalent
performance on the Sphere function. However, PSO required 30% fewer function
evaluations, making it the most efficient choice for this problem."
```

### Scenario D: Not All Normal + Kruskal-Wallis Not Significant

**What It Means**:
- Data violate normality
- Non-parametric test finds no significant differences

**What To Do**:
1. Report medians and ranks as summary statistics
2. Emphasize robustness (non-parametric test is conservative)
3. Consider sample size adequacy

**Example Report**:
```
"Kruskal-Wallis test found no significant differences (H = 2.33, p = 0.312),
indicating empirical equivalence of algorithms on this benchmark. Descriptive
statistics (median fitness: PSO=1.234, EDA=1.245, ABC=1.256) confirm close
performance."
```

---

## Effect Size and Practical Significance

While p-values tell us about **statistical** significance, **effect size** measures the **magnitude** of differences.

### Cohen's d (for comparing two groups)

$$d = \frac{\bar{x}_1 - \bar{x}_2}{s_p}$$

where $s_p$ is the pooled standard deviation:

$$s_p = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}}$$

#### Interpretation

| $|d|$ Value | Magnitude |
|-------------|-----------|
| $< 0.2$ | Negligible |
| $0.2 - 0.5$ | Small |
| $0.5 - 0.8$ | Medium |
| $> 0.8$ | Large |

#### Example

```python
from scipy.stats import norm

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    s_p = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1 + n2 - 2))
    return (np.mean(group1) - np.mean(group2)) / s_p

pso = [1.234, 1.245, ..., 1.256]
eda = [2.345, 2.456, ..., 2.567]

d = cohens_d(pso, eda)
print(f"Cohen's d (PSO vs EDA): {d:.3f}")

if abs(d) < 0.2:
    print("  → Negligible effect")
elif abs(d) < 0.5:
    print("  → Small effect")
elif abs(d) < 0.8:
    print("  → Medium effect")
else:
    print("  → Large effect")
```

---

## Complete Example: From Data to Conclusion

### Step 1: Collect Results

```python
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere

bounds = [(-5, 5)] * 10

# Run 30 independent trials
pso_results = [PSO(sphere, bounds).run()[1] for _ in range(30)]
eda_results = [EDA(sphere, bounds).run()[1] for _ in range(30)]
abc_results = [ABC(sphere, bounds).run()[1] for _ in range(30)]
```

### Step 2: Test Normality

```python
from scipy.stats import shapiro

for name, results in [("PSO", pso_results), ("EDA", eda_results), ("ABC", abc_results)]:
    stat, p = shapiro(results)
    print(f"{name}: W={stat:.4f}, p={p:.6f}", 
          "✓ Normal" if p > 0.05 else "✗ Non-normal")
```

**Output**:
```
PSO: W=0.9812, p=0.841234 ✓ Normal
EDA: W=0.9734, p=0.523456 ✓ Normal
ABC: W=0.9201, p=0.001234 ✗ Non-normal
```

**Decision**: Not all normal → Use Kruskal-Wallis

### Step 3: Primary Hypothesis Test

```python
from scipy.stats import kruskal

h_stat, p_val = kruskal(pso_results, eda_results, abc_results)
print(f"Kruskal-Wallis: H={h_stat:.4f}, p={p_val:.6f}")

if p_val < 0.05:
    print("✓ Significant difference detected → Proceed to post-hoc tests")
else:
    print("✗ No significant difference → Algorithms are empirically equivalent")
```

**Output**:
```
Kruskal-Wallis: H=45.3210, p=0.000001
✓ Significant difference detected
```

### Step 4: Post-Hoc Testing (Dunn)

```python
# Simplified Dunn's test using pairwise Mann-Whitney
from scipy.stats import mannwhitneyu

alpha_corrected = 0.05 / 3  # 3 pairwise comparisons

comparisons = [
    ("PSO vs EDA", pso_results, eda_results),
    ("PSO vs ABC", pso_results, abc_results),
    ("EDA vs ABC", eda_results, abc_results)
]

for name, group1, group2 in comparisons:
    stat, p = mannwhitneyu(group1, group2)
    sig = "✓" if p < alpha_corrected else "✗"
    print(f"{name}: p={p:.6f} {sig}")
```

**Output**:
```
PSO vs EDA: p=0.000032 ✓ Significant
PSO vs ABC: p=0.000001 ✓ Significant
EDA vs ABC: p=0.045267 ✗ Not significant
```

### Step 5: Report Findings

```python
print("="*60)
print("FINAL CONCLUSION")
print("="*60)
print(f"""
PSO achieved significantly lower fitness than both EDA and ABC
on the 10D Sphere function. The difference between EDA and ABC
was not statistically significant.

Algorithm Performance (Median ± IQR):
  - PSO: {np.median(pso_results):.6f} ± {np.percentile(pso_results, 75) - np.percentile(pso_results, 25):.6f}
  - EDA: {np.median(eda_results):.6f} ± {np.percentile(eda_results, 75) - np.percentile(eda_results, 25):.6f}
  - ABC: {np.median(abc_results):.6f} ± {np.percentile(abc_results, 75) - np.percentile(abc_results, 25):.6f}

Recommendation: PSO is the best choice for this problem.
""")
```

---

## Implementation in evobench

All this methodology is automated in the `analyze()` function:

```python
from evobench.stats import analyze, stat_report

results = analyze(
    func_name="sphere",
    result_list=[pso_results, eda_results, abc_results],
    algorithm_names=["PSO", "EDA", "ABC"],
    alpha=0.05
)

print(stat_report(results))
```

Output is automatically formatted with all statistical details and appropriate interpretation.

---

## Best Practices

### DO ✓

- Run at least 20–30 independent trials per algorithm per function
- Check normality assumptions before choosing tests
- Report both statistical significance AND effect sizes
- Use appropriate post-hoc tests when significant
- Document all decisions and parameters
- Make results reproducible (fix random seeds for documentation)

### DON'T ✗

- Use p-values alone to interpret results (without effect sizes)
- Perform multiple tests without correction for multiple comparisons
- Assume normal distribution without testing
- Cherry-pick benchmarks based on preferred algorithm
- Report only mean values; variance matters!
- Ignore practical significance when p < 0.05

---

## References

### Statistical Testing

- Shapiro, S. S., & Wilk, M. B. (1965). "An analysis of variance test for normality." *Biometrika*, 52(3-4), 591–611.

- Kruskal, W. H., & Wallis, W. A. (1952). "Use of ranks in one-criterion variance analysis." *Journal of the American Statistical Association*, 47(260), 583–621.

- Tukey, J. W. (1949). "Comparing individual means in the analysis of variance." *Biometrics*, 5(2), 99–114.

### Applied to Evolutionary Computation

- Derrac, J., García, S., Molina, D., & Herrera, F. (2011). "A practical tutorial on the use of nonparametric statistical tests as a methodology for comparing evolutionary and swarm intelligence algorithms." *Swarm and Evolutionary Computation*, 1(1), 3–18.

- García, S., Molina, D., Lozano, M., & Herrera, F. (2009). "A study on the use of non-parametric tests for analyzing the evolutionary algorithms' behaviour." *Journal of Heuristics*, 15(6), 617–644.

---

## See Also

- [Benchmark Function Theory](benchmark-functions.md)
- [Statistical Analysis API](../reference/index.md#statistics)
- [Practical Guides](../guide/index.md)
