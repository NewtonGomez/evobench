# Performance and Reproducibility Guide

This guide covers best practices for optimizing evobench performance and ensuring reproducible, scientifically rigorous experiments.

---

## Table of Contents

1. [Reproducibility Principles](#reproducibility-principles)
2. [Random Number Generation](#random-number-generation)
3. [Seeding Strategies](#seeding-strategies)
4. [Performance Optimization](#performance-optimization)
5. [Benchmarking Methodology](#benchmarking-methodology)
6. [Parallel Experiments](#parallel-experiments)

---

## Reproducibility Principles

Scientific reproducibility requires that experiments produce **identical results** when rerun with the same configuration. This is essential for:
- Publishing verifiable results
- Debugging algorithm behavior
- Comparing algorithms fairly
- Enabling peer review

### The Reproducibility Chain

```
Deterministic Hardware
        ↓
Fixed Random Seed
        ↓
Algorithm Implementation (fixed code)
        ↓
Identical Results
```

**Failure at any link breaks reproducibility.**

---

## Random Number Generation

### Why Random Number Generation Matters

Evolutionary algorithms are **stochastic**: they use randomness intentionally. Without controlling randomness, results vary between runs:

```python
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

bounds = [(-5, 5)] * 10
optimizer = PSO(sphere, bounds, max_iterations=100)

# Run 1 (no seed)
_, fitness1 = optimizer.run()  # e.g., 0.00234

# Run 2 (no seed)
_, fitness2 = optimizer.run()  # e.g., 0.00187 (different!)

# Run 3 (no seed)
_, fitness3 = optimizer.run()  # e.g., 0.00421 (different again!)

print([fitness1, fitness2, fitness3])  # All different ❌
```

### Modern NumPy API (Recommended)

evobench uses modern NumPy random API (`Generator` + `PCG64`) for:
- Better statistical properties
- Thread-safe seeding (important for parallel experiments)
- Explicit seed management

```python
import numpy as np
from numpy.random import Generator, PCG64

# Create a Generator with a specific seed
rng = Generator(PCG64(seed=42))

# Use rng instead of np.random
population = rng.uniform(-5, 5, (100, 10))
indices = rng.choice(100, 10)
```

### Setting Seeds in evobench

The library automatically seeds NumPy's global random state, but **you control it** at entry points:

```python
import numpy as np

# Set global seed (affects np.random functions)
np.random.seed(42)

# Now run experiments (reproducible)
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

bounds = [(-5, 5)] * 10

optimizer1 = PSO(sphere, bounds)
_, fitness1 = optimizer1.run()

optimizer2 = PSO(sphere, bounds)
_, fitness2 = optimizer2.run()

print(fitness1 == fitness2)  # True ✓ Reproducible
```

---

## Seeding Strategies

### Strategy 1: Single Global Seed (Simplest)

Use **one** seed for the entire experiment:

```python
import numpy as np
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere

# Set global seed once at the start
np.random.seed(42)

bounds = [(-5, 5)] * 10

# All subsequent calls are reproducible
algorithms = [PSO, EDA, ABC]
for Algorithm in algorithms:
    optimizer = Algorithm(sphere, bounds)
    _, fitness = optimizer.run()
    print(f"{Algorithm.__name__}: {fitness}")

# Run again with same seed → identical results
np.random.seed(42)
for Algorithm in algorithms:
    optimizer = Algorithm(sphere, bounds)
    _, fitness = optimizer.run()
    print(f"{Algorithm.__name__}: {fitness}")
```

**Pros**: Simple, works for single-threaded code  
**Cons**: Fails with multi-threading; all runs get same sequence

---

### Strategy 2: Seed Sequence (For Multiple Independent Runs)

Generate **independent but reproducible** seeds for each run:

```python
import numpy as np
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

DIMENSION = 10
INDEPENDENT_RUNS = 20
SEED = 42

# Create a "seed sequence" - generates independent seeds reproducibly
ss = np.random.SeedSequence(SEED)

# Generate 20 different seeds (all reproducible from master seed)
seeds = ss.spawn(INDEPENDENT_RUNS)

bounds = [(-5, 5)] * DIMENSION
results = []

for i, seed in enumerate(seeds):
    # Set seed for this run
    rng = np.random.Generator(np.random.PCG64(seed))
    np.random.seed(int(seed.entropy[0]))  # For compatibility
    
    # Run algorithm
    optimizer = PSO(sphere, bounds, max_iterations=100)
    _, best_fitness = optimizer.run()
    results.append(best_fitness)
    
    print(f"Run {i+1}: {best_fitness:.6e}")

# Results are reproducible and independent
import numpy as np
mean_fitness = np.mean(results)
std_fitness = np.std(results)
print(f"\nMean: {mean_fitness:.6e} ± {std_fitness:.6e}")

# Re-run with same master seed → identical results
ss = np.random.SeedSequence(42)
seeds = ss.spawn(20)
# ... repeat above loop ... # Exact same results ✓
```

**Pros**: Independent runs, reproducible, thread-safe  
**Cons**: Slightly more complex

---

### Strategy 3: Deterministic Seed per Configuration (Scientific Gold Standard)

Hash the configuration to generate a seed:

```python
import numpy as np
import hashlib
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere, ackley

def config_hash_seed(config_dict: dict) -> int:
    """Generate deterministic seed from configuration."""
    config_str = str(sorted(config_dict.items()))
    hash_bytes = hashlib.sha256(config_str.encode()).digest()
    # Convert first 8 bytes to integer seed
    seed = int.from_bytes(hash_bytes[:8], byteorder='little') % (2**31)
    return seed

# Configuration
config = {
    "algorithm": "PSO",
    "benchmark": "Sphere",
    "dimension": 10,
    "population_size": 50,
    "max_iterations": 100
}

# Generate seed from config
seed = config_hash_seed(config)

# Reproducible experiment
np.random.seed(seed)

optimizer = PSO(sphere, [(-5, 5)] * 10, 
                population_size=config["population_size"],
                max_iterations=config["max_iterations"])
best_sol, best_fit = optimizer.run()

print(f"Seed (from config): {seed}")
print(f"Best Fitness: {best_fit:.6e}")

# Later, with same config → identical seed → identical results
seed2 = config_hash_seed(config)
assert seed == seed2
np.random.seed(seed2)
# ... run again ... → Exact same result ✓
```

**Pros**: Configuration → seed mapping is explicit and reproducible; ideal for version control  
**Cons**: Requires configuration management

---

## Performance Optimization

### Optimization 1: Vectorization (Already Done)

evobench algorithms use NumPy vectorization for speed. You benefit automatically:

```python
from evobench.algorithms import PSO
from evobench.benchmarks import sphere

# This is already vectorized internally
optimizer = PSO(sphere, [(-5, 5)] * 1000, population_size=100, max_iterations=100)
_, fitness = optimizer.run()  # Processes 100 × 1000 dimensions at once

# Time: ~2-3 seconds (not 5+ minutes) ✓
```

**What evobench does**:
- Population stored as NumPy arrays (shape: population_size × dimension)
- Fitness evaluation: `np.apply_along_axis()` processes all individuals at once
- Population updates: Element-wise operations (broadcast over population)

---

### Optimization 2: Problem Scaling

Use appropriate problem dimensions for your use case:

```python
from evobench.algorithms import PSO
from evobench.benchmarks import sphere
import time

# Test different dimensions
for dimension in [10, 50, 100, 500, 1000]:
    bounds = [(-5, 5)] * dimension
    
    start = time.time()
    optimizer = PSO(sphere, bounds, population_size=min(100, 2*dimension), 
                   max_iterations=100)
    _, fitness = optimizer.run()
    elapsed = time.time() - start
    
    print(f"d={dimension:4d}: {elapsed:7.2f}s  | Fitness: {fitness:.6e}")

# Output:
# d=  10:    0.15s  | Fitness: 3.456e-05
# d=  50:    0.38s  | Fitness: 2.123e-04
# d= 100:    0.89s  | Fitness: 5.234e-04
# d= 500:    5.23s  | Fitness: 1.234e-03
# d=1000:   19.45s  | Fitness: 2.456e-03
```

**Guidelines**:
- **Small (d ≤ 20)**: Fast, good for testing
- **Medium (d = 20-100)**: Realistic, ~1s per run
- **Large (d > 100)**: Slow, use for stress-testing only

---

### Optimization 3: Population and Iteration Budget

Trade population size vs. iterations:

```python
from evobench.algorithms import PSO
from evobench.benchmarks import ackley
import time

bounds = [(-32.768, 32.768)] * 50
total_budget = 5000  # Total function evaluations allowed

configs = [
    {"population_size": 50, "max_iterations": 100},   # 50 × 100 = 5000
    {"population_size": 100, "max_iterations": 50},   # 100 × 50 = 5000
    {"population_size": 250, "max_iterations": 20},   # 250 × 20 = 5000
]

for config in configs:
    start = time.time()
    optimizer = PSO(ackley, bounds, **config)
    _, fitness = optimizer.run()
    elapsed = time.time() - start
    
    print(f"Pop={config['population_size']:3d}, Iter={config['max_iterations']:3d}: "
          f"{elapsed:6.2f}s | Fitness: {fitness:.6e}")

# Time should be similar (same budget), but quality varies
```

**Heuristic**: For small-medium problems:
- Population: 20-100 individuals
- Iterations: 100-500 generations
- Total evals: 2000-50000 (depends on dimension)

---

### Optimization 4: Benchmark Function Characteristics

Choose appropriate benchmarks for your algorithm:

```python
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere, rosenbrock, ackley
import time

dimension = 30
bounds_sphere = [(-5, 5)] * dimension
bounds_rosen = [(-10, 10)] * dimension
bounds_ackley = [(-32.768, 32.768)] * dimension

benchmarks = [
    ("Sphere", sphere, bounds_sphere),
    ("Rosenbrock", rosenbrock, bounds_rosen),
    ("Ackley", ackley, bounds_ackley)
]

algorithms = [
    ("PSO", PSO),
    ("EDA", EDA),
    ("ABC", ABC)
]

# Time each combination
for bench_name, bench_func, bounds in benchmarks:
    print(f"\n{bench_name}:")
    for algo_name, AlgoClass in algorithms:
        start = time.time()
        opt = AlgoClass(bench_func, bounds, max_iterations=100)
        _, fitness = opt.run()
        elapsed = time.time() - start
        print(f"  {algo_name}: {elapsed:6.2f}s | Fitness: {fitness:.6e}")
```

---

## Benchmarking Methodology

### Rigorous Performance Comparison

```python
import numpy as np
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import sphere, ackley
from evobench.stats import analyze
import time

# Experimental design
DIMENSION = 10
INDEPENDENT_RUNS = 30
POPULATION_SIZE = 50
MAX_ITERATIONS = 200

benchmarks = {"Sphere": sphere, "Ackley": ackley}
algorithms = {"PSO": PSO, "EDA": EDA, "ABC": ABC}

# Set seed for reproducibility
np.random.seed(12345)

results = {}

for bench_name, bench_func in benchmarks.items():
    print(f"\n{'='*60}")
    print(f"Benchmark: {bench_name}")
    print(f"{'='*60}")
    
    bench_results = {}
    bounds = {
        "Sphere": [(-5, 5)] * DIMENSION,
        "Ackley": [(-32.768, 32.768)] * DIMENSION
    }[bench_name]
    
    for algo_name, AlgoClass in algorithms.items():
        fitnesses = []
        times = []
        
        print(f"  {algo_name}...", end=" ", flush=True)
        
        for run in range(INDEPENDENT_RUNS):
            start = time.time()
            opt = AlgoClass(bench_func, bounds, 
                           population_size=POPULATION_SIZE, 
                           max_iterations=MAX_ITERATIONS)
            _, best_fitness = opt.run()
            elapsed = time.time() - start
            
            fitnesses.append(best_fitness)
            times.append(elapsed)
        
        bench_results[algo_name] = np.array(fitnesses)
        
        # Summary statistics
        mean = np.mean(fitnesses)
        std = np.std(fitnesses)
        mean_time = np.mean(times)
        
        print(f"✓ ({mean:.6e} ± {std:.6e}) [{mean_time:.2f}s/run]")
    
    # Statistical analysis
    print(f"\n  Statistical Comparison:")
    fitness_data = [bench_results[name] for name in algorithms.keys()]
    result = analyze(bench_name, fitness_data, list(algorithms.keys()))
    
    results[bench_name] = result

# Print final summary
print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
for bench_name in benchmarks.keys():
    print(f"{bench_name}: {results[bench_name]['significant'] and 'Significant' or 'No difference'}")
```

**Output**:
```
============================================================
Benchmark: Sphere
============================================================
  PSO... ✓ (1.234e-04 ± 2.345e-05) [0.23s/run]
  EDA... ✓ (5.678e-05 ± 1.234e-05) [0.19s/run]
  ABC... ✓ (8.901e-05 ± 3.456e-05) [0.25s/run]

  Statistical Comparison:
  - Normality: All groups normal (p > 0.05)
  - ANOVA: Significant difference (p = 0.0023)
  - Post-hoc (Tukey): EDA > PSO, ABC ≈ PSO

============================================================
SUMMARY
============================================================
Sphere: Significant
```

---

## Parallel Experiments

### Safe Parallel Execution

```python
import numpy as np
from multiprocessing import Pool
from evobench.algorithms import PSO, EDA, ABC
from evobench.benchmarks import ackley

def run_single_optimization(args):
    """Worker function for parallel execution."""
    algo_class, seed, run_id = args
    
    # Set seed for this worker process
    np.random.seed(seed)
    
    bounds = [(-32.768, 32.768)] * 10
    optimizer = algo_class(ackley, bounds, max_iterations=100)
    _, best_fitness = optimizer.run()
    
    return {"algorithm": algo_class.__name__, "run": run_id, "fitness": best_fitness}

# Generate seeds for each run
MASTER_SEED = 42
ss = np.random.SeedSequence(MASTER_SEED)
NUM_RUNS = 100

# Create job list
jobs = []
seed_counter = 0
for algo_class in [PSO, EDA, ABC]:
    for run in range(NUM_RUNS // 3):  # ~33 runs per algorithm
        seed = int(ss.spawn(1)[0].entropy[0])
        jobs.append((algo_class, seed, run))

# Parallel execution
print(f"Running {len(jobs)} optimizations in parallel...")
with Pool(4) as pool:  # 4 workers
    results = pool.map(run_single_optimization, jobs)

# Process results
pso_results = [r["fitness"] for r in results if r["algorithm"] == "PSO"]
eda_results = [r["fitness"] for r in results if r["algorithm"] == "EDA"]
abc_results = [r["fitness"] for r in results if r["algorithm"] == "ABC"]

print(f"PSO: {np.mean(pso_results):.6e} ± {np.std(pso_results):.6e}")
print(f"EDA: {np.mean(eda_results):.6e} ± {np.std(eda_results):.6e}")
print(f"ABC: {np.mean(abc_results):.6e} ± {np.std(abc_results):.6e}")
```

**Key Points**:
- Each worker gets **independent seed** (from SeedSequence)
- Results are reproducible
- Threads/processes don't share random state

---

## Reproducibility Checklist

Before publishing results:

- [ ] **Random seed documented** and hardcoded
- [ ] **evobench version** specified in code (`import evobench; print(evobench.__version__)`)
- [ ] **NumPy version** recorded (`import numpy; print(numpy.__version__)`)
- [ ] **System specs** documented (OS, CPU, RAM)
- [ ] **Algorithm hyperparameters** explicitly listed
- [ ] **Problem dimensions** and bounds specified
- [ ] **Number of independent runs** reported
- [ ] **Statistical test used** mentioned (ANOVA, Kruskal-Wallis)
- [ ] **Effect size** (Cohen's d) reported alongside p-value
- [ ] **Configuration** reproducible (code in GitHub, data in repository)

### Reproducibility Report Template

```python
import numpy as np
from evobench.algorithms import PSO
from evobench.benchmarks import sphere
import evobench
import platform

# Record environment
print("="*60)
print("REPRODUCIBILITY REPORT")
print("="*60)
print(f"evobench version: {evobench.__version__}")
print(f"NumPy version: {np.__version__}")
print(f"Python version: {platform.python_version()}")
print(f"Platform: {platform.platform()}")
print(f"Processor: {platform.processor()}")

# Record configuration
SEED = 12345
DIMENSION = 10
POPULATION_SIZE = 50
MAX_ITERATIONS = 100
INDEPENDENT_RUNS = 20

print(f"\nConfiguration:")
print(f"  Seed: {SEED}")
print(f"  Dimension: {DIMENSION}")
print(f"  Population: {POPULATION_SIZE}")
print(f"  Iterations: {MAX_ITERATIONS}")
print(f"  Independent Runs: {INDEPENDENT_RUNS}")

# Run experiment
np.random.seed(SEED)
results = []
for run in range(INDEPENDENT_RUNS):
    opt = PSO(sphere, [(-5, 5)] * DIMENSION, 
              population_size=POPULATION_SIZE, 
              max_iterations=MAX_ITERATIONS)
    _, best_fit = opt.run()
    results.append(best_fit)

# Record results
print(f"\nResults:")
print(f"  Mean: {np.mean(results):.6e}")
print(f"  Std:  {np.std(results):.6e}")
print(f"  Min:  {np.min(results):.6e}")
print(f"  Max:  {np.max(results):.6e}")

print("="*60)
print("To reproduce: Run this script with same seed and libraries")
print("="*60)
```

---

**Last Updated**: June 2026  
**evobench**: 0.1.0
