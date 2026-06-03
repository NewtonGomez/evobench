# Glossary of Evolutionary Computation Terms

This glossary provides formal definitions of terminology used throughout evobench and the broader field of evolutionary computation. This is designed to be accessible to newcomers while maintaining scientific rigor for researchers.

---

## A

### Algorithm
A step-by-step procedure for solving a problem. In evolutionary computation, an algorithm specifies the sequence of operations (initialization, evaluation, selection, variation, replacement) applied to a population of candidate solutions.

### Artificial Bee Colony (ABC)
A swarm intelligence metaheuristic inspired by the foraging behavior of honeybees. The population is divided into three types: **employed bees** (exploiting known solutions), **onlooker bees** (probabilistically selecting solutions based on quality), and **scout bees** (exploring new regions). See [reference/algorithms/abc.md](../reference/algorithms/abc.md).

### Attraction
In swarm intelligence, the tendency of particles or agents to move toward promising solutions. In PSO, particles are attracted to their **personal best** and the **global best**.

---

## B

### Benchmark Function
A mathematical function used to evaluate algorithm performance. Benchmark functions have known properties (global optimum, landscape structure) that allow rigorous comparison. Examples: Sphere, Ackley, Rosenbrock. See [reference/benchmarks.md](../reference/benchmarks.md).

### Bounds
The acceptable range of values for each decision variable. Typically expressed as $[\mathbf{L}, \mathbf{U}]$ where $L_i$ and $U_i$ are lower and upper limits for dimension $i$. Also called **search domain** or **feasible region**.

Example: `bounds = [(-5, 5)] * 10` for a 10-dimensional problem with each variable in $[-5, 5]$.

---

## C

### Cognitive Component
In PSO, the term modeling the particle's attraction to its own personal best solution. Controlled by the **cognitive parameter** $c_1$. Represents the particle's "memory" of past success.

### Convergence
The process by which a population transitions from diversity (exploring the search space) to homogeneity (concentrating around promising regions). Ideally, convergence leads to the global optimum or a high-quality solution.

### Convergence Curve
A plot of fitness over generations, showing how algorithm performance improves (or stagnates) over time. Also called **convergence trajectory** or **fitness history**.

### Convexity
A property of a function where any line segment between two points on the function lies above the function curve. Convex functions have a single global minimum; non-convex functions may have local minima.

---

## D

### Dimension
The number of decision variables in an optimization problem. A 10-dimensional problem has 10 variables to optimize. Also called **problem dimensionality** or **problem size**.

### Distribution (Probabilistic)
In model-based algorithms like EDA, a probability distribution (typically Gaussian) estimated from elite solutions and used to generate new candidates. Allows systematic exploration of promising regions.

---

## E

### Elitism
A selection strategy that guarantees the best solution(s) found so far are preserved in the population for future generations. Ensures monotonic (non-decreasing) fitness improvement.

### Estimation of Distribution Algorithm (EDA)
A model-based evolutionary algorithm that estimates a probabilistic distribution from elite solutions and samples new candidates from this distribution. Unlike traditional GA, it doesn't use explicit crossover/mutation. See [reference/algorithms/eda.md](../reference/algorithms/eda.md).

### Evolutionary Algorithm (EA)
A population-based metaheuristic inspired by Darwinian evolution. Uses mechanisms of **selection**, **variation** (mutation/crossover), and **replacement** to evolve a population toward optimal solutions.

### Exploitation
The process of intensively searching within a promising region. Exploitation refines solutions but may converge prematurely to local optima. Opposite of **exploration**.

### Exploration
The process of sampling diverse regions of the search space. Exploration discovers new promising areas but may miss local refinements. Opposite of **exploitation**.

---

## F

### Fitness
A scalar value quantifying how well a candidate solution solves the problem. Algorithms minimize (or maximize) fitness. In evobench, fitness is always **minimized**.

### Fitness Function
See **objective function**.

### Fitness History
A list of the best fitness values found at each generation, tracked during optimization. Used for analysis and visualization of convergence behavior.

---

## G

### Generation
One complete cycle of the evolutionary algorithm: evaluation of all individuals, selection, variation (mutation/crossover), and replacement. Also called **iteration**.

### Genetic Algorithm (GA)
A traditional evolutionary algorithm using **crossover** (recombination of parent solutions) and **mutation** (random perturbation) as variation operators. Originally designed for discrete/binary problems.

