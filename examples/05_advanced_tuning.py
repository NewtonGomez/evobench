#!/usr/bin/env python3
"""
Example 5: Hyperparameter Tuning via Grid Search

This example demonstrates:
- Systematic exploration of hyperparameter space
- Grid Search strategy for tuning algorithms
- Evaluation of parameter sensitivity
- Identifying optimal configuration for a problem

Learning outcomes:
- Understand which hyperparameters affect performance
- Learn Grid Search methodology (brute force parameter exploration)
- Interpret parameter sensitivity plots
- Select optimal hyperparameters for deployment
"""

import numpy as np
import itertools
from evobench import PSO, sphere


# CONFIGURATION


DIMENSION = 10
BOUNDS = [(-5, 5)] * DIMENSION
MAX_ITERATIONS = 100
INDEPENDENT_RUNS = 3  # Reduce for faster execution

print("="*70)
print("HYPERPARAMETER TUNING: GRID SEARCH")
print("="*70)
print()

print(f"Problem Setup:")
print(f"  Benchmark: Sphere function")
print(f"  Dimensionality: {DIMENSION}D")
print(f"  Max iterations: {MAX_ITERATIONS}")
print(f"  Runs per configuration: {INDEPENDENT_RUNS}")
print()


# STEP 1: Define hyperparameter grid


# PSO hyperparameters to tune
param_grid = {
    'population_size': [20, 50, 100],
    'inertia_weight': [0.4, 0.7, 1.0],
    'cognitive_constant': [1.5, 2.0],
    'social_constant': [1.5, 2.0]
}

# Generate all combinations
param_names = list(param_grid.keys())
param_values = list(param_grid.values())
configurations = list(itertools.product(*param_values))

print(f"Hyperparameter Grid:")
for param_name, values in param_grid.items():
    print(f"  {param_name:20s}: {values}")

print()
print(f"Total configurations to test: {len(configurations)}")
print()


# STEP 2: Run Grid Search


print("Running Grid Search...")
print()

np.random.seed(42)

results = []
config_idx = 0

for config in configurations:
    # Unpack configuration
    params = {name: value for name, value in zip(param_names, config)}
    
    config_idx += 1
    print(f"Configuration {config_idx}/{len(configurations)}")
    print(f"  Parameters: {params}")
    
    # Run independent runs
    fitnesses = []
    for run_id in range(INDEPENDENT_RUNS):
        optimizer = PSO(
            objective_function=sphere,
            bounds=BOUNDS,
            max_iterations=MAX_ITERATIONS,
            **params
        )
        _, best_fit = optimizer.run()
        fitnesses.append(best_fit)
    
    # Compute statistics
    mean_fitness = np.mean(fitnesses)
    std_fitness = np.std(fitnesses)
    
    print(f"  Results: {mean_fitness:.6e} ± {std_fitness:.6e}")
    print()
    
    # Store result
    results.append({
        'config': params,
        'mean_fitness': mean_fitness,
        'std_fitness': std_fitness,
        'fitnesses': fitnesses
    })


# STEP 3: Analyze Results


print("="*70)
print("GRID SEARCH RESULTS")
print("="*70)
print()

# Sort by mean fitness (best first)
sorted_results = sorted(results, key=lambda x: x['mean_fitness'])

# Display top 5 configurations
print("Top 5 Configurations:")
print()

for rank, result in enumerate(sorted_results[:5], 1):
    config = result['config']
    mean_fit = result['mean_fitness']
    std_fit = result['std_fitness']
    
    print(f"{rank}. Mean Fitness: {mean_fit:.6e} (±{std_fit:.6e})")
    for param_name, value in config.items():
        print(f"   {param_name:20s}: {value}")
    print()


# STEP 4: Analyze Parameter Sensitivity


print("="*70)
print("PARAMETER SENSITIVITY ANALYSIS")
print("="*70)
print()

# Analyze each parameter independently
for param_name in param_names:
    print(f"\n{param_name}:")
    
    # Group results by parameter value
    param_values_used = {}
    for result in results:
        value = result['config'][param_name]
        if value not in param_values_used:
            param_values_used[value] = []
        param_values_used[value].append(result['mean_fitness'])
    
    # Calculate mean performance for each parameter value
    print(f"  Values: {sorted(param_values_used.keys())}")
    for value in sorted(param_values_used.keys()):
        fitnesses = param_values_used[value]
        mean = np.mean(fitnesses)
        std = np.std(fitnesses)
        print(f"    {value:10} → Mean: {mean:.6e} (σ={std:.6e})")


