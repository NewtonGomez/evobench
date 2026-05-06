# Estimation of Distribution Algorithm (EDA)

## Overview

**Estimation of Distribution Algorithm** is a model-based evolutionary approach that learns probabilistic models of promising regions in the search space and uses these models to generate new candidate solutions.

Unlike traditional evolutionary algorithms that explicitly apply variation operators (crossover, mutation), EDA learns statistical distributions from elite solutions and samples new candidates by drawing from these distributions. This provides systematic exploration with strong theoretical grounding in statistical learning.

**Location**: `evobench.algorithms.EDA`

**Inspiration**: Probabilistic learning from population structure

**Key Characteristic**: Model-based generation of candidate solutions through learned distributions

---

## Algorithm Characteristics

| Property | Value |
|----------|-------|
| **Population Type** | Continuous real vectors |
| **Learning Mechanism** | Gaussian distribution estimation |
| **Selection Strategy** | Tournament selection of elite individuals |
| **Exploration Bias** | High (diverse sampling from model) |
| **Exploitation Bias** | Moderate (model concentrates on promising regions) |
| **Computational Complexity** | $O(n \cdot d^2)$ per iteration (quadratic in dimension for covariance) |
| **Convergence Pattern** | Steady, gradual |

---

## Mathematical Formulation

### Core Components

#### 1. Elite Selection via Tournament

Tournament selection identifies $\tau$ elite individuals from the population of $N$ individuals. For each tournament round:

$$\text{winner} = \arg\min_{i \in \text{random sample}} f(x_i)$$

where $f(x_i)$ is the fitness of individual $i$.

#### 2. Gaussian Model Estimation

From elite solutions $\{x_1^{\text{elite}}, \ldots, x_{\tau}^{\text{elite}}\}$, estimate mean and covariance:

$$\boldsymbol{\mu} = \frac{1}{\tau} \sum_{k=1}^{\tau} \mathbf{x}_k^{\text{elite}}$$

$$\boldsymbol{\Sigma} = \frac{1}{\tau} \sum_{k=1}^{\tau} (\mathbf{x}_k^{\text{elite}} - \boldsymbol{\mu})(\mathbf{x}_k^{\text{elite}} - \boldsymbol{\mu})^T$$

#### 3. Sampling New Population

Generate new candidates by sampling from the learned multivariate Gaussian:

$$\mathbf{x}_i^{\text{new}} \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$$

Applied element-wise for efficiency (univariate approximation):

$$x_{i,j}^{\text{new}} \sim \mathcal{N}(\mu_j, \sigma_j^2)$$

#### 4. Boundary Constraints

New candidates are clipped to satisfy search domain constraints:

$$x_{i,j}^{\text{new}} = \text{clip}(x_{i,j}^{\text{new}}, L_j, U_j)$$

---

## Constructor

### Signature

```python
class EDA(EvolutionaryAlgorithm):
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
| `bounds` | `List[Tuple[float, float]]` | Required | Search domain boundaries; list of `(lower, upper)` tuples |
| `population_size` | `int` | 50 | Population size (number of individuals) |
| `max_iterations` | `int` | 100 | Maximum number of generations |

### Inherited Attributes

From `EvolutionaryAlgorithm`:

- `objective_function`: Reference to benchmark function
- `bounds`: Search space boundaries
- `population_size`: Number of individuals
- `max_iterations`: Iteration budget
- `dimension`: Problem dimensionality
- `best_individual`: Best solution found
- `best_fitness`: Fitness of best solution
- `fitness_history`: Best fitness per generation

---

## Hyperparameters

EDA's behavior is controlled by the **elite ratio**, determining how many individuals contribute to model estimation.

### Default Configuration

```python
elite_ratio = 0.2             # Fraction of population used for model
elite_size = int(population_size * elite_ratio)  # ~10 individuals per 50
```

### Effect on Behavior

- **Small elite ratio (~0.1)**: Faster convergence, risk of premature convergence
- **Large elite ratio (~0.5)**: Slower convergence, better exploration
- **Default (0.2)**: Balanced compromise

---

## Algorithm Flow

### Pseudocode

```
Algorithm: EDA (Estimation of Distribution Algorithm)
Input: objective_function, bounds, population_size, max_iterations
Output: best_individual, best_fitness

