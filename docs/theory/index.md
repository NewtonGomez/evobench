# Theory & Concepts

## Overview

This section provides the theoretical foundation and scientific background for understanding evolutionary algorithms and benchmarking methodology. It covers:

- **Benchmark Function Theory**: Mathematical properties and evaluation criteria
- **Statistical Testing**: Rigorous hypothesis testing framework for algorithm comparison
- **Evolutionary Algorithm Fundamentals**: Core concepts and convergence principles
- **Convergence Analysis**: Understanding optimization dynamics

The material here is intended for **researchers, practitioners, and educators** who want to understand *why* algorithms work the way they do and *how* to interpret experimental results rigorously.

---

## Key Topics

### Benchmark Functions

Benchmark functions are far more than random test cases—they represent specific optimization problem classes with well-studied properties.

**→ Full Reference**: [Benchmark Function Theory](benchmark-functions.md)

Key topics include:
- Mathematical properties (separability, modality, convexity)
- Landscape topology and difficulty assessment
- Theoretical optima and convergence guarantees
- Function selection strategies

### Statistical Testing Framework

Comparing evolutionary algorithms requires rigorous statistical methodology. The decision flow implemented in evobench ensures that performance differences are not merely artifacts of stochastic variation.

**→ Full Reference**: [Statistical Testing and Hypothesis Testing](statistical-testing.md)

Key topics include:
- Normality testing (Shapiro-Wilk test)
- Primary hypothesis tests (ANOVA, Kruskal-Wallis)
- Post-hoc pairwise comparisons (Tukey, Dunn)
- Interpretation guidelines and common scenarios

### Evolutionary Algorithm Principles

Understanding the fundamental mechanisms and dynamics of population-based optimization.

**Topics covered**:
- Selection mechanisms (fitness-based, rank-based, tournament)
- Variation operators (crossover, mutation, recombination)
- Population diversity and convergence pressure
- Exploration vs. exploitation tradeoff

### Convergence Analysis

Tools and techniques for analyzing how algorithms approach optimal solutions.

**Topics covered**:
- Convergence curves and their interpretation
- Early stopping criteria and stagnation detection
- Convergence rate measurement
- Performance metrics and comparative analysis

---

## Document Structure

```
theory/
├── index.md                          ← You are here
├── benchmark-functions.md            # Detailed benchmark theory
└── statistical-testing.md            # Hypothesis testing methodology
```

---

## Recommended Reading Path

### For Practitioners

1. **[Benchmark Functions](benchmark-functions.md)**: Understand test landscapes
2. **[Statistical Testing](statistical-testing.md)**: Learn to interpret results rigorously
3. **Guides**: Read practical tutorials in the "Guide" section

### For Researchers

1. **Evolutionary Algorithm Principles**: Understand EA taxonomy and dynamics
2. **[Benchmark Functions](benchmark-functions.md)**: Deep dive into function properties
3. **[Statistical Testing](statistical-testing.md)**: Design rigorous experiments
4. **Convergence Analysis**: Analyze algorithm behavior quantitatively

### For Educators

1. **[Benchmark Functions](benchmark-functions.md)**: Teach landscape diversity
2. **Evolutionary Algorithm Principles**: Teach EA mechanisms
3. **[Statistical Testing](statistical-testing.md)**: Teach experimental design
4. **Example studies**: Use provided examples in courses

---

## Key Concepts Glossary

### Population-Based Optimization

- **Individual**: A candidate solution $\mathbf{x} = (x_1, x_2, \ldots, x_d)$
- **Population**: Set of individuals $\{\mathbf{x}^{(1)}, \mathbf{x}^{(2)}, \ldots, \mathbf{x}^{(n)}\}$
- **Fitness**: Objective function value $f(\mathbf{x})$ (lower is better for minimization)
- **Generation/Iteration**: One complete cycle of selection, variation, evaluation

### Landscape Properties

