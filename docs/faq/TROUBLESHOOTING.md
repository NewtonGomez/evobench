# Troubleshooting Guide

This document provides solutions to common issues encountered when using evobench. If you encounter a problem not listed here, please open an issue on [GitHub](https://github.com/NewtonGomez/evobench/issues).

---

## Import Errors

### Error: `ImportError: cannot import name 'PSO' from 'evobench'`

**Problem**: Attempting to import algorithms from the root package fails:
```python
from evobench import PSO  # ❌ ImportError
```

**Root Cause**: The Facade API in the root `__init__.py` must be properly configured to expose public APIs.

**Solution**: Import from subpackages instead:
```python
# ✅ Correct: Import from subpackages
from evobench.algorithms import PSO
from evobench.benchmarks import sphere
from evobench.stats import analyze

# ✅ Also works: Import from root (if __init__.py is configured)
# from evobench import PSO, sphere, analyze
```

**Verification**:
```bash
python -c "from evobench.algorithms import PSO; print('Import successful')"
```

**Permanent Fix** (for package maintainers): Ensure `src/evobench/__init__.py` contains:
```python
from .algorithms import PSO, EDA, ABC
from .benchmarks import sphere, rosenbrock, ackley, schwefel, trid, get_benchmark, BENCHMARK_REGISTRY
from .stats import analyze, stat_report
from .base import EvolutionaryAlgorithm

__all__ = [
    "PSO", "EDA", "ABC",
    "sphere", "rosenbrock", "ackley", "schwefel", "trid", "get_benchmark", "BENCHMARK_REGISTRY",
    "analyze", "stat_report",
    "EvolutionaryAlgorithm",
]
```

---

### Error: `ModuleNotFoundError: No module named 'evobench'`

**Problem**: evobench is not installed in your Python environment.

**Solution**: Install evobench:
```bash
# From PyPI (recommended)
pip install evobench

# From source (for development)
git clone https://github.com/NewtonGomez/evobench.git
cd evobench
pip install -e .

# With development dependencies
pip install -e ".[dev]"
```

**Verify Installation**:
```bash
python -c "import evobench; print(evobench.__version__)"
```

---

## Type Errors

### Error: `TypeError: __init__() got an unexpected keyword argument 'inertia_weight'`

**Problem**: Attempting to customize PSO's hyperparameters using keyword arguments that the documentation claims exist but aren't recognized:
```python
pso = PSO(sphere, bounds, inertia_weight=0.9)  # ❌ TypeError
```

**Root Cause**: PSO constructor signature may be undocumented or incorrect.

**Solution**: Check the PSO constructor accepts these parameters. Use explicit parameters:
```python
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

bounds = [(-5, 5)] * 10

# ✅ Correct: All hyperparameters
pso = PSO(
    objective_function=sphere,
    bounds=bounds,
    population_size=50,
    max_iterations=100,
    inertia_weight=0.9,        # ← Controls velocity momentum
    cognitive_constant=1.5,    # ← Attraction to personal best
    social_constant=1.5        # ← Attraction to global best
)

best_solution, best_fitness = pso.run()
```

**Default Values** (if not specified):
| Parameter | Default |
|-----------|---------|
| `population_size` | 50 |
| `max_iterations` | 100 |
| `inertia_weight` (PSO) | 0.7 |
| `cognitive_constant` (PSO) | 1.5 |
| `social_constant` (PSO) | 1.5 |
| `selection_ratio` (EDA) | 0.5 |
| `limit` (ABC) | 20 |

**Check Parameter Availability**:
```python
import inspect
from evobench.algorithms import PSO

sig = inspect.signature(PSO.__init__)
print("PSO parameters:", sig)
# Output: (self, objective_function, bounds, population_size=50, max_iterations=100, inertia_weight=0.7, cognitive_constant=1.5, social_constant=1.5) -> None
```

---

### Error: `TypeError: unsupported operand type(s) for -: 'list' and 'list'`

**Problem**: Operations on population fail with numpy type errors:
```python
TypeError: unsupported operand type(s) for -: 'list' and 'list'
```

**Root Cause**: Bounds passed as list instead of numpy array or list of tuples.

**Solution**: Ensure bounds are properly formatted:
```python
import numpy as np
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

# ✅ Correct: List of tuples
bounds_tuples = [(-5, 5), (-5, 5), (-5, 5)]

# ✅ Correct: NumPy array (shape: n_dims × 2)
bounds_array = np.array([[-5, 5], [-5, 5], [-5, 5]])

# ✅ Correct: Broadcasted list (shorthand)
bounds_broadcast = [(-5, 5)] * 10

# ✅ All three formats are accepted
pso = PSO(sphere, bounds_tuples)
```

---

## Value Errors

### Error: `ValueError: Benchmark '{name}' is not implemented in the registry`

**Problem**: Attempting to access a benchmark function that doesn't exist:
```python
from evobench.benchmarks import get_benchmark

func = get_benchmark("MyCustomFunction")  # ❌ ValueError
```

**Root Cause**: The benchmark name is not registered or was misspelled.

**Solution**: Use only registered benchmarks or implement a custom one:

**Available Benchmarks**:
```python
from evobench.benchmarks import BENCHMARK_REGISTRY, get_benchmark

print(BENCHMARK_REGISTRY.keys())
# Output: dict_keys(['sphere', 'rosenbrock', 'ackley', 'schwefel 1.2', 'trid'])

# ✅ Correct: Use existing benchmarks
sphere_func = get_benchmark("sphere")
ackley_func = get_benchmark("ackley")
```

**For Custom Benchmarks**: Create your own function:
```python
import numpy as np
from evobench.algorithms import PSO

# Define custom objective function
def rastrigin(x: np.ndarray) -> float:
    """Rastrigin function: multimodal benchmark."""
    A = 10
    n = len(x)
    return A * n + sum(x**2 - A * np.cos(2 * np.pi * x))

# Use with algorithms
bounds = [(-5.12, 5.12)] * 10
optimizer = PSO(rastrigin, bounds)
best_solution, best_fitness = optimizer.run()
```

---

### Error: `ValueError: invalid bounds shape` or dimension mismatch

**Problem**: Bounds dimensions don't match population dimension:
```python
bounds = [(-5, 5)] * 10      # 10 dimensions
population = np.random.rand(50, 20)  # 20 dimensions ❌ Mismatch
```

**Root Cause**: Inconsistent problem dimensionality.

**Solution**: Ensure bounds and initial conditions match:
```python
import numpy as np
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

DIMENSION = 10

# ✅ Correct: Consistent dimensionality
bounds = [(-5.12, 5.12)] * DIMENSION

optimizer = PSO(
    objective_function=sphere,
    bounds=bounds,  # 10 dimensions
    population_size=50
)

best_solution, best_fitness = optimizer.run()
# best_solution shape: (10,) ✅
```

---

## Python Version Errors

### Error: `SyntaxError` or incompatible type hints in Python 3.8

**Problem**: Running evobench on Python 3.8 despite installation appearing successful:
```
SyntaxError: invalid syntax
# or
TypeError: unsupported operand type(s) for |: 'type' and 'type'
```

**Root Cause**: evobench requires Python 3.9+ due to:
- Type hint union syntax `X | Y` (requires Python 3.10+)
- NumPy features requiring 3.9+
- Modern setuptools requirements

**Solution**: Upgrade Python:
```bash
# Check current Python version
python --version

# If < 3.9, upgrade:
# macOS
brew upgrade python@3.11

# Linux (Ubuntu/Debian)
sudo apt install python3.11 python3.11-venv

# Windows
# Download from python.org or use Windows Store

# Create virtual environment with Python 3.9+
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install evobench
pip install evobench
```

**Verify Python Version**:
```bash
python --version  # Should be 3.9 or higher
```

---

## Numerical Errors

### Error: `RuntimeWarning: invalid value encountered in sqrt` or `NaN` fitness values

**Problem**: Algorithm produces NaN values in fitness calculation:
```
RuntimeWarning: invalid value encountered in sqrt
Best Fitness: nan
```

**Root Cause**: Objective function evaluation or bounds constraints causing invalid operations (e.g., sqrt of negative, log of zero).

**Solution**: Debug the objective function:
```python
import numpy as np
from evobench.algorithms import PSO
from evobench.benchmarks import ackley

# ✅ Safe: Ackley is well-bounded and numerically stable
bounds = [(-32.768, 32.768)] * 10

optimizer = PSO(ackley, bounds)
best_solution, best_fitness = optimizer.run()

# Custom function: Ensure it's numerically stable
def custom_objective(x: np.ndarray) -> float:
    """Example objective with safety checks."""
    # Avoid division by zero
    denominator = np.sum(x**2) + 1e-10  # Add small epsilon
    
    # Avoid sqrt of negative
    term = np.maximum(np.sum(x**4), 0)
    
    return term / denominator

# Test with safe bounds
test_x = np.random.rand(10)
result = custom_objective(test_x)
assert np.isfinite(result), "Objective function produced NaN!"

optimizer = PSO(custom_objective, bounds)
best_solution, best_fitness = optimizer.run()
```

---

### Error: Convergence stuck at poor fitness value

**Problem**: Algorithm converges to suboptimal solution:
```python
Best Fitness: 1.23e-2  # Should be < 1e-4 on Sphere
```

**Root Cause**: Hyperparameter configuration not suited to problem landscape.

**Solution**: Tune hyperparameters or increase budget:
```python
import numpy as np
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere

bounds = [(-5, 5)] * 10

# Try different algorithms
print("Testing different optimizers...")

# PSO with exploration-focused settings
pso = PSO(sphere, bounds, population_size=100, max_iterations=500, 
          inertia_weight=0.9)  # High inertia = more exploration
_, pso_fitness = pso.run()
print(f"PSO: {pso_fitness:.6e}")

# EDA with weak selection (diversity)
eda = EDA(sphere, bounds, population_size=100, max_iterations=500,
          selection_ratio=0.7)  # Weak selection = more diversity
_, eda_fitness = eda.run()
print(f"EDA: {eda_fitness:.6e}")

# ABC with slower abandonment
abc = ABC(sphere, bounds, population_size=100, max_iterations=500,
          limit=100)  # High limit = slower abandonment
_, abc_fitness = abc.run()
print(f"ABC: {abc_fitness:.6e}")

# If still poor, increase budget
pso_large = PSO(sphere, bounds, population_size=200, max_iterations=1000)
_, pso_large_fitness = pso_large.run()
print(f"PSO (larger budget): {pso_large_fitness:.6e}")
```

**Tuning Guidelines**:
| Problem | Strategy |
|---------|----------|
| Simple (Sphere) | Small budget, any algorithm |
| Multimodal (Ackley) | Large population, high `max_iterations` |
| Non-separable (Trid) | Algorithms with strong learning (EDA) |
| Constrained bounds | Tight bounds → smaller `mutation_rate` |

---

## Memory and Performance Issues

### Error: `MemoryError` on large population sizes

**Problem**: Out of memory when running large experiments:
```
MemoryError: Unable to allocate X.XX GiB for an array with shape...
```

**Root Cause**: Population size × dimension × iterations exceeds available memory.

**Solution**: Reduce population size or use batch processing:
```python
import numpy as np
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

DIMENSION = 1000  # Very high-dimensional
POPULATION_SIZE = 10000  # Large population

# ❌ May cause memory error
# pso = PSO(sphere, [(-5, 5)] * DIMENSION, population_size=POPULATION_SIZE)

# ✅ Solution 1: Reduce population
pso = PSO(sphere, [(-5, 5)] * DIMENSION, population_size=100)

# ✅ Solution 2: Run multiple small experiments instead of one large
results = []
for run in range(100):  # 100 independent runs
    optimizer = PSO(sphere, [(-5, 5)] * DIMENSION, population_size=50, max_iterations=50)
    _, fitness = optimizer.run()
    results.append(fitness)

avg_fitness = np.mean(results)
std_fitness = np.std(results)
print(f"Average Fitness: {avg_fitness:.6e} ± {std_fitness:.6e}")
```

---

### Issue: Slow execution on high-dimensional problems

**Problem**: Algorithm runs very slowly on problems with dimension > 100:
```
Evaluating Benchmark: Sphere
    Running PSO...... (taking > 5 minutes)
```

**Root Cause**: NumPy operations scale with dimension; population fitness evaluations are O(population_size × dimension) per iteration.

**Solution**: Optimize using vectorization and reasonable bounds:
```python
import numpy as np
from evobench.algorithms import PSO
from evobench.benchmarks import sphere
import time

DIMENSION = 500

bounds = [(-5, 5)] * DIMENSION

# Time the optimization
start = time.time()

optimizer = PSO(
    sphere,
    bounds,
    population_size=50,      # Keep reasonable
    max_iterations=100       # Reduce iterations for testing
)

best_solution, best_fitness = optimizer.run()

elapsed = time.time() - start

print(f"Time: {elapsed:.2f} seconds")
print(f"Best Fitness: {best_fitness:.6e}")
print(f"Fitness evals per second: {50 * 100 / elapsed:.0f}")
```

**Performance Tips**:
1. **Vectorization**: evobench already uses NumPy vectorization ✓
2. **Reasonable dimensions**: Start with d ≤ 50, then scale up
3. **Population control**: Use `population_size ≤ min(100, 2×d)`
4. **Batch processing**: Run multiple small experiments instead of one huge one

---

## Statistical Analysis Issues

### Error: `ValueError: Not enough groups for statistical test`

**Problem**: Attempting to run statistical tests with insufficient data:
```python
from evobench.stats import analyze

fitness_data = [np.array([1.2, 1.5])]  # Only 1 algorithm, 2 runs
analyze("Sphere", fitness_data, ["PSO"])  # ❌ Error: need ≥ 2 algorithms
```

**Root Cause**: Statistical tests require at least 2 groups for comparison.

**Solution**: Compare multiple algorithms:
```python
import numpy as np
from evobench.algorithms import PSO, EDA
from evobench.benchmarks import sphere
from evobench.stats import analyze

INDEPENDENT_RUNS = 20
DIMENSION = 10
bounds = [(-5, 5)] * DIMENSION

# Collect data from multiple algorithms
algorithms = [PSO, EDA]
fitness_data = []

for Algorithm in algorithms:
    runs = []
    for _ in range(INDEPENDENT_RUNS):
        opt = Algorithm(sphere, bounds, max_iterations=100)
        _, fitness = opt.run()
        runs.append(fitness)
    fitness_data.append(np.array(runs))

# ✅ Now statistical test works (2 algorithms × 20 runs each)
result = analyze("Sphere", fitness_data, ["PSO", "EDA"])
print(result)
```

---

## Documentation and Examples

### Where to find examples?

See the `examples/` directory:
```bash
git clone https://github.com/NewtonGomez/evobench.git
cd evobench/examples

# Run examples
python 01_basic_usage.py
python 02_multimodal_comparison.py
python 03_statistical_analysis.py
```

---

### Where is the full API reference?

- **Algorithms**: [reference/algorithms/](../reference/algorithms/index.md)
- **Benchmarks**: [reference/benchmarks.md](../reference/benchmarks.md)
- **Statistics**: [reference/index.md](../reference/index.md)
- **Theory**: [theory/index.md](../theory/index.md)

---

## Still Having Issues?

1. **Check the documentation**: [evobench docs](https://evobench.readthedocs.io)
2. **Search existing issues**: [GitHub Issues](https://github.com/NewtonGomez/evobench/issues)
3. **Create a new issue** with:
   - Python version: `python --version`
   - evobench version: `pip show evobench`
   - Minimal reproducible example (MRE)
   - Full error traceback
   - System information: `python -c "import platform; print(platform.platform())"`

---

## Common Questions (FAQ)

**Q: How do I implement my own algorithm?**  
A: Inherit from `EvolutionaryAlgorithm` and override the `run()` method. See [Example 4](../../examples/04_custom_algorithm.py).

**Q: How do I seed random numbers for reproducibility?**  
A: Use NumPy's `default_rng()`. See [Reproducibility Guide](../guide/PERFORMANCE_AND_REPRODUCIBILITY.md).

**Q: How do I visualize convergence curves?**  
A: See [Visualization Guide](../guide/VISUALIZATION.md) for complete examples with matplotlib.

**Q: Why is my algorithm slower than expected?**  
A: Check [Performance Guide](../guide/PERFORMANCE_AND_REPRODUCIBILITY.md) for optimization techniques.

---

**Last Updated**: June 2026  
**evobench Version**: 0.1.0
