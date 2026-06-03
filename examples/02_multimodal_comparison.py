#!/usr/bin/env python3
"""
Example 2: Multi-Algorithm Comparison with Visualization

This example demonstrates:
- Running multiple algorithms on the same benchmark
- Tracking convergence across independent runs
- Creating professional convergence plots with error bands
- Comparing algorithm performance visually

Learning outcomes:
- Understand algorithm behavior through convergence curves
- Visualize exploration vs. exploitation phases
- Identify when algorithms converge vs. stagnate
"""

import numpy as np
import matplotlib.pyplot as plt
from evobench import PSO, EDA, ABC, ackley


# CONFIGURATION


DIMENSION = 10
BOUNDS = [(-32.768, 32.768)] * DIMENSION  # Ackley search space
POPULATION_SIZE = 50
MAX_ITERATIONS = 150
INDEPENDENT_RUNS = 5  # Multiple runs for uncertainty quantification

print(f"Experimental Configuration:")
print(f"  Benchmark: Ackley function (multimodal, highly challenging)")
print(f"  Dimensionality: {DIMENSION}D")
print(f"  Algorithms: PSO, EDA, ABC")
print(f"  Independent runs: {INDEPENDENT_RUNS} (for error quantification)")
print(f"  Population size: {POPULATION_SIZE}")
print(f"  Max iterations: {MAX_ITERATIONS}")
print()


# STEP 1: Run algorithms and collect convergence histories


np.random.seed(42)  # Reproducibility

algorithms = {
    'PSO': PSO,
    'EDA': EDA,
    'ABC': ABC
}

# Store convergence histories for each algorithm and run
convergence_data = {}

for algo_name, AlgoClass in algorithms.items():
    print(f"Running {algo_name}...")
    histories = []
    
    for run_id in range(INDEPENDENT_RUNS):
        # Create optimizer
        optimizer = AlgoClass(
            objective_function=ackley,
            bounds=BOUNDS,
            population_size=POPULATION_SIZE,
            max_iterations=MAX_ITERATIONS
        )
        
        # Run optimization
        _, _ = optimizer.run()
        
        # Store convergence history
        histories.append(optimizer.fitness_history)
        print(f"  Run {run_id + 1}/{INDEPENDENT_RUNS}: "
              f"Final fitness = {optimizer.fitness_history[-1]:.6e}")
    
    convergence_data[algo_name] = np.array(histories)
    print()


# STEP 2: Compute statistics (mean, std, min, max)


print("Computing statistics...")
statistics = {}

for algo_name, all_runs in convergence_data.items():
    mean_conv = np.mean(all_runs, axis=0)
    std_conv = np.std(all_runs, axis=0)
    min_conv = np.min(all_runs, axis=0)
    max_conv = np.max(all_runs, axis=0)
    
    statistics[algo_name] = {
        'mean': mean_conv,
        'std': std_conv,
        'min': min_conv,
        'max': max_conv
    }
    
    print(f"  {algo_name}:")
    print(f"    Mean final fitness: {mean_conv[-1]:.6e}")
    print(f"    Std final fitness:  {std_conv[-1]:.6e}")
    print(f"    Min final fitness:  {min_conv[-1]:.6e}")
    print(f"    Max final fitness:  {max_conv[-1]:.6e}")

print()


# STEP 3: Create convergence plot with confidence bands


print("Creating visualization...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

colors = {'PSO': '#1f77b4', 'EDA': '#ff7f0e', 'ABC': '#2ca02c'}
generations = np.arange(MAX_ITERATIONS)

# ---- Subplot 1: Linear scale ----
ax = axes[0]
for algo_name, stats in statistics.items():
    mean = stats['mean']
    std = stats['std']
    
    # Plot mean line
    ax.plot(generations, mean, linewidth=3, label=algo_name, 
            color=colors[algo_name])
    
    # Add error band (±1 std)
    ax.fill_between(generations, mean - std, mean + std, 
                     alpha=0.2, color=colors[algo_name])

ax.set_xlabel('Generation', fontsize=12)
ax.set_ylabel('Best Fitness', fontsize=12)
ax.set_title('Convergence - Linear Scale', fontsize=13)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3)

# ---- Subplot 2: Logarithmic scale (reveals structure) ----
ax = axes[1]
for algo_name, stats in statistics.items():
    mean = stats['mean']
    std = stats['std']
    
    # Avoid log(0) by adding small epsilon
    mean_safe = np.maximum(mean, 1e-10)
    std_safe = np.maximum(std, 1e-10)
    
    # Plot mean line
    ax.semilogy(generations, mean_safe, linewidth=3, label=algo_name,
                color=colors[algo_name])
    
    # Add error band (±1 std)
    ax.fill_between(generations, 
                     np.maximum(mean_safe - std_safe, 1e-10),
                     mean_safe + std_safe,
                     alpha=0.2, color=colors[algo_name])

ax.set_xlabel('Generation', fontsize=12)
ax.set_ylabel('Best Fitness (log scale)', fontsize=12)
ax.set_title('Convergence - Logarithmic Scale', fontsize=13)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3, which='both')

plt.suptitle(f'Algorithm Comparison on Ackley Function ({INDEPENDENT_RUNS} runs each)', 
             fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('comparison_ackley.png', dpi=100, bbox_inches='tight')
print("✓ Comparison plot saved to 'comparison_ackley.png'")
plt.close()


# STEP 4: Identify convergence characteristics


print("\nConvergence Characteristics:")
for algo_name, all_runs in convergence_data.items():
    histories = np.array(all_runs)
    
    # Early convergence (first 25% of generations)
    early_idx = MAX_ITERATIONS // 4
    early_improvement = histories[:, 0] - histories[:, early_idx]
    
    # Late convergence (last 25% of generations)
    late_idx = 3 * MAX_ITERATIONS // 4
    late_improvement = histories[:, late_idx] - histories[:, -1]
    
    print(f"\n  {algo_name}:")
    print(f"    Early convergence (gen 0-{early_idx}): {np.mean(early_improvement):.6e} avg improvement")
    print(f"    Late convergence (gen {late_idx}-{MAX_ITERATIONS}): {np.mean(late_improvement):.6e} avg improvement")
    
    # Stagnation detection
    improvements = -np.diff(histories, axis=1)
    zero_improvements = np.sum(improvements < 1e-10, axis=1)
    stagnation_ratio = np.mean(zero_improvements) / (MAX_ITERATIONS - 1) * 100
    print(f"    Stagnation ratio: {stagnation_ratio:.2f}%")


# STEP 5: Summary and interpretation


print("\n" + "="*70)
print("INTERPRETATION GUIDE:")
print("="*70)

best_algo = min(statistics.items(), 
                key=lambda x: x[1]['mean'][-1])[0]

print(f"\n✓ Best average performance: {best_algo}")
print(f"\nWhat the plots show:")
print(f"  - Linear scale: Overall convergence trend")
print(f"  - Log scale: Fine-grained convergence stages")
print(f"  - Shaded areas: Uncertainty (±1 std over {INDEPENDENT_RUNS} runs)")
print(f"  - Steep early phase: Exploration phase")
print(f"  - Flat late phase: Exploitation/stagnation phase")
print("\nNext steps:")
print(f"  - Run example 3 for statistical significance testing")
print(f"  - Tune hyperparameters to improve performance")
print(f"  - Try other benchmarks: sphere, rosenbrock, schwefel")
print("="*70)
