import numpy as np
from typing import Callable, Tuple
from evobench.base import EvolutionaryAlgorithm
import evobench.tools.operators as ops

class ArtificialBeeColony(EvolutionaryAlgorithm):
    """
    Artificial Bee Colony (ABC) metaheuristic for continuous optimization.

    This algorithm mimics the intelligent foraging behavior of a honey bee swarm. 
    The population is divided into three groups: Employed Bees, Onlooker Bees, 
    and Scout Bees. It utilizes a trial-counter mechanism to manage food source 
    exhaustion, ensuring the swarm escapes local optima through a structured 
    stagnation-replacement strategy.
    """

    def __init__(
        self, 
        objective_function: Callable[[np.ndarray], float], 
        bounds: np.ndarray, 
        population_size: int = 50, 
        max_iterations: int = 100, 
        limit: int = 20
    ) -> None:
        """
        Initializes the ABC hyperparameters and structural attributes.

        Args:
            objective_function (Callable): The mathematical function to minimize.
            bounds (np.ndarray): Spatial boundaries [min, max] for each dimension.
            population_size (int): Total number of bees. Half will be employed.
            max_iterations (int): Maximum number of search cycles.
            limit (int): Trials allowed before a food source is abandoned.
        """
        super().__init__(objective_function, bounds, population_size, max_iterations)
        
        # In ABC, the number of food sources is equal to half of the population
        self.food_sources_count = population_size // 2
        
        # Maximum trials allowed for a food source to improve before being discarded
        self.limit = limit
        
        # Array to track the number of failed attempts at improving each food source
        self.trial_counters = np.zeros(self.food_sources_count)

    def _apply_boundary_constraints(self, individual: np.ndarray) -> np.ndarray:
        """
        Clips the coordinates of a candidate solution to the defined search space.

        Args:
            individual (np.ndarray): The continuous vector to be constrained.

        Returns:
            np.ndarray: The bounded candidate solution.
        """
        lower_bounds = self.bounds[:, 0]
        upper_bounds = self.bounds[:, 1]
        
        return np.clip(individual, lower_bounds, upper_bounds)

    def run(self) -> Tuple[np.ndarray, float]:
        """
        Executes the three-phase artificial foraging cycle.

        Returns:
            Tuple[np.ndarray, float]: The global best solution and its fitness.
        """
        # Initial food sources are sampled uniformly from the search domain
        # In this algorithm, population size reflects the number of active food sources
        food_sources = self._initialize_population()[:self.food_sources_count]
        
        # Initial evaluation of the food source fitness
        fitness_values = np.apply_along_axis(self.objective_function, 1, food_sources)
        
        for iteration in range(self.max_iterations):
            
            # --- EMPLOYED BEES PHASE ---
            # Each employed bee explores a neighbor of its assigned food source
            for i in range(self.food_sources_count):
                
                # Select a random neighbor index different from current source
                neighbor_idx = np.random.choice([idx for idx in range(self.food_sources_count) if idx != i])
                
                # Select a random dimension to perturb
                dimension_idx = np.random.randint(self.dimension)
                
                # Calculate the neighbor solution using the ABC search formula
                # Phi is a random scaling factor in the range [-1, 1]
                phi = np.random.uniform(-1, 1)
                candidate_solution = np.copy(food_sources[i])
                candidate_solution[dimension_idx] += phi * (food_sources[i][dimension_idx] - food_sources[neighbor_idx][dimension_idx])
                
                # Enforce space boundaries and evaluate
                candidate_solution = self._apply_boundary_constraints(candidate_solution)
                candidate_fitness = self.objective_function(candidate_solution)
                
                # Greedy selection: update source if the new candidate is better
                if candidate_fitness < fitness_values[i]:
                    food_sources[i] = candidate_solution
                    fitness_values[i] = candidate_fitness
                    self.trial_counters[i] = 0
                else:
                    self.trial_counters[i] += 1

            # --- ONLOOKER BEES PHASE ---
            # Bees in the hive choose food sources to exploit based on probability (Roulette)
            for _ in range(self.food_sources_count):
                
                # Use the roulette selection from operators.py to favor better sources
                # We pass the full matrix and fitness values to pick a winning source index
                # Note: We simulate the selection of a source for additional local search
                selected_idx = ops.roulette_wheel_selection_index(food_sources, fitness_values)
                
                # Repeat the local search logic for the chosen source
                neighbor_idx = np.random.choice([idx for idx in range(self.food_sources_count) if idx != selected_idx])
                dimension_idx = np.random.randint(self.dimension)
                phi = np.random.uniform(-1, 1)
                
                candidate_solution = np.copy(food_sources[selected_idx])
                candidate_solution[dimension_idx] += phi * (food_sources[selected_idx][dimension_idx] - food_sources[neighbor_idx][dimension_idx])
                
                candidate_solution = self._apply_boundary_constraints(candidate_solution)
                candidate_fitness = self.objective_function(candidate_solution)
                
                # Greedy selection for the onlooker bee's target
                if candidate_fitness < fitness_values[selected_idx]:
                    food_sources[selected_idx] = candidate_solution
                    fitness_values[selected_idx] = candidate_fitness
                    self.trial_counters[selected_idx] = 0
                else:
                    self.trial_counters[selected_idx] += 1

            # --- SCOUT BEES PHASE ---
            # Identify food sources that have exceeded the trial limit without improvement
            for i in range(self.food_sources_count):
                if self.trial_counters[i] > self.limit:
                    
                    # Abandon the exhausted source and re-initialize it randomly
                    # This step prevents premature convergence to local optima
                    lower_bounds = self.bounds[:, 0]
                    upper_bounds = self.bounds[:, 1]
                    food_sources[i] = np.random.uniform(lower_bounds, upper_bounds, self.dimension)
                    fitness_values[i] = self.objective_function(food_sources[i])
                    self.trial_counters[i] = 0

            # Update the global optimum record
            best_idx = np.argmin(fitness_values)
            if fitness_values[best_idx] < self.best_fitness:
                self.best_fitness = fitness_values[best_idx]
                self.best_individual = np.copy(food_sources[best_idx])
            
            # Store best fitness for convergence history tracking
            self.fitness_history.append(self.best_fitness)

        return self.best_individual, self.best_fitness