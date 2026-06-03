#!/usr/bin/env python3
"""
Example 1: Basic Usage of evobench

This example demonstrates the simplest way to use evobench:
optimize the Sphere function using Particle Swarm Optimization (PSO).

Learning outcomes:
- Import algorithms and benchmarks from the Facade API
- Create an optimizer instance
- Run optimization and retrieve results
- Interpret convergence history
"""

import numpy as np
from evobench import PSO, sphere


# STEP 1: Define the problem


# Problem dimensionality
DIMENSION = 10

# Search space bounds: Sphere is typically defined on [-5, 5]^d
BOUNDS = [(-5, 5)] * DIMENSION

print(f"Problem Setup:")
print(f"  Benchmark: Sphere function")
print(f"  Dimensionality: {DIMENSION}D")
print(f"  Search space: {BOUNDS[0]} per dimension")
print()


# STEP 2: Create optimizer instance


# Initialize PSO with default hyperparameters
optimizer = PSO(
    objective_function=sphere,
    bounds=BOUNDS,
    population_size=50,
    max_iterations=100
)

print(f"Optimizer Setup:")
print(f"  Algorithm: PSO (Particle Swarm Optimization)")
print(f"  Population size: 50 particles")
print(f"  Max iterations: 100 generations")
print()


# STEP 3: Run optimization


print("Running optimization...")
best_solution, best_fitness = optimizer.run()

print(f"✓ Optimization complete!")
print()


# STEP 4: Inspect results


print(f"Results:")
print(f"  Best solution shape: {best_solution.shape}")
print(f"  Best solution (first 5 dims): {best_solution[:5]}")
print(f"  Best fitness value: {best_fitness:.6e}")
print()


# STEP 5: Analyze convergence


print(f"Convergence Analysis:")
print(f"  Generations tracked: {len(optimizer.fitness_history)}")
print(f"  Initial fitness: {optimizer.fitness_history[0]:.6e}")
print(f"  Final fitness: {optimizer.fitness_history[-1]:.6e}")

# Calculate improvement
initial = optimizer.fitness_history[0]
final = optimizer.fitness_history[-1]
improvement_ratio = (initial - final) / initial * 100
print(f"  Improvement: {improvement_ratio:.2f}%")
print()


# STEP 6: Visualize convergence (optional)


try:
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 6))
    plt.semilogy(optimizer.fitness_history, linewidth=2, color='blue', marker='o', 
                 markevery=max(1, len(optimizer.fitness_history)//10))
    plt.xlabel('Generation', fontsize=12)
    plt.ylabel('Best Fitness (log scale)', fontsize=12)
    plt.title(f'PSO Convergence on Sphere Function (d={DIMENSION})', fontsize=14)
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    
    # Save to examples directory
    plt.savefig('convergence_sphere.png', dpi=100, bbox_inches='tight')
    print("✓ Convergence plot saved to 'convergence_sphere.png'")
    plt.close()
except ImportError:
    print("(matplotlib not available; skipping visualization)")
print()


# STEP 7: Verify solution quality


# Evaluate the best solution independently
independent_eval = sphere(best_solution)
assert np.isclose(independent_eval, best_fitness), "Mismatch between reported and computed fitness!"

print(f"✓ Solution verification passed")
print(f"  Reported fitness: {best_fitness:.6e}")
print(f"  Independent eval: {independent_eval:.6e}")
print()

print("=" * 70)
print("Example 1 complete! Next steps:")
print("  - Try different algorithms: from evobench import EDA, ABC")
print("  - Try different benchmarks: from evobench import rosenbrock, ackley")
print("  - Tune hyperparameters (population_size, max_iterations)")
print("  - Run example 3 for statistical comparison of algorithms")
print("=" * 70)
