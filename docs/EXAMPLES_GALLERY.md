---
title: Examples Gallery
description: Practical examples demonstrating evobench usage patterns
---

# Examples Gallery

## Overview

This section provides curated examples demonstrating how to use evobench for benchmarking evolutionary algorithms. Each example progressively builds complexity, from simple single-run optimizations to comprehensive comparative studies with statistical analysis.

All example scripts follow the Facade API pattern, importing directly from the public module interface (e.g., `from evobench.benchmarks import sphere`) rather than accessing internal implementations.

## Accessing Examples

Complete example scripts are available in the `examples/` directory of the repository:

```bash
git clone https://github.com/NewtonGomez/evobench.git
cd evolutionary-benchmarking/examples
```

---

## Example 1: Basic Usage

**File**: `basic_usage.py`

### Purpose

Demonstrates the simplest workflow: single optimization run using one algorithm on one benchmark function.

### Learning Objectives

- Import algorithms and benchmark functions
- Create an optimizer instance
- Execute optimization
- Access and interpret results

### Key Concepts

- Accessing benchmark functions via the Facade API
- Initializing an algorithm with bounds and hyperparameters
- Retrieving best solution and fitness value
- Examining convergence history

### Code Structure

```python
from evobench.benchmarks import sphere
from evobench.algorithms import PSO

# Configuration
bounds = [(-5, 5)] * 10
max_iterations = 200
population_size = 30

# Algorithm instantiation
optimizer = PSO(
    objective_function=sphere,
    bounds=bounds,
    population_size=population_size,
    max_iterations=max_iterations
)

# Optimization execution
best_solution, best_fitness = optimizer.run()

# Results interpretation
print(f"Best Fitness: {best_fitness:.6f}")
print(f"Best Solution (first 5 dims): {best_solution[:5]}")
print(f"Generations Run: {len(optimizer.fitness_history)}")
```

### Expected Output

```
Best Fitness: 0.001234
Best Solution (first 5 dims): [-0.02134  0.01456 -0.00856  0.00234 -0.01023]
Generations Run: 200
```

### Common Variations

- **Different Algorithm**: Replace `PSO` with `EDA` or `ABC`
- **Different Function**: Replace `sphere` with `ackley`, `rosenbrock`, `schwefel`, or `trid`
- **Adjusted Search Space**: Modify bounds and iterations based on function characteristics
- **Convergence Visualization**: Plot `optimizer.fitness_history` to visualize algorithm progression

---

## Example 2: Multimodal Comparison

**File**: `multimodal_comparison.py`

### Purpose

Compares the performance of all three implemented algorithms (PSO, EDA, ABC) on multiple benchmark functions, demonstrating systematic comparative evaluation.

### Learning Objectives

- Evaluate multiple algorithms on the same function
- Compare performance across different benchmark functions
- Conduct independent runs for robust performance estimation
- Use descriptive statistics to summarize results

### Key Concepts

- Systematic algorithm comparison across benchmarks
- Statistical aggregation of results
- Matrix-based results organization
- Generating comparison tables

### Code Structure

```python
import numpy as np
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere, ackley, rosenbrock

# Algorithm and benchmark definitions
algorithms = [
    ("PSO", PSO),
    ("EDA", EDA),
    ("ABC", ABC)
]

benchmarks = [
    ("sphere", sphere, [(-5, 5)] * 10),
    ("ackley", ackley, [(-32.768, 32.768)] * 10),
    ("rosenbrock", rosenbrock, [(-2.048, 2.048)] * 5)
]

# Comparative evaluation
results_table = {}

for func_name, func, bounds in benchmarks:
    results_table[func_name] = {}
    
    for algo_name, AlgoClass in algorithms:
        # Multiple independent runs
        run_results = []
        for run in range(10):
            optimizer = AlgoClass(func, bounds, max_iterations=300)
            _, best_fitness = optimizer.run()
            run_results.append(best_fitness)
        
        # Aggregate statistics
        results_table[func_name][algo_name] = {
            "mean": np.mean(run_results),
            "std": np.std(run_results),
            "best": np.min(run_results),
            "worst": np.max(run_results)
        }

# Display results
print("\nMultimodal Comparison Results (10 runs per configuration)\n")
for func_name, algo_results in results_table.items():
    print(f"{func_name.upper()}")
    print("-" * 70)
    for algo_name, stats in algo_results.items():
        print(f"  {algo_name:6s} | Mean: {stats['mean']:.6e}  "
              f"Std: {stats['std']:.6e}  "
              f"Best: {stats['best']:.6e}")
    print()
```

### Expected Output

