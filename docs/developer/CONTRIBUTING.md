# Contributing to evobench

Thank you for your interest in contributing to evobench! We welcome contributions from researchers, developers, and practitioners in the evolutionary computation community. This document outlines how to contribute effectively.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful of others' ideas and experiences. Harassment, discrimination, and disrespect will not be tolerated.

---

## Ways to Contribute

### 1. Reporting Bugs

Before opening a bug report, please check the [GitHub Issues](https://github.com/NewtonGomez/evobench/issues) to see if it has already been reported.

**When reporting a bug, include:**
- Clear, descriptive title
- Exact steps to reproduce the issue
- Expected vs. actual behavior
- Python version, OS, and evobench version
- Full traceback (if applicable)
- Screenshots or code samples

**Example:**
```
Title: PSO fails with bounds containing negative values

Steps to reproduce:
1. Create bounds = [[-10, -5], [-20, -10]]
2. Instantiate PSO with these bounds
3. Call run()

Expected: Algorithm executes normally
Actual: ValueError in _apply_boundary_constraints

Python: 3.9.0
OS: macOS 12.1
evobench: 0.1.0
Traceback: [full traceback here]
```

### 2. Suggesting Features

We encourage feature suggestions! Please open a GitHub Discussion or Issue with:
- Clear description of the proposed feature
- Use cases and benefits
- Example API (if applicable)
- Alternative approaches you've considered

**Note:** Before working on a major feature, please discuss it with maintainers first.

### 3. Improving Documentation

Documentation improvements are always welcome:
- Fixed typos, grammar, clarity issues
- Expanded examples
- Translated documentation to other languages
- Better mathematical notation

Simply open a Pull Request with your improvements.

### 4. Contributing Code

#### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/NewtonGomez/evobench.git
cd evobench

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

#### Code Style

We follow **PEP 8** strictly. Key points:

- **Indentation**: 4 spaces (never tabs)
- **Line length**: 100 characters (soft limit, hard limit 120)
- **Imports**: Group alphabetically; use `isort` for automatic sorting
- **Type hints**: Required for all public functions (PEP 484)
- **Docstrings**: Google style format

```python
def calculate_fitness(population: np.ndarray, objective_fn: Callable) -> np.ndarray:
    """
    Compute fitness values for all individuals in the population.
    
    Args:
        population (np.ndarray): Matrix of shape (population_size, dimensions).
        objective_fn (Callable): The fitness function to minimize.
    
    Returns:
        np.ndarray: Vector of fitness values.
    
    Raises:
        ValueError: If population is empty.
    
    Example:
        >>> pop = np.random.randn(10, 5)
        >>> fitness = calculate_fitness(pop, lambda x: np.sum(x**2))
    """
    if population.size == 0:
        raise ValueError("Population cannot be empty")
    
    fitness_values = np.array([objective_fn(ind) for ind in population])
    return fitness_values
```

#### Writing Tests

Tests are **mandatory** for all new code. Use pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=evobench --cov-report=term-missing

# Run specific test file
pytest tests/test_base.py

# Run specific test
pytest tests/test_base.py::test_abstract_enforcement
```

**Test Template:**
```python
import pytest
import numpy as np
from evobench.algorithms import PSO

def test_pso_convergence():
    """PSO should reduce fitness over generations."""
    from evobench.benchmarks import sphere_function
    
    bounds = [[-10, 10]] * 5
    pso = PSO(sphere_function, bounds, population_size=20, max_iterations=50)
    
    best_pos, best_fitness = pso.run()
    
    assert isinstance(best_pos, np.ndarray)
    assert len(best_pos) == 5
    assert best_fitness < 100  # Basic convergence check

def test_pso_boundary_constraints():
    """PSO individuals should remain within bounds."""
    from evobench.benchmarks import sphere_function
    
    bounds = [[-5, 5], [-10, 10], [-1, 1]]
    pso = PSO(sphere_function, bounds, population_size=10, max_iterations=5)
    
    best_pos, _ = pso.run()
    
    for i, (lower, upper) in enumerate(bounds):
        assert lower <= best_pos[i] <= upper
```

#### Before Submitting a Pull Request

1. **Format code** with `black` and `isort`:
   ```bash
   black evobench/
   isort evobench/
   ```

2. **Lint** with `flake8`:
   ```bash
   flake8 evobench/ tests/
   ```

3. **Type check** with `mypy`:
   ```bash
   mypy evobench/
   ```

4. **Run all tests**:
   ```bash
   pytest --cov=evobench
   ```

5. **Update documentation** if needed:
   - Add docstrings to new functions
   - Update existing docstrings if behavior changed
   - Add entries to CHANGELOG

### 5. Pull Request Process

1. **Fork the repository** and create a feature branch:
   ```bash
   git checkout -b feature/my-new-algorithm
   ```

2. **Make your changes** following the code style guidelines.

3. **Commit with clear messages**:
   ```bash
   git commit -m "feat(algorithms): add Genetic Algorithm implementation"
   ```
   
   Use conventional commit format:
   - `feat:` A new feature
   - `fix:` A bug fix
   - `refactor:` Code refactoring without functional change
   - `docs:` Documentation improvements
   - `test:` Adding or updating tests
   - `chore:` Build, CI, or dependency updates

4. **Push to your fork** and open a Pull Request:
   ```bash
   git push origin feature/my-new-algorithm
   ```

5. **PR Description** should include:
   - Closes #[issue number] (if fixing an issue)
   - Brief description of changes
   - Type of change (feature/bugfix/refactor)
   - Testing performed
   - Any breaking changes

6. **Wait for review** and address feedback.

---

## Adding New Components

### Adding a New Algorithm

1. **Create file** `src/evobench/algorithms/my_algorithm.py`:
   ```python
   import numpy as np
   from evobench.base import EvolutionaryAlgorithm
   
   class MyAlgorithm(EvolutionaryAlgorithm):
       """
       Brief description of My Algorithm.
       
       [Detailed explanation with references]
       """
       
       def __init__(self, objective_function, bounds, population_size=50,
                    max_iterations=100, **kwargs):
           super().__init__(objective_function, bounds, population_size, max_iterations)
           # Store algorithm-specific parameters
       
       def run(self):
           """Execute the algorithm."""
           population = self._initialize_population()
           
           for generation in range(self.max_iterations):
               # Your algorithm logic here
               pass
           
           return self.best_individual, self.best_fitness
   ```

2. **Add tests** in `tests/test_my_algorithm.py`:
   ```python
   from evobench.algorithms import MyAlgorithm
   from evobench.benchmarks import sphere_function
   
   def test_my_algorithm_runs():
       algo = MyAlgorithm(sphere_function, [[-10, 10]] * 5)
       best_pos, best_fit = algo.run()
       assert best_fit < float('inf')
   ```

3. **Export from `__init__.py`**:
   ```python
   # src/evobench/algorithms/__init__.py
   from .my_algorithm import MyAlgorithm
   ```

4. **Document** in `docs/reference/algorithms/my_algorithm.md`

5. **Add example** in `docs/examples/`

### Adding a New Benchmark Function

1. **Add to** `src/evobench/benchmarks.py`:
   ```python
   def my_benchmark_function(x: np.ndarray) -> float:
       """
       [Full mathematical description]
       
       Optimal value: F(x*) = 0
       Bounds: [-5, 5]
       
       Args:
           x: Candidate solution vector
       
       Returns:
           Fitness value (to be minimized)
       """
       return np.sum(x**2) + np.sum(np.sin(x))
   ```

2. **Add validation test** in `tests/test_benchmarks.py`:
   ```python
   def test_my_benchmark_at_optimum():
       optimal_solution = np.zeros(10)
       expected_fitness = 0.0
       actual_fitness = my_benchmark_function(optimal_solution)
       assert actual_fitness == pytest.approx(expected_fitness, abs=1e-9)
   ```

3. **Document** in docs with: formula, search domain, optimal point, difficulty level

---

## Development Tools & CI/CD

All pull requests automatically run:
- **Unit tests** via pytest
- **Code coverage** tracking (target: >90%)
- **Linting** via flake8
- **Type checking** via mypy
- **Documentation build** verification

These checks must pass before merging.

---

## Getting Help

- **Questions?** Open a GitHub Discussion
- **Need guidance?** Comment on an issue you're interested in
- **Found a bug?** Open a GitHub Issue with details
- **Want to chat?** Join the [Discussions Forum](https://github.com/NewtonGomez/evobench/discussions)

---

## Recognition

Contributors will be recognized in:
- Project README
- Release notes
- "Contributors" section of documentation
- GitHub Sponsors (if applicable)

---

## Thank You! 🙏

We deeply appreciate your contributions to making evolutionary algorithm benchmarking more scientific and accessible.

Happy contributing!
