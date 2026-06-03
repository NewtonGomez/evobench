# Benchmark Function Theory

## Overview

Benchmark functions are standardized mathematical functions used to evaluate evolutionary algorithm performance. Beyond simply being test cases, they represent **specific optimization problem classes** with well-studied mathematical properties that affect algorithm behavior.

This document provides the theoretical foundation for understanding:

- **Mathematical properties**: Separability, modality, convexity
- **Landscape topology**: How problem structure affects optimization difficulty
- **Theoretical analysis**: Mathematical basis for function behavior
- **Selection criteria**: How to choose appropriate benchmarks

---

## Fundamental Properties

### 1. Separability

**Definition**: A function is **separable** if it can be decomposed into independent functions of individual variables.

#### Fully Separable Functions

$$F(\mathbf{x}) = \sum_{i=1}^{d} f_i(x_i)$$

Each dimension can be optimized independently.

**Example (Sphere)**:
$$F(\mathbf{x}) = \sum_{i=1}^{d} x_i^2 = f_1(x_1) + f_2(x_2) + \cdots + f_d(x_d)$$

**Algorithm Advantage**: Simple decomposition strategies work well

#### Non-Separable Functions

Variables interact; cannot optimize dimensions independently.

**Example (Rosenbrock)**:
$$F(\mathbf{x}) = \sum_{i=1}^{d-1} [100(x_{i+1} - x_i^2)^2 + (1 - x_i)^2]$$

Each term involves two consecutive dimensions: $f_i(x_i, x_{i+1})$

**Algorithm Challenge**: Must discover and exploit variable relationships

#### Impact on Algorithm Design

| Separability | Algorithm Strategy |
|--------------|-------------------|
| Fully separable | Coordinate descent works well |
| Partially coupled | Linkage learning is beneficial |
| Fully coupled | Must learn relationships |

---

### 2. Modality

**Definition**: The number of local minima in the search space.

#### Unimodal Functions

**Definition**: Single global minimum, no local minima.

**Mathematical Property**: Any point is closer to optimum following a gradient direction (or random walk follows monotonic improving trend on average).

**Examples**:
- Sphere: $F(\mathbf{x}) = \sum x_i^2$ (convex quadratic)
- Rosenbrock: Narrow valley to optimum
- Schwefel 1.2: Coupled but no local traps

**Optimization Implication**: Gradient-based and simple evolutionary methods often succeed.

#### Multimodal Functions

**Definition**: Multiple local minima; global optimum is just one of many.

**Mathematical Property**: Gradients may not guide toward global optimum; may be trapped in local optima.

**Example (Ackley)**:

$$F(\mathbf{x}) = -20 \exp\left(-0.2\sqrt{\frac{1}{d}\sum_{i=1}^{d} x_i^2}\right) - \exp\left(\frac{1}{d}\sum_{i=1}^{d} \cos(2\pi x_i)\right) + 20 + e$$

The cosine term creates $\approx 2^d$ local minima.

**Optimization Implication**: Population diversity is critical to escape local optima.

#### Practical Difficulty Ranking

| Modality | Local Minima | Algorithm Challenge |
|----------|--------------|-------------------|
| Unimodal | 0 (only global) | Convergence to single point |
| Weakly multimodal | Few (~10) | Escape some local optima |
| Multimodal | Many (~100+) | Global exploration critical |
| Highly multimodal | Exponential in $d$ | Difficult without robust mechanisms |

---

### 3. Convexity

**Definition**: A function is **convex** if the line segment between any two points lies above the function graph.

#### Strictly Convex Functions

$$F(\lambda \mathbf{x}_1 + (1-\lambda) \mathbf{x}_2) < \lambda F(\mathbf{x}_1) + (1-\lambda) F(\mathbf{x}_2) \quad \forall 0 < \lambda < 1$$

**Properties**:
- Unique global minimum
- Every local minimum is global
- Hessian matrix is positive definite everywhere

**Example (Sphere)**:
$$F(\mathbf{x}) = \sum_{i=1}^{d} x_i^2$$

Hessian: $H = 2I$ (positive definite)

**Optimization Implication**: Convex functions are relatively easy; all local optima are global.

