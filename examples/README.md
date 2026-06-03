# Examples Directory

Welcome to the evobench examples! This directory contains executable Python scripts demonstrating all major features of the evobench library.

---

## Quick Start

### Prerequisites

Ensure evobench is installed with all dependencies:

```bash
cd ..  # Go to project root
pip install -e ".[dev]"
```

### Run Any Example

```bash
python 01_basic_usage.py
python 02_multimodal_comparison.py
python 03_statistical_analysis.py
python 04_custom_algorithm.py
python 05_advanced_tuning.py
```

All examples are self-contained and produce output in the current directory.

---

## Learning Path

### Beginner: Start Here

**[01_basic_usage.py](01_basic_usage.py)** - 5 minutes
- Import algorithms and benchmarks using the Facade API
- Create an optimizer and run optimization
- Track and interpret convergence
- **Output**: Console output + convergence plot (`convergence_sphere.png`)

**Concepts Covered**:
- Basic optimization workflow
- Sphere function (unimodal benchmark)
- Fitness tracking
- Simple visualization

---

### Intermediate: Algorithm Comparison

**[02_multimodal_comparison.py](02_multimodal_comparison.py)** - 10 minutes
- Compare three algorithms (PSO, EDA, ABC) on one problem
- Run multiple independent trials
- Track convergence statistics (mean, std, min, max)
- Visualize with error bands
- **Output**: Console output + comparison plot (`comparison_ackley.png`)

**Concepts Covered**:
- Multi-algorithm comparison
- Independent runs for statistics
- Ackley function (multimodal benchmark)
- Error quantification
- Linear vs. logarithmic scale visualization

---

### Advanced: Statistical Analysis