1. Initialize population randomly within bounds
2. Evaluate all individuals
3. Identify global best
4. 
5. For generation = 1 to max_iterations:
    6. Select elite individuals via tournament selection
    7. Estimate Gaussian model (mean and covariance) from elite
    8. Generate new population by sampling from model
    9. Apply boundary constraints to new population
    10. Evaluate new population
    11. Update global best if improvement found
    12. Record best fitness in fitness_history
13. 
14. Return best_individual, best_fitness
```

### Detailed Iteration Logic

```python
def run(self):
    population = self._initialize_population()
    fitness = np.array([self.objective_function(ind) for ind in population])
    
    self.best_individual = population[np.argmin(fitness)].copy()
    self.best_fitness = np.min(fitness)
    
    for generation in range(self.max_iterations):
        # Step 1: Tournament selection for elite
        elite_indices = self._tournament_selection(fitness)
        elite = population[elite_indices]
        
        # Step 2: Estimate Gaussian model
        mean = np.mean(elite, axis=0)
        std = np.std(elite, axis=0) + 1e-8  # Avoid zero variance
        
        # Step 3: Sample new population
        population = np.zeros_like(population)
        for i in range(self.population_size):
            for d in range(self.dimension):
                population[i, d] = np.random.normal(mean[d], std[d])
        
        # Step 4: Apply boundary constraints
        population = self._apply_boundary_constraints(population)
        
        # Step 5: Evaluate and update
        fitness = np.array([self.objective_function(ind) for ind in population])
        
        best_idx = np.argmin(fitness)
        if fitness[best_idx] < self.best_fitness:
            self.best_fitness = fitness[best_idx]
            self.best_individual = population[best_idx].copy()
        
        self.fitness_history.append(self.best_fitness)
    
    return self.best_individual, self.best_fitness
```

---

## Usage Examples

### Basic Optimization

```python
from evobench.algorithms import EDA
from evobench.benchmarks import schwefel

# Define search domain
bounds = [(-100, 100)] * 10

# Create EDA instance
optimizer = EDA(
    objective_function=schwefel,
    bounds=bounds,
    population_size=40,
    max_iterations=150
)

# Run optimization
best_solution, best_fitness = optimizer.run()

print(f"Best Fitness: {best_fitness:.6f}")
print(f"Solution: {best_solution}")
```

### Convergence Comparison with PSO

```python
import matplotlib.pyplot as plt
import numpy as np
from evobench.algorithms import EDA, PSO
from evobench.benchmarks import ackley

bounds = [(-32.768, 32.768)] * 8

# Run both algorithms
eda_opt = EDA(ackley, bounds, max_iterations=500)
pso_opt = PSO(ackley, bounds, max_iterations=500)

eda_opt.run()
pso_opt.run()

# Plot convergence
plt.figure(figsize=(12, 6))
plt.semilogy(eda_opt.fitness_history, 'r-', label='EDA', linewidth=2)
plt.semilogy(pso_opt.fitness_history, 'b-', label='PSO', linewidth=2)
plt.xlabel('Generation')
plt.ylabel('Best Fitness (log scale)')
plt.title('EDA vs PSO Convergence on Ackley Function')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### Multiple Runs with Analysis

```python
import numpy as np
from evobench.algorithms import EDA
from evobench.benchmarks import trid

bounds = [(-400, 400)] * 10
num_runs = 30

results = []
convergence_curves = []

for run in range(num_runs):
    optimizer = EDA(trid, bounds, max_iterations=300)
    _, best_fit = optimizer.run()
    results.append(best_fit)
    convergence_curves.append(optimizer.fitness_history)

# Summary statistics
print(f"Mean Fitness: {np.mean(results):.6f}")
print(f"Median Fitness: {np.median(results):.6f}")
print(f"Std Dev: {np.std(results):.6f}")
print(f"Min Fitness: {np.min(results):.6f}")
print(f"Max Fitness: {np.max(results):.6f}")

# Average convergence curve
avg_convergence = np.mean(convergence_curves, axis=0)
plt.figure(figsize=(10, 6))
plt.semilogy(avg_convergence, 'g-', linewidth=2)
plt.xlabel('Generation')
plt.ylabel('Best Fitness (log scale)')
plt.title('EDA Average Convergence over 30 Runs')
plt.grid(True, alpha=0.3)
plt.show()
```

### Non-Separable Problem Advantage