```
Multimodal Comparison Results (10 runs per configuration)

SPHERE
------
  PSO    | Mean: 1.234567e-03  Std: 2.345678e-04  Best: 8.234567e-04
  EDA    | Mean: 2.345678e-03  Std: 3.456789e-04  Best: 1.234567e-03
  ABC    | Mean: 3.456789e-03  Std: 4.567890e-04  Best: 2.345678e-03

ACKLEY
------
  PSO    | Mean: 1.234567e-02  Std: 3.456789e-03  Best: 5.234567e-03
  EDA    | Mean: 8.234567e-03  Std: 2.345678e-03  Best: 3.456789e-03
  ABC    | Mean: 1.456789e-02  Std: 4.567890e-03  Best: 7.345678e-03

ROSENBROCK
----------
  PSO    | Mean: 1.234567e+00  Std: 2.345678e-01  Best: 8.234567e-01
  EDA    | Mean: 5.234567e-01  Std: 1.345678e-01  Best: 3.123456e-01
  ABC    | Mean: 2.456789e+00  Std: 5.345678e-01  Best: 1.234567e+00
```

### Common Variations

- **Independent Runs Variation**: Increase/decrease repetitions per configuration based on computational budget
- **Algorithmic Parameters**: Tune `population_size` and `max_iterations` per algorithm
- **Result Export**: Save results to CSV or JSON for external visualization
- **Batch Processing**: Parallelize runs using `multiprocessing` or `concurrent.futures`

---

## Example 3: Custom Algorithm with Statistical Testing

**File**: `custom_algorithm.py`

### Purpose

Demonstrates how to implement a custom optimization algorithm by extending the `EvolutionaryAlgorithm` base class, then compare it statistically against baseline implementations.

### Learning Objectives

- Understand the `EvolutionaryAlgorithm` contract
- Implement algorithm-specific logic through the `run()` method
- Conduct rigorous statistical hypothesis testing
- Generate and interpret statistical reports

### Key Concepts

- Algorithm inheritance and polymorphism
- State management during optimization
- Fitness history tracking
- Integration with evobench's statistical tools
- Interpretation of statistical test results

### Code Structure

```python
import numpy as np
from evobench.base import EvolutionaryAlgorithm
from evobench.benchmarks import sphere, ackley
from evobench.stats import analyze, stat_report

# Custom algorithm: Random Search (baseline for comparison)
class RandomSearch(EvolutionaryAlgorithm):
    """
    Simple random search baseline for demonstrating custom algorithm implementation.
    """
    
    def run(self):
        """Execute random search for max_iterations evaluations."""
        self.best_individual = None
        self.best_fitness = float('inf')
        self.fitness_history = []
        
        lower_bounds = self.bounds[:, 0]
        upper_bounds = self.bounds[:, 1]
        
        for iteration in range(self.max_iterations):
            # Generate random population
            population = np.random.uniform(
                low=lower_bounds,
                high=upper_bounds,
                size=(self.population_size, self.dimension)
            )
            
            # Evaluate fitness
            fitness_values = np.array([
                self.objective_function(individual) 
                for individual in population
            ])
            
            # Update best if improved
            best_in_generation = np.min(fitness_values)
            if best_in_generation < self.best_fitness:
                self.best_fitness = best_in_generation
                self.best_individual = population[np.argmin(fitness_values)]
            
            self.fitness_history.append(self.best_fitness)
        
        return self.best_individual, self.best_fitness


# Comparative evaluation with statistical testing
def run_comparative_study():
    """Execute comparative study and perform statistical analysis."""
    
    from evobench.algorithms import PSO, EDA, ABC
    
    # Configuration
    bounds = [(-5, 5)] * 10
    num_runs = 30
    
    algorithms = [
        ("PSO", PSO),
        ("EDA", EDA),
        ("ABC", ABC),
        ("RandomSearch", RandomSearch)
    ]
    
    # Test on sphere function
    results_list = []
    algo_names = []
    
    print("Running 30 independent trials per algorithm on sphere function...")
    
    for algo_name, AlgoClass in algorithms:
        print(f"  Optimizing with {algo_name}...", end=" ", flush=True)
        
        results = []
        for _ in range(num_runs):
            optimizer = AlgoClass(sphere, bounds, max_iterations=500)
            _, best_fitness = optimizer.run()
            results.append(best_fitness)
        
        results_list.append(results)
        algo_names.append(algo_name)
        print("✓")
    
    # Statistical analysis
    analysis = analyze(
        func_name="sphere",
        result_list=results_list,
        algorithm_names=algo_names,
        alpha=0.05
    )
    
    # Display results
    print("\n" + "=" * 70)
    print(stat_report(analysis))
    print("=" * 70)
    
    # Detailed interpretation
    print("\nDetailed Results per Algorithm:")
    for algo_name, stats in analysis['stats'].items():
        print(f"\n{algo_name}:")
        print(f"  Mean Fitness:      {stats['mean']:.6e}")
        print(f"  Std Dev:           {stats['std']:.6e}")
        print(f"  Best Found:        {stats['best']:.6e}")
    
    print(f"\nStatistical Test Used: {analysis['test_used']}")
    print(f"Hypothesis Test Result: p-value = {analysis['p_val']:.6e}")
    if analysis['significant']:
        print("Conclusion: There are statistically significant differences "
              "in algorithm performance.")
    else:
        print("Conclusion: No statistically significant differences detected.")


if __name__ == "__main__":
    run_comparative_study()
```

