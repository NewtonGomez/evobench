import numpy as np
from typing import Callable, Tuple
from evobench.base import EvolutionaryAlgorithm

class ParticleSwarmOptimization(EvolutionaryAlgorithm):
    """
    Standard Particle Swarm Optimization (PSO) for continuous spaces.

    This algorithm simulates a swarm of particles moving through a multi-dimensional 
    search space. Each particle maintains a velocity and a memory of its personal 
    best position. The movement is guided by an inertia weight, a cognitive 
    component (personal experience), and a social component (global best), 
    effectively balancing exploration and exploitation.
    """

    def __init__(
        self, 
        objective_function: Callable[[np.ndarray], float], 
        bounds: np.ndarray, 
        population_size: int = 50, 
        max_iterations: int = 100, 
        inertia_weight: float = 0.7, 
        cognitive_constant: float = 1.5, 
        social_constant: float = 1.5
    ) -> None:
        """
        Initializes the PSO hyperparameters and the base evolutionary attributes.

        Args:
            objective_function (Callable): The mathematical function to minimize.
            bounds (np.ndarray): Spatial boundaries [min, max] for each dimension.
            population_size (int): Number of particles in the swarm.
            max_iterations (int): Maximum number of iterations for the loop.
            inertia_weight (float): Factor that controls the impact of previous velocity.
            cognitive_constant (float): Acceleration coefficient for personal best.
            social_constant (float): Acceleration coefficient for global best.
        """
        super().__init__(objective_function, bounds, population_size, max_iterations)
        
        # Hyperparameters for the velocity update equation
        self.w = inertia_weight
        self.c1 = cognitive_constant
        self.c2 = social_constant

    def _apply_boundary_constraints(self, population: np.ndarray) -> np.ndarray:
        """
        Keeps particles within the search space and handles velocity reflections.

        Args:
            population (np.ndarray): The current positions of the swarm.

        Returns:
            np.ndarray: The bounded population matrix.
        """
        lower_bounds = self.bounds[:, 0]
        upper_bounds = self.bounds[:, 1]
        
        # Clip positions that exceed the established search domain
        return np.clip(population, lower_bounds, upper_bounds)

    def run(self) -> Tuple[np.ndarray, float]:
        """
        Executes the main PSO swarm intelligence loop.

        Returns:
            Tuple[np.ndarray, float]: The global best position and its fitness.
        """
        # Initializing swarm positions using the base uniform sampling method
        current_positions = self._initialize_population()
        
        # Velocities are initialized to zero for all particles and dimensions
        velocities = np.zeros((self.population_size, self.dimension))
        
        # Personal best positions (p_best) are initialized to the starting positions
        personal_best_positions = np.copy(current_positions)
        
        # Personal best fitness values initialized to infinity for minimization
        personal_best_fitness = np.full(self.population_size, float('inf'))
        
        for iteration in range(self.max_iterations):
            # Evaluate objective function for every particle in the swarm
            fitness_values = np.apply_along_axis(self.objective_function, 1, current_positions)
            
            # Update personal and global bests based on current evaluations
            for i in range(self.population_size):
                if fitness_values[i] < personal_best_fitness[i]:
                    personal_best_fitness[i] = fitness_values[i]
                    personal_best_positions[i] = np.copy(current_positions[i])
                    
                # Update the global optimum if a better solution is found
                if fitness_values[i] < self.best_fitness:
                    self.best_fitness = fitness_values[i]
                    self.best_individual = np.copy(current_positions[i])
            
            # Store the best fitness of the iteration for convergence tracking
            self.fitness_history.append(self.best_fitness)
            
            # Generate random coefficients for the stochastic components of the velocity
            r1 = np.random.rand(self.population_size, self.dimension)
            r2 = np.random.rand(self.population_size, self.dimension)
            
            # Calculate the cognitive and social attraction vectors
            cognitive_acceleration = self.c1 * r1 * (personal_best_positions - current_positions)
            social_acceleration = self.c2 * r2 * (self.best_individual - current_positions)
            
            # Update velocity applying inertia and acceleration components
            velocities = (self.w * velocities) + cognitive_acceleration + social_acceleration
            
            # Update particle positions based on the new velocity vectors
            current_positions += velocities
            
            # Enforce boundary constraints to keep the swarm within the domain
            current_positions = self._apply_boundary_constraints(current_positions)
            
        return self.best_individual, self.best_fitness