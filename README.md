# evolutionary-benchmarking

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: GLP-3](https://img.shields.io/badge/license-GNU%20GPLv3-brightgreen)](https://www.gnu.org/licenses/gpl-3.0.html)
[![PyPI version](https://img.shields.io/badge/PyPI-v0.1.0-brightgreen.svg)](https://pypi.org/project/evobench/)
[![Documentation](https://img.shields.io/badge/docs-available-blue.svg)](https://evobench.readthedocs.io/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/NewtonGomez/evolutionary-benchmarking)

---

## Overview

**evobench** is a lightweight, standards-based library for benchmarking evolutionary algorithms and metaheuristics. It addresses the critical gap in scientific rigor when validating custom algorithm implementations by providing:

- **Native baseline implementations** of industry-standard metaheuristics (EDA, PSO, ABC)
- **Automated experiment orchestration** over classical continuous optimization benchmarks
- **Rigorous statistical analysis** tools for hypothesis testing and convergence evaluation
- **Reproducibility guarantees** through standardized experimental protocols

Whether you're developing a novel evolutionary strategy or comparing existing methods, evobench ensures your experimental results are scientifically sound, statistically valid, and directly comparable across different implementations.

### Why evobench?

The scientific literature on evolutionary computation suffers from inconsistencies in experimental methodology:
- Different research groups use different benchmark functions with varying dimensionalities
- Hyperparameter configurations are often incompletely specified
- Statistical significance is rarely established through rigorous testing
- Convergence behavior is rarely analyzed beyond point estimates

**evobench eliminates these issues** by enforcing standardized experimental protocols, enabling the global research community to perform fair algorithmic comparisons.

---

## Key Features

### Standardized Benchmarking
- Classical continuous optimization functions (Ackley, Rosenbrock, Sphere, Schwefel 1.2, Trid)
- Configurable problem dimensions and search space bounds
- Deterministic initialization and reproducible random number generation

### Native Algorithm Baseline
- **Estimation of Distribution Algorithm (EDA)**: probabilistic model-based search
- **Particle Swarm Optimization (PSO)**: velocity-based population dynamics
- **Artificial Bee Colony (ABC)**: swarm intelligence with three behavioral phases
- All implementations fully vectorized with NumPy for computational efficiency

### Experiment Engine
- Single configuration dictionary for complex multi-algorithm, multi-benchmark studies
- Automatic execution of independent runs with timing and convergence tracking
- JSON-based result persistence for post-hoc analysis
- System metadata capture for reproducibility

### Statistical Analysis
- Fitness vector extraction and organization for arbitrary algorithm combinations
- Parametric (ANOVA) and non-parametric (Kruskal-Wallis) significance testing
- Colored ANSI reporting with dynamic α support for customized significance levels
- Convergence curve visualization and statistical reporting
- Effect size computation (Cohen's d) for practical significance assessment

---

## Installation

### From PyPI (Recommended)

```bash
pip install evobench-lib
```

### From Source

```bash
git clone https://github.com/NewtonGomez/evolutionary-benchmarking.git
cd evobench
pip install -e .
```

### Requirements

- Python 3.8+
- NumPy >= 1.19.0
- SciPy >= 1.5.0 (for statistical tests)

---

## [Quickstart](docs/SETUP_CONFIG.md)

### 1. Define Your Custom Algorithm

Create a class inheriting from `EvolutionaryAlgorithm`:

```python
import numpy as np
from evobench.base import EvolutionaryAlgorithm

class MyCustomAlgorithm(EvolutionaryAlgorithm):
    """
    A simple evolutionary strategy for demonstration.
    """
    def __init__(self, objective_function, bounds, population_size=50, 
                 max_iterations=100, learning_rate=0.1):
        super().__init__(objective_function, bounds, population_size, max_iterations)
        self.learning_rate = learning_rate
    
    def run(self):
        """Execute the custom algorithm."""
        population = self._initialize_population()
        
        for generation in range(self.max_iterations):
            # Evaluate fitness
            fitness_values = np.array([
                self.objective_function(ind) for ind in population
            ])
            
            # Track best solution
            best_idx = np.argmin(fitness_values)
            if fitness_values[best_idx] < self.best_fitness:
                self.best_individual = population[best_idx].copy()
                self.best_fitness = fitness_values[best_idx]
            
            self.fitness_history.append(self.best_fitness)
            
            # Simple update: move towards best solution
            best_solution = population[best_idx]
            population += self.learning_rate * (best_solution - population)
            
            # Enforce boundaries
            lower_bounds = self.bounds[:, 0]
            upper_bounds = self.bounds[:, 1]
            population = np.clip(population, lower_bounds, upper_bounds)
        
        return self.best_individual, self.best_fitness
```

### 2. Configure and Run Experiments

```python
import numpy as np
from evobench.benchmarks import sphere, ackley
from evobench.algorithms import PSO, EDA, ABC
from evobench.tools.experiment_engine import run_automated_experiment
from my_algorithm import MyCustomAlgorithm

# Define experiment configuration
experiment_config = {
    "dimensions": 10,
    "population_size": 50,
    "max_iterations": 100,
    "independent_runs": 20,  # 20 independent trials per algorithm-benchmark pair
    
    "benchmarks": [
        {
            "name": "Sphere",
            "func": sphere,
            "bounds": [[-600, 600]] * 10
        },
        {
            "name": "Ackley",
            "func": ackley,
            "bounds": [[-10, 10]] * 10
        }
    ],
    
    "algorithms": [
        {
            "name": "PSO",
            "class": PSO,
            "params": {"inertia_weight": 0.7, "cognitive_coeff": 1.5, "social_coeff": 1.5}
        },
        {
            "name": "EDA",
            "class": EDA,
            "params": {"elite_fraction": 0.2, "variance_fraction": 0.1}
        },
        {
            "name": "ABC",
            "class": ABC,
            "params": {"limit": 50}
        },
        {
            "name": "Custom Algorithm",
            "class": MyCustomAlgorithm,
            "params": {"learning_rate": 0.05}
        }
    ]
}

# Execute the experiment
run_automated_experiment(experiment_config, output_file="results.json")
```

### 3. Analyze Results Statistically

```python
from evobench.tools.experiment_engine import unpack_fitness_results
from evobench.stats import analyze, stat_report

# Load experimental results and extract fitness vectors for a specific benchmark
fitness_dict = unpack_fitness_results("results.json", "Sphere")
# Extract the algorithm names and their corresponding fitness arrays.
algo_names = list(fitness_dict.keys())
fitness_data = list(fitness_dict.values())
# Run the statistical analysis.
# The 'analyze' function will calculate descriptive stats, run normality checks, 
# and execute the appropriate hypothesis test. You can optionally adjust 'alpha' (default: 0.05).
result_dict = analyze("Sphere Function (10D)", fitness_data, algo_names, alpha=0.05)
# Print the beautifully formatted, color-coded performance report (ANSI colors).
stat_report(result_dict)
```

**Output:**
```
Algorithm Performance on Sphere Function 
============================================================

PSO:
  Mean fitness:     1.24e-02
  Std deviation:    8.63e-03
  Best result:      2.41e-03

EDA:
  Mean fitness:     3.15e-02
  Std deviation:    1.92e-02
  Best result:      8.77e-03

ABC:
  Mean fitness:     2.87e-02
  Std deviation:    1.54e-02
  Best result:      6.23e-03

Custom Algorithm:
  Mean fitness:     5.42e-02
  Std deviation:    3.21e-02
  Best result:      1.52e-02

============================================================
ANOVA Test Results:
  F-statistic:      18.523
  p-value:          2.31e-10
  Significant:      Yes (α=0.05)
```

---

## Project Structure

```
evobench/
├── src/evobench/
│   ├── __init__.py                # Facade: exposes main APIs
│   ├── base.py                    # Abstract base class for evolutionary algorithms
│   ├── algorithms/
│   │   ├── __init__.py            # Facade: PSO, EDA, ABC
│   │   ├── eda.py                 # Estimation of Distribution Algorithm
│   │   ├── pso.py                 # Particle Swarm Optimization
│   │   └── bee.py                 # Artificial Bee Colony
│   ├── benchmarks/                # Benchmark function modules
│   │   ├── __init__.py            # Facade: sphere, ackley, rosenbrock, schwefel, trid
│   │   ├── unimodal.py            # Unimodal functions (sphere, rosenbrock, schwefel, trid)
│   │   └── multimodal.py          # Multimodal functions (ackley)
│   ├── stats/                     # Statistical analysis tools
│   │   ├── __init__.py            # Facade: analyze, stat_report
│   │   ├── core_test.py           # Normality and hypothesis tests
│   │   ├── reporter.py            # Colored ANSI reporting
│   │   └── analyzer.py            # Fitness data analysis
│   └── tools/
│       ├── __init__.py
│       ├── operators.py           # Genetic operators (selection, crossover, mutation)
│       └── experiment_engine.py   # Automated experiment orchestration
├── tests/
│   ├── __init__.py
│   ├── test_base.py              # Unit tests for base class
│   ├── test_operators.py         # Operator validation
│   └── test_benchmarks.py        # Benchmark function correctness
├── docs/                          # Sphinx/MkDocs documentation
├── README.md
├── LICENSE
├── pyproject.toml
└── CONTRIBUTING.md
```

---

## Usage Patterns

### Pattern 1: Comparing Two Algorithms on a Single Benchmark

To see all the benchmark functions, [click here](docs/benchmarks.md).

```python
from evobench.algorithms import PSO, ABC
from evobench.benchmarks import rosenbrock
from evobench.tools.experiment_engine import run_automated_experiment

config = {
    "dimensions": 5,
    "population_size": 30,
    "max_iterations": 50,
    "independent_runs": 10,
    "benchmarks": [
        {
            "name": "Rosenbrock",
            "func": rosenbrock,
            "bounds": [[-10, 10]] * 5
        }
    ],
    "algorithms": [
        {"name": "PSO", "class": PSO, "params": {}},
        {"name": "ABC", "class": ABC, "params": {}}
    ]
}

run_automated_experiment(config)
```

### Pattern 2: Parameter Sensitivity Analysis

```python
# Test how PSO performance varies with inertia weight
inertia_weights = [0.5, 0.7, 0.9]

for w in inertia_weights:
    config = {
        "dimensions": 10,
        "population_size": 50,
        "max_iterations": 100,
        "independent_runs": 15,
        "benchmarks": [...],
        "algorithms": [
            {
                "name": f"PSO (w={w})",
                "class": PSO,
                "params": {"inertia_weight": w}
            }
        ]
    }
    run_automated_experiment(config, output_file=f"pso_sensitivity_w{w}.json")
```

### Pattern 3: Validating Custom Algorithm Implementation

```python
from evobench.algorithms import PSO
from my_algorithms import MyNovelAlgorithm

# Test that your algorithm performs at least comparably to known baseline
config = {
    "dimensions": 10,
    "population_size": 50,
    "max_iterations": 100,
    "independent_runs": 30,  # Higher number for statistical power
    "benchmarks": [
        {"name": "Sphere", "func": sphere_function, "bounds": [[-600, 600]] * 10},
        {"name": "Ackley", "func": ackley_function, "bounds": [[-10, 10]] * 10},
    ],
    "algorithms": [
        {"name": "PSO Baseline", "class": PSO, "params": {}},
        {"name": "My Algorithm", "class": MyNovelAlgorithm, "params": {}}
    ]
}

run_automated_experiment(config, output_file="validation_results.json")
```

---

## API Reference

### Core Classes

#### `EvolutionaryAlgorithm` (Abstract Base Class)

All algorithms must inherit from this class:

```python
class EvolutionaryAlgorithm(ABC):
    def __init__(self, objective_function: Callable, bounds: List, 
                 population_size: int = 50, max_iterations: int = 100):
        """Initialize the algorithm with common parameters."""
        
    @abstractmethod
    def run(self) -> Tuple[np.ndarray, float]:
        """Execute the algorithm and return best solution and fitness."""
```

### [Benchmark Functions](docs/BENCHMARKS.md)

All functions have signature `fn(x: np.ndarray) -> float`:

- `sphere(x)`: Convex, unimodal baseline
- `rosenbrock(x)`: Non-convex valley topology
- `ackley(x)`: Multimodal with shallow exterior
- `schwefel(x)`: Non-separable, quadratic
- `trid(x)`: Highly interdependent variables

### Experiment Engine

```python
run_automated_experiment(config: Dict[str, Any], 
                        output_file: str = "results.json") -> None:
    """Execute a full benchmark experiment."""

unpack_fitness_results(json_path: str, 
                       target_function: str) -> Dict[str, np.ndarray]:
    """Extract and organize fitness vectors from results JSON."""
```

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on:
- Code style (PEP 8)
- Testing requirements
- Documentation standards
- Pull request process

---

## Citation

If you use evobench in your research, please cite:

```bibtex
@software{evobench2026,
  title={evobench: Standardized Benchmarking for Evolutionary Algorithms},
  author={Gómez, Enrique and Galván, Victoria},
  year={2026},
  url={https://github.com/NewtonGomez/evolutionary-benchmarking}
}
```

---

## Known Limitations

- Current implementation focuses on continuous optimization only (no discrete/combinatorial problems)
- Benchmark functions are limited to 1000-dimensional spaces for numerical stability
- Statistical tests currently assume normal distribution of fitness values
- DEAP integration and third-party operator libraries are planned for future releases

---

## License

This project is licensed under the GPL-3 License. See [LICENSE](LICENSE) file for details.

---

## Support

For bug reports and feature requests, please open an issue on [GitHub](https://github.com/NewtonGomez/evolutionary-benchmarking/issues).

For questions and discussions, visit our [Discussions Forum](https://github.com/NewtonGomez/evolutionary-benchmarking/discussions).

---

## Acknowledgments

- NumPy and SciPy communities for foundational numerical computing tools
- Continuous optimization research community for standardized benchmark functions
- Academic advisors and collaborators who influenced the design philosophy

---

**Last Updated**: April 2026  
**Version**: 0.1.0  
**Authors**:
- Enrique Gómez ([GitHub](https://github.com/NewtonGomez), [Email](mailto:ing.enrique_gomez@outlook.com))
- Victoria Galván ([GitHub](https://github.com/galvandvictoria-alt), [Email](mailto:galvand.victoria@gmail.com))
