# Artificial Bee Colony (ABC)

## Overview

**Artificial Bee Colony** is a swarm intelligence algorithm inspired by the foraging behavior of honeybees. Unlike PSO (attraction-based) or EDA (model-based), ABC uses distinct behavioral roles to balance exploration and exploitation.

The algorithm divides the population into three types of agents:

1. **Employed Bees**: Exploit known food sources (candidate solutions)
2. **Onlooker Bees**: Make probabilistic choices based on dance information
3. **Scout Bees**: Explore new regions when sources are abandoned

This three-phase mechanism provides robust exploration-exploitation balance and strong performance on multimodal landscapes.

**Location**: `evobench.algorithms.ABC`

**Inspiration**: Honeybee foraging behavior (Karaboga, 2005)

**Key Characteristic**: Multi-phase swarm with explicit exploration-exploitation roles

---

## Algorithm Characteristics

| Property | Value |
|----------|-------|
| **Population Type** | Continuous position vectors |
| **Behavioral Roles** | Employed, onlooker, and scout bees |
| **Selection Strategy** | Fitness-proportional (roulette wheel) for onlookers |
| **Exploration Strategy** | Scout bees escape local optima |
| **Exploitation Bias** | Moderate-high |
| **Exploration Bias** | Strong (all three phases contribute) |
| **Computational Complexity** | $O(n \cdot d)$ per iteration |
| **Convergence Pattern** | Robust, moderate speed |

---

## Mathematical Formulation

### Phase 1: Employed Bee Phase

Each employed bee exploits its food source by modifying one dimension:

$$x_i^{\text{new}} = x_i + \phi_{i,k} \cdot (x_i - x_k)$$

where:

- $x_i$: Current position of employed bee $i$
- $x_k$: Position of randomly selected bee $k \neq i$
- $\phi_{i,k}$: Random factor uniformly distributed in $[-1, 1]$

The new solution is accepted if it improves fitness (greedy selection):

$$x_i \leftarrow \begin{cases} x_i^{\text{new}} & \text{if } f(x_i^{\text{new}}) < f(x_i) \\ x_i & \text{otherwise} \end{cases}$$

### Phase 2: Onlooker Bee Phase

Onlooker bees select food sources probabilistically based on fitness:

$$p_i = \frac{f_i}{\sum_{j=1}^{n} f_j}$$

where $f_i$ is a fitness quality measure (typically: $f_i = \frac{1}{1 + \text{fitness}_i}$ for minimization).

Selected bees then exploit their chosen source using the same modification as employed bees.

### Phase 3: Scout Bee Phase

If a food source is not improved after `limit` iterations, it is abandoned and replaced by a scout bee:

$$x_i^{\text{new}} = \text{random}(\text{bounds})$$

The `limit` parameter controls exploration pressure:

$$\text{limit} = \text{population\_size} \times \text{dimension}$$

### Boundary Constraints

New solutions are clipped to the search domain:

$$x_i^{\text{new}} = \text{clip}(x_i^{\text{new}}, \text{bounds})$$

---

## Constructor

### Signature

```python
class ABC(EvolutionaryAlgorithm):
    def __init__(
        self,
        objective_function: Callable[[np.ndarray], float],
        bounds: List[Tuple[float, float]],
        population_size: int = 50,
        max_iterations: int = 100
    ) -> None
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `objective_function` | `Callable` | Required | Continuous optimization function to minimize |
| `bounds` | `List[Tuple[float, float]]` | Required | Search domain; list of `(lower, upper)` tuples per dimension |
| `population_size` | `int` | 50 | Number of bees (employed + onlooker bees) |
| `max_iterations` | `int` | 100 | Maximum number of generations |

### Inherited Attributes

From `EvolutionaryAlgorithm`:

- `objective_function`: Reference to benchmark function
- `bounds`: Search space boundaries
- `population_size`: Total number of bees
- `max_iterations`: Iteration budget
- `dimension`: Problem dimensionality
- `best_individual`: Best solution found
- `best_fitness`: Fitness of best solution
- `fitness_history`: Best fitness per generation

### ABC-Specific Attributes

```python
self.trial_count: np.ndarray         # Shape (population_size,)
                                     # Abandonment counter per bee

self.limit: int                      # Abandonment threshold
                                     # Typically: population_size × dimension
```

---

## Hyperparameters

### Default Configuration

```python
limit = population_size * dimension    # Abandonment threshold
```

### Effect on Behavior

The `limit` parameter controls how many unsuccessful iterations before abandoning a source:

- **Small limit (~50)**: Frequent exploration, less exploitation
- **Large limit (~500)**: More exploitation, less frequent reset
- **Default**: Product of population size and dimension

---

## Algorithm Flow

### Pseudocode

```
Algorithm: ABC (Artificial Bee Colony)
Input: objective_function, bounds, population_size, max_iterations
Output: best_individual, best_fitness