```python
from evobench.algorithms import EDA, PSO
from evobench.stats import analyze, stat_report

# Rosenbrock: non-separable, valley-shaped
bounds = [(-2.048, 2.048)] * 5

eda_results = [EDA(rosenbrock, bounds).run()[1] for _ in range(30)]
pso_results = [PSO(rosenbrock, bounds).run()[1] for _ in range(30)]

analysis = analyze(
    func_name="rosenbrock",
    result_list=[eda_results, pso_results],
    algorithm_names=["EDA", "PSO"],
    alpha=0.05
)

print(stat_report(analysis))
```

---

## Strengths & Weaknesses

### ✓ Strengths

| Advantage | Description |
|-----------|-------------|
| **Non-Separable Problems** | Excellent on problems with variable dependencies |
| **Robust Exploration** | Systematic sampling prevents premature convergence |
| **Model Interpretability** | Learned distributions reveal problem structure |
| **Diversity Maintenance** | Population diversity naturally preserved through sampling |
| **Scalability** | Works well as dimensionality increases (≥ 20D) |

### ✗ Weaknesses

| Limitation | Description |
|-----------|-------------|
| **Convergence Speed** | Generally slower than PSO on smooth landscapes |
| **Computational Cost** | Computing mean/covariance costs $O(n \cdot d^2)$ |
| **Multimodal Challenges** | Gaussian model may not capture multimodal structure |
| **Model Degeneracy** | Covariance matrix can become singular if population clusters |
| **Limited Exploitation** | Wide variance early on may slow convergence |

---

## Best Suited For

- ✓ **Non-separable optimization problems** (variables interact)
- ✓ **Problems with variable correlations**
- ✓ **Seeking diverse high-quality solutions**
- ✓ **High-dimensional continuous optimization**
- ✓ **Problems where model learning is valuable**

---

## Recommended Benchmark Functions

| Benchmark | Difficulty | Reason |
|-----------|-----------|--------|
| **Schwefel 1.2** | Medium | Fully coupled variables; tests dependency handling |
| **Trid** | High | Highly interdependent; structured correlations |
| **Ackley** | High | Multimodal; tests exploration robustness |

---

## Variant: Univariate Marginal Distribution Algorithm (UMDA)

The current implementation uses **univariate** Gaussian estimation (independent dimensions). The multivariate form (learning full covariance matrix) would capture variable correlations but increases computational cost from $O(n \cdot d)$ to $O(n \cdot d^2)$.

For high-dimensional problems, the univariate approximation is often preferable.

---

## Literature References

### Foundational Papers

1. **Mühlenbein, H., & Paass, G. (1996).** "From Recombination of Genes to the Estimation of Distributions I: Binary Parameters." *Lecture Notes in Computer Science*, 1141, 178–187.

2. **Larrañaga, P., & Lozano, J. A. (Eds.). (2002).** *Estimation of Distribution Algorithms: A New Tool for Evolutionary Computation*. Kluwer Academic Publishers.

3. **Larranaga, P., Etxeberria, R., Lozano, J. A., & Peña, J. M. (2000).** "Optimization in Continuous Domains by Learning and Simulating Gaussian Bayesian Networks." *IEEE Transactions on Evolutionary Computation*, 4(2), 120–130.

### Variants & Extensions

- Multivariate EDA (MEDA)
- Bayesian Optimization Algorithm (BOA)
- Real-coded EDA
- Adaptive EDA with dynamic elite ratio

---

## Comparison with PSO and ABC

| Aspect | EDA | PSO | ABC |
|--------|-----|-----|-----|
| **Model Type** | Probabilistic | Velocity-based | Bee phases |
| **Exploration** | Systematic sampling | Attracted to best | Probabilistic choice |
| **Non-Separable** | Excellent | Good | Moderate |
| **Multimodal** | Moderate | Moderate | Good |
| **Speed** | Moderate | Fast | Moderate |
| **Complexity** | $O(n \cdot d^2)$ | $O(n \cdot d)$ | $O(n \cdot d)$ |

---

## See Also

- [Algorithm Comparison](index.md)
- [Benchmark Functions](../benchmarks.md)
- [Statistical Analysis](../../theory/statistical-testing.md)
- [PSO Documentation](pso.md)
- [ABC Documentation](abc.md)
- [Base Class Documentation](../base.md)
