# Benchmark Functions

## Overview

**Benchmark functions** are standardized test problems used to evaluate evolutionary algorithm performance. Each function has:

- **Known mathematical properties**: Documented global optimum and landscape characteristics
- **Scalable dimensionality**: Can be evaluated in different problem dimensions
- **Diverse behaviors**: Range from simple convex to complex multimodal landscapes

The five functions in evobench represent different optimization problem classes, enabling comprehensive algorithm evaluation across varying difficulty levels and landscape topologies.

**Location**: `evobench.benchmarks`

**Import Format**: `from evobench.benchmarks import sphere, rosenbrock, ackley, schwefel, trid`

---

## Benchmark Registry

All benchmark functions are accessible through the centralized `BENCHMARK_REGISTRY`:

```python
from evobench.benchmarks import BENCHMARK_REGISTRY, get_benchmark

# Direct access
sphere_func = BENCHMARK_REGISTRY["sphere"]

# Programmatic access
ackley_func = get_benchmark("ackley")
```

### Supported Identifiers

| ID | Function | Dimensionality | Optimum | Difficulty |
|----|----------|-----------------|---------|-----------|
| `"sphere"` | Sphere | Any | 0.0 | Very Low |
| `"rosenbrock"` | Rosenbrock | Any | 0.0 | Medium-High |
| `"ackley"` | Ackley | Any | 0.0 | High |
| `"schwefel"` | Schwefel 1.2 | Any | 0.0 | Medium |
| `"trid"` | Trid | Any | Varies | High |

---

## Sphere Function

### Mathematical Definition

$$F(\mathbf{x}) = \sum_{i=1}^{d} x_i^2$$

### Properties

| Property | Value |
|----------|-------|
| **Search Domain** | $[-5.12, 5.12]^d$ (typical) |
| **Global Optimum** | $\mathbf{x}^* = (0, 0, \ldots, 0)$ |
| **Optimum Value** | $F(\mathbf{x}^*) = 0$ |
| **Separability** | **Fully separable** (each dimension independent) |
| **Modality** | **Unimodal** (single global minimum) |
| **Convexity** | **Strictly convex** (quadratic) |
| **Gradients** | Everywhere smooth and informative |

### Usage

```python
from evobench.benchmarks import sphere

# Direct call
fitness = sphere(x)  # x is np.ndarray of shape (d,)

# In an optimizer
from evobench.algorithms import PSO

bounds = [(-5.12, 5.12)] * 10
optimizer = PSO(sphere, bounds)
best_solution, best_fitness = optimizer.run()
```

### Benchmark Qualities

- **Simplest test function**: Validates basic algorithm correctness
- **No local minima**: Measures pure convergence speed
- **Fully separable**: Each dimension can be optimized independently
- **Ideal baseline**: Compare performance across algorithms on trivial problem
- **Expected convergence**: All algorithms should reach $F < 10^{-4}$ easily

### When to Use

- ✓ Debugging algorithm implementation
- ✓ Quick performance baseline
- ✓ Validating that optimization loop works correctly
- ✓ Measuring CPU time on simple problem

---

## Rosenbrock Function

### Mathematical Definition

$$F(\mathbf{x}) = \sum_{i=1}^{d-1} \left[ 100(x_{i+1} - x_i^2)^2 + (1 - x_i)^2 \right]$$

### Properties

| Property | Value |
|----------|-------|
| **Search Domain** | $[-10, 10]^d$ (typical) |
| **Global Optimum** | $\mathbf{x}^* = (1, 1, \ldots, 1)$ |
| **Optimum Value** | $F(\mathbf{x}^*) = 0$ |
| **Separability** | **Completely non-separable** (all variables interact) |
| **Modality** | **Unimodal** (single global minimum, no local optima) |
| **Convexity** | **Non-convex** (variable curvature, narrow valley) |
| **Structure** | Optimal solution lies in a parabolic valley |

### Usage

```python
from evobench.benchmarks import rosenbrock

# Direct call
fitness = rosenbrock(x)

# In optimizer
from evobench.algorithms import EDA

bounds = [(-2.048, 2.048)] * 5
optimizer = EDA(rosenbrock, bounds, max_iterations=150)
best_solution, best_fitness = optimizer.run()
```