1. Initialize population randomly within bounds
2. Evaluate all solutions
3. Initialize trial_count to 0 for all bees
4. Identify global best solution
5. 
6. For generation = 1 to max_iterations:
    7.     ========== EMPLOYED BEE PHASE ==========
    8.     For each employed bee i:
    9.         Select random bee k ≠ i
    10.        Generate random φ ∈ [-1, 1]
    11.        x_new ← x_i + φ·(x_i - x_k)
    12.        Apply boundary constraints
    13.        If f(x_new) < f(x_i):
    14.            x_i ← x_new
    15.            trial_count[i] ← 0
    16.        Else:
    17.            trial_count[i] ← trial_count[i] + 1
    18.    
    19.        ========== ONLOOKER BEE PHASE ==========
    20.        Calculate selection probabilities p_i
    21.        For each onlooker bee:
    22.            Select bee i with probability p_i
    23.            Perform same exploitation as employed bee
    24.            Update trial_count[i]
    25.    
    26.        ========== SCOUT BEE PHASE ==========
    27.        For each bee i where trial_count[i] > limit:
    28.            x_i ← random_within_bounds()
    29.            trial_count[i] ← 0
    30.            Evaluate new solution
    31.    
    32.    Update global best solution
    33.    Record best fitness in fitness_history
34. 
35. Return best_individual, best_fitness
```

---

## Usage Examples

### Basic Optimization

```python
from evobench.algorithms import ABC
from evobench.benchmarks import ackley

# Define search domain
bounds = [(-32.768, 32.768)] * 8

# Create ABC instance
optimizer = ABC(
    objective_function=ackley,
    bounds=bounds,
    population_size=50,
    max_iterations=500
)

# Run optimization
best_solution, best_fitness = optimizer.run()

print(f"Best Fitness: {best_fitness:.6f}")
print(f"Solution: {best_solution}")
```

### Multimodal Problem Performance

```python
import matplotlib.pyplot as plt
import numpy as np
from evobench.algorithms import ABC, PSO, EDA
from evobench.benchmarks import ackley

bounds = [(-32.768, 32.768)] * 10

# Run all three algorithms
algorithms = [
    (ABC, "ABC"),
    (PSO, "PSO"),
    (EDA, "EDA")
]

plt.figure(figsize=(12, 6))

for AlgoClass, name in algorithms:
    optimizer = AlgoClass(ackley, bounds, max_iterations=500)
    optimizer.run()
    plt.semilogy(optimizer.fitness_history, label=name, linewidth=2)

