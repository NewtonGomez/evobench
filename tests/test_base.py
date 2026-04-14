from typing import Callable, List, Any, Tuple
import pytest
import numpy as np
import inspect

from src.evobench.base import EvolutionaryAlgorithm

# import mccma_evolucion_u2.algorithms.eda 
# import mccma_evolucion_u2.algorithms.pso

"""
Unit testing module for the EvolutionaryAlgorithm abstract base class.

This suite verifies the structural integrity of the base class, ensuring it 
cannot be instantiated directly and that its concrete methods (like population 
initialization) operate mathematically correctly. Furthermore, it dynamically 
validates the contract of any subclass implemented in the package.
"""


# FIXTURES AND MOCK OBJECTS


def dummy_objective_function(x: np.ndarray) -> float:
    """A simple convex function (Sphere) to use as a placeholder during tests."""
    return np.sum(x**2)

class MockMetaheuristic(EvolutionaryAlgorithm):
    """
    A concrete mock implementation of the abstract base class.
    
    This object is strictly used to bypass the ABC instantiation restriction, 
    allowing the test suite to evaluate the base methods (e.g., _initialize_population) 
    in isolation.
    """
    def run(self) -> Tuple[np.ndarray, float]:
        # Dummy implementation strictly to satisfy the abstract method contract
        return self.best_individual, self.best_fitness


@pytest.fixture
def standard_bounds() -> List[List[float]]:
    """Provides a standardized continuous search space for testing boundaries."""
    # A 3-dimensional problem with varying asymmetrical boundaries
    return [[-5.0, 5.0], [-10.0, 20.0], [0.0, 1.0]]



# BASE CLASS VALIDATION


def test_abstract_enforcement(standard_bounds: List[List[float]]) -> None:
    """
    Verifies that the abstract base class strictly prevents direct instantiation.

    It is mathematically and logically invalid to execute an evolutionary process 
    without a defined search strategy (the 'run' method).
    """
    with pytest.raises(TypeError) as exception_info:
        # Attempting to instantiate the base class directly should trigger a TypeError
        EvolutionaryAlgorithm(dummy_objective_function, standard_bounds)
        
    assert "Can't instantiate abstract class" in str(exception_info.value)


def test_population_initialization(standard_bounds: List[List[float]]) -> None:
    """
    Validates the spatial and dimensional correctness of the initial population.

    This test executes the _initialize_population method via the Mock object and 
    asserts that every generated candidate vector strictly respects the defined 
    multidimensional search domain.
    """
    population_size = 30
    dimension = len(standard_bounds)
    
    # Instantiate the Mock object to access the inherited initialization method
    mock_algo = MockMetaheuristic(dummy_objective_function, standard_bounds, population_size)
    initial_population = mock_algo._initialize_population()
    
    # Assertion: Verify the structural shape of the resulting population matrix
    assert isinstance(initial_population, np.ndarray), "Population must be a numpy array."
    assert initial_population.shape == (population_size, dimension), "Incorrect population matrix dimensions."
    
    # Assertion: Verify spatial boundaries for every dimension across all individuals
    for i in range(dimension):
        lower_limit = standard_bounds[i][0]
        upper_limit = standard_bounds[i][1]
        
        column_data = initial_population[:, i]
        assert np.all(column_data >= lower_limit), f"Dimension {i} violated lower bound."
        assert np.all(column_data <= upper_limit), f"Dimension {i} violated upper bound."



# DYNAMIC SUBCLASS CONTRACT TESTING


def get_implemented_algorithms() -> List[type]:
    """
    Dynamically discovers all functional metaheuristics implemented in the package.
    
    Utilizes Python's method resolution order and subclass tracking to find any 
    class that inherits from EvolutionaryAlgorithm (excluding the Mock object).
    """
    subclasses = EvolutionaryAlgorithm.__subclasses__()
    # Filter out the mock class used for isolated testing
    valid_algorithms = [cls for cls in subclasses if cls.__name__ != 'MockMetaheuristic']
    return valid_algorithms


@pytest.mark.parametrize("algorithm_class", get_implemented_algorithms())
def test_algorithm_contract_compliance(algorithm_class: type, standard_bounds: List[List[float]]) -> None:
    """
    Automatically tests newly developed metaheuristics against the architectural contract.

    When a new algorithm (e.g., EDA, PSO) is added to the package, this test will 
    dynamically discover it, instantiate it, and verify that it possesses the mandatory 
    execution signature without causing instantiation errors.
    """
    # Attempt to initialize the dynamically discovered algorithm
    try:
        algo_instance = algorithm_class(
            objective_function=dummy_objective_function, 
            bounds=standard_bounds, 
            population_size=10, 
            max_iterations=5
        )
    except Exception as e:
        pytest.fail(f"Failed to instantiate {algorithm_class.__name__}. Contract violation: {e}")
        
    # Verify that the required 'run' method exists and is callable
    assert hasattr(algo_instance, 'run'), f"{algorithm_class.__name__} is missing the 'run' method."
    assert callable(getattr(algo_instance, 'run')), f"The 'run' attribute in {algorithm_class.__name__} must be a method."