### Mathematical Properties

The difficulty arises from the *parabolic valley*:

1. The valley is easy to find: $x_i \approx x_{i-1}^2$
2. **Convergence within the valley is hard**: Small changes in early dimensions cause large changes in later ones

For example, with $d=2$:

$$F(x_1, x_2) = 100(x_2 - x_1^2)^2 + (1 - x_1)^2$$

The contours form a narrow, curved channel that gradient-based and simple metaheuristics struggle to navigate efficiently.

### Benchmark Qualities

- **Tests efficiency in non-convex spaces**: Can algorithms navigate valley?
- **Detects premature convergence**: Poor algorithms converge to suboptimal points in the valley
- **Variable coupling**: Suboptimal early dimensions (close to 1) are needed
- **Exploitation challenge**: Finding valley is easy; exploiting it requires fine control

### When to Use

- ✓ Evaluating refinement ability and exploitation
- ✓ Testing convergence in non-convex landscapes
- ✓ Assessing efficiency on intermediate-difficulty problems
- ✓ Comparing optimization speed in narrow regions

---

## Ackley Function

### Mathematical Definition

$$F(\mathbf{x}) = -20 \exp\left(-0.2\sqrt{\frac{1}{d}\sum_{i=1}^{d} x_i^2}\right) - \exp\left(\frac{1}{d}\sum_{i=1}^{d} \cos(2\pi x_i)\right) + 20 + e$$

where $e$ is Euler's number ($\approx 2.71828$).

### Properties

| Property | Value |
|----------|-------|
| **Search Domain** | $[-32.768, 32.768]^d$ (typical) |
| **Global Optimum** | $\mathbf{x}^* = (0, 0, \ldots, 0)$ |
| **Optimum Value** | $F(\mathbf{x}^*) = 0$ |
| **Separability** | **Weakly non-separable** (variables interact via norms) |
| **Modality** | **Highly multimodal** ($\approx 2^d$ local minima) |
| **Landscape Structure** | Flat exterior, many shallow local minima, deep hole at center |
| **Local Minima Count** | Exponential in dimension ($2^d$) |

### Usage

```python
from evobench.benchmarks import ackley

# Direct call
fitness = ackley(x)

# In optimizer (multimodal benchmark)
from evobench.algorithms import ABC

bounds = [(-32.768, 32.768)] * 8
optimizer = ABC(ackley, bounds, max_iterations=500)
best_solution, best_fitness = optimizer.run()
```

### Landscape Features

The Ackley function exhibits unique characteristics:

1. **Flat exterior regions**: The first exponential term dominates far from origin, creating featureless plateaus
2. **Many local minima**: The cosine term creates shallow wells throughout the space
3. **Global minimum at center**: A deep "hole" exists at the origin (0, 0, ..., 0)
4. **Deceptive structure**: Gradients in flat regions are nearly zero, misleading gradient-based methods

### Benchmark Qualities

- **Tests global exploration**: Can algorithms escape flat regions and find the center?
- **Detects local optimum entrapment**: Poor exploration algorithms get stuck in shallow wells
- **Multimodal challenge**: Population diversity is critical
- **Non-informative gradients**: Gradient-based methods perform poorly

### When to Use

- ✓ Evaluating global exploration ability
- ✓ Testing multimodal landscape performance
- ✓ Assessing population diversity maintenance
- ✓ Benchmarking on hard problems (high difficulty)

---

## Schwefel 1.2 Function

### Mathematical Definition

$$F(\mathbf{x}) = \sum_{i=1}^{d} \left(\sum_{j=1}^{i} x_j\right)^2$$

### Properties

| Property | Value |
|----------|-------|
| **Search Domain** | $[-40, 60]^d$ (typical, asymmetric) |
| **Global Optimum** | $\mathbf{x}^* = (0, 0, \ldots, 0)$ |
| **Optimum Value** | $F(\mathbf{x}^*) = 0$ |
| **Separability** | **Completely non-separable** (total variable coupling) |
| **Modality** | **Unimodal** (no local minima) |
| **Convexity** | **Convex** (quadratic structure) |
| **Variable Coupling** | **Total** (every variable depends on all previous ones) |
| **Conditioning** | **Ill-conditioned** (high Hessian eigenvalue ratio) |