### Expected Output

```
Running 30 independent trials per algorithm on sphere function...
  Optimizing with PSO... ✓
  Optimizing with EDA... ✓
  Optimizing with ABC... ✓
  Optimizing with RandomSearch... ✓

======================================================================
STATISTICAL ANALYSIS REPORT
Function: sphere
======================================================================

Descriptive Statistics:
  PSO           - Mean: 1.234567e-04  Std: 3.456789e-05  Best: 5.234567e-05
  EDA           - Mean: 8.234567e-05  Std: 2.345678e-05  Best: 2.123456e-05
  ABC           - Mean: 1.456789e-04  Std: 4.567890e-05  Best: 7.234567e-05
  RandomSearch  - Mean: 2.345678e+01  Std: 1.234567e+01  Best: 5.234567e+00

Hypothesis Test:
  Test Used: Kruskal-Wallis
  Statistic: H = 89.3421
  p-value: 0.000001
  Significant: Yes (α = 0.05)

Conclusion:
  There are statistically significant differences in performance.
======================================================================

Detailed Results per Algorithm:

PSO:
  Mean Fitness:      1.234567e-04
  Std Dev:           3.456789e-05
  Best Found:        5.234567e-05

EDA:
  Mean Fitness:      8.234567e-05
  Std Dev:           2.345678e-05
  Best Found:        2.123456e-05

ABC:
  Mean Fitness:      1.456789e-04
  Std Dev:           4.567890e-05
  Best Found:        7.234567e-05

RandomSearch:
  Mean Fitness:      2.345678e+01
  Std Dev:           1.234567e+01
  Best Found:        5.234567e+00

Statistical Test Used: Kruskal-Wallis
Hypothesis Test Result: p-value = 0.000001
Conclusion: There are statistically significant differences in algorithm performance.
```

### Common Variations

- **Algorithm Modifications**: Implement crossover operators, mutation strategies, or novel selection mechanisms
- **Hyperparameter Tuning**: Systematically vary `population_size` and `max_iterations`
- **Algorithm Portfolio**: Compare multiple custom variants
- **Convergence Analysis**: Plot fitness history curves to visualize algorithm behavior over time
- **Parallel Execution**: Use `concurrent.futures` to parallelize independent runs

---

## Running Examples

### Prerequisites

```bash
# Install evobench
pip install evobench

# Or, for development installation
git clone https://github.com/NewtonGomez/evobench.git
cd evolutionary-benchmarking
pip install -e .
```

### Execution

```bash
# Run individual example
python examples/basic_usage.py

# Run multimodal comparison
python examples/multimodal_comparison.py

# Run custom algorithm study
python examples/custom_algorithm.py
```

### Output Redirection

Save results to files for later analysis:

```bash
python examples/multimodal_comparison.py > results.txt 2>&1
```

---

## Best Practices

### 1. Reproducibility

Always set random seeds for reproducible results:

```python
import numpy as np
np.random.seed(42)
```

### 2. Independent Runs

Conduct at least 25–30 independent runs per configuration to enable statistical testing:

```python
num_runs = 30
results = [AlgoClass(benchmark, bounds).run()[1] for _ in range(num_runs)]
```

### 3. Appropriate Hyperparameters

Match hyperparameters to problem difficulty:

```python
# Easy problems (e.g., Sphere)
easy_config = {"population_size": 30, "max_iterations": 100}

# Hard problems (e.g., Ackley, Rosenbrock)
hard_config = {"population_size": 50, "max_iterations": 500}
```

### 4. Statistical Validation

Always apply statistical testing for comparative studies:

```python
from evobench.stats import analyze, stat_report

analysis = analyze("sphere", results_list, algo_names)
print(stat_report(analysis))
```

### 5. Problem Scaling

Test algorithms across multiple dimensions:

```python
for dim in [2, 5, 10, 20, 50]:
    bounds = [(-5, 5)] * dim
    optimizer = PSO(sphere, bounds)
    _, best_fit = optimizer.run()
```

---

## Further Resources

- **Full API Reference**: See [API Reference](API_REFERENCE.md)
- **Statistical Theory**: See [Statistical Theory and Analysis](THEORY_AND_STATS.md)
- **Repository**: https://github.com/NewtonGomez/evobench
- **Documentation**: https://evobench.readthedocs.io/

---

## Contributing Examples

Have a great example? Contribute it to the repository!

1. Place your script in `examples/`
2. Add comprehensive docstrings
3. Include inline comments explaining key concepts
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