# STEP 5: Visualization


try:
    import matplotlib.pyplot as plt
    
    print()
    print("Creating visualization...")
    
    # Prepare data for visualization
    best_fitnesses = [r['mean_fitness'] for r in results]
    config_labels = [f"Config {i+1}" for i in range(len(results))]
    
    # Sort for better visualization
    sorted_indices = np.argsort(best_fitnesses)
    best_fitnesses_sorted = [best_fitnesses[i] for i in sorted_indices]
    
    # Create bar plot of top 10 configurations
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: All configurations (sorted)
    ax = axes[0, 0]
    ax.bar(range(len(best_fitnesses_sorted)), best_fitnesses_sorted, 
           color='steelblue', alpha=0.7)
    ax.set_xlabel('Configuration Index (sorted)', fontsize=11)
    ax.set_ylabel('Mean Best Fitness', fontsize=11)
    ax.set_title('All Configurations Performance', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Top 10 configurations
    ax = axes[0, 1]
    top_10 = best_fitnesses_sorted[:10]
    ax.barh(range(len(top_10)), top_10, color='forestgreen', alpha=0.7)
    ax.set_yticks(range(len(top_10)))
    ax.set_yticklabels([f"#{i+1}" for i in range(len(top_10))])
    ax.set_xlabel('Mean Best Fitness', fontsize=11)
    ax.set_title('Top 10 Configurations', fontsize=12)
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, axis='x')
    
    # Plot 3: Parameter sensitivity - Population Size
    ax = axes[1, 0]
    pop_sizes = sorted(param_grid['population_size'])
    pop_perf = []
    for pop_size in pop_sizes:
        perf = [r['mean_fitness'] for r in results 
                if r['config']['population_size'] == pop_size]
        pop_perf.append(np.mean(perf))
    
    ax.plot(pop_sizes, pop_perf, 'o-', linewidth=2, markersize=8, 
           color='darkblue')
    ax.set_xlabel('Population Size', fontsize=11)
    ax.set_ylabel('Mean Best Fitness', fontsize=11)
    ax.set_title('Population Size Sensitivity', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Parameter sensitivity - Inertia Weight
    ax = axes[1, 1]
    inertias = sorted(param_grid['inertia_weight'])
    inertia_perf = []
    for inertia in inertias:
        perf = [r['mean_fitness'] for r in results 
                if r['config']['inertia_weight'] == inertia]
        inertia_perf.append(np.mean(perf))
    
    ax.plot(inertias, inertia_perf, 's-', linewidth=2, markersize=8,
           color='darkred')
    ax.set_xlabel('Inertia Weight', fontsize=11)
    ax.set_ylabel('Mean Best Fitness', fontsize=11)
    ax.set_title('Inertia Weight Sensitivity', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.suptitle('Hyperparameter Grid Search Results', 
                fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('grid_search_results.png', dpi=100, bbox_inches='tight')
    print("✓ Grid search visualization saved to 'grid_search_results.png'")
    plt.close()
    
except ImportError:
    print("(matplotlib not available; skipping visualization)")


# STEP 6: Recommendations and Next Steps


print()
print("="*70)
print("RECOMMENDATIONS")
print("="*70)
print()

best_config = sorted_results[0]
print(f"Optimal Configuration Found:")
print(f"  Mean Fitness: {best_config['mean_fitness']:.6e}")
print()
print("  Hyperparameters:")
for param_name, value in best_config['config'].items():
    print(f"    {param_name:20s}: {value}")
print()

print("Key Insights:")
print("  - Parameter sensitivity reveals which settings matter most")
print("  - Some parameters may have negligible impact (consider fixing them)")
print("  - Optimal settings depend on problem characteristics")
print("  - Consider Random Search or Bayesian Optimization for finer tuning")
print()

print("Next Steps:")
print("  - Use optimal configuration in deployment")
print("  - Verify performance on test set")
print("  - Try different tuning strategies (Bayesian, Genetic Algorithms)")
print("  - Tune parameters for other algorithms (EDA, ABC)")
print()

print("="*70)