### Usage

```python
from evobench.benchmarks import schwefel

# Direct call
fitness = schwefel(x)

# In optimizer
from evobench.algorithms import EDA

bounds = [(-100, 100)] * 10
optimizer = EDA(schwefel, bounds)
best_solution, best_fitness = optimizer.run()
```

### Variable Interdependence

The sum structure creates **total interdependence**:

$$F = x_1^2 + (x_1 + x_2)^2 + (x_1 + x_2 + x_3)^2 + \cdots$$

Changing dimension 1 affects all subsequent terms. Variables **cannot be optimized independently**. This structure tests:

- Ability to discover and exploit variable correlations
- Handling of highly-coupled optimization problems
- Convergence on ill-conditioned (difficult conditioning number) problems

### Benchmark Qualities

- **Tests correlation detection**: Can algorithms identify variable dependencies?
- **Coupling challenge**: Changing one variable affects many terms
- **Ill-conditioning**: High Hessian eigenvalue ratio slows gradient-based methods
- **Structure preservation**: Population diversity helps maintain search structure

### When to Use

- ✓ Evaluating performance on fully-coupled problems
- ✓ Testing handling of variable correlations
- ✓ Assessing convergence on ill-conditioned problems
- ✓ Comparing algorithms on intermediate-difficulty benchmarks

---

## Trid Function

### Mathematical Definition

$$F(\mathbf{x}) = \sum_{i=1}^{d} (x_i - i)^2 - \sum_{i=2}^{d} x_i \cdot x_{i-1}$$

### Global Optimum (Dimension-Dependent)

$$x_i^* = i(d + 1 - i) \quad \text{for } i = 1, 2, \ldots, d$$

$$F(\mathbf{x}^*) = -\frac{d(d+4)(d-1)}{6}$$

### Example Optimal Values

| Dimension | Optimal Solution | $F(\mathbf{x}^*)$ |
|-----------|------------------|-----------------|
| 2 | $(2, 2)$ | $-4$ |
| 3 | $(3, 4, 3)$ | $-12$ |
| 5 | $(5, 8, 9, 8, 5)$ | $-50$ |
| 10 | $(10, 18, 24, 28, 30, 30, 28, 24, 18, 10)$ | $-440$ |

### Properties

