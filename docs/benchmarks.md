# Benchmark Functions Reference

## Overview

Benchmark functions are standardized test problems for evaluating evolutionary algorithm performance. Each function has:

- **Known mathematical properties**: Documented global optimum and landscape characteristics
- **Scalable dimensionality**: Can be evaluated in different problem dimensions
- **Diverse behaviors**: Range from simple to complex landscapes

The five functions implemented represent different optimization problem classes, enabling comprehensive algorithm evaluation across varying difficulty levels.

**Import alias format:** `from evobench.benchmarks import sphere, ackley, rosenbrock, schwefel, trid`

---

## Sphere

**Function:**
$$F(\mathbf{x}) = \sum_{i=1}^{d} x_i^2$$

**Properties:**

| Property | Value |
|----------|-------|
| Search Space | [-600, 600]^n |
| Global Optimum | $\mathbf{x}^* = (0, 0, \ldots, 0)$ |
| Optimum Value | $F(\mathbf{x}^*) = 0$ |
| Separability | **Fully separable** |
| Modality | Unimodal |
| Convexity | Strictly convex |

**Benchmark Qualities:**
- Simplest test function; validates basic algorithm convergence
- No local minima; measures pure convergence speed
- Ideal for validating implementation correctness before complex functions
- Good baseline for performance comparison
---

## Rosenbrock

**Function:**
$$F(\mathbf{x}) = \sum_{i=1}^{d-1} \left[ 100(x_{i+1} - x_i^2)^2 + (1 - x_i)^2 \right]$$

**Properties:**

| Property | Value |
|----------|-------|
| Search Space | [-10, 10]^n |
| Global Optimum | $\mathbf{x}^* = (1, 1, \ldots, 1)$ |
| Optimum Value | $F(\mathbf{x}^*) = 0$ |
| Separability | **Non-separable** |
| Modality | Unimodal |
| Convexity | Non-convex (variable curvature) |

**Benchmark Qualities:**
- Optimal solution lies in narrow parabolic valley; trivial to locate valley, difficult to converge within it
- Tests exploitation vs. exploration balance
- Detects premature convergence to suboptimal points
- Evaluates algorithm efficiency in non-convex landscapes with poor conditioning
---

## Ackley

**Function:**
$$F(\mathbf{x}) = -20 \exp\left(-0.2\sqrt{\frac{1}{d}\sum_{i=1}^{d} x_i^2}\right) - \exp\left(\frac{1}{d}\sum_{i=1}^{d} \cos(2\pi x_i)\right) + 20 + e$$

**Properties:**

| Property | Value |
|----------|-------|
| Search Space | [-10, 10]^n (typical) |
| Global Optimum | $\mathbf{x}^* = (0, 0, \ldots, 0)$ |
| Optimum Value | $F(\mathbf{x}^*) = 0$ |
| Separability | **Non-separable** |
| Modality | **Highly multimodal** (~$2^d$ local minima) |
| Structure | Flat exterior with deep hole at center |

**Benchmark Qualities:**
- Global optimum surrounded by many local minima; tests global exploration capacity
- Flat exterior regions make gradient-based techniques ineffective
- Detects algorithm entrapment in local optima
- Measures robustness in escaping deceptive plateaus
- Evaluates exploration-exploitation balance in multimodal landscapes
---

## Schwefel 1.2

**Function:**
$$F(\mathbf{x}) = \sum_{i=1}^{d} \left(\sum_{j=1}^{i} x_j\right)^2$$

**Properties:**

| Property | Value |
|----------|-------|
| Search Space | [-40, 60]^n |
| Global Optimum | $\mathbf{x}^* = (0, 0, \ldots, 0)$ |
| Optimum Value | $F(\mathbf{x}^*) = 0$ |
| Separability | **Completely non-separable** |
| Modality | Unimodal |
| Convexity | Convex |
| Variable Coupling | Total (all variables coupled) |

**Benchmark Qualities:**
- Accumulative summation creates total interdependence between variables
- Variables cannot be optimized independently
- Tests algorithm's ability to exploit variable correlations
- Evaluates convergence in high-conditioned problems
- Assesses whether algorithm maintains population diversity and structure
---

## Trid

**Function:**
$$F(\mathbf{x}) = \sum_{i=1}^{d} (x_i - 1)^2 - \sum_{i=2}^{d} x_i \cdot x_{i-1}$$

**Global Optimum (Non-trivial):**
$$x_i^* = i(d + 1 - i) \quad \text{for } i = 1, 2, \ldots, d$$

$$F(\mathbf{x}^*) = -\frac{d(d+4)(d-1)}{6}$$

**Example values:**
- d=2: $\mathbf{x}^* = (2, 2)$, $F(\mathbf{x}^*) = -4$
- d=3: $\mathbf{x}^* = (3, 4, 3)$, $F(\mathbf{x}^*) = -12$
- d=10: $F(\mathbf{x}^*) = -440$

**Properties:**

| Property | Value |
|----------|-------|
| Search Space | [-d², d²]^n |
| Separability | **Non-separable** |
| Modality | Unimodal (no local minima) |
| Interdependence | **Highly interdependent** |
| Gradient Reliability | Misleading (gradients don't guide well) |

**Benchmark Qualities:**
- No local minima but complex topography; challenges global exploration
- Strong interdependence between consecutive variables
- Tests ability to discover and exploit variable correlations
- Detects algorithms fooled by deceptive gradient information
- Evaluates robustness in spaces with complex variable relationships
---

## Comparative Analysis

### Summary Table

| Function | Separability | Modality | Convexity | Difficulty | Variable Coupling |
|----------|--------------|----------|-----------|------------|-------------------|
| **Sphere** | ✓ Separable | Unimodal | Convex | Very Low | None |
| **Rosenbrock** | ✗ Non-sep | Unimodal | Non-convex | Medium-High | Local (pairs) |
| **Ackley** | ✗ Non-sep | **Multimodal** | Non-convex | High | Low |
| **Schwefel 1.2** | ✗ Non-sep | Unimodal | Convex | Medium | **Total** |
| **Trid** | ✗ Non-sep | Unimodal | Non-convex | High | **Total** |

### Selection Guide

**Choose based on algorithm aspect to evaluate:**

- **Convergence speed on simple landscapes**: Sphere
- **Refinement ability and narrow-valley navigation**: Rosenbrock
- **Global exploration and multimodal robustness**: Ackley
- **Handling fully-coupled variables**: Schwefel 1.2, Trid
- **Correlation exploitation**: Trid

**Recommended evaluation sequence:** Sphere → Rosenbrock → Ackley → Schwefel 1.2 → Trid (increasing difficulty)