- **Separability**: Whether dimensions can be optimized independently
- **Modality**: Number of local optima (unimodal vs. multimodal)
- **Convexity**: Whether all local optima are global
- **Conditioning**: Ratio of steepest to gentlest descent directions

### Algorithm Properties

- **Exploration**: Search across diverse regions (broad sampling)
- **Exploitation**: Refine solutions in promising regions (intense sampling)
- **Convergence**: Progress toward better solutions over time
- **Premature Convergence**: Convergence to local optimum before finding global best

### Statistical Terms

- **Hypothesis Test**: Decision procedure for comparing groups
- **p-value**: Probability of observing data if null hypothesis is true
- **Significance Level ($\alpha$)**: Threshold for rejecting null hypothesis (typically 0.05)
- **Power**: Ability to detect true differences when they exist
- **Effect Size**: Magnitude of difference between groups

---

## Important References

### Foundational Works

- Hansen, N., Auger, A., & Ros, R. (2016). "Benchmarking optimization problems". In *CEC 2016 Proceedings*.

- Derrac, J., García, S., Molina, D., & Herrera, F. (2011). "A practical tutorial on the use of nonparametric statistical tests". *Swarm and Evolutionary Computation*, 1(1), 3–18.

### Algorithm-Specific

- Kennedy, J., & Eberhart, R. (1995). "Particle Swarm Optimization". In *ICNN'95 Proceedings*.

- Karaboga, D., & Basturk, B. (2007). "A powerful and efficient algorithm for numerical function optimization: artificial bee colony (ABC)". *Journal of Global Optimization*, 39(3), 459–471.

---

## Integration with evobench

### Using Theory to Guide Practice

All the theoretical concepts here are **operationalized** in evobench's code:

```python
# Statistical testing framework (theory → practice)
from evobench.stats import analyze, stat_report

results = analyze(
    func_name="sphere",
    result_list=[pso_results, eda_results, abc_results],
    algorithm_names=["PSO", "EDA", "ABC"],
    alpha=0.05  # Significance level from statistical theory
)

# Interpreting results through theory
print(stat_report(results))  # Hypothesis testing decision
```

### Theory → Design → Implementation

The evobench framework embodies these principles:

1. **Benchmark selection**: Based on desired problem properties (separability, modality, etc.)
2. **Algorithm comparison**: Using rigorous statistical hypothesis testing
3. **Result interpretation**: Via convergence analysis and effect sizes
4. **Reproducibility**: Through careful documentation and seeding

---

## See Also

- **[API Reference](../reference/index.md)**: Detailed technical documentation
- **[Guides & Tutorials](../guide/index.md)**: Practical how-to instructions
- **[Examples](../examples/index.md)**: Runnable code samples

---

## Questions & Further Learning

### Common Questions

**Q: Why use multiple hypothesis tests?**  
A: Different tests make different assumptions. Shapiro-Wilk checks normality; ANOVA vs. Kruskal-Wallis choice depends on the result.

**Q: How many runs do I need?**  
A: Generally 20–30 independent runs per condition. More runs increase statistical power; fewer runs reduce computational cost.

**Q: What's a "significant" difference?**  
A: Statistically, when $p < \alpha$ (typically 0.05). Practically, even statistically significant differences may be negligible if effect sizes are small.

**Q: Can I use gradient-based optimization on these benchmarks?**  
A: For smooth landscapes (Sphere, Rosenbrock), yes. For multimodal landscapes (Ackley, Trid), no—gradients are either missing or misleading.

### Recommended Study Path

1. **Week 1**: Read [Benchmark Functions](benchmark-functions.md)
2. **Week 2**: Read [Statistical Testing](statistical-testing.md)
3. **Week 3**: Study provided examples and run experiments
4. **Week 4**: Design and conduct your own benchmarking study

---

**Last Updated**: 2026-05-06  
**Version**: evobench 0.1.0
