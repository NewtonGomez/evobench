# Algorithms

## Overview

This section provides complete technical documentation for all evolutionary baselines algorithms implemented in evobench. Each algorithm represents a distinct solution strategy and inherits from the `EvolutionaryAlgorithm` base class.

All algorithms follow the same interface contract, making them **interchangeable** for fair comparative evaluation on benchmark functions.

---

## Algorithm Characteristics Comparison

| Algorithm | Type | Inspiration | Exploration | Exploitation | Best For |
|-----------|------|-------------|-------------|--------------|----------|
| **PSO** | Swarm Intelligence | Bird flocking | Moderate | High | Smooth landscapes, fast convergence |
| **EDA** | Model-Based | Probabilistic modeling | Strong | Moderate | Non-separable problems, diverse solutions |
| **ABC** | Swarm Intelligence | Bee foraging | Strong | Moderate | Multimodal landscapes, robustness |

---

## Particle Swarm Optimization (PSO)

**Velocity-based swarm intelligence** simulating collective behavior of flocking birds or schooling fish.

**Key Features**:
- Continuous position and velocity updates
- Personal best (`pbest`) + global best (`gbest`) attraction
- Fast convergence on smooth landscapes
- Pronounced exploitation in later iterations

**→ Full Documentation**: [PSO Reference](pso.md)

### Quick Example

```python
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

bounds = [(-5, 5)] * 10
optimizer = PSO(sphere, bounds, population_size=30, max_iterations=200)
best_solution, best_fitness = optimizer.run()
```

---

## Estimation of Distribution Algorithm (EDA)

**Model-based evolutionary approach** that learns probabilistic models of the search space.

**Key Features**:
- Gaussian model learning from elite solutions
- Tournament selection for elite identification
- Systematic sampling from learned distributions
- Good exploration properties in non-separable spaces

**→ Full Documentation**: [EDA Reference](eda.md)

### Quick Example

```python
from evobench.algorithms import EDA
from evobench.benchmarks import rosenbrock

bounds = [(-2, 2)] * 5
optimizer = EDA(rosenbrock, bounds, population_size=40, max_iterations=150)
best_solution, best_fitness = optimizer.run()
```

---

## Artificial Bee Colony (ABC)

**Swarm intelligence inspired by honeybee foraging** with three behavioral roles.

**Key Features**:
- **Employed bees**: Exploit known food sources
- **Onlooker bees**: Make probabilistic choices based on fitness
- **Scout bees**: Explore new regions when sources are abandoned
- Limit-based abandonment mechanism prevents stagnation

**→ Full Documentation**: [ABC Reference](abc.md)

### Quick Example

```python
from evobench.algorithms import ABC
from evobench.benchmarks import ackley

bounds = [(-32.768, 32.768)] * 8
optimizer = ABC(ackley, bounds, population_size=50, max_iterations=500)
best_solution, best_fitness = optimizer.run()
```

---

## Common Interface

All algorithms share the same constructor signature and execution pattern:

### Constructor

```python
Algorithm(
    objective_function: Callable[[np.ndarray], float],
    bounds: List[Tuple[float, float]],
    population_size: int = 50,
    max_iterations: int = 100
)
```

### Execution

```python
best_solution, best_fitness = optimizer.run()

# Access internal state
print(optimizer.fitness_history)        # Convergence curve
print(optimizer.best_individual)        # Solution vector
print(optimizer.dimension)              # Problem dimensionality
```

---

## Comparative Example

Run all three algorithms on the same benchmark to compare performance:

```python
import numpy as np
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere
from evobench.stats import analyze, stat_report

bounds = [(-5, 5)] * 10
num_runs = 30

# Run each algorithm 30 times
pso_results = []
eda_results = []
abc_results = []

for _ in range(num_runs):
    pso_results.append(PSO(sphere, bounds).run()[1])
    eda_results.append(EDA(sphere, bounds).run()[1])
    abc_results.append(ABC(sphere, bounds).run()[1])

# Statistical comparison
analysis = analyze(
    func_name="sphere",
    result_list=[pso_results, eda_results, abc_results],
    algorithm_names=["PSO", "EDA", "ABC"],
    alpha=0.05
)

print(stat_report(analysis))
```

---

## Selection Guide

### Choose PSO When:
- Working with smooth, continuous optimization landscapes
- Seeking fast convergence on unimodal problems
- Memory constraints limit population size
- Hyperparameter tuning effort is acceptable

**Benchmark recommendations**: Sphere, Rosenbrock

### Choose EDA When:
- Problem has non-separable variables (variables interact)
- Seeking robust exploration across diverse optima
- Need probabilistic model interpretation
- Population diversity is prioritized

**Benchmark recommendations**: Ackley, Schwefel 1.2, Trid

### Choose ABC When:
- Dealing with highly multimodal landscapes
- Need balanced exploration-exploitation dynamics
- Seeking algorithm robustness across diverse problem classes
- Simple hyperparameter tuning preferred

**Benchmark recommendations**: Ackley, Trid

---

## Sequence of Increasing Difficulty

To profile algorithm performance across difficulty levels:

```python
from evobench.algorithms import PSO
from evobench.benchmarks import sphere, rosenbrock, ackley, schwefel, trid

bounds_dict = {
    'sphere': [(-5, 5)] * 10,
    'rosenbrock': [(-2.048, 2.048)] * 10,
    'ackley': [(-32.768, 32.768)] * 10,
    'schwefel': [(-100, 100)] * 10,
    'trid': [(-100, 100)] * 10
}

from evobench.benchmarks import BENCHMARK_REGISTRY

algorithms = [PSO, EDA, ABC]

for func_name in ['sphere', 'rosenbrock', 'ackley', 'schwefel', 'trid']:
    benchmark = BENCHMARK_REGISTRY[func_name]
    bounds = bounds_dict[func_name]
    
    print(f"\n{func_name.upper()}")
    print("-" * 50)
    
    for AlgoClass in algorithms:
        optimizer = AlgoClass(benchmark, bounds)
        _, best_fit = optimizer.run()
        print(f"{AlgoClass.__name__}: {best_fit:.6f}")
```

---

## Implementation Details

Each algorithm implements:

- **Initialization**: Random population within bounds
- **Fitness evaluation**: Per-generation objective function calls
- **State management**: Tracking best solution and convergence history
- **Boundary handling**: Clipping individuals to search domain
- **Termination**: Stopping after `max_iterations` generations

For algorithm-specific variation operators (PSO velocity updates, EDA model construction, ABC bee phases), see individual documentation pages.

---

## See Also

- [Base Class Contract](../base.md)
- [Benchmark Functions](../benchmarks.md)
- [Statistical Analysis](../../../theory/statistical-testing.md)
- [Custom Algorithm Development](../../guide/custom-algorithms.md)

---

## File Structure

```
algorithms/
├── index.md         ← You are here
├── pso.md          # Particle Swarm Optimization
├── eda.md          # Estimation of Distribution Algorithm
└── abc.md          # Artificial Bee Colony
```
