#!/usr/bin/env python3
"""
Example 4: Custom Algorithm - Extending the Framework

This example demonstrates extensibility by implementing a custom algorithm:
- Genetic Algorithm (GA) with tournament selection and mutation/crossover
- Inherits from EvolutionaryAlgorithm abstract base class
- Uses utilities from evobench.tools

Learning outcomes:
- Understand the EvolutionaryAlgorithm interface
- Implement a custom optimization algorithm
- Use inherited methods and state tracking
- Test custom algorithms alongside built-in ones
"""

import numpy as np
from evobench.base import EvolutionaryAlgorithm
from evobench.benchmarks import sphere
from typing import Tuple


# CUSTOM ALGORITHM: Simple Genetic Algorithm (GA)


class SimpleGeneticAlgorithm(EvolutionaryAlgorithm):
    """
    A simple Genetic Algorithm implementation.
    
    Features:
    - Tournament selection for parent selection
    - Single-point crossover for recombination
    - Gaussian mutation for perturbation
    - Elitism: best solution preserved automatically
    
    Hyperparameters:
    - mutation_rate: Probability of mutation per gene [0, 1]
    - crossover_rate: Probability of crossover [0, 1]
    - tournament_size: Number of individuals in tournament selection
    """
    
    def __init__(self, objective_function, bounds,
                 population_size=50, max_iterations=100,
                 mutation_rate=0.1, crossover_rate=0.8, 
                 tournament_size=3):
        """Initialize GA with hyperparameters."""
        super().__init__(objective_function, bounds, 
                         population_size, max_iterations)
        
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
    
    def _tournament_selection(self, population: np.ndarray, 
                              fitness: np.ndarray) -> np.ndarray:
        """Select individual via tournament."""
        tournament_idx = np.random.choice(len(population), 
                                          self.tournament_size, 
                                          replace=False)
        best_in_tournament = tournament_idx[np.argmin(fitness[tournament_idx])]
        return population[best_in_tournament].copy()
    
    def _crossover(self, parent1: np.ndarray, 
                   parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Single-point crossover."""
        if np.random.rand() < self.crossover_rate:
            crossover_point = np.random.randint(1, self.dimension)
            child1 = np.concatenate([parent1[:crossover_point], 
                                     parent2[crossover_point:]])
            child2 = np.concatenate([parent2[:crossover_point], 
                                     parent1[crossover_point:]])
            return child1, child2
        else:
            return parent1.copy(), parent2.copy()
    
    def _mutate(self, individual: np.ndarray) -> np.ndarray:
        """Gaussian mutation."""
        mutation_mask = np.random.rand(self.dimension) < self.mutation_rate
        sigma = (self.bounds[:, 1] - self.bounds[:, 0]) * 0.01
        
        mutant = individual.copy()
        mutant[mutation_mask] += np.random.normal(0, sigma[mutation_mask])
        
        # Apply boundary constraints
        lower = self.bounds[:, 0]
        upper = self.bounds[:, 1]
        mutant = np.clip(mutant, lower, upper)
        
        return mutant
    
    def run(self) -> Tuple[np.ndarray, float]:
        """Execute GA optimization loop."""
        # Initialize population
        population = self._initialize_population()
        
        for generation in range(self.max_iterations):
            # Evaluate fitness
            fitness = np.apply_along_axis(self.objective_function, 1, population)
            
            # Track best
            best_idx = np.argmin(fitness)
            if fitness[best_idx] < self.best_fitness:
                self.best_fitness = fitness[best_idx]
                self.best_individual = population[best_idx].copy()
            
            self.fitness_history.append(self.best_fitness)
            
            # Create next generation
            new_population = []
            
            # Elitism: preserve best
            new_population.append(self.best_individual.copy())
            
            # Generate remaining individuals via selection/crossover/mutation
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self._tournament_selection(population, fitness)
                parent2 = self._tournament_selection(population, fitness)
                
                # Crossover
                child1, child2 = self._crossover(parent1, parent2)
                
                # Mutation
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)
                
                new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)
            
            population = np.array(new_population[:self.population_size])
        
        return self.best_individual, self.best_fitness



# DEMONSTRATION: Compare custom GA with built-in algorithms


if __name__ == "__main__":
    from evobench import PSO, EDA, ABC
    
    print("="*70)
    print("CUSTOM ALGORITHM DEMONSTRATION")
    print("="*70)
    print()
    
    # Problem setup
    DIMENSION = 10
    BOUNDS = [(-5, 5)] * DIMENSION
    POPULATION_SIZE = 50
    MAX_ITERATIONS = 100
    
    print(f"Problem Setup:")
    print(f"  Benchmark: Sphere function")
    print(f"  Dimensionality: {DIMENSION}D")
    print(f"  Search space: {BOUNDS[0]} per dimension")
    print()
    
    # Initialize all algorithms
    print("Initializing algorithms...")
    print()
    
    algorithms = {
        'PSO (built-in)': PSO(sphere, BOUNDS, POPULATION_SIZE, MAX_ITERATIONS),
        'EDA (built-in)': EDA(sphere, BOUNDS, POPULATION_SIZE, MAX_ITERATIONS),
        'ABC (built-in)': ABC(sphere, BOUNDS, POPULATION_SIZE, MAX_ITERATIONS),
        'GA (custom)': SimpleGeneticAlgorithm(
            sphere, BOUNDS, 
            population_size=POPULATION_SIZE, 
            max_iterations=MAX_ITERATIONS,
            mutation_rate=0.1,
            crossover_rate=0.8,
            tournament_size=3
        )
    }
    
    # Run all algorithms
    print("Running optimization...")
    print()
    
    results = {}
    np.random.seed(42)
    
    for algo_name, optimizer in algorithms.items():
        best_sol, best_fit = optimizer.run()
        results[algo_name] = {
            'best_fitness': best_fit,
            'fitness_history': optimizer.fitness_history,
            'optimizer': optimizer
        }
        print(f"✓ {algo_name:20s}: Final fitness = {best_fit:.6e}")
    
    print()
    
    
    # ANALYSIS AND VISUALIZATION
    
    
    try:
        import matplotlib.pyplot as plt
        
        print("Creating comparison visualization...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        colors = {
            'PSO (built-in)': '#1f77b4',
            'EDA (built-in)': '#ff7f0e',
            'ABC (built-in)': '#2ca02c',
            'GA (custom)': '#d62728'
        }
        
        # Linear scale
        for algo_name, data in results.items():
            history = data['fitness_history']
            ax1.plot(history, linewidth=2.5, label=algo_name, 
                    color=colors[algo_name], marker='o',
                    markevery=max(1, len(history)//15))
        
        ax1.set_xlabel('Generation', fontsize=12)
        ax1.set_ylabel('Best Fitness', fontsize=12)
        ax1.set_title('Convergence - Linear Scale', fontsize=13)
        ax1.legend(fontsize=10, loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # Log scale
        for algo_name, data in results.items():
            history = np.maximum(np.array(data['fitness_history']), 1e-10)
            ax2.semilogy(history, linewidth=2.5, label=algo_name,
                        color=colors[algo_name], marker='o',
                        markevery=max(1, len(history)//15))
        
        ax2.set_xlabel('Generation', fontsize=12)
        ax2.set_ylabel('Best Fitness (log scale)', fontsize=12)
        ax2.set_title('Convergence - Logarithmic Scale', fontsize=13)
        ax2.legend(fontsize=10, loc='upper right')
        ax2.grid(True, alpha=0.3, which='both')
        
        plt.suptitle('Custom GA vs Built-in Algorithms on Sphere Function', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('custom_algorithm_comparison.png', dpi=100, bbox_inches='tight')
        print("✓ Comparison plot saved to 'custom_algorithm_comparison.png'")
        plt.close()
        
    except ImportError:
        print("(matplotlib not available; skipping visualization)")
    
    
    # PERFORMANCE RANKING
    
    
    print()
    print("="*70)
    print("PERFORMANCE RANKING")
    print("="*70)
    print()
    
    ranking = sorted(results.items(), 
                    key=lambda x: x[1]['best_fitness'])
    
    for rank, (algo_name, data) in enumerate(ranking, 1):
        improvement = ((results[list(results.keys())[0]]['best_fitness'] - 
                       data['best_fitness']) / 
                      results[list(results.keys())[0]]['best_fitness'] * 100)
        print(f"{rank}. {algo_name:20s}: {data['best_fitness']:.6e}")
    
    print()
    print("="*70)
    print("KEY TAKEAWAYS")
    print("="*70)
    print()
    print("✓ Successfully implemented and tested a custom algorithm (GA)")
    print("✓ Custom GA integrates seamlessly with evobench framework")
    print("✓ All algorithms tracked fitness_history automatically")
    print("✓ Can mix custom and built-in algorithms for fair comparison")
    print()
    print("Next steps:")
    print("  - Extend GA with advanced features (niching, adaptive mutation)")
    print("  - Implement other algorithms (DE, PSO variants, etc.)")
    print("  - Package custom algorithms in separate module")
    print("  - Share on PyPI for community use")
    print()
    print("="*70)
