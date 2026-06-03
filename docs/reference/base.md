# EvolutionaryAlgorithm Base Class

## Overview

`EvolutionaryAlgorithm` is an abstract base class that defines the standard interface and contract for all population-based evolutionary algorithms and metaheuristics in evobench.

**Location**: `evobench.base.EvolutionaryAlgorithm`

**Purpose**: Enforce a uniform architectural pattern across all implementations, ensuring:

- Consistent initialization protocols
- Standardized state tracking throughout optimization
- Interchangeable algorithms for rigorous comparative evaluation
- Clear separation between algorithm-specific and shared functionality

---

## Class Definition

```python
from abc import ABC, abstractmethod
import numpy as np
from typing import Callable, List, Tuple

class EvolutionaryAlgorithm(ABC):
    """
    Abstract base class for population-based evolutionary algorithms.
    
    Defines the minimal contract that all evolutionary metaheuristics must
    satisfy for integration into evobench's benchmarking framework.
    """
```

---

## Constructor

### Signature

```python
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
| `objective_function` | `Callable[[np.ndarray], float]` | **Required** | The continuous optimization function to be minimized. Must accept an `np.ndarray` of shape `(dimensions,)` and return a scalar float fitness value. |
| `bounds` | `List[Tuple[float, float]]` | **Required** | Search domain boundaries. List of `(lower, upper)` tuples defining $[L_i, U_i]$ for each dimension $i$. Shape after conversion: `(n_dimensions, 2)`. |
| `population_size` | `int` | 50 | Number of candidate solutions maintained per generation. Controls memory usage and population diversity. Must be $\geq 2$. |
| `max_iterations` | `int` | 100 | Maximum number of evolutionary cycles before termination. Sets computational budget for optimization. Must be $\geq 1$. |

### Example

```python
from evobench.base import EvolutionaryAlgorithm
from evobench.benchmarks import sphere

# Define 10-dimensional continuous optimization problem
bounds = [(-5, 5)] * 10

# Create a hypothetical PSO instance (concrete subclass)
class MyAlgorithm(EvolutionaryAlgorithm):
    def run(self):
        # Implementation here
        pass

optimizer = MyAlgorithm(
    objective_function=sphere,
    bounds=bounds,
    population_size=30,
    max_iterations=200
)
```

---

## Attributes

### Instance Attributes

| Attribute | Type | Access | Description |
|-----------|------|--------|-------------|
| `objective_function` | `Callable` | Read-only | Reference to the benchmark function being optimized. |
| `bounds` | `np.ndarray` | Read-only | Search space boundaries converted to numpy array of shape `(dimension, 2)`. |
| `population_size` | `int` | Read-only | Number of individuals per generation. |
| `max_iterations` | `int` | Read-only | Iteration budget. |
| `dimension` | `int` | Read-only | Problem dimensionality (rows of `bounds`). |
| `best_individual` | `np.ndarray` or `None` | Read/Write | Best solution found so far. Shape: `(dimension,)`. Initially `None`. |
| `best_fitness` | `float` | Read/Write | Fitness value of `best_individual`. Initialized to `float('inf')`. |
| `fitness_history` | `List[float]` | Read/Write | List of best fitness values recorded at each generation. Length: `0` to `max_iterations`. |

### Property Access Example

```python
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

bounds = [(-5, 5)] * 10
optimizer = PSO(sphere, bounds)

# Before running
print(f"Dimension: {optimizer.dimension}")  # Output: 10
print(f"Best Fitness: {optimizer.best_fitness}")  # Output: inf
print(f"History Length: {len(optimizer.fitness_history)}")  # Output: 0

# Run optimization
best_sol, best_fit = optimizer.run()

