from typing import Tuple, List, Callable
import inspect
import numpy as np
import pytest

import evobench.tools.operators as ops 

"""
Unit testing module for Evolutionary Crossover Operators.

This module dynamically discovers and tests all recombination mechanisms 
within the operators module. It guarantees that every crossover function 
accepts two parent vectors and successfully returns two offspring vectors 
while preserving the continuous search space dimensionality.
"""

# TEST CROSSOVER FUNCTIONS

def get_crossover_functions() -> List[Callable]:
    """
    Dynamically retrieves all functions from the operators module designed 
    for genetic recombination.

    It scans the module's namespace and filters for callable objects containing 
    the keyword 'crossover' in their definition name. This introspective approach 
    ensures the test suite scales automatically as new operators are developed.

    Returns:
        list: A collection of callable crossover function objects.
    """
    crossover_funcs = []
    
    # Iterate through all available attributes in the operators module
    for name, obj in inspect.getmembers(ops):
        # Isolate callable functions that match the crossover naming convention
        if inspect.isfunction(obj) and 'crossover' in name:
            crossover_funcs.append(obj)
            
    return crossover_funcs


@pytest.fixture
def synthetic_parents_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Pytest fixture supplying standardized parent vectors for recombination tests.

    Generates two deterministic, continuous vectors representing candidate 
    solutions in a multi-dimensional search space. Seeding the random generator 
    ensures test reproducibility.

    Returns:
        tuple: Two distinct numpy arrays representing the parent genomes.
    """
    dimension = 10
    
    # Initialize the random seed to maintain consistent test execution
    np.random.seed(42)
    
    # Generate continuous candidate vectors representing the parent generation
    parent_a = np.random.uniform(-100, 100, dimension)
    parent_b = np.random.uniform(-100, 100, dimension)
    
    return parent_a, parent_b


@pytest.mark.parametrize("crossover_function", get_crossover_functions())
def test_crossover_operators_validity(crossover_function: Callable, 
                                      synthetic_parents_data: Tuple[np.ndarray, np.ndarray]) -> None:
    """
    Validates the structural and dimensional integrity of crossover operators.

    This test injects the synthetic parent vectors into each discovered crossover 
    function. It asserts that the operation yields exactly two distinct offspring 
    and that the original dimensionality of the problem remains unaltered.

    Args:
        crossover_function (callable): The specific recombination function injected 
                                       by the parametrize decorator.
        synthetic_parents_data (tuple): The standardized parent vectors.
    """
    parent_a, parent_b = synthetic_parents_data
    expected_dimension = len(parent_a)
    
    # Analyze the function signature to handle specific hyperparameter requirements
    signature = inspect.signature(crossover_function)
    
    # Execute the recombination process, adapting to required arguments
    if 'crossover_rate' in signature.parameters:
        # Provide a standard recombination probability for uniform crossover
        test_rate = 0.8
        result = crossover_function(parent_a, parent_b, test_rate)
    else:
        # Standard execution for operators requiring only the parent vectors
        result = crossover_function(parent_a, parent_b)
        
    # Assertion: Verify the function returns exactly two elements (tuple unpacking)
    assert isinstance(result, tuple), "The crossover operator must return a tuple."
    assert len(result) == 2, "The crossover operator must return exactly two offspring."
    
    offspring_a, offspring_b = result
    
    # Assertion: Verify both offspring are strictly numpy arrays for vectorized operations
    assert isinstance(offspring_a, np.ndarray), "First offspring must be a numpy array."
    assert isinstance(offspring_b, np.ndarray), "Second offspring must be a numpy array."
    
    # Assertion: Verify the genetic recombination maintained the problem dimensionality
    assert offspring_a.shape == (expected_dimension,), "First offspring dimension mismatch."
    assert offspring_b.shape == (expected_dimension,), "Second offspring dimension mismatch."
    
    # Assertion: Verify the operator created new objects in memory, avoiding reference bugs
    assert offspring_a is not parent_a, "Offspring A references Parent A memory space."
    assert offspring_b is not parent_b, "Offspring B references Parent B memory space."


# TEST SELECTION FUNCTIONS

def get_selection_functions() -> List[Callable]:
    """
    Dynamically retrieves all functions from the operators module that are 
    intended for selection purposes.

    It filters the module's attributes, identifying callable objects whose 
    names indicate they are selection operators. This approach ensures that 
    new selection mechanisms added in the future are automatically tested 
    without modifying this test suite.

    Returns:
        list: A collection of callable function objects.
    """
    selection_funcs = []
    
    # Iterate over all members of the operators module
    for name, obj in inspect.getmembers(ops):
        # Filter for callables (functions) that include 'selection' in their name
        if inspect.isfunction(obj) and 'selection' in name:
            selection_funcs.append(obj)
            
    return selection_funcs


@pytest.fixture
def synthetic_population_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Pytest fixture providing a standardized synthetic population and corresponding 
    fitness values for testing purposes.

    Creates a small, deterministic dataset representing a population of vectors 
    in a continuous space. This ensures reproducible test conditions across 
    different execution environments.

    Returns:
        tuple: A pair containing the population matrix (numpy.ndarray) and 
               the fitness vector (numpy.ndarray).
    """
    population_size = 10
    dimension = 5
    
    # Seed the random number generator to guarantee deterministic outputs during testing
    np.random.seed(42)
    
    # Generate a matrix of random floats to simulate candidate solutions
    population = np.random.uniform(-10, 10, (population_size, dimension))
    
    # Generate a corresponding array of random fitness values
    fitness_values = np.random.uniform(0, 100, population_size)
    
    return population, fitness_values