**[03_statistical_analysis.py](03_statistical_analysis.py)** - 15 minutes
- Collect samples from multiple algorithms
- Test for normality (Shapiro-Wilk)
- Apply hypothesis testing (ANOVA or Kruskal-Wallis)
- Calculate effect sizes (Cohen's d)
- Perform pairwise comparisons
- **Output**: Console report with statistical analysis

**Concepts Covered**:
- Descriptive statistics
- Normality testing
- Parametric vs. non-parametric tests
- Effect size interpretation
- Post-hoc analysis
- Statistical significance

---

### Expert: Extensibility & Tuning

**[04_custom_algorithm.py](04_custom_algorithm.py)** - 20 minutes
- Implement a custom Genetic Algorithm (GA)
- Inherit from `EvolutionaryAlgorithm` abstract base class
- Implement required methods (run, selection, crossover, mutation)
- Test custom algorithm alongside built-in ones
- **Output**: Console output + comparison plot (`custom_algorithm_comparison.png`)

**Concepts Covered**:
- Framework extensibility
- Abstract base class patterns
- GA implementation details
- Integration of custom algorithms
- Elitism and tournament selection

---

**[05_advanced_tuning.py](05_advanced_tuning.py)** - 20 minutes
- Systematic hyperparameter exploration (Grid Search)
- Evaluate multiple configurations
- Analyze parameter sensitivity
- Identify optimal settings
- Visualize trade-offs
- **Output**: Console analysis + sensitivity plots (`grid_search_results.png`)

**Concepts Covered**:
- Hyperparameter tuning methodology
- Grid Search strategy
- Parameter sensitivity analysis
- Configuration evaluation
- Performance ranking

---

## File Descriptions

| File | Purpose | Difficulty | Time | Algorithm |
|------|---------|------------|------|-----------|
| [01_basic_usage.py](01_basic_usage.py) | First optimization run | ⭐ | 5 min | PSO |
| [02_multimodal_comparison.py](02_multimodal_comparison.py) | Compare 3 algorithms visually | ⭐⭐ | 10 min | PSO, EDA, ABC |
| [03_statistical_analysis.py](03_statistical_analysis.py) | Statistical hypothesis testing | ⭐⭐⭐ | 15 min | PSO, EDA, ABC |
| [04_custom_algorithm.py](04_custom_algorithm.py) | Implement custom GA | ⭐⭐⭐ | 20 min | GA (custom) |
| [05_advanced_tuning.py](05_advanced_tuning.py) | Grid Search hyperparameters | ⭐⭐⭐⭐ | 20 min | PSO |

---

## Output Files Generated

Each example produces visualizations saved in the current directory:

- **convergence_sphere.png** - Convergence plot for single run (Example 1)
- **comparison_ackley.png** - Multi-algorithm comparison with error bands (Example 2)
- **custom_algorithm_comparison.png** - Custom GA vs. built-ins (Example 4)
- **grid_search_results.png** - Hyperparameter sensitivity analysis (Example 5)

---

## Key Concepts Demonstrated

### 1. Facade API Pattern
All examples use the clean public API from `src/evobench/__init__.py`:

```python
from evobench import PSO, EDA, ABC  # Algorithms
from evobench import sphere, ackley, rosenbrock  # Benchmarks
from evobench import analyze  # Statistics
```

✓ No need to navigate internal module structure  
✓ Consistent, discoverable interface

### 2. EvolutionaryAlgorithm Interface Contract
All algorithms implement a common interface:

```python
optimizer = PSO(objective_function, bounds, population_size, max_iterations)
best_solution, best_fitness = optimizer.run()

# All algorithms provide:
optimizer.fitness_history  # Track convergence
optimizer.best_individual  # Best solution found
optimizer.best_fitness  # Quality of best solution
```

### 3. Reproducibility via Seeding
Examples use `np.random.seed()` for reproducibility:

```python
np.random.seed(42)  # Set seed once
# All subsequent random operations are deterministic
```

Modern approach (see [docs/guide/PERFORMANCE_AND_REPRODUCIBILITY.md](../docs/guide/PERFORMANCE_AND_REPRODUCIBILITY.md)):

```python
from numpy.random import Generator, PCG64
rng = Generator(PCG64(seed=42))
```

### 4. Statistical Analysis
Example 3 demonstrates rigorous scientific comparison:

```python
# Collect samples
results = [algorithm.run() for _ in range(20)]

# Test normality
stat, p_value = scipy.stats.shapiro(results)

# Apply appropriate statistical test
f_stat, p_value = scipy.stats.f_oneway(pso_results, eda_results, abc_results)

# Calculate effect sizes
cohens_d = (mean1 - mean2) / pooled_std
```

### 5. Extensibility via Inheritance
Example 4 shows how to extend the framework:

```python
from evobench import EvolutionaryAlgorithm

class MyAlgorithm(EvolutionaryAlgorithm):
    def run(self):
        # Implement algorithm
        for generation in range(self.max_iterations):
            # Track fitness
            self.fitness_history.append(self.best_fitness)
        return self.best_individual, self.best_fitness
```

### 6. Hyperparameter Tuning
Example 5 demonstrates systematic exploration:

```python
param_grid = {
    'population_size': [20, 50, 100],
    'inertia_weight': [0.4, 0.7, 1.0]
}

# Evaluate all combinations
configurations = itertools.product(*param_grid.values())
for config in configurations:
    optimizer = PSO(**config)
    _, fitness = optimizer.run()
```

---

## Common Tasks

### Task: Run all examples in sequence

```bash
for file in 0*.py; do
    echo "Running $file..."
    python "$file"
    echo ""
done
```

### Task: Run only examples 1 and 3

```bash
python 01_basic_usage.py
python 03_statistical_analysis.py
```

### Task: Modify Example 1 to use Ackley instead of Sphere

Edit `01_basic_usage.py`, change line:
```python
from evobench import PSO, sphere
# to
from evobench import PSO, ackley
```

And update bounds:
```python
BOUNDS = [(-32.768, 32.768)] * DIMENSION  # Ackley bounds
```

Then update function call:
```python
optimizer = PSO(ackley, BOUNDS, ...)  # Was sphere, now ackley
```

---

## Troubleshooting

### Issue: ImportError when running examples

**Solution**: Ensure evobench is installed in development mode:

```bash
cd ..  # Go to project root
pip install -e .
```

Verify installation:
```bash
python -c "from evobench import PSO, sphere; print('✓ OK')"
```

### Issue: matplotlib not found

Examples gracefully skip visualization if matplotlib is not installed.

**Solution**: Install visualization extras:

```bash
pip install -e ".[dev]"
```

This includes matplotlib as a dependency.

### Issue: Examples run but produce wrong results

**Solution**: Check that you're using the correct seed:

```python
import numpy as np
np.random.seed(42)  # Add at the start of your script
```

Different seeds produce different results (stochastic algorithms).

---

## Next Steps

After running these examples:

1. **Read the Documentation**
   - [docs/reference/](../docs/reference/) - API reference
   - [docs/guide/PERFORMANCE_AND_REPRODUCIBILITY.md](../docs/guide/PERFORMANCE_AND_REPRODUCIBILITY.md) - Best practices
   - [docs/guide/VISUALIZATION.md](../docs/guide/VISUALIZATION.md) - Plotting guide
   - [docs/GLOSSARY.md](../docs/GLOSSARY.md) - EA terminology

2. **Run on Your Own Problems**
   - Define custom objective functions
   - Implement custom benchmarks
   - Tune hyperparameters for your domain

3. **Extend the Framework**
   - Implement custom algorithms (follow Example 4 pattern)
   - Add specialized operators (selection, mutation, crossover)
   - Create domain-specific benchmarks

4. **Publish Results**
   - Run statistical comparisons (Example 3 pattern)
   - Generate publication-quality plots
   - Document reproducibility (seed, versions, environment)

---

## Citation

If you use evobench in research, please cite:

```bibtex
@software{evobench2026,
  title={evobench: A Comprehensive Benchmarking Suite for Evolutionary Algorithms},
  author={G{\'o}mez Linares, Enrique and Galv{\'a}n Delgadillo, Victoria},
  year={2026},
  url={https://github.com/yourusername/evobench-lib}
}
```

---

## Support

For issues, questions, or suggestions:

1. Check [docs/faq/TROUBLESHOOTING.md](../docs/faq/TROUBLESHOOTING.md)
2. Review [docs/GLOSSARY.md](../docs/GLOSSARY.md) for terminology
3. Open an issue on GitHub
4. Check existing examples for similar patterns

---

**Last Updated**: June 2026  
**evobench Version**: 0.1.0