### Global Best
The best solution found by the entire population. In PSO and some variants of ABC, particles/bees are attracted to this global reference point. Also called **global optimum** (if it's the true optimum) or **population best**.

### Global Optimum
The absolute best solution to an optimization problem, theoretically achieving the minimum (or maximum) objective function value. See $\mathbf{x}^*$ in mathematical notation.

---

## H

### Hyperparameter
A parameter that controls algorithm behavior, set by the user before optimization. Examples in evobench:
- `population_size`: Number of individuals
- `max_iterations`: Number of generations
- `inertia_weight` (PSO): Momentum control
- `selection_ratio` (EDA): Fraction of elite solutions

---

## I

### Inertia Weight
In PSO, a coefficient $w$ that controls the influence of previous velocity on future movement. High inertia (w > 0.7) encourages exploration; low inertia (w < 0.4) encourages exploitation.

### Individual
A single candidate solution in a population. Represented as a vector of decision variables $\mathbf{x} = [x_1, x_2, \ldots, x_d]$.

---

## J

### (No standard EA terms starting with J)

---

## K

### K-means Clustering
A clustering algorithm sometimes used to partition populations in niching strategies, maintaining diversity by partitioning the population into subgroups that optimize different regions.

---

## L

### Landscape
The geometric structure of an objective function's fitness values across the search space. Key properties include **modality** (number of local minima), **separability** (independence of variables), and **convexity**.

### Learning Rate
In continuous optimization, a parameter controlling the step size of solution updates. High learning rates enable rapid movement but risk overshooting; low learning rates enable fine-tuning but converge slowly.

### Limit (ABC Specific)
In ABC, the maximum number of unsuccessful trial improvements allowed before a food source (candidate solution) is abandoned by a scout bee. See [reference/algorithms/abc.md](../reference/algorithms/abc.md).

### Local Best / Personal Best
In PSO, the best solution ever found by an individual particle. Each particle maintains memory of $pbest_i$ and is attracted toward it.

### Local Optimum
A solution better than all nearby solutions but not globally optimal. Local optima are "traps" that algorithms may converge to prematurely. See **multimodal**.

---

## M

### Metaheuristic
A high-level algorithmic framework for solving difficult optimization problems. Metaheuristics (PSO, GA, SA, etc.) provide general-purpose problem-solving strategies without problem-specific knowledge.

### Modality
The number of local minima in a function. **Unimodal**: single global minimum (no local traps). **Multimodal**: multiple local minima (challenging for algorithms).

### Mutation
A variation operator that randomly perturbs a solution. In continuous spaces, mutation often adds Gaussian noise: $\mathbf{x}' = \mathbf{x} + \mathcal{N}(0, \sigma^2)$.

---

## N

### Niche / Niching
A population strategy that maintains diversity by partitioning the population into subgroups that specialize in different regions. Helps escape local optima.

### Non-separable / Non-separability
A function property where variables interact (cannot be optimized independently). Non-separable functions are harder because changing one variable affects the fitness impact of changing others. See **separability**.

---

## O

### Objective Function
The mathematical function being optimized. In evobench, this is the `objective_function` passed to algorithms. Algorithms minimize this function.

Example:
```python
def sphere(x):
    """Objective function (Sphere)."""
    return float(np.sum(x**2))
```

### Optimum / Optimal
The best solution to an optimization problem, achieving the minimum (minimum problem) or maximum (maximum problem) objective function value. See **global optimum** and **local optimum**.

### Optimization
The process of finding the best (or near-best) solution to a problem. Evolutionary algorithms are one approach to black-box optimization.

---

## P

### Parameter Tuning / Hyperparameter Optimization
The process of selecting appropriate algorithm hyperparameters for a specific problem. Example: choosing `inertia_weight=0.9` vs. `0.4` for PSO.

### Particle (PSO Specific)
In PSO, an individual candidate solution. The term "particle" emphasizes movement through the solution space (velocity-based updates).

### Particle Swarm Optimization (PSO)
A swarm intelligence metaheuristic inspired by bird flocking. Each particle moves through the search space influenced by its velocity, personal best, and the global best. See [reference/algorithms/pso.md](../reference/algorithms/pso.md).

### Population
The set of candidate solutions maintained by the algorithm. In evobench, represented as a matrix of shape (population_size, dimension).

### Population-based
An algorithm that maintains and evolves a population of solutions (as opposed to single-solution methods like local search or simulated annealing).

### Post-hoc Test
A statistical test applied after a primary hypothesis test (e.g., ANOVA) to identify which groups differ. Common post-hoc tests: Tukey's HSD, Dunn's test.

---

## Q

### Quadratic
A mathematical function containing terms of degree 2, e.g., $f(x) = ax^2 + bx + c$. Quadratic functions (like Sphere) are unimodal and convex.

---

## R

### Registry (Pattern)
A design pattern for dynamically discovering and loading implementations. In evobench, `BENCHMARK_REGISTRY` is a dictionary mapping benchmark names to functions, enabling configuration-driven access without hardcoding imports.

### Replacement Strategy
The mechanism for deciding which individuals survive to the next generation. Common strategies: **elitism** (keep best), **tournament selection** (probabilistic selection based on fitness), **truncation** (keep top-ranked).

### Reproducibility
The ability to obtain identical results by rerunning an experiment with the same seed and code. Essential for scientific validity and debugging.

---

## S

### Search Domain
The feasible region of the optimization problem, defined by **bounds** on each variable. Also called **search space** or **feasible region**.

### Search Space
See **search domain**.

### Separability
A function property where variables can be optimized independently. Example: Sphere function $F(x) = \sum x_i^2$ is fully separable because each term depends on only one variable.

### Selection
The mechanism for choosing which individuals become parents for the next generation. Fitness-better individuals have higher probability of selection. Common methods: **tournament**, **fitness-proportional**, **rank-based**.

### Selection Pressure
The strength of selection—how strongly the algorithm favors better solutions. High pressure accelerates convergence but risks premature termination. Low pressure maintains diversity but converges slowly.

### Selection Ratio (EDA Specific)
In EDA, the fraction of the population selected as elite for estimating the probabilistic distribution. Higher ratio = weaker selection = more diversity. See [reference/algorithms/eda.md](../reference/algorithms/eda.md).

### Significant / Significance (Statistical)
A statistical result is significant (at level $\alpha = 0.05$) if the p-value is less than $\alpha$. Indicates that observed differences are unlikely due to random chance.

### Social Component (PSO Specific)
In PSO, the term modeling the particle's attraction to the global best solution (population consensus). Controlled by the **social parameter** $c_2$. Represents "following the swarm."

### Stagnation
Lack of improvement in fitness over multiple generations. Indicates the algorithm has converged (reached a local/global optimum) or is stuck (premature convergence).

### Stochastic
Involving randomness. Evolutionary algorithms are stochastic: same input + different random seed = different output.

---

## T

### Tournament Selection
A selection mechanism where a random subset (tournament) of individuals is chosen, and the best is selected. Tournament size controls selection pressure.

---

## U

### Unimodal
A function with a single global minimum and no local minima. Unimodal functions are easier to optimize because any improving move can be continued.

---

## V

### Variance / Standard Deviation
Statistical measures of spread. In experimental evaluation, high variance (large standard deviation) indicates inconsistent algorithm performance across runs.

### Variation Operators
Mechanisms for generating new solutions from existing ones. Common operators: **mutation** (perturbation), **crossover** (recombination).

### Velocity (PSO Specific)
In PSO, a vector representing the direction and magnitude of particle movement. Updated as: $v_i^{t+1} = w \cdot v_i^t + c_1 r_1 (pbest_i - x_i^t) + c_2 r_2 (gbest - x_i^t)$.

---

## W

### Weighted Average / Weighted Selection
In tournament selection or fitness-proportional selection, solutions are chosen with probability proportional to their fitness (or rank). Better solutions are "weighted" more heavily.

---

## X

### (No standard EA terms starting with X)

---

## Y

### (No standard EA terms starting with Y)

---

## Z

### (No standard EA terms starting with Z)

---

## Notation Reference

| Symbol | Meaning |
|--------|---------|
| $\mathbf{x}$ | A candidate solution vector |
| $\mathbf{x}^*$ | The global optimum |
| $f(\mathbf{x})$ | Fitness of solution $\mathbf{x}$ |
| $d$ | Problem dimensionality |
| $N$ | Population size |
| $t$ | Generation/iteration counter |
| $w$ | Inertia weight (PSO) |
| $c_1, c_2$ | Cognitive and social parameters (PSO) |
| $p_i$ | Personal best of particle $i$ (PSO) |
| $g$ | Global best (PSO) |
| $v_i$ | Velocity of particle $i$ (PSO) |
| $\alpha$ | Significance level (typically 0.05) |
| $p$ | p-value from hypothesis test |
| $\mu$ | Mean of a distribution |
| $\sigma$ | Standard deviation |

---

## References and Further Reading

### Classic Papers
- Dorigo, M., & Blum, C. (2005). "Ant Colony Optimization Theory." *Theoretical Computer Science*. (Foundation of metaheuristics)
- Kennedy, J., & Eberhart, R. (1995). "Particle Swarm Optimization." *Proceedings of ICNN*. (Original PSO)
- Karaboga, D. (2005). "An Idea Based on Honey Bee Swarm for Numerical Optimization." (ABC algorithm)

### Benchmark Functions
- Suganthan, P. N., et al. (2005). "Problem Definitions and Evaluation Criteria for the CEC 2005." *Technical Report*. (Standard benchmark suite)

### Statistical Testing
- Wilcoxon, F. (1945). "Individual Comparisons by Ranking Methods." *Biometrics*. (Non-parametric testing)
- Tukey, J. W. (1949). "Comparing Individual Means in the Analysis of Variance." *Biometrics*. (Post-hoc testing)

---

**Last Updated**: June 2026  
**evobench**: 0.1.0
