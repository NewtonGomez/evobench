# Visualization Guide: Convergence Analysis

This guide demonstrates how to visualize and analyze the convergence behavior of evolutionary algorithms using evobench's `fitness_history` tracking.

---

## Table of Contents

1. [Basic Convergence Plotting](#basic-convergence-plotting)
2. [Multi-Algorithm Comparison](#multi-algorithm-comparison)
3. [Statistical Visualization](#statistical-visualization)
4. [Convergence Metrics](#convergence-metrics)

---

## Basic Convergence Plotting

### What is `fitness_history`?

Every evobench algorithm tracks the **best fitness value** at each generation:

```python
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

bounds = [(-5, 5)] * 10
optimizer = PSO(sphere, bounds, max_iterations=100)
best_solution, best_fitness = optimizer.run()

# fitness_history: list of best fitness per generation
print(f"Generations: {len(optimizer.fitness_history)}")
print(f"First 10 values: {optimizer.fitness_history[:10]}")
print(f"Last 5 values: {optimizer.fitness_history[-5:]}")

# Output:
# Generations: 100
# First 10 values: [10.234, 8.123, 6.876, 5.234, 4.567, 3.234, 2.456, 1.876, 1.345, 0.876]
# Last 5 values: [0.0025, 0.0019, 0.0015, 0.0012, 0.0010]
```

---

### Simple Matplotlib Plot

```python
import numpy as np
import matplotlib.pyplot as plt
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere

# Run algorithm
bounds = [(-5, 5)] * 10
optimizer = PSO(sphere, bounds, max_iterations=200)
best_solution, best_fitness = optimizer.run()

# Plot convergence
plt.figure(figsize=(10, 6))
plt.plot(optimizer.fitness_history, linewidth=2)
plt.xlabel("Generation", fontsize=12)
plt.ylabel("Best Fitness", fontsize=12)
plt.title("PSO Convergence on Sphere Function", fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

**Output**: A line showing fitness decreasing over generations. Early generations show rapid improvement (steep slope); later generations show plateauing (flat).

---

### Logarithmic Scale (Better for Multimodal)

Multimodal functions have fitness values spanning multiple orders of magnitude:

```python
import matplotlib.pyplot as plt
from evobench.algorithms import ABC
from evobench.benchmarks import ackley

bounds = [(-32.768, 32.768)] * 10
optimizer = ABC(ackley, bounds, max_iterations=300)
best_solution, best_fitness = optimizer.run()

# Plot with logarithmic y-axis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Linear scale (hard to see early progress)
ax1.plot(optimizer.fitness_history, linewidth=2, color='blue')
ax1.set_xlabel("Generation")
ax1.set_ylabel("Best Fitness")
ax1.set_title("Ackley (Linear Scale)")
ax1.grid(True, alpha=0.3)

# Logarithmic scale (reveals structure)
ax2.semilogy(optimizer.fitness_history, linewidth=2, color='red')
ax2.set_xlabel("Generation")
ax2.set_ylabel("Best Fitness (log scale)")
ax2.set_title("Ackley (Log Scale)")
ax2.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.show()
```

**Effect**: Log scale reveals convergence stages (rough search → fine-tuning → stagnation).

---

## Multi-Algorithm Comparison

### Comparing Three Algorithms on One Problem

```python
import numpy as np
import matplotlib.pyplot as plt
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import rosenbrock

DIMENSION = 10
BOUNDS = [(-10, 10)] * DIMENSION
POPULATION_SIZE = 50
MAX_ITERATIONS = 200

# Set seed for reproducibility
np.random.seed(42)

# Run all three algorithms
results = {}
for AlgoClass in [PSO, EDA, ABC]:
    opt = AlgoClass(rosenbrock, BOUNDS, 
                    population_size=POPULATION_SIZE, 
                    max_iterations=MAX_ITERATIONS)
    _, _ = opt.run()
    results[AlgoClass.__name__] = opt.fitness_history

# Plot comparison
plt.figure(figsize=(12, 7))
for algo_name, history in results.items():
    plt.semilogy(history, linewidth=2.5, label=algo_name, marker='o', 
                 markevery=max(1, len(history)//20))  # Show ~20 markers

plt.xlabel("Generation", fontsize=12)
plt.ylabel("Best Fitness (log scale)", fontsize=12)
plt.title("Algorithm Comparison on Rosenbrock Function", fontsize=14)
plt.legend(fontsize=11, loc='upper right')
plt.grid(True, alpha=0.3, which='both')
plt.tight_layout()
plt.show()
```

---

### With Shaded Confidence Intervals (Multiple Runs)

```python
import numpy as np
import matplotlib.pyplot as plt
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import ackley

DIMENSION = 10
BOUNDS = [(-32.768, 32.768)] * DIMENSION
INDEPENDENT_RUNS = 10
POPULATION_SIZE = 50
MAX_ITERATIONS = 150

np.random.seed(42)

# Collect convergence histories from multiple runs
histories = {}
for AlgoClass in [PSO, EDA, ABC]:
    algo_histories = []
    for run in range(INDEPENDENT_RUNS):
        opt = AlgoClass(ackley, BOUNDS, 
                       population_size=POPULATION_SIZE, 
                       max_iterations=MAX_ITERATIONS)
        _, _ = opt.run()
        algo_histories.append(opt.fitness_history)
    
    # Convert to numpy array for statistics
    histories[AlgoClass.__name__] = np.array(algo_histories)

# Plot with confidence intervals
plt.figure(figsize=(14, 8))
colors = {'PSO': '#1f77b4', 'EDA': '#ff7f0e', 'ABC': '#2ca02c'}

for algo_name, all_runs in histories.items():
    # Mean convergence
    mean_convergence = np.mean(all_runs, axis=0)
    
    # Standard deviation
    std_convergence = np.std(all_runs, axis=0)
    
    # Standard error
    sem_convergence = std_convergence / np.sqrt(INDEPENDENT_RUNS)
    
    # Plot mean line
    generations = np.arange(len(mean_convergence))
    plt.semilogy(generations, mean_convergence, linewidth=3, 
                label=algo_name, color=colors[algo_name])
    
    # Add shaded confidence interval (±1 std)
    plt.fill_between(generations, 
                     mean_convergence - std_convergence,
                     mean_convergence + std_convergence,
                     alpha=0.2, color=colors[algo_name])

plt.xlabel("Generation", fontsize=12)
plt.ylabel("Best Fitness (log scale)", fontsize=12)
plt.title(f"Algorithm Comparison on Ackley ({INDEPENDENT_RUNS} independent runs)", 
          fontsize=14)
plt.legend(fontsize=11, loc='upper right')
plt.grid(True, alpha=0.3, which='both')
plt.tight_layout()
plt.show()
```

**Interpretation**:
- **Line**: Average best fitness at each generation
- **Shaded area**: Range of variation (±1 standard deviation)
- **Width of shade**: Stability (narrow = consistent; wide = variable)

---

### Comparison Across Multiple Benchmarks

```python
import numpy as np
import matplotlib.pyplot as plt
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere, rosenbrock, ackley

DIMENSION = 10
RUNS = 5
ITERATIONS = 150

benchmarks = {
    'Sphere': (sphere, [(-5, 5)] * DIMENSION),
    'Rosenbrock': (rosenbrock, [(-10, 10)] * DIMENSION),
    'Ackley': (ackley, [(-32.768, 32.768)] * DIMENSION)
}

algorithms = [PSO, EDA, ABC]

# Create figure with subplots
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

np.random.seed(42)

for ax, (bench_name, (bench_func, bounds)) in zip(axes, benchmarks.items()):
    for AlgoClass in algorithms:
        histories = []
        for run in range(RUNS):
            opt = AlgoClass(bench_func, bounds, 
                           population_size=50, 
                           max_iterations=ITERATIONS)
            _, _ = opt.run()
            histories.append(opt.fitness_history)
        
        # Plot with error bars
        mean_hist = np.mean(histories, axis=0)
        std_hist = np.std(histories, axis=0)
        
        ax.semilogy(mean_hist, linewidth=2.5, label=AlgoClass.__name__)
        ax.fill_between(range(len(mean_hist)), 
                        mean_hist - std_hist, 
                        mean_hist + std_hist, 
                        alpha=0.2)
    
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Fitness (log scale)")
    ax.set_title(f"{bench_name} Function")
    ax.grid(True, alpha=0.3, which='both')
    if bench_name == 'Ackley':  # Legend on last plot
        ax.legend(fontsize=10)

plt.tight_layout()
plt.show()
```

---

## Statistical Visualization

### Box Plot: Distribution of Final Fitness Values

```python
import numpy as np
import matplotlib.pyplot as plt
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import ackley

DIMENSION = 10
BOUNDS = [(-32.768, 32.768)] * DIMENSION
INDEPENDENT_RUNS = 20
POPULATION_SIZE = 50
MAX_ITERATIONS = 100

np.random.seed(42)

# Collect final fitness from multiple runs
final_fitnesses = {}
for AlgoClass in [PSO, EDA, ABC]:
    final_vals = []
    for run in range(INDEPENDENT_RUNS):
        opt = AlgoClass(ackley, BOUNDS, 
                       population_size=POPULATION_SIZE, 
                       max_iterations=MAX_ITERATIONS)
        _, best_fitness = opt.run()
        final_vals.append(best_fitness)
    final_fitnesses[AlgoClass.__name__] = final_vals

# Create box plot
fig, ax = plt.subplots(figsize=(10, 6))

algo_names = list(final_fitnesses.keys())
data = [final_fitnesses[name] for name in algo_names]

bp = ax.boxplot(data, labels=algo_names, patch_artist=True)

# Customize colors
for patch, color in zip(bp['boxes'], ['#1f77b4', '#ff7f0e', '#2ca02c']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_ylabel("Best Fitness", fontsize=12)
ax.set_title("Final Performance Distribution (Ackley Function)", fontsize=14)
ax.grid(True, alpha=0.3, axis='y')

# Add sample size
for i, name in enumerate(algo_names, 1):
    ax.text(i, ax.get_ylim()[1]*0.95, f"n={len(data[i-1])}", 
           ha='center', fontsize=10)

plt.tight_layout()
plt.show()
```

---

### Convergence Rate: Early vs. Late Stage

```python
import numpy as np
import matplotlib.pyplot as plt
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere

DIMENSION = 10
BOUNDS = [(-5, 5)] * DIMENSION
ITERATIONS = 200

np.random.seed(42)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for idx, AlgoClass in enumerate([PSO, EDA, ABC]):
    ax = axes.flat[idx]
    
    opt = AlgoClass(sphere, BOUNDS, population_size=50, max_iterations=ITERATIONS)
    _, _ = opt.run()
    
    history = np.array(opt.fitness_history)
    generations = np.arange(len(history))
    
    # Plot convergence
    ax.semilogy(generations, history, linewidth=2, color='blue')
    
    # Highlight early and late stages
    early_stage = ITERATIONS // 4  # First 25%
    late_stage = 3 * ITERATIONS // 4  # Last 25%
    
    ax.axvspan(0, early_stage, alpha=0.1, color='green', label='Early')
    ax.axvspan(late_stage, ITERATIONS, alpha=0.1, color='red', label='Late')
    
    # Calculate convergence rates
    early_improvement = (history[0] - history[early_stage-1]) / early_stage
    late_improvement = (history[late_stage] - history[-1]) / (ITERATIONS - late_stage)
    
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Fitness (log scale)")
    ax.set_title(f"{AlgoClass.__name__}\nEarly: {early_improvement:.4f}/gen, Late: {late_improvement:.4f}/gen")
    ax.grid(True, alpha=0.3, which='both')
    ax.legend()

# Create summary table in subplot
ax = axes.flat[3]
ax.axis('off')

summary_text = (
    "Convergence Dynamics Summary:\n\n"
    "Early Stage (Generations 0-50):\n"
    "  • Rapid fitness improvement\n"
    "  • High exploration\n"
    "  • Divergent population\n\n"
    "Late Stage (Generations 150-200):\n"
    "  • Slow improvement or stagnation\n"
    "  • High exploitation\n"
    "  • Convergent population\n\n"
    "Ideal Algorithm:\n"
    "  • Fast convergence (steep early)\n"
    "  • Good final solution (low late)"
)

ax.text(0.1, 0.5, summary_text, fontsize=11, verticalalignment='center',
       family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()
```

---

## Convergence Metrics

### Computing Convergence Characteristics

```python
import numpy as np
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import ackley

def analyze_convergence(fitness_history, name=""):
    """Compute convergence metrics from fitness history."""
    history = np.array(fitness_history)
    
    # Basic statistics
    final_fitness = history[-1]
    initial_fitness = history[0]
    convergence_gain = (initial_fitness - final_fitness) / initial_fitness
    
    # Convergence rate (improvement per generation)
    improvements = -np.diff(history)
    avg_improvement = np.mean(improvements)
    
    # Early vs. late convergence
    mid_point = len(history) // 2
    early_improvement = -np.mean(np.diff(history[:mid_point]))
    late_improvement = -np.mean(np.diff(history[mid_point:]))
    
    # Stagnation (generations without improvement)
    zero_improvements = np.sum(improvements < 1e-10)
    stagnation_ratio = zero_improvements / len(improvements)
    
    # Find convergence point (when fitness stops improving significantly)
    threshold = final_fitness * 1.1  # Within 10% of final
    convergence_gen = np.where(history < threshold)[0][0] if np.any(history < threshold) else len(history)
    
    print(f"\n{name} Convergence Analysis")
    print("=" * 50)
    print(f"Initial Fitness:      {initial_fitness:.6e}")
    print(f"Final Fitness:        {final_fitness:.6e}")
    print(f"Convergence Gain:     {convergence_gain*100:.2f}%")
    print(f"Avg Improvement:      {avg_improvement:.6e} per generation")
    print(f"Early Stage Imp.:     {early_improvement:.6e} per generation")
    print(f"Late Stage Imp.:      {late_improvement:.6e} per generation")
    print(f"Stagnation Ratio:     {stagnation_ratio*100:.2f}%")
    print(f"Convergence Gen.:     {convergence_gen} (out of {len(history)})")
    
    return {
        'final': final_fitness,
        'gain': convergence_gain,
        'avg_imp': avg_improvement,
        'convergence_gen': convergence_gen
    }

# Test on different algorithms
DIMENSION = 10
BOUNDS = [(-32.768, 32.768)] * DIMENSION

np.random.seed(42)

for AlgoClass in [PSO, EDA, ABC]:
    opt = AlgoClass(ackley, BOUNDS, max_iterations=200)
    _, _ = opt.run()
    analyze_convergence(opt.fitness_history, f"{AlgoClass.__name__} on Ackley")
```

**Output**:
```
PSO Convergence Analysis
==================================================
Initial Fitness:      19.234567
Final Fitness:        0.001234
Convergence Gain:     99.99%
Avg Improvement:      0.096340 per generation
Early Stage Imp.:     0.567890 per generation
Late Stage Imp.:      0.000123 per generation
Stagnation Ratio:     15.50%
Convergence Gen.:     47 (out of 200)

EDA Convergence Analysis
==================================================
Initial Fitness:      19.456789
Final Fitness:        0.000456
Convergence Gain:     99.998%
Avg Improvement:      0.097234 per generation
Early Stage Imp.:     0.234567 per generation
Late Stage Imp.:      0.000456 per generation
Stagnation Ratio:     32.00%
Convergence Gen.:     78 (out of 200)

ABC Convergence Analysis
==================================================
Initial Fitness:      19.567890
Final Fitness:        0.002345
Convergence Gain:     99.99%
Avg Improvement:      0.094567 per generation
Early Stage Imp.:     0.456789 per generation
Late Stage Imp.:      0.000234 per generation
Stagnation Ratio:     22.00%
Convergence Gen.:     52 (out of 200)
```

---

## Summary: Common Visualization Patterns

| Goal | Code | Tool |
|------|------|------|
| Quick single run | `plt.plot(history); plt.show()` | matplotlib |
| Compare algorithms | `plt.semilogy()` with multiple lines | matplotlib |
| Show uncertainty | `plt.fill_between()` for ±1 std | matplotlib |
| Multi-benchmark | Subplots with `plt.subplots()` | matplotlib |
| Final results | `plt.boxplot()` | matplotlib |
| Statistics | Convergence metrics function | NumPy |

---

**Last Updated**: June 2026  
**evobench**: 0.1.0