plt.xlabel('Generation')
plt.ylabel('Best Fitness (log scale)')
plt.title('ABC vs PSO vs EDA on Ackley Function (Multimodal)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### Statistical Comparison

```python
import numpy as np
from evobench.algorithms import ABC, PSO, EDA
from evobench.benchmarks import trid
from evobench.stats import analyze, stat_report

bounds = [(-400, 400)] * 10
num_runs = 30

# Run each algorithm multiple times
abc_results = [ABC(trid, bounds).run()[1] for _ in range(num_runs)]
pso_results = [PSO(trid, bounds).run()[1] for _ in range(num_runs)]
eda_results = [EDA(trid, bounds).run()[1] for _ in range(num_runs)]

# Statistical analysis
analysis = analyze(
    func_name="trid",
    result_list=[abc_results, pso_results, eda_results],
    algorithm_names=["ABC", "PSO", "EDA"],
    alpha=0.05
)

print(stat_report(analysis))
```

### Convergence Dynamics

```python
from evobench.algorithms import ABC
from evobench.benchmarks import rosenbrock

bounds = [(-2.048, 2.048)] * 5

# Run ABC with detailed tracking
optimizer = ABC(rosenbrock, bounds, max_iterations=300)
best_sol, best_fit = optimizer.run()

# Analyze convergence phases
history = optimizer.fitness_history

# Detect phase transitions
if len(history) > 100:
    early_phase = history[:100]
    mid_phase = history[100:200]
    late_phase = history[200:]
    
    print(f"Early phase improvement: {early_phase[0] - early_phase[-1]:.6f}")
    print(f"Mid phase improvement: {mid_phase[0] - mid_phase[-1]:.6f}")
    print(f"Late phase improvement: {late_phase[0] - late_phase[-1]:.6f}")
```

### Performance on Different Landscapes

```python
from evobench.algorithms import ABC
from evobench.benchmarks import sphere, ackley, trid

benchmarks = [
    ("sphere", sphere, [(-5, 5)] * 8),
    ("ackley", ackley, [(-32.768, 32.768)] * 8),
    ("trid", trid, [(-64, 64)] * 8)
]

print("ABC Performance Across Benchmark Functions")
print("-" * 50)

for name, func, bounds in benchmarks:
    results = []
    for _ in range(10):
        optimizer = ABC(func, bounds, max_iterations=300)
        _, best_fit = optimizer.run()
        results.append(best_fit)
    
    print(f"{name:12} | Mean: {np.mean(results):10.6f} | "
          f"Std: {np.std(results):10.6f} | Best: {np.min(results):10.6f}")
```

---

## Strengths & Weaknesses

### ✓ Strengths

| Advantage | Description |
|-----------|-------------|
| **Multimodal Robustness** | Three-phase mechanism escapes local optima effectively |
| **Balanced Search** | Employed+onlooker+scout naturally balance exploitation-exploration |
| **Simplicity** | Straightforward implementation, minimal hyperparameters |
| **Efficiency** | $O(n \cdot d)$ computational cost per iteration |
| **Robustness** | Works well across diverse function landscapes |
| **Exploration Power** | Scout phase systematically explores new regions |

### ✗ Weaknesses

| Limitation | Description |
|-----------|-------------|
| **Convergence Speed** | Generally slower than PSO on smooth landscapes |
| **Limited Exploitation** | Once solution found, refining it can be slow |
| **Parameter Tuning** | `limit` parameter requires problem-dependent tuning |
| **Trial Counter Logic** | Fixed limit may not adapt well to function difficulty |
| **Memory Usage** | Must track trial counters for all bees |

---

## Best Suited For

- ✓ **Multimodal optimization problems** (many local optima)
- ✓ **Complex, rugged landscapes**
- ✓ **Problems requiring robust global exploration**
- ✓ **When escaped from local optima is critical**
- ✓ **Applications where reliability matters more than convergence speed**

---

## Recommended Benchmark Functions

| Benchmark | Difficulty | Reason |
|-----------|-----------|--------|
| **Ackley** | High | Multimodal; tests exploration and escape capability |
| **Trid** | High | Multimodal-like structure; tests robustness |
| **Schwefel 1.2** | Medium | Difficult landscape; tests systematic search |

---

## Parameter Sensitivity Analysis

### Effect of `limit` on ABC Behavior

```python
from evobench.algorithms import ABC
from evobench.benchmarks import ackley
import matplotlib.pyplot as plt

bounds = [(-32.768, 32.768)] * 8
limit_values = [100, 500, 1000, 2000]

plt.figure(figsize=(12, 6))

for limit_val in limit_values:
    # NOTE: Current implementation uses fixed limit calculation
    # This example shows how limit affects behavior conceptually
    
    optimizer = ABC(ackley, bounds, max_iterations=300)
    _, best_fit = optimizer.run()
    
    # Run multiple times to get average curve
    curves = []
    for _ in range(5):
        opt = ABC(ackley, bounds, max_iterations=300)
        opt.run()
        curves.append(opt.fitness_history)
    
    avg_curve = np.mean(curves, axis=0)
    plt.semilogy(avg_curve, label=f'limit={limit_val}', linewidth=2)

plt.xlabel('Generation')
plt.ylabel('Best Fitness (log scale)')
plt.title('ABC: Effect of Abandonment Limit on Convergence')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

## Literature References

### Foundational Papers

1. **Karaboga, D. (2005).** "An Idea Based on Honey Bee Swarm for Numerical Optimization." *Technical Report, Erciyes University*.

2. **Karaboga, D., & Basturk, B. (2007).** "A powerful and efficient algorithm for numerical function optimization: artificial bee colony (ABC) algorithm." *Journal of Global Optimization*, 39(3), 459–471.

3. **Karaboga, D., & Akay, B. (2009).** "A comparative study of Artificial Bee Colony algorithm." *Applied Mathematics and Computation*, 214(1), 108–132.

### Variants & Extensions

- Gbest-guided ABC (GABC)
- Multi-objective ABC
- Hybrid ABC with differential evolution
- Adaptive ABC with dynamic limit

---

## Comparison with PSO and EDA

| Aspect | ABC | PSO | EDA |
|--------|-----|-----|-----|
| **Bee Phases** | 3 phases | Single attraction | Model-based |
| **Exploration** | Strong (scouts) | Moderate | Systematic |
| **Multimodal** | Excellent | Moderate | Moderate |
| **Unimodal** | Good | Excellent | Good |
| **Speed** | Moderate | Fast | Moderate |
| **Parameter Tuning** | Minimal | Moderate | Minimal |

---

## See Also

- [Algorithm Comparison](index.md)
- [Benchmark Functions](../benchmarks.md)
- [Statistical Analysis](../../theory/statistical-testing.md)
- [PSO Documentation](pso.md)
- [EDA Documentation](eda.md)
- [Base Class Documentation](../base.md)
