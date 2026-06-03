# Particle Swarm Optimization (PSO)

## Overview

**Particle Swarm Optimization** is a velocity-based swarm intelligence algorithm that simulates the collective behavior of bird flocking or fish schooling. Each particle (candidate solution) maintains its position in the search space and updates it through attraction to two attractors:

1. **Personal best** (`pbest`): The best solution the particle has found
2. **Global best** (`gbest`): The best solution found by the entire swarm

**Location**: `evobench.algorithms.PSO`

**Inspiration**: Social behavior of bird flocking (Reynolds, 1987)

**Key Characteristic**: Velocity-based updates combined with personal and social learning components

---

## Algorithm Characteristics

| Property | Value |
|----------|-------|
| **Population Type** | Continuous positions + velocities |
| **Update Mechanism** | Velocity-based |
| **Selection Strategy** | Best position memory + global best attraction |
| **Exploration Bias** | Moderate (early iterations) → Low (late iterations) |
| **Exploitation Bias** | High (early iterations) → Very High (late iterations) |
| **Computational Complexity** | $O(n \cdot d)$ per iteration (linear in population and dimension) |
| **Convergence Speed** | Fast on smooth landscapes |

---

## Mathematical Formulation

### Velocity Update Equation

$$v_i^{t+1} = w \cdot v_i^t + c_1 \cdot r_1 \cdot (pbest_i - x_i^t) + c_2 \cdot r_2 \cdot (gbest - x_i^t)$$

where:

- $v_i^t$: velocity of particle $i$ at iteration $t$
- $x_i^t$: position of particle $i$ at iteration $t$
- $w$: inertia weight (typically 0.4–0.9)
- $c_1$: cognitive parameter (typically 1.5–2.0)
- $c_2$: social parameter (typically 1.5–2.0)
- $r_1, r_2$: random values in $[0, 1]$ (independent samples)
- $pbest_i$: personal best position of particle $i$
- $gbest$: global best position across all particles

### Position Update Equation

$$x_i^{t+1} = x_i^t + v_i^{t+1}$$

### Boundary Handling

Positions are clipped to the search domain $[L_i, U_i]$ for each dimension $i$:

$$x_i^{t+1} = \text{clip}(x_i^{t+1}, L_i, U_i)$$

---

## Constructor

### Signature

```python
class PSO(EvolutionaryAlgorithm):
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
| `population_size` | `int` | 50 | Number of particles in the swarm |
| `max_iterations` | `int` | 100 | Maximum number of generations |

### Inherited Attributes

From `EvolutionaryAlgorithm`:

- `objective_function`: Reference to benchmark function
- `bounds`: Search space boundaries (converted to `np.ndarray`)
- `population_size`: Number of particles
- `max_iterations`: Iteration budget
- `dimension`: Problem dimensionality
- `best_individual`: Best solution found (updated throughout optimization)
- `best_fitness`: Fitness of best solution (initialized to `inf`)
- `fitness_history`: List of best fitness per generation

### PSO-Specific Attributes

```python
self.velocity: np.ndarray          # Shape (population_size, dimension)
                                   # Current velocity of each particle

self.pbest: np.ndarray             # Shape (population_size, dimension)
                                   # Personal best position of each particle

self.pbest_fitness: np.ndarray     # Shape (population_size,)
                                   # Fitness of each particle's personal best
```

---

## Hyperparameters

PSO's behavior is controlled by three main coefficients. The current implementation uses **fixed default values**:

### Default Configuration

```python
inertia_weight = 0.7          # w: Controls momentum (velocity retention)
cognitive_parameter = 1.5     # c1: Attraction to personal best
social_parameter = 1.5        # c2: Attraction to global best
```

### Effect on Behavior

- **Inertia Weight (`w`)**
  - Small values (~0.4): Encourages exploitation
  - Large values (~0.9): Encourages exploration
  - Default 0.7: Balanced mid-point

- **Cognitive Parameter (`c1`)**
  - Controls attraction to personal experience
  - Typical range: 1.5–2.0
  - Higher values = stronger individual memory

- **Social Parameter (`c2`)**
  - Controls attraction to swarm consensus
  - Typical range: 1.5–2.0
  - Higher values = stronger social pressure

### Velocity Clamping (Optional)

Some PSO implementations clamp velocity to avoid explosion. Current implementation does **not** clamp velocity but relies on boundary constraints of position.

---

## Algorithm Flow

### Pseudocode

```
Algorithm: PSO
Input: objective_function, bounds, population_size, max_iterations
Output: best_individual, best_fitness

1. Initialize population randomly within bounds
2. Initialize velocity to zero for all particles
3. Evaluate all particles (pbest ← population, pbest_fitness ← fitness)
4. Record global best (gbest)
5. 
6. For generation = 1 to max_iterations:
    7. For each particle i:
        8. Generate random r1, r2 ~ U(0,1)
        9. Update velocity: v_i ← w·v_i + c1·r1·(pbest_i - x_i) + c2·r2·(gbest - x_i)
        10. Update position: x_i ← x_i + v_i
        11. Apply boundary constraints: x_i ← clip(x_i, bounds)
    12. Evaluate new population
    13. Update pbest for particles with fitness improvement
    14. Update gbest if better solution found
    15. Record best fitness in fitness_history