| Property | Value |
|----------|-------|
| **Search Domain** | $[-d^2, d^2]^d$ (dimension-dependent) |
| **Global Optimum** | Dimension-dependent formula above |
| **Optimum Value** | Negative (decreases with dimension) |
| **Separability** | **Completely non-separable** (all variables interact) |
| **Modality** | **Unimodal** (no local minima) |
| **Convexity** | **Non-convex** (variable curvature) |
| **Gradient Reliability** | Misleading (gradients don't guide well) |
| **Structure** | Highly interdependent, symmetric optimum |

### Usage

```python
from evobench.benchmarks import trid

# Direct call (optimum dimension-dependent)
fitness = trid(x)

# In optimizer
from evobench.algorithms import EDA

bounds = [(-100, 100)] * 10
optimizer = EDA(trid, bounds, max_iterations=300)
best_solution, best_fitness = optimizer.run()
```

### Landscape Features

Trid presents a unique challenge:

1. **No local minima**: The landscape is unimodal in structure
2. **Complex topology**: Multiple coupled terms create non-obvious pathways to optimum
3. **Symmetric optimum**: Solution values follow a symmetric pattern
4. **Interdependence**: Each variable couples with its neighbors
5. **Misleading gradients**: Steepest descent directions don't lead to global optimum

### Benchmark Qualities

- **Tests correlation exploitation**: Algorithm must discover optimal variable relationships
- **No local trap guarantee**: Useful for testing robust convergence
- **Dimension-dependent difficulty**: Increases with problem size
- **Deceptive geometry**: Structure optimization, not gradient descent

### When to Use

- ✓ Evaluating exploitation of variable structure
- ✓ Testing on dimension-dependent problems
- ✓ Assessing convergence on non-convex interdependent landscapes
- ✓ Benchmarking difficult problems (high difficulty)

---

## Comparative Difficulty Ranking

### Summary Table

| Function | Separability | Modality | Convexity | Difficulty | Coupling |
|----------|--------------|----------|-----------|------------|----------|
| **Sphere** | ✓ Separable | Unimodal | Convex | **Very Low** | None |
| **Rosenbrock** | ✗ Non-sep | Unimodal | Non-convex | **Medium-High** | Pairwise |
| **Ackley** | ✗ Non-sep | **Multimodal** | Non-convex | **High** | Low |
| **Schwefel 1.2** | ✗ Non-sep | Unimodal | Convex | **Medium** | **Total** |
| **Trid** | ✗ Non-sep | Unimodal | Non-convex | **High** | **Total** |

### Recommended Evaluation Sequence

Progress from simple to complex:

1. **Sphere**: Baseline validation (very low difficulty)
2. **Rosenbrock**: Valley navigation (medium-high difficulty)
3. **Ackley**: Global exploration (high difficulty, multimodal)
4. **Schwefel 1.2**: Variable coupling (medium difficulty, total coupling)
5. **Trid**: Structure exploitation (high difficulty, symmetric optimum)

---

## Selection Guide

### Choose Sphere When:
- ✓ Validating algorithm implementation correctness
- ✓ Measuring baseline convergence speed
- ✓ Quick algorithm testing (low computational cost)

### Choose Rosenbrock When:
- ✓ Testing refinement in non-convex spaces
- ✓ Evaluating exploitation in narrow regions
- ✓ Intermediate-difficulty benchmark needed

### Choose Ackley When:
- ✓ Testing global exploration capability
- ✓ Evaluating multimodal landscape performance
- ✓ Benchmarking robustness on hard problems

### Choose Schwefel 1.2 When:
- ✓ Testing variable coupling detection
- ✓ Evaluating performance on fully-coupled problems
- ✓ Assessing ill-conditioning handling

### Choose Trid When:
- ✓ Testing exploitation of problem structure
- ✓ Evaluating dimension-dependent difficulty
- ✓ Benchmarking on highly complex landscapes

---

## Example: Complete Benchmark Suite

```python
import numpy as np
from evobench.benchmarks import sphere, rosenbrock, ackley, schwefel, trid, BENCHMARK_REGISTRY
from evobench.algorithms import PSO, EDA, ABC

# Problem definitions
problems = {
    'sphere': {
        'func': sphere,
        'bounds': [(-5.12, 5.12)] * 10,
        'difficulty': 'Very Low'
    },
    'rosenbrock': {
        'func': rosenbrock,
        'bounds': [(-2.048, 2.048)] * 10,
        'difficulty': 'Medium-High'
    },
    'ackley': {
        'func': ackley,
        'bounds': [(-32.768, 32.768)] * 10,
        'difficulty': 'High'
    },
    'schwefel': {
        'func': schwefel,
        'bounds': [(-100, 100)] * 10,
        'difficulty': 'Medium'
    },
    'trid': {
        'func': trid,
        'bounds': [(-400, 400)] * 10,
        'difficulty': 'High'
    }
}

algorithms = [PSO, EDA, ABC]

# Run comprehensive evaluation
print("Algorithm Performance Across Benchmark Suite")
print("=" * 70)

for prob_name, prob_info in problems.items():
    print(f"\n{prob_name.upper()} (Difficulty: {prob_info['difficulty']})")
    print("-" * 70)
    
    for AlgoClass in algorithms:
        results = []
        for _ in range(10):
            optimizer = AlgoClass(
                prob_info['func'],
                prob_info['bounds'],
                max_iterations=300
            )
            _, best_fit = optimizer.run()
            results.append(best_fit)
        
        mean_fit = np.mean(results)
        std_fit = np.std(results)
        
        print(f"{AlgoClass.__name__:5} | "
              f"Mean: {mean_fit:12.6f} | Std: {std_fit:12.6f}")
```

---

## See Also

- [Algorithm Reference](index.md)
- [PSO Documentation](algorithms/pso.md)
- [EDA Documentation](algorithms/eda.md)
- [ABC Documentation](algorithms/abc.md)
- [Benchmark Theory](../../theory/benchmark-functions.md)
- [Statistical Analysis](../../theory/statistical-testing.md)