# After running
print(f"Best Fitness: {optimizer.best_fitness}")
print(f"History Length: {len(optimizer.fitness_history)}")  # Output: 100 (max_iterations)
```

---

## Abstract Methods

### `run()`

The core algorithm loop. Every subclass **must** implement this method.

#### Signature

```python
@abstractmethod
def run(self) -> Tuple[np.ndarray, float]
```

#### Returns

| Element | Type | Description |
|---------|------|-------------|
| Best Solution | `np.ndarray` | Optimal candidate found, shape `(dimension,)`. All values should satisfy bounds. |
| Best Fitness | `float` | Fitness value at the best solution. Must be a scalar (not NaN). |

#### Contract & Responsibilities

When implementing `run()`, your subclass must:

1. **Initialize population**: Generate initial candidate solutions within bounds
2. **Maintain state**: Update `best_individual` and `best_fitness` throughout iterations
3. **Record history**: Append best fitness value to `fitness_history` each generation
4. **Respect bounds**: All population members must remain within `[L_i, U_i]` for each dimension
5. **Iterate**: Run for exactly `max_iterations` generations (unless early stopping is explicitly documented)
6. **Return results**: Return tuple of `(best_individual, best_fitness)` at termination

#### Implementation Template

```python
from evobench.base import EvolutionaryAlgorithm
import numpy as np

class MyMetaheuristic(EvolutionaryAlgorithm):
    """
    Custom evolutionary algorithm inheriting from EvolutionaryAlgorithm.
    """
    
    def __init__(self, objective_function, bounds, population_size=50,
                 max_iterations=100):
        super().__init__(objective_function, bounds, population_size, max_iterations)
        # Initialize algorithm-specific parameters here
    
    def run(self):
        """Execute the algorithm."""
        
        # Step 1: Initialize population
        population = self._initialize_population()
        
        # Step 2: Evaluate initial population
        fitness = np.array([self.objective_function(ind) for ind in population])
        
        # Step 3: Main evolutionary loop
        for generation in range(self.max_iterations):
            # Update best solution
            best_idx = np.argmin(fitness)
            if fitness[best_idx] < self.best_fitness:
                self.best_fitness = fitness[best_idx]
                self.best_individual = population[best_idx].copy()
            
            # Record history
            self.fitness_history.append(self.best_fitness)
            
            # Algorithm-specific variation and selection
            population = self._selection_operation(population, fitness)
            population = self._variation_operation(population)
            population = self._apply_boundary_constraints(population)
            
            # Re-evaluate population
            fitness = np.array([self.objective_function(ind) for ind in population])
        
        return self.best_individual, self.best_fitness
    
    def _initialize_population(self):
        """Generate random population within bounds."""
        population = np.zeros((self.population_size, self.dimension))
        for i in range(self.dimension):
            lower, upper = self.bounds[i]
            population[:, i] = np.random.uniform(lower, upper, self.population_size)
        return population
    
    def _apply_boundary_constraints(self, population):
        """Clip population to stay within bounds."""
        for i in range(self.dimension):
            lower, upper = self.bounds[i]
            population[:, i] = np.clip(population[:, i], lower, upper)
        return population
```

---

## Helper Methods

While not abstract, the following methods are commonly used by subclasses:

### `_apply_boundary_constraints(population)`

Ensures all individuals remain within the search domain.

```python
def _apply_boundary_constraints(self, population: np.ndarray) -> np.ndarray:
    """
    Clip population members to satisfy bounds.
    
    Args:
        population: Array of shape (population_size, dimension)
    
    Returns:
        Clipped population array
    """
    for i in range(self.dimension):
        lower, upper = self.bounds[i]
        population[:, i] = np.clip(population[:, i], lower, upper)
    return population
```

---

## Complete Algorithm Example

Here is a minimal but complete implementation of PSO as a concrete subclass:

```python
from evobench.base import EvolutionaryAlgorithm
import numpy as np
from typing import Tuple

