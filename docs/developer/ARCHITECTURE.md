# Architecture and Design Patterns

This document describes the architectural decisions, design patterns, and engineering principles behind evobench. Understanding this document is essential for contributors and advanced users who want to extend the library.

---

## Table of Contents

1. [Project Philosophy](#project-philosophy)
2. [Modular Architecture](#modular-architecture)
3. [Design Patterns](#design-patterns)
4. [Core Components](#core-components)
5. [Extensibility](#extensibility)
6. [Performance Considerations](#performance-considerations)

---

## Project Philosophy

evobench is built on three core principles:

### 1. **Scientific Rigor**
Every component follows evidence-based evolutionary computation principles. The library enforces:
- **Standardized protocols**: Reproducible, documented experiment workflows
- **Statistical validity**: Built-in hypothesis testing and effect size calculation
- **Transparent implementation**: All algorithms expose their hyperparameters; no magic

### 2. **User-Centric Simplicity**
Despite scientific rigor, the API is intuitive:
- **Minimal boilerplate**: Optimize in 5 lines of Python
- **Sensible defaults**: Hyperparameters chosen for robustness, not obscurity
- **Progressive disclosure**: Basic usage is simple; advanced features are discoverable

### 3. **Extensibility-First Design**
The library anticipates customization:
- **Abstract base classes**: Easy to implement new algorithms
- **Plugin registry**: Add benchmarks without modifying core code
- **Composable tools**: Mix and match statistical tests, operators, utilities

---

## Modular Architecture

```
evobench/
├── algorithms/          # Population-based optimizers (PSO, EDA, ABC)
├── benchmarks/          # Test functions (Sphere, Rosenbrock, Ackley, Schwefel, Trid)
├── stats/               # Statistical analysis (hypothesis testing, post-hoc analysis)
├── tools/               # Utilities (experiment orchestration, operators, plotting)
├── base.py              # Abstract base class (EvolutionaryAlgorithm)
└── __init__.py          # Public API (Facade)
```

### Design Rationale

**Why separate modules instead of monolithic file?**

1. **Clarity**: Each module has a single responsibility
2. **Scalability**: Easy to add new algorithms or benchmarks
3. **Testing**: Each module can be tested independently
4. **Import efficiency**: Users only load what they need

**Why use subpackages instead of single files?**

```python
# ✓ Subpackage approach (current)
from evobench.benchmarks import sphere
from evobench.algorithms import PSO

# ✗ Monolithic approach (abandoned)
from evobench import benchmarks, algorithms  # Forces loading everything
```

---

## Design Patterns

### Pattern 1: Facade API

**Purpose**: Provide a clean, intuitive public interface while hiding implementation complexity.

**Implementation**:

```python
# src/evobench/__init__.py (root Facade)
from .algorithms import PSO, EDA, ABC
from .benchmarks import sphere, rosenbrock, ackley, schwefel, trid, get_benchmark
from .stats import analyze, stat_report

__all__ = ["PSO", "EDA", "ABC", "sphere", "rosenbrock", ...]
```

**Benefit**: Users see only the public API:
```python
# What users import (clean)
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

# What they don't see (internal)
# from evobench.algorithms.pso import ParticleSwarmOptimization  ← Hidden
# from evobench.benchmarks.unimodal import sphere_function       ← Hidden
```

**Example**:

```python
from evobench import PSO, sphere  # Clean and professional

# vs.

from evobench.algorithms.pso import ParticleSwarmOptimization  # Verbose
from evobench.benchmarks.unimodal import sphere_function       # Internal names leak
```

### Pattern 2: Registry Pattern for Benchmarks

**Purpose**: Allow dynamic discovery and instantiation of benchmark functions without polluting the namespace.

**Implementation**:

```python
# src/evobench/benchmarks/__init__.py
from .unimodal import sphere_function as sphere
from .multimodal import ackley_function as ackley

# Central registry (single source of truth)
BENCHMARK_REGISTRY = {
    "sphere": sphere,
    "rosenbrock": rosenbrock,
    "ackley": ackley,
    "schwefel 1.2": schwefel,
    "trid": trid
}

def get_benchmark(name: str):
    """Retrieve benchmark by name."""
    search_name = name.lower()
    if search_name not in BENCHMARK_REGISTRY:
        raise ValueError(f"Benchmark '{name}' is not implemented.")
    return BENCHMARK_REGISTRY[search_name]
```

**Why Registry Pattern?**

```python
# ✗ Without registry: Must know all function names
from evobench.benchmarks import sphere, rosenbrock, ackley, schwefel, trid

# ✓ With registry: Dynamic lookup
from evobench.benchmarks import get_benchmark, BENCHMARK_REGISTRY

# Programmatic access
for name in BENCHMARK_REGISTRY:
    func = get_benchmark(name)
    # Process dynamically

# Configuration-driven access
config = {"benchmark": "ackley"}
func = get_benchmark(config["benchmark"])  # No hardcoding!
```

**Extensibility**:

To add a new benchmark without modifying core code:

```python
# User's custom_benchmarks.py
from evobench.benchmarks import BENCHMARK_REGISTRY

def my_benchmark(x):
    """Custom optimization landscape."""
    return sum(x**2) + 10 * sum(np.sin(x))

# Register it
BENCHMARK_REGISTRY["my_benchmark"] = my_benchmark

# Now use it
from evobench.benchmarks import get_benchmark
func = get_benchmark("my_benchmark")
```

### Pattern 3: Abstract Base Class for Algorithms

**Purpose**: Enforce a uniform interface across all algorithms while allowing algorithmic freedom.

**Implementation**:

```python
# src/evobench/base.py
from abc import ABC, abstractmethod

class EvolutionaryAlgorithm(ABC):
    """
    Abstract base class defining the contract for all population-based
    evolutionary algorithms in evobench.
    """
    
    def __init__(self, objective_function, bounds, population_size=50, max_iterations=100):
        """Standard initialization contract."""
        self.objective_function = objective_function
        self.bounds = np.array(bounds)
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.dimension = len(self.bounds)
        self.best_individual = None
        self.best_fitness = float('inf')
        self.fitness_history = []
    
    @abstractmethod
    def run(self) -> Tuple[np.ndarray, float]:
        """
        Execute the optimization loop.
        
        Must return:
            - best_individual: shape (dimension,)
            - best_fitness: scalar float
        """
        pass
    
    def _initialize_population(self) -> np.ndarray:
        """Standard population initialization."""
        lower = self.bounds[:, 0]
        upper = self.bounds[:, 1]
        return np.random.uniform(lower, upper, (self.population_size, self.dimension))
```

**Inheritance Contract**:

```python
class MyCustomAlgorithm(EvolutionaryAlgorithm):
    """Implement your own optimizer."""
    
    def __init__(self, objective_function, bounds, population_size=50, 
                 max_iterations=100, my_param=0.5):
        super().__init__(objective_function, bounds, population_size, max_iterations)
        self.my_param = my_param
    
    def run(self) -> Tuple[np.ndarray, float]:
        """Implement core algorithm logic."""
        # Use inherited attributes
        # self.objective_function
        # self.bounds
        # self.population_size
        # self.max_iterations
        # self.fitness_history
        
        population = self._initialize_population()
        
        for iteration in range(self.max_iterations):
            # Algorithm-specific logic
            fitness = np.apply_along_axis(self.objective_function, 1, population)
            
            # Track best (inherited pattern)
            best_idx = np.argmin(fitness)
            if fitness[best_idx] < self.best_fitness:
                self.best_fitness = fitness[best_idx]
                self.best_individual = population[best_idx].copy()
            
            self.fitness_history.append(self.best_fitness)
            
            # Population update (algorithm-specific)
            population = self._update_population(population, fitness)
        
        return self.best_individual, self.best_fitness
    
    def _update_population(self, population, fitness):
        """Algorithm-specific update rule."""
        # Implementation here
        return population
```

**Benefits of ABC Pattern**:
- ✓ Enforces consistent interface
- ✓ `fitness_history` tracking guaranteed
- ✓ Users know what to expect from any algorithm
- ✓ Enables algorithm swapping in experiments

---

## Core Components

### Component 1: EvolutionaryAlgorithm Base Class

**Location**: `src/evobench/base.py`

**Responsibility**: Define the contract for all algorithms.

**Key Methods**:
- `__init__()`: Initialize hyperparameters and state
- `run()`: Execute optimization (abstract; must be implemented)
- `_initialize_population()`: Standard uniform initialization
- `_apply_boundary_constraints()`: Optional boundary handling

**State Tracking**:
```python
class EvolutionaryAlgorithm(ABC):
    # Tracked throughout optimization
    best_individual: np.ndarray          # Best solution found
    best_fitness: float                  # Fitness of best solution
    fitness_history: List[float]         # Best fitness per generation
```

### Component 2: Algorithms Package

**Location**: `src/evobench/algorithms/`

**Implementations**:
- **PSO** (`pso.py`): Particle Swarm Optimization
  - Velocity-based updates
  - Personal best + global best attraction
  - Inertia weight, cognitive/social coefficients tunable

- **EDA** (`eda.py`): Estimation of Distribution Algorithm
  - Probabilistic model-based search
  - Gaussian distribution estimation
  - Selection ratio tunable

- **ABC** (`bee.py`): Artificial Bee Colony
  - Three-phase (employed, onlooker, scout)
  - Trial-counter mechanism
  - Limit parameter (abandonment threshold) tunable

**Common Pattern**:
```python
class ParticleSwarmOptimization(EvolutionaryAlgorithm):
    def __init__(self, objective_function, bounds, 
                 population_size=50, max_iterations=100,
                 inertia_weight=0.7, cognitive_constant=1.5, social_constant=1.5):
        super().__init__(...)
        # Algorithm-specific hyperparameters
        self.w = inertia_weight
        self.c1 = cognitive_constant
        self.c2 = social_constant
    
    def run(self) -> Tuple[np.ndarray, float]:
        # Implement PSO loop
        pass
```

### Component 3: Benchmarks Package

**Location**: `src/evobench/benchmarks/`

**Organization**:
- `unimodal.py`: Single-optimum functions (Sphere, Rosenbrock, Schwefel 1.2, Trid)
- `multimodal.py`: Multiple local optima (Ackley)
- `__init__.py`: Registry, `get_benchmark()` utility, aliases

**Function Signature Convention**:
```python
def sphere_function(x: np.ndarray) -> float:
    """
    Vectorized Sphere function.
    
    Args:
        x: Candidate solution (shape: (dimension,))
    
    Returns:
        Fitness value (scalar float)
    """
    return float(np.sum(x**2))
```

**Why Vectorization Matters**:
```python
# ✗ Slow: Loop-based (element-wise operations)
def sphere_slow(x):
    total = 0.0
    for xi in x:
        total += xi**2
    return total

# ✓ Fast: NumPy vectorized
def sphere_fast(x):
    return float(np.sum(x**2))

# Speed comparison on x with 10000 dimensions:
# sphere_slow:  ~1000 μs
# sphere_fast:  ~10 μs (100× faster!)
```

### Component 4: Statistics Package

**Location**: `src/evobench/stats/`

**Organization**:
- `core_tests.py`: Normality tests (Shapiro-Wilk), parametric/non-parametric tests
- `analyzer.py`: Orchestrate statistical analysis workflow
- `reporter.py`: Colored ANSI output with significance indicators
- `post_hoc.py`: Pairwise comparisons (Tukey, Dunn)

**Workflow**:
```python
from evobench.stats import analyze

# Input: Fitness vectors from multiple algorithms
fitness_data = [
    np.array([1.2, 1.1, 1.3, 1.15, 1.25]),  # PSO runs
    np.array([0.9, 0.95, 0.88, 0.92, 0.87])  # EDA runs
]

# Automatic decision flow:
# 1. Check normality (Shapiro-Wilk)
# 2. If normal: ANOVA; else: Kruskal-Wallis
# 3. If significant: Post-hoc (Tukey or Dunn)
# 4. Calculate effect size (Cohen's d)
result = analyze("Sphere", fitness_data, ["PSO", "EDA"])
```

### Component 5: Tools Package

**Location**: `src/evobench/tools/`

**Modules**:
- `experiment_engine.py`: Orchestrate multi-algorithm, multi-benchmark studies
- `operators.py`: Tournament selection, mutation operators (reusable)
- `plotter.py`: Visualization utilities (convergence curves)

**Experiment Engine**:
```python
from evobench.tools import run_automated_experiment

config = {
    "dimensions": 10,
    "population_size": 50,
    "max_iterations": 100,
    "independent_runs": 20,
    "benchmarks": [...],
    "algorithms": [...]
}

run_automated_experiment(config, output_file="results.json")
# Produces:
# - JSON with all results
# - System metadata (for reproducibility)
# - Timing information
```

---

## Extensibility

### Extending the Library

#### Scenario 1: Add a New Algorithm

```python
# my_algorithm.py
import numpy as np
from evobench.base import EvolutionaryAlgorithm

class DifferentialEvolution(EvolutionaryAlgorithm):
    """Differential Evolution for continuous optimization."""
    
    def __init__(self, objective_function, bounds, 
                 population_size=50, max_iterations=100,
                 F=0.8, CR=0.9):
        super().__init__(objective_function, bounds, population_size, max_iterations)
        self.F = F    # Mutation scale
        self.CR = CR  # Crossover rate
    
    def run(self):
        population = self._initialize_population()
        
        for generation in range(self.max_iterations):
            fitness = np.apply_along_axis(self.objective_function, 1, population)
            
            # DE mutation and crossover logic
            # ...
            
            # Track best
            best_idx = np.argmin(fitness)
            if fitness[best_idx] < self.best_fitness:
                self.best_fitness = fitness[best_idx]
                self.best_individual = population[best_idx].copy()
            
            self.fitness_history.append(self.best_fitness)
        
        return self.best_individual, self.best_fitness

# Use it immediately
from evobench.benchmarks import sphere
bounds = [(-5, 5)] * 10
de = DifferentialEvolution(sphere, bounds, F=0.8, CR=0.9)
best_sol, best_fit = de.run()
```

#### Scenario 2: Add a New Benchmark

```python
# custom_benchmarks.py
import numpy as np
from evobench.benchmarks import BENCHMARK_REGISTRY

def levy_function(x):
    """Lévy function: difficult multimodal landscape."""
    d = len(x)
    w = 1 + (x - 1) / 4
    
    term1 = np.sin(np.pi * w[0])**2
    term2 = np.sum((w[:-1] - 1)**2 * (1 + 10 * np.sin(np.pi * w[:-1] + 1)**2))
    term3 = (w[-1] - 1)**2 * (1 + np.sin(2 * np.pi * w[-1])**2)
    
    return term1 + term2 + term3

# Register it
BENCHMARK_REGISTRY["levy"] = levy_function

# Use it
from evobench.benchmarks import get_benchmark
from evobench.algorithms import PSO

levy = get_benchmark("levy")
bounds = [(-10, 10)] * 10
optimizer = PSO(levy, bounds)
best_solution, best_fitness = optimizer.run()
```

#### Scenario 3: Use Custom Operators

```python
# custom_operators.py
import numpy as np
from evobench.tools.operators import tournament_selection

def rank_selection(population, fitness, rank_pressure=2.0):
    """Rank-based selection (alternative to tournament)."""
    n = len(fitness)
    ranks = np.argsort(np.argsort(fitness))  # Lower fitness → higher rank
    
    # Exponential rank pressure
    weights = np.exp(-rank_pressure * (n - 1 - ranks) / n)
    weights /= np.sum(weights)
    
    idx = np.random.choice(n, p=weights)
    return population[idx].copy()

# Use in custom algorithm
from evobench.base import EvolutionaryAlgorithm

class CustomGA(EvolutionaryAlgorithm):
    def run(self):
        population = self._initialize_population()
        
        for gen in range(self.max_iterations):
            fitness = np.apply_along_axis(self.objective_function, 1, population)
            
            # Use custom selection
            new_pop = []
            for _ in range(self.population_size):
                parent = rank_selection(population, fitness)
                new_pop.append(parent)
            
            population = np.array(new_pop)
            
            # Track best
            best_idx = np.argmin(fitness)
            if fitness[best_idx] < self.best_fitness:
                self.best_fitness = fitness[best_idx]
                self.best_individual = population[best_idx].copy()
            
            self.fitness_history.append(self.best_fitness)
        
        return self.best_individual, self.best_fitness
```

---

## Performance Considerations

### NumPy Vectorization

All evobench algorithms rely on NumPy vectorization for speed:

```python
# Population: shape (population_size, dimension)
population = np.random.rand(100, 50)  # 100 individuals, 50 dimensions

# ✓ Vectorized (fast)
fitness = np.apply_along_axis(sphere, 1, population)  # O(n*d)
# vs.
fitness = np.array([sphere(p) for p in population])   # Same speed but simpler

# ✓ Vectorized operations
population += 0.1 * best_solution  # Update all at once

# ✗ Loop-based (slow, avoid)
for i in range(len(population)):
    fitness[i] = sphere(population[i])
```

### Memory Efficiency

```python
# Problem: High-dimensional, large population
DIMENSION = 10000
POPULATION_SIZE = 1000

# Memory footprint: 10000 × 1000 × 8 bytes = 80 MB per generation
# For 100 iterations: 8 GB (problematic)

# Solution: Batch processing or reduce population
POPULATION_SIZE = 100  # 8 MB per generation; 800 MB for 100 iterations ✓

# Or: Streaming evaluation (no history)
for iteration in range(max_iterations):
    fitness = np.apply_along_axis(objective_function, 1, population)
    # Process and discard fitness values (don't accumulate)
```

### Reproducibility via Seeding

```python
import numpy as np
from numpy.random import Generator, PCG64

# Modern NumPy API (3.9+)
rng = Generator(PCG64(seed=42))

# Use rng instead of np.random
population = rng.uniform(-5, 5, (population_size, dimension))
indices = rng.choice(population_size, size=tournament_size, replace=False)

# Old API (still works but deprecated)
# np.random.seed(42)
# population = np.random.uniform(...)
```

---

## Testing Architecture

```
tests/
├── test_base.py          # Tests for EvolutionaryAlgorithm contract
├── test_algorithms.py    # PSO, EDA, ABC correctness
├── test_benchmarks.py    # Benchmark properties (optima, bounds)
├── test_statistics.py    # Statistical analysis accuracy
└── test_integration.py   # End-to-end workflows
```

**Testing Principles**:
1. Unit tests for each component
2. Integration tests for workflows
3. Property-based tests (e.g., fitness always improves or stays same)
4. Regression tests for known solutions

---

## Future Extensibility

**Planned (v0.2.0+)**:
- Discrete optimization algorithms (GA for binary/categorical problems)
- Multi-objective optimization (NSGA-II, MOEA/D)
- Hybrid algorithms (Local search + global optimization)
- Parallel execution (Thread pool, multiprocessing, Ray)
- Custom metrics and logging

---

**Document Version**: 1.0  
**Last Updated**: June 2026  
**evobench**: 0.1.0