#### Non-Convex Functions

Local minima can exist that are not global optima.

**Examples**:
- Rosenbrock: Variable curvature, non-convex valley
- Ackley: Multimodal landscape, highly non-convex

**Optimization Implication**: Cannot rely on gradient-based methods alone.

---

### 4. Conditioning (Ill-Conditioning)

**Definition**: The ratio of maximum to minimum Hessian eigenvalues (for twice-differentiable functions).

$$\text{Condition Number} \kappa = \frac{\lambda_{\max}}{\lambda_{\min}}$$

#### Well-Conditioned Problems

$\kappa \approx 1$: All directions have similar curvature.

**Properties**:
- Smooth descent toward optimum
- Gradient-based methods perform well

**Example (Sphere)**:
All Hessian eigenvalues equal 2; $\kappa = 1$

#### Ill-Conditioned Problems

$\kappa \gg 1$: Directions have vastly different curvatures.

**Properties**:
- Narrow valley or ridge structure
- Gradient descent zigzags inefficiently
- Small changes in some dimensions → large function changes

**Example (Rosenbrock)**:
Valley is extremely narrow; steep walls, narrow valley floor.
Condition number increases with dimension.

**Optimization Implication**: Requires careful step sizing or adaptive methods.

---

## Landscape Topology

### Gradient Information

#### Gradient Availability

**Smooth functions** (Sphere, Rosenbrock, Schwefel): Gradients exist and may be informative.

$$\nabla F(\mathbf{x}) = \left( \frac{\partial F}{\partial x_1}, \frac{\partial F}{\partial x_2}, \ldots, \frac{\partial F}{\partial x_d} \right)$$

**Non-smooth or deceptive functions** (Ackley has flat regions): Gradients may be zero or misleading.

#### Deceptive Landscapes

**Definition**: Landscapes where gradients point away from global optimum.

**Example (Ackley exterior)**:
In flat regions far from origin, all gradients are nearly zero—providing no guidance toward the global minimum in the center.

**Algorithm Challenge**: Population-based methods must maintain diversity despite lack of gradient information.

---

### Separability Structure

#### Fully Separable (e.g., Sphere)

$$F(\mathbf{x}) = \sum_{i=1}^{d} x_i^2$$

```
Contours are perfect circles/spheres
Each dimension independent
Simple optimization: set x_i = 0 for all i
```

#### Partially Coupled (e.g., Rosenbrock)

$$F(\mathbf{x}) = \sum_{i=1}^{d-1} [100(x_{i+1} - x_i^2)^2 + (1-x_i)^2]$$

```
Contours form elongated ellipses
Adjacent dimensions couple: x_{i+1} depends on x_i^2
Optimization requires balancing dependent variables
```

#### Fully Coupled (e.g., Schwefel 1.2)

$$F(\mathbf{x}) = \sum_{i=1}^{d} \left(\sum_{j=1}^{i} x_j\right)^2$$

```
Every dimension couples with all others
No decomposition possible
Optimization must handle complete interdependence
```

---

## Theoretical Analysis of evobench Benchmarks

### 1. Sphere Function

#### Mathematical Properties

$$F(\mathbf{x}) = \sum_{i=1}^{d} x_i^2$$

**Hessian**: $H = 2I$ (identity matrix scaled by 2)

**Eigenvalues**: All equal to 2

**Condition Number**: $\kappa = 1$ (perfectly conditioned)

#### Convergence Rate

For algorithms using random initialization in $[-R, R]^d$, convergence to $F < \epsilon$ typically follows:

$$T(\epsilon) = O\left( d \log \frac{R^2}{\epsilon} \right)$$

#### Separability Analysis

$$F(\mathbf{x}) = x_1^2 + x_2^2 + \cdots + x_d^2$$

Each dimension independently minimizes to $x_i = 0$.

**Optimal Strategy**: Reduce each dimension toward 0 independently.

---

### 2. Rosenbrock Function

#### Mathematical Properties

$$F(\mathbf{x}) = \sum_{i=1}^{d-1} [100(x_{i+1} - x_i^2)^2 + (1-x_i)^2]$$

**Optimal Solution**: $\mathbf{x}^* = (1, 1, \ldots, 1)$