class SimplePSO(EvolutionaryAlgorithm):
    """
    Simplified Particle Swarm Optimization for demonstration.
    """
    
    def __init__(self, objective_function, bounds, population_size=50,
                 max_iterations=100, w=0.7, c1=1.5, c2=1.5):
        super().__init__(objective_function, bounds, population_size, max_iterations)
        self.w = w      # Inertia weight
        self.c1 = c1    # Cognitive parameter
        self.c2 = c2    # Social parameter
        self.velocity = None
        self.pbest = None
        self.pbest_fitness = None
    
    def run(self) -> Tuple[np.ndarray, float]:
        # Initialize position and velocity
        population = np.random.uniform(
            [b[0] for b in self.bounds],
            [b[1] for b in self.bounds],
            (self.population_size, self.dimension)
        )
        
        self.velocity = np.zeros_like(population)
        fitness = np.array([self.objective_function(ind) for ind in population])
        
        self.pbest = population.copy()
        self.pbest_fitness = fitness.copy()
        
        # Main loop
        for generation in range(self.max_iterations):
            # Update global best
            best_idx = np.argmin(self.pbest_fitness)
            gbest = self.pbest[best_idx].copy()
            gbest_fitness = self.pbest_fitness[best_idx]
            
            if gbest_fitness < self.best_fitness:
                self.best_fitness = gbest_fitness
                self.best_individual = gbest.copy()
            
            self.fitness_history.append(self.best_fitness)
            
            # Update velocity and position
            r1 = np.random.random((self.population_size, self.dimension))
            r2 = np.random.random((self.population_size, self.dimension))
            
            self.velocity = (self.w * self.velocity +
                           self.c1 * r1 * (self.pbest - population) +
                           self.c2 * r2 * (gbest - population))
            
            population = population + self.velocity
            population = self._apply_boundary_constraints(population)
            
            # Evaluate new population
            fitness = np.array([self.objective_function(ind) for ind in population])
            
            # Update personal best
            improved = fitness < self.pbest_fitness
            self.pbest[improved] = population[improved]
            self.pbest_fitness[improved] = fitness[improved]
        
        return self.best_individual, self.best_fitness
```

---

## Design Principles

### 1. **Single Responsibility**

The base class handles:
- Initialization validation
- State tracking (`best_individual`, `best_fitness`, `fitness_history`)
- Dimension calculation from bounds

Subclasses handle:
- Algorithm-specific variation operators (mutation, crossover, velocity updates)
- Problem-specific initialization if needed

### 2. **Flexibility**

Subclasses can:
- Add algorithm-specific hyperparameters
- Override boundary constraint strategies
- Implement custom termination criteria

### 3. **Type Safety**

All public interfaces use type hints (PEP 484):

```python
def __init__(self, objective_function: Callable[[np.ndarray], float], ...) -> None
```

### 4. **Reproducibility**

State is fully captured in instance attributes, allowing:
- Serialization of algorithm state
- Restart from checkpoints
- Parallel independent runs

---

## Common Pitfalls

### ❌ Don't

```python
# WRONG: Modifying bounds after creation
optimizer = PSO(sphere, bounds)
optimizer.bounds[0] = (0, 10)  # Will cause issues

# WRONG: Not updating fitness_history
def run(self):
    # ... missing self.fitness_history.append(...)
    pass

# WRONG: Returning NaN or inf
return best_individual, float('nan')  # Invalid
```

### ✓ Do

```python
# CORRECT: Respecting immutable state
bounds = [(-5, 5)] * 10
optimizer = PSO(sphere, bounds)
# bounds is set once, not modified

# CORRECT: Always updating history
def run(self):
    for gen in range(self.max_iterations):
        # ... evaluation ...
        self.fitness_history.append(self.best_fitness)

# CORRECT: Valid fitness values
return best_individual, 1.234  # finite float
```

---

## See Also

- [PSO Implementation](algorithms/pso.md)
- [EDA Implementation](algorithms/eda.md)
- [ABC Implementation](algorithms/abc.md)
- [Custom Algorithms Guide](../guide/custom-algorithms.md)