@pytest.mark.parametrize("selection_function", get_selection_functions())
def test_selection_operators_validity(selection_function: Callable, 
                                      synthetic_population_data: Tuple[np.ndarray, np.ndarray]) -> None:
    """
    Validates the execution and output integrity of discovered selection functions.

    This test iterates over each selection function found in the module. It executes 
    the function using the synthetic data and asserts that the returned individual 
    belongs to the original population and retains the correct dimensionality.

    Args:
        selection_function (callable): The specific selection function to be tested, 
                                       provided dynamically by the parametrize decorator.
        synthetic_population_data (tuple): The injected deterministic dataset.
    """
    population, fitness_values = synthetic_population_data
    dimension = population.shape[1]
    
    # Retrieve the signature of the function to handle different parameter requirements
    signature = inspect.signature(selection_function)
    
    # Execute the selection function, injecting specific parameters if required
    if 'temperature' in signature.parameters:
        # Boltzmann selection requires a temperature parameter
        test_temperature = 100.0
        selected_individual = selection_function(population, fitness_values, test_temperature)
    elif 'tournament_size' in signature.parameters:
        # Tournament selection accepts a tournament size
        test_tournament_size = 3
        selected_individual = selection_function(population, fitness_values, test_tournament_size)
    else:
        # Standard execution for operators like roulette wheel
        selected_individual = selection_function(population, fitness_values)
        
    # Extract the function name to determine the expected return signature
    operator_name = selection_function.__name__
    
    # Assertion branch: Handle operators specifically designed to return indices
    if 'index' in operator_name:
        
        assert isinstance(selected_individual, int), "Index selection operators must return an integer."
        assert 0 <= selected_individual < len(population), "The returned index is out of array bounds."
        
        # Map the valid index back to the population matrix for dimensional testing
        selected_individual = population[selected_individual]
        
    # Assertion branch: Handle standard operators returning full genotype vectors
    else:
        assert isinstance(selected_individual, np.ndarray), "The selection operator must return a numpy array."
    
    # Assertion: Verify that the resulting candidate matches the problem dimensionality
    assert selected_individual.shape == (dimension,), "The selected individual has an incorrect dimension."
    
    # Assertion: Verify that the candidate genetically exists within the source population
    is_in_population = any(np.array_equal(selected_individual, row) for row in population)
    assert is_in_population, "The selected individual must be a true member of the original population." 



# TEST MUTATION FUNCTIONS