**Separability**: Each term couples $x_i$ and $x_{i+1}$, but dimension 1 and dimension $d$ are special (no pairing).

**Gradient at Optimum**: $\nabla F(\mathbf{1}) = \mathbf{0}$ (satisfied)

#### Valley Structure

The constraint $x_{i+1} = x_i^2$ defines the optimal valley.

**Difficulty Zones**:
1. **Finding the valley**: Relatively easy (region where $x_{i+1} \approx x_i^2$)
2. **Navigating within the valley**: Very hard (interior is extremely narrow)

#### Convergence Characteristics

- **Phase 1 (Finding valley)**: Fast progress (large fitness improvements)
- **Phase 2 (Inside valley)**: Slow progress (narrow, constrained movement)
- **Total iterations needed**: Often 10–100× more than Sphere for same accuracy

#### Why Rosenbrock Is Difficult

The curvature varies dramatically:

$$\frac{\partial^2 F}{\partial x_i^2} \approx 2 + 200 \cdot (\text{some function of } x_i, x_{i+1})$$

In the valley, one direction has very high curvature while perpendicular direction is flat.

---

### 3. Ackley Function

#### Mathematical Properties

$$F(\mathbf{x}) = -20 \exp\left(-0.2\sqrt{\frac{1}{d}\sum_{i=1}^{d} x_i^2}\right) - \exp\left(\frac{1}{d}\sum_{i=1}^{d} \cos(2\pi x_i)\right) + 20 + e$$

This is a **composition** of two exponentials:

- **First term**: Related to $\|\mathbf{x}\|_2$ (distance from origin)
- **Second term**: Related to periodic cosine oscillations

#### Two-Scale Landscape

**Exterior (far from origin)**:
First exponential dominates; landscape is nearly flat (value $\approx -20 + 20 = 0$).

**Interior (near origin)**:
Cosine term dominates; creates $2^d$ shallow local minima surrounding the global minimum at $\mathbf{0}$.

**Contour visualization** (2D):
```
Exterior:     Many shallow wells (local minima)
              |  |  |  |  |
              v  v  v  v  v
Center:       Deep hole (global minimum)
```

#### Local Minima Count

For each dimension, cosine has 2 minima per period:

$$\cos(2\pi x_i): \text{ minima at } x_i = k + 0.5 \text{ for integer } k$$

With $d$ dimensions, approximately $2^d$ combinations → $2^d$ local minima.

**Example**: 10D Ackley has $\approx 1024$ local minima!

#### Optimization Challenge

1. **Escape flat exterior**: Population must explore despite nearly-zero gradients
2. **Avoid local minima**: Surrounded by shallow wells
3. **Navigate to center**: Find the deep hole among thousands of shallow wells

---

### 4. Schwefel 1.2 Function

#### Mathematical Properties

$$F(\mathbf{x}) = \sum_{i=1}^{d} \left(\sum_{j=1}^{i} x_j\right)^2$$

**Expanded form (d=3)**:
$$F(x_1, x_2, x_3) = x_1^2 + (x_1 + x_2)^2 + (x_1 + x_2 + x_3)^2$$

#### Complete Variable Coupling

**Chain structure**:
- Dimension 1 appears in all 3 terms
- Dimension 2 appears in last 2 terms
- Dimension 3 appears in last term

**Optimization implications**:
- Cannot optimize each dimension independently
- Changing $x_1$ affects all terms
- Must respect cumulative structure

#### Hessian Analysis

The Hessian is fully dense (no zero off-diagonals):

$$H_{ij} = \frac{\partial^2 F}{\partial x_i \partial x_j} \neq 0 \quad \forall i, j$$

**Ill-conditioning**: Eigenvalue ratio is large, meaning:
- Some directions have high curvature
- Other directions have low curvature
- Optimization is slow in ill-conditioned directions

#### Optimal Solution

Setting $\frac{\partial F}{\partial x_i} = 0$ for all $i$ leads to:

$$x_i^* = 0 \quad \forall i$$

**Verification**: $F(\mathbf{0}) = 0 + 0 + \cdots + 0 = 0$ ✓

---

