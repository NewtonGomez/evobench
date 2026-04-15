import numpy as np
from typing import Callable, Tuple
from evobench.base import EvolutionaryAlgorithm
import evobench.tools.operators as ops

class EDA(EvolutionaryAlgorithm):
    """
    Continuous Estimation of Distribution Algorithm (EDA) with static typing.

    This metaheuristic models the search space using a probabilistic approach. 
    Instead of applying classical genetic operators like crossover or mutation, 
    it selects a subset of the best-performing individuals to estimate the 
    parameters of a Gaussian distribution (mean and standard deviation). 
    The subsequent generation is then entirely sampled from this updated 
    probability model, effectively guiding the search towards promising regions.
    """

    def __init__(
        self, 
        objective_function: Callable[[np.ndarray], float], 
        bounds: np.ndarray, 
        population_size: int = 50, 
        max_iterations: int = 100, 
        selection_ratio: float = 0.5
    ) -> None:
        """
        Initializes the EDA-specific hyperparameters alongside the standard 
        evolutionary algorithm attributes.

        Args:
            objective_function (Callable[[np.ndarray], float]): The mathematical 
                                                                function to minimize.
            bounds (np.ndarray): The spatial boundaries for the search domain.
            population_size (int): Total number of candidate solutions per generation.
            max_iterations (int): The termination criterion.
            selection_ratio (float): The fraction of the population selected to 
                                     estimate the probability distribution.
        """
        super().__init__(objective_function, bounds, population_size, max_iterations)
        
        # Determine the exact number of individuals that will form the elite pool
        self.selection_size = int(self.population_size * selection_ratio)

    def _apply_boundary_constraints(self, population: np.ndarray) -> np.ndarray:
        """
        Enforces spatial boundaries on a newly sampled population.

        Since the Gaussian distribution spans infinitely, sampled individuals 
        might fall outside the mathematical domain of the objective function.
        This method clips the values strictly within the permitted limits.

        Args:
            population (np.ndarray): The unbounded matrix of candidate solutions.

        Returns:
            np.ndarray: The spatially bounded population matrix.
        """
        lower_bounds = self.bounds[:, 0]
        upper_bounds = self.bounds[:, 1]
        
        # Apply strict clipping across all dimensions simultaneously
        bounded_population: np.ndarray = np.clip(population, lower_bounds, upper_bounds)
        return bounded_population

    def run(self) -> Tuple[np.ndarray, float]:
        """
        Executes the main probabilistic evolutionary loop.

        The process iteratively evaluates the population, selects the elite 
        subset using tournament selection, calculates the mean and standard 
        deviation vectors, and samples the new candidate solutions.

        Returns:
            Tuple[np.ndarray, float]: The global best candidate vector and 
                                      its corresponding fitness.
        """
        # Generate the initial uniform random population
        population = self._initialize_population()
        
        for _ in range(self.max_iterations):
            # Evaluate the objective function for every individual in the matrix
            fitness_values = np.apply_along_axis(self.objective_function, 1, population)
            
            # Track the best individual found in the current generation
            current_best_index = np.argmin(fitness_values)
            current_best_fitness = float(fitness_values[current_best_index])
            
            if current_best_fitness < self.best_fitness:
                self.best_fitness = current_best_fitness
                self.best_individual = np.copy(population[current_best_index])
            
            # Record the convergence history for later statistical analysis
            self.fitness_history.append(self.best_fitness)
            
            # Construct the elite pool using the previously defined selection operator
            # The tournament selection provides selection pressure while maintaining diversity
            elite_pool = np.empty((self.selection_size, self.dimension))
            for i in range(self.selection_size):
                elite_pool[i] = ops.tournament_selection(population, fitness_values, tournament_size=3)
            
            # Estimate the probability distribution parameters from the elite pool
            # The mean acts as the center of mass for the promising region
            mean_vector = np.mean(elite_pool, axis=0)
            
            # The standard deviation acts as the search radius or exploration threshold
            # A tiny constant is added to prevent mathematical errors if variance collapses to zero
            standard_deviation_vector = np.std(elite_pool, axis=0) + 1e-8
            
            # Sample the completely new population from the estimated Gaussian model
            # Elitism: Preserve the global best individual to guarantee monotonic improvement
            population = np.random.normal(
                loc=mean_vector, 
                scale=standard_deviation_vector, 
                size=(self.population_size, self.dimension)
            )
            
            population[0] = self.best_individual
            
            # Ensure the newly sampled coordinates do not violate the problem domain
            population = self._apply_boundary_constraints(population)
            
        return self.best_individual, self.best_fitness