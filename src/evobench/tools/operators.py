from typing import Tuple
import numpy as np

"""
Evolutionary Operators Module

This module contains the selection, crossover, and mutation mechanisms
required for population-based metaheuristics operating in continuous 
search spaces. These operators are designed to be dynamically injected 
into the main evolutionary algorithms.
"""


# SELECTION OPERATORS


def tournament_selection(population: np.ndarray, fitness_values: np.ndarray, tournament_size: int = 3) -> np.ndarray:
    """
    Selects a single individual from the population using tournament selection.
    
    A subset of individuals is chosen uniformly at random. The individual 
    with the best (lowest) fitness within this subset is selected to reproduce.
    This method allows easy adjustment of selection pressure via the tournament size.

    Args:
        population (numpy.ndarray): The current matrix of candidate solutions.
        fitness_values (numpy.ndarray): The corresponding objective function values.
        tournament_size (int): The amount of individuals competing in the tournament.

    Returns:
        numpy.ndarray: The selected parent vector.
    """
    population_size = len(population)
    
    # Randomly sample indices without replacement to form the tournament subset
    tournament_indices = np.random.choice(population_size, size=tournament_size, replace=False)
    tournament_fitnesses = fitness_values[tournament_indices]
    
    # Identify the index of the individual with the minimum fitness value
    winner_local_index = np.argmin(tournament_fitnesses)
    winner_global_index = tournament_indices[winner_local_index]
    
    return population[winner_global_index]


def roulette_wheel_selection(population: np.ndarray, fitness_values: np.ndarray) -> np.ndarray:
    """
    Selects an individual using stochastic sampling with replacement (Roulette Wheel).
    
    Since the objective is minimization, the fitness values are inverted so that 
    lower objective values correspond to higher probabilities of selection.
    
    Args:
        population (numpy.ndarray): The current matrix of candidate solutions.
        fitness_values (numpy.ndarray): The corresponding objective function values.

    Returns:
        numpy.ndarray: The selected parent vector.
    """
    # Shift and invert fitness values to handle minimization properly
    maximum_fitness = np.max(fitness_values)
    inverted_fitness = maximum_fitness - fitness_values
    
    # Calculate the total inverted fitness to normalize probabilities
    total_fitness = np.sum(inverted_fitness)
    
    # Handle the edge case where all individuals have the exact same fitness
    if total_fitness == 0:
        selection_probabilities = np.ones(len(fitness_values)) / len(fitness_values)
    else:
        selection_probabilities = inverted_fitness / total_fitness
        
    # Select a single index based on the calculated probability distribution
    selected_index = np.random.choice(len(population), p=selection_probabilities)
    
    return population[selected_index]


def boltzmann_selection(population: np.ndarray, fitness_values: np.ndarray, temperature: float) -> np.ndarray:
    """
    Selects an individual using Boltzmann distribution probabilities.
    
    This method incorporates a simulated annealing concept. High temperatures 
    at the beginning of the run smooth out the probabilities, encouraging exploration.
    Low temperatures towards the end sharpen the probabilities, driving exploitation.

    Args:
        population (numpy.ndarray): The current matrix of candidate solutions.
        fitness_values (numpy.ndarray): The corresponding objective function values.
        temperature (float): The current cooling parameter.

    Returns:
        numpy.ndarray: The selected parent vector.
    """
    # Subtracting the minimum fitness prevents numerical underflow in the exponential
    adjusted_fitness = fitness_values - np.min(fitness_values)
    
    # Calculate Boltzmann weights
    exponential_weights = np.exp(-adjusted_fitness / temperature)
    selection_probabilities = exponential_weights / np.sum(exponential_weights)
    
    # Choose parent according to the thermally adjusted probabilities
    selected_index = np.random.choice(len(population), p=selection_probabilities)
    
    return population[selected_index]



# CROSSOVER OPERATORS (REAL RECOMBINATION)