16. 
17. Return best_individual, best_fitness
```

---

## Usage Examples

### Basic Optimization

```python
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

# Define search domain
bounds = [(-5, 5)] * 10

# Create PSO instance
optimizer = PSO(
    objective_function=sphere,
    bounds=bounds,
    population_size=30,
    max_iterations=200
)

# Run optimization
best_solution, best_fitness = optimizer.run()

print(f"Best Fitness: {best_fitness:.6f}")
print(f"Solution: {best_solution}")
print(f"Convergence Curve Length: {len(optimizer.fitness_history)}")
```

### Convergence Analysis

```python
import matplotlib.pyplot as plt
from evobench.algorithms import PSO
from evobench.benchmarks import rosenbrock

bounds = [(-2.048, 2.048)] * 5
optimizer = PSO(rosenbrock, bounds, max_iterations=500)

best_sol, best_fit = optimizer.run()

# Plot convergence
plt.figure(figsize=(10, 6))
plt.semilogy(optimizer.fitness_history, 'b-', linewidth=2)
plt.xlabel('Generation')
plt.ylabel('Best Fitness (log scale)')
plt.title('PSO Convergence on Rosenbrock Function')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('pso_convergence.png')
plt.show()
```

### Multiple Runs with Statistical Analysis

```python
import numpy as np
from evobench.algorithms import PSO
from evobench.benchmarks import ackley
from evobench.stats import analyze, stat_report

bounds = [(-32.768, 32.768)] * 8
num_runs = 30

results = []
for run in range(num_runs):
    optimizer = PSO(ackley, bounds, max_iterations=500)
    _, best_fit = optimizer.run()
    results.append(best_fit)

# Descriptive statistics
print(f"Mean: {np.mean(results):.6f}")
print(f"Std:  {np.std(results):.6f}")
print(f"Best: {np.min(results):.6f}")
print(f"Worst: {np.max(results):.6f}")
```

### Comparative Study

```python
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere
from evobench.stats import analyze, stat_report

bounds = [(-5, 5)] * 10

algorithms = [
    (PSO, "PSO"),
    (EDA, "EDA"),
    (ABC, "ABC")
]

results_list = []
algo_names = []

for AlgoClass, name in algorithms:
    results = [AlgoClass(sphere, bounds).run()[1] for _ in range(30)]
    results_list.append(results)
    algo_names.append(name)

analysis = analyze(
    func_name="sphere",
    result_list=results_list,
    algorithm_names=algo_names,
    alpha=0.05
)

print(stat_report(analysis))
```

---

## Strengths & Weaknesses

### ✓ Strengths

| Advantage | Description |
|-----------|-------------|
| **Fast Convergence** | Often finds good solutions quickly on smooth landscapes |
| **Simplicity** | Straightforward implementation, few hyperparameters |
| **Robustness** | Works well across diverse benchmark functions |
| **Efficiency** | Linear computational cost per iteration |
| **Memory Efficient** | Only stores position and velocity (no large matrices) |

### ✗ Weaknesses

| Limitation | Description |
|-----------|-------------|
| **Premature Convergence** | May converge to local optima on multimodal landscapes |
| **Flat Regions** | Struggles with plateaus (flat fitness regions) |
| **Parameter Sensitivity** | Performance depends on inertia weight and acceleration coefficients |
| **Stagnation** | Swarm can become stuck if particles cluster around local optimum |
| **Limited Memory** | No long-term learning; particles are attracted only to recent best positions |

---

## Best Suited For

- ✓ **Smooth, continuous optimization problems**
- ✓ **Unimodal or weakly multimodal landscapes**
- ✓ **Problems requiring fast initial convergence**
- ✓ **High-dimensional optimization (dimension ≥ 20)**
- ✓ **Real-time or resource-constrained applications**

---

## Recommended Benchmark Functions

| Benchmark | Difficulty | Reason |
|-----------|-----------|--------|
| **Sphere** | Very Low | Simple validation; PSO converges easily |
| **Rosenbrock** | Medium-High | Tests valley navigation; convergence in narrow valley |
| **Ackley** | High | Tests global exploration; many local minima |

---

## Literature References

### Foundational Papers

1. **Kennedy, J., & Eberhart, R. (1995).** "Particle Swarm Optimization." *Proceedings of ICNN'95*, Perth, Australia, pp. 1942–1948.

2. **Shi, Y., & Eberhart, R. C. (1998).** "A Modified Particle Swarm Optimizer." *Proceedings of CEC 1998*, pp. 69–73.

3. **Clerc, M., & Kennedy, J. (2002).** "The Particle Swarm - Explosion, Stability, and Convergence in a Multidimensional Complex Space." *IEEE Transactions on Evolutionary Computation*, 6(1), 58–73.

### Variants & Extensions

- Constriction Coefficient PSO (Clerc & Kennedy, 2002)
- Adaptive PSO (Zhu et al., 2011)
- Multi-swarm PSO (Blackwell & Branke, 2006)

---

## See Also

- [Algorithm Comparison](index.md)
- [Benchmark Functions](../benchmarks.md)
- [Statistical Analysis](../../theory/statistical-testing.md)
- [Base Class Documentation](../base.md)
- [Custom Algorithm Guide](../../guide/custom-algorithms.md)
