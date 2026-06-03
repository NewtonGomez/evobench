# API Reference

## Overview

This section provides complete technical documentation for the public API of **evobench**—a standardized benchmarking framework for evolutionary algorithms and metaheuristics. All documented classes and functions are intended for direct use in benchmarking studies.

The reference material is organized into three primary modules:

- **[Core Architecture](#core-architecture)**: Abstract base class and standards
- **[Algorithms](#algorithms)**: Implemented baselines evolutionary algorithms (PSO, EDA, ABC)
- **[Benchmarks](#benchmarks)**: Standardized test functions
- **[Statistics](#statistics)**: Hypothesis testing and comparative analysis tools

---

## Core Architecture

The foundation of evobench is built on a strict object-oriented design. All algorithms inherit from a common abstract base class, ensuring:

✓ **Uniform interface** across all metaheuristics  
✓ **Consistent state tracking** throughout optimization  
✓ **Standardized initialization** protocols  
✓ **Interchangeable algorithms** for fair comparative evaluation  

**→ Learn more**: [EvolutionaryAlgorithm Base Class](base.md)

---

## Algorithms

evobench implements three foundational evolutionary algorithms, each representing distinct solution strategies:

### Particle Swarm Optimization (PSO)

Velocity-based swarm intelligence inspired by flocking behavior. Fast convergence with pronounced exploitation in later iterations.

**Characteristics**: Continuous velocity updates, personal + social learning, good for smooth landscapes  
**→ Full Reference**: [PSO Documentation](algorithms/pso.md)

### Estimation of Distribution Algorithm (EDA)

Model-based metaheuristic that learns probabilistic distributions of promising solutions. Robust exploration with systematic sampling.

**Characteristics**: Gaussian modeling, tournament selection, good for non-separable problems  
**→ Full Reference**: [EDA Documentation](algorithms/eda.md)

### Artificial Bee Colony (ABC)

Swarm intelligence inspired by honeybee foraging. Three behavioral roles (employed, onlooker, scout) provide balanced exploration-exploitation.

**Characteristics**: Multiple bee phases, limit-based abandonment, good for multimodal problems  
**→ Full Reference**: [ABC Documentation](algorithms/abc.md)

---

## Benchmarks

Standardized continuous optimization test functions covering diverse landscape properties:

| Function | Type | Difficulty | Best For |
|----------|------|------------|----------|
| **Sphere** | Unimodal | Very Low | Baseline validation |
| **Rosenbrock** | Unimodal | Medium-High | Valley navigation |
| **Ackley** | Multimodal | High | Global exploration |
| **Schwefel 1.2** | Unimodal | Medium | Variable coupling |
| **Trid** | Unimodal | High | Correlation exploitation |

**→ Full Reference**: [Benchmark Functions](benchmarks.md)

---

## Statistics

Automated statistical hypothesis testing framework with decision flow:

1. **Normality Assessment** (Shapiro-Wilk test)
2. **Primary Hypothesis Test** (ANOVA or Kruskal-Wallis)
3. **Post-Hoc Pairwise Comparisons** (Tukey or Dunn's test)

**Key Functions**:
- `analyze()`: Automatic test selection and execution
- `stat_report()`: Formatted human-readable reports

**→ Learn more**: See [Statistical Theory](../theory/statistical-testing.md)

---

## Quick API Overview

### Import Main Components

```python
# Algorithms
from evobench.algorithms import PSO, EDA, ABC

# Benchmarks
from evobench.benchmarks import sphere, rosenbrock, ackley, schwefel, trid

# Statistical analysis
from evobench.stats import analyze, stat_report

# Base class for custom algorithms
from evobench.base import EvolutionaryAlgorithm
```

### Basic Usage Pattern

```python
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

# Define search domain
bounds = [(-5, 5)] * 10

# Create optimizer
optimizer = PSO(
    objective_function=sphere,
    bounds=bounds,
    population_size=30,
    max_iterations=200
)

# Run optimization
best_solution, best_fitness = optimizer.run()
print(f"Best Fitness: {best_fitness:.6f}")
print(f"Convergence: {optimizer.fitness_history}")
```

---

## File Structure

```
reference/
├── index.md                    ← You are here
├── base.md                     # EvolutionaryAlgorithm abstract base
├── benchmarks.md               # Benchmark function registry and API
└── algorithms/
    ├── index.md               # Algorithms overview
    ├── pso.md                 # Particle Swarm Optimization
    ├── eda.md                 # Estimation of Distribution Algorithm
    └── abc.md                 # Artificial Bee Colony
```

---

## Related Documentation

- **[Getting Started](../getting-started/index.md)**: Installation and quick introduction
- **[Guides & Tutorials](../guide/index.md)**: Practical how-to instructions
- **[Theory & Concepts](../theory/index.md)**: Mathematical background and benchmarking methodology
- **[Examples](../examples/index.md)**: Runnable code samples

---

## Version Compatibility

This reference documentation applies to **evobench 0.1.0+**.

For version-specific features and breaking changes, see the [Changelog](../changelog/index.md).