### 5. Trid Function

#### Mathematical Properties

$$F(\mathbf{x}) = \sum_{i=1}^{d} (x_i - i)^2 - \sum_{i=2}^{d} x_i \cdot x_{i-1}$$

**Optimal solution (dimension-dependent)**:

$$x_i^* = i(d + 1 - i)$$

**Example (d=5)**:
$$x^* = (5, 8, 9, 8, 5)$$

Solution is **symmetric**: $x_1^* = x_d^*$, $x_2^* = x_{d-1}^*$, etc.

#### Unique Characteristics

**Unlike other benchmarks**:

1. **No local minima**: Unimodal structure (no traps)
2. **Non-obvious optimum**: Cannot guess solution from objective function alone
3. **Dimension-dependent**: Solution changes with $d$
4. **Symmetric pattern**: Optimal vector is palindromic

#### Gradient Information

$$\nabla_i F = 2(x_i - i) - x_{i-1} - x_{i+1} + \cdots$$

Gradients provide **misleading information**: Steepest descent from random starting point does NOT lead to global optimum efficiently.

**Reason**: The coupling between adjacent variables creates a deceptive landscape where gradients pull in directions away from the true optimum.

#### Optimization Challenge

Algorithms must:
1. Discover the symmetric structure ($x_1^* = x_d^*$)
2. Navigate the coupled optimization space
3. Avoid being misled by gradient information
4. Handle dimension-dependent difficulty scaling

---

## Function Selection Strategy

### Decision Tree

```
Problem Type?
│
├─→ VALIDATION needed
│   └─→ Use SPHERE (simplest)
│
├─→ Intermediate difficulty needed
│   ├─→ Non-separable? → Use ROSENBROCK
│   └─→ Coupled? → Use SCHWEFEL 1.2
│
└─→ CHALLENGE needed
    ├─→ Multimodal exploration? → Use ACKLEY
    └─→ Structure exploitation? → Use TRID
```

### Recommended Benchmark Suites

#### Minimal Suite (3 functions)
- Sphere (validation)
- Ackley (multimodal)
- Schwefel 1.2 (coupling)

#### Standard Suite (5 functions)
- Sphere (easiest)
- Rosenbrock (intermediate)
- Ackley (multimodal)
- Schwefel 1.2 (coupling)
- Trid (hardest)

#### Extended Suite (add 10+ functions)
- Include dimension variants (2D, 5D, 10D, 20D)
- Add CEC benchmark functions
- Include domain-specific problems

---

## Difficulty Scaling

### Sphere: Linear Difficulty

With increasing dimension:
- Computational cost ∝ $d$
- Number of local optima: 0 (always)
- Difficulty: Constant (easy across all $d$)

### Ackley: Exponential Difficulty

Number of local minima ≈ $2^d$:
- 5D: ~32 local minima
- 10D: ~1024 local minima
- 20D: ~1M local minima

Difficulty increases exponentially with dimension.

### Trid: Polynomial Difficulty

Condition number and coupling both increase with $d$. Difficulty grows polynomially (approximately $d^2$).

---

## References

### Foundational Works

- De Jong, K. A. (1975). "Analysis of the behavior of a class of genetic adaptive systems." *Dissertation, University of Michigan*.

- Spall, J. C. (2005). *Introduction to Stochastic Search and Optimization: Estimation, Simulation, and Control*. Wiley.

- Hansen, N., & Ostermeier, A. (2001). "Completely derandomized self-adaptation in evolution strategies." *Evolutionary Computation*, 9(2), 159–195.

### Modern Benchmarking

- Hansen, N., Auger, A., Finck, S., & Ros, R. (2016). "Real-parameter optimization benchmarking 2016: fun use of the COCO/BBOB tools and beyond." *CEC 2016 Companion*.

- Liang, J. J., Qu, B. Y., & Suganthan, P. N. (2013). "Problem definitions and evaluation criteria for the CEC2013 special session on real-parameter optimization." *Computational Intelligence Laboratory*.

---

## See Also

- [Benchmark API Reference](../reference/benchmarks.md)
- [Statistical Testing Theory](statistical-testing.md)
- [Algorithm Reference](../reference/index.md)
