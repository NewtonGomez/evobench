import numpy as np
import pytest
from typing import Callable, List, Tuple

from evobench.benchmarks import (
    ackley_function,
    rosenbrock_function,
    sphere_function,
    schwefel_1_2_function,
    trid_function
)

"""
Unit testing module for Evolutionary Benchmarking Functions.

This test suite rigorously validates the mathematical correctness of the 
objective functions. It evaluates each mathematical model at its known 
theoretical global optimum to guarantee that the vectorized implementations 
do not introduce numerical deviations or indexing errors.
"""

def generate_benchmark_test_cases() -> List[Tuple[Callable[[np.ndarray], float], np.ndarray, float]]:
    """
    Constructs the test cases containing the mathematical functions, their 
    exact optimal coordinate vectors, and the expected theoretical minimum fitness.

    The dimension is fixed to 10 as established by the experimental design. 
    The Trid function requires a specific geometric formula to calculate 
    both its optimal coordinates and its global minimum value.

    Returns:
        List[Tuple[Callable, np.ndarray, float]]: A collection of test cases.
    """
    dimension = 10
    
    # The coordinate vector representing the absolute center of the search space
    origin_vector = np.zeros(dimension)
    
    # The coordinate vector representing the global minimum for Rosenbrock
    ones_vector = np.ones(dimension)
    
    # Calculate the specific optimal coordinates for the Trid function
    # Formula: x_i = i * (d + 1 - i) for i = 1, ..., d
    trid_optimal_coordinates = np.array(
        [i * (dimension + 1 - i) for i in range(1, dimension + 1)], 
        dtype=float
    )
    
    # Calculate the theoretical global minimum value for the Trid function
    # Formula: F(x*) = -d * (d + 4) * (d - 1) / 6
    trid_expected_minimum = -(dimension * (dimension + 4) * (dimension - 1)) / 6.0
    
    test_cases = [
        (sphere_function, origin_vector, 0.0),
        (ackley_function, origin_vector, 0.0),
        (rosenbrock_function, ones_vector, 0.0),
        (schwefel_1_2_function, origin_vector, 0.0),
        (trid_function, trid_optimal_coordinates, trid_expected_minimum)
    ]
    
    return test_cases


@pytest.mark.parametrize("benchmark_function, optimal_vector, expected_minimum", generate_benchmark_test_cases())
def test_global_optimum_evaluation(
    benchmark_function: Callable[[np.ndarray], float], 
    optimal_vector: np.ndarray, 
    expected_minimum: float
) -> None:
    """
    Validates that the objective function evaluates to the correct theoretical 
    minimum when provided with the optimal continuous coordinates.

    Due to the floating-point arithmetic inherent in Python and NumPy operations, 
    an exact equality assertion is avoided. Instead, a strict tolerance is 
    applied to confirm mathematical equivalence.

    Args:
        benchmark_function (Callable): The objective function to evaluate.
        optimal_vector (np.ndarray): The continuous coordinates of the global minimum.
        expected_minimum (float): The theoretical lowest possible fitness value.
    """
    # Execute the mathematical evaluation using the theoretically perfect solution
    calculated_fitness = benchmark_function(optimal_vector)
    
    # Assertion: Verify the return type aligns with the type hints
    assert isinstance(calculated_fitness, float), "The function must return a standard float scalar."
    
    # Assertion: Verify mathematical correctness using a tight precision tolerance
    # pytest.approx handles floating point precision issues naturally
    assert calculated_fitness == pytest.approx(expected_minimum, rel=1e-9, abs=1e-9), \
        f"Mathematical deviation detected. Expected {expected_minimum}, but got {calculated_fitness}."


@pytest.mark.parametrize("benchmark_function, _1, _2", generate_benchmark_test_cases())
def test_random_evaluation_structural_integrity(
    benchmark_function: Callable[[np.ndarray], float], 
    _1: np.ndarray, 
    _2: float
) -> None:
    """
    Ensures that the functions can handle arbitrary continuous vectors without 
    raising unexpected indexing or dimensionality errors.

    Args:
        benchmark_function (Callable): The objective function to evaluate.
        _ (np.ndarray): Ignored optimal vector from the parametrization.
        __ (float): Ignored expected minimum from the parametrization.
    """
    dimension = 10
    
    # Seed the random generator to maintain deterministic test behavior
    np.random.seed(42)
    
    # Generate an arbitrary coordinate vector within a broad domain
    arbitrary_vector = np.random.uniform(-50, 50, dimension)
    
    try:
        # Attempt to evaluate the function using the arbitrary vector
        fitness_result = benchmark_function(arbitrary_vector)
        
        # Assertion: Ensure a valid numerical response was generated
        assert not np.isnan(fitness_result), "The function evaluated to Not-a-Number (NaN)."
        assert not np.isinf(fitness_result), "The function evaluated to infinity."
        
    except Exception as execution_error:
        pytest.fail(f"Execution failed on arbitrary vector evaluation: {execution_error}")