def arithmetic_crossover(parent_a: np.ndarray, parent_b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Performs arithmetic crossover between two continuous vectors.
    
    Creates two offspring that are linear combinations of the parents. 
    This operator is highly effective for continuous optimization as it 
    allows the algorithm to interpolate within the search space.

    Args:
        parent_a (numpy.ndarray): The first parent vector.
        parent_b (numpy.ndarray): The second parent vector.

    Returns:
        tuple: Two new offspring vectors (numpy.ndarray, numpy.ndarray).
    """
    # Generate a random interpolation coefficient for the linear combination
    alpha = np.random.rand()
    
    # Compute the arithmetic mean weighted by the alpha parameter
    child_a = alpha * parent_a + (1 - alpha) * parent_b
    child_b = alpha * parent_b + (1 - alpha) * parent_a
    
    return child_a, child_b


def uniform_crossover(parent_a: np.ndarray, parent_b: np.ndarray, crossover_rate: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Executes uniform crossover by randomly swapping alleles between parents.
    
    Each gene (dimension) is evaluated independently. If a random float is 
    below the crossover rate, the genes are swapped between the two parents.

    Args:
        parent_a (numpy.ndarray): The first parent vector.
        parent_b (numpy.ndarray): The second parent vector.
        crossover_rate (float): The probability of swapping a specific dimension.

    Returns:
        tuple: Two new offspring vectors (numpy.ndarray, numpy.ndarray).
    """
    child_a = np.copy(parent_a)
    child_b = np.copy(parent_b)
    
    # Create a boolean mask indicating which dimensions should be swapped
    swap_mask = np.random.rand(len(parent_a)) < crossover_rate
    
    # Perform the swap using logical indexing based on the generated mask
    child_a[swap_mask] = parent_b[swap_mask]
    child_b[swap_mask] = parent_a[swap_mask]
    
    return child_a, child_b


def one_point_crossover(parent_a: np.ndarray, parent_b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Applies classical single-point crossover to continuous vectors.
    
    A random crossover point is selected along the vector length. The tail 
    segments of the parents are exchanged to create the offspring.

    Args:
        parent_a (numpy.ndarray): The first parent vector.
        parent_b (numpy.ndarray): The second parent vector.

    Returns:
        tuple: Two new offspring vectors (numpy.ndarray, numpy.ndarray).
    """
    vector_length = len(parent_a)
    
    # Select a random split point ensuring at least one element is swapped
    crossover_point = np.random.randint(1, vector_length)
    
    child_a = np.copy(parent_a)
    child_b = np.copy(parent_b)
    
    # Recombine the head of one parent with the tail of the other
    child_a[crossover_point:] = parent_b[crossover_point:]
    child_b[crossover_point:] = parent_a[crossover_point:]
    
    return child_a, child_b



# MUTATION OPERATORS (REAL CODING)


def gaussian_mutation(individual: np.ndarray, bounds: np.ndarray, mutation_probability: float, sigma: float = 0.1) -> np.ndarray:
    """
    Perturbs an individual using a Gaussian distribution.
    
    This is the standard mutation operator for fine-tuning (exploitation) 
    in continuous spaces. It adds normally distributed noise to the alleles.

    Args:
        individual (numpy.ndarray): The candidate vector to mutate.
        bounds (numpy.ndarray): The lower and upper boundaries of the search space.
        mutation_probability (float): The chance of mutating each individual gene.
        sigma (float): The standard deviation controlling the step size.

    Returns:
        numpy.ndarray: The mutated individual.
    """
    mutated_individual = np.copy(individual)
    
    for i in range(len(mutated_individual)):
        # Determine if the current dimension will undergo mutation
        if np.random.rand() < mutation_probability:
            # Calculate the domain range to scale the Gaussian noise accordingly
            domain_range = bounds[i][1] - bounds[i][0]
            noise = np.random.normal(0, sigma * domain_range)
            
            mutated_individual[i] += noise
            
            # Enforce boundary constraints to prevent leaving the search space
            mutated_individual[i] = np.clip(mutated_individual[i], bounds[i][0], bounds[i][1])
            
    return mutated_individual


def uniform_mutation(individual: np.ndarray, bounds: np.ndarray, mutation_probability: float) -> np.ndarray:
    """
    Replaces an individual's gene with a completely random value.
    
    This operator prevents premature convergence by promoting global exploration.
    It replaces the existing allele with a new uniform random value drawn 
    from the domain boundaries.

    Args:
        individual (numpy.ndarray): The candidate vector to mutate.
        bounds (numpy.ndarray): The lower and upper boundaries of the search space.
        mutation_probability (float): The chance of mutating each individual gene.

    Returns:
        numpy.ndarray: The mutated individual.
    """
    mutated_individual = np.copy(individual)
    
    for i in range(len(mutated_individual)):
        # Evaluate the probability constraint for the current gene
        if np.random.rand() < mutation_probability:
            # Generate a completely new value independent of the previous state
            mutated_individual[i] = np.random.uniform(bounds[i][0], bounds[i][1])
            
    return mutated_individual


def non_uniform_mutation(individual: np.ndarray, bounds: np.ndarray, current_iteration: int, max_iterations: int, b_parameter: float = 2) -> np.ndarray:
    """
    Applies dynamic mutation that decreases in magnitude over generations.
    
    Initially allows large jumps across the search space. As the current iteration
    approaches the maximum iterations, the mutation step size shrinks to perform
    local search. Based on Michalewicz's non-uniform mutation.

    Args:
        individual (numpy.ndarray): The candidate vector to mutate.
        bounds (numpy.ndarray): The lower and upper boundaries of the search space.
        current_iteration (int): The current generation counter.
        max_iterations (int): The total generations allowed.
        b_parameter (float): Determines the degree of dependency on the iteration number.

    Returns:
        numpy.ndarray: The mutated individual.
    """
    mutated_individual = np.copy(individual)
    
    for i in range(len(mutated_individual)):
        # Calculate the distance from the current allele to both boundaries
        lower_bound = bounds[i][0]
        upper_bound = bounds[i][1]
        
        # Decide randomly whether to shift towards the upper or lower boundary
        random_direction = np.random.rand()
        
        if random_direction < 0.5:
            delta = upper_bound - mutated_individual[i]
        else:
            delta = mutated_individual[i] - lower_bound
            
        # Compute the non-uniform adjustment factor
        random_value = np.random.rand()
        decay_factor = (1 - (current_iteration / max_iterations)) ** b_parameter
        shift_magnitude = delta * (1 - (random_value ** decay_factor))
        
        # Apply the dynamic shift to the gene
        if random_direction < 0.5:
            mutated_individual[i] += shift_magnitude
        else:
            mutated_individual[i] -= shift_magnitude
            
    return mutated_individual