def get_mutation_functions() -> List[Callable]:
    """
    Dynamically extracts all functions related to mutation from the operators module.

    The module namespace is evaluated to isolate callable objects containing 
    the keyword 'mutation' in their identifier. This guarantees that newly 
    integrated mutation strategies are automatically covered by the test suite 
    without requiring manual updates to this file.

    Returns:
        list: A collection of callable mutation function objects.
    """
    mutation_funcs = []
    
    # Iterate through all available attributes in the operators module namespace
    for name, obj in inspect.getmembers(ops):
        # Isolate callable functions that match the mutation naming convention
        if inspect.isfunction(obj) and 'mutation' in name:
            mutation_funcs.append(obj)
            
    return mutation_funcs


@pytest.fixture
def synthetic_individual_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Pytest fixture providing a standardized candidate vector and search space boundaries.

    A deterministic continuous vector and corresponding multidimensional boundaries 
    are generated to ensure reproducibility across test executions.

    Returns:
        tuple: A pair containing the candidate vector (numpy.ndarray) and 
               the search space boundaries (numpy.ndarray).
    """
    dimension = 10
    
    # Initialize the random seed to maintain consistent test execution
    np.random.seed(42)
    
    # Define uniform lower and upper boundaries for all dimensions
    lower_bound = -100.0
    upper_bound = 100.0
    bounds = np.array([[lower_bound, upper_bound] for _ in range(dimension)])
    
    # Generate a candidate solution strictly within the defined continuous boundaries
    individual = np.random.uniform(lower_bound, upper_bound, dimension)
    
    return individual, bounds


@pytest.mark.parametrize("mutation_function", get_mutation_functions())
def test_mutation_operators_validity(mutation_function: Callable, 
                                     synthetic_individual_data: Tuple[np.ndarray, np.ndarray]) -> None:
    """
    Validates the mathematical and structural integrity of mutation operators.

    The test injects a synthetic individual into each discovered mutation function. 
    It verifies that the function executes without structural errors, maintains 
    the original problem dimensionality, and strictly enforces the search space bounds.

    Args:
        mutation_function (callable): The specific mutation function injected 
                                      by the parametrize decorator.
        synthetic_individual_data (tuple): The standardized vector and boundaries.
    """
    individual, bounds = synthetic_individual_data
    expected_dimension = len(individual)
    
    # Analyze the function signature to handle specific hyperparameter requirements
    signature = inspect.signature(mutation_function)
    
    # Define a maximum mutation probability to force execution during the test
    test_probability = 1.0 
    
    # Adapt the function execution based on the dynamic signature analysis
    if 'current_iteration' in signature.parameters:
        # Non-uniform mutation requires generation tracking for its cooling schedule
        test_iteration = 50
        test_max_iterations = 100
        mutated_individual = mutation_function(
            individual, bounds, test_iteration, test_max_iterations
        )
    elif 'sigma' in signature.parameters:
        # Gaussian mutation requires a standard deviation parameter for the noise
        test_sigma = 0.2
        mutated_individual = mutation_function(
            individual, bounds, test_probability, test_sigma
        )
    else:
        # Standard execution for operators like uniform mutation
        mutated_individual = mutation_function(
            individual, bounds, test_probability
        )
        
    # Assertion: Verify the operator returns a strictly numerical array
    assert isinstance(mutated_individual, np.ndarray), "The mutated individual must be a numpy array."
    
    # Assertion: Verify the genetic alteration preserved the problem dimensionality
    assert mutated_individual.shape == (expected_dimension,), "Mutated individual dimension mismatch."
    
    # Assertion: Verify the mutation process respected the global search space boundaries
    # This prevents the objective functions from evaluating out-of-domain coordinates
    for i in range(expected_dimension):
        lower_limit = bounds[i][0]
        upper_limit = bounds[i][1]
        assert mutated_individual[i] >= lower_limit, f"Dimension {i} violated the defined lower bound."
        assert mutated_individual[i] <= upper_limit, f"Dimension {i} violated the defined upper bound."