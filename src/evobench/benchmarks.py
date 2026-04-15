import numpy as np

"""
Evolutionary Benchmarking Functions Module

This module provides the implementation of five classic continuous optimization 
benchmark functions: Ackley, Rosenbrock, Sphere, Schwefel 1.2, and Trid. 
These functions are designed to evaluate the performance, convergence speed, 
and exploration capabilities of population-based metaheuristics.

All functions are strictly vectorized using NumPy to ensure computational 
efficiency when evaluating large populations in multi-dimensional spaces.
"""

def ackley_function(x: np.ndarray) -> float:
    """
    Evaluates the Ackley function for a given continuous vector.

    The Ackley function is characterized by a nearly flat outer region and 
    a large hole at the center. It poses a risk for optimization algorithms 
    to be trapped in one of its many local minima.

    Search space bounds: [-10, 10]
    Global optimum: F(0) = 0

    Args:
        x (np.ndarray): The candidate solution vector representing coordinates.

    Returns:
        float: The evaluated fitness value (objective to minimize).
    """
    # Extract the dimensionality of the search space directly from the vector length
    dimension: int = len(x)
    
    # Calculate the sum of squared elements for the first exponential term
    sum_of_squares: float = float(np.sum(x**2))
    
    # Calculate the sum of cosine evaluations for the second exponential term
    sum_of_cosines: float = float(np.sum(np.cos(2.0 * np.pi * x)))
    
    # Compute the first component of the Ackley mathematical equation
    term_one: float = -20.0 * np.exp(-0.2 * np.sqrt(sum_of_squares / dimension))
    
    # Compute the second component involving the trigonometric summation
    term_two: float = -np.exp(sum_of_cosines / dimension)
    
    # Aggregate all terms alongside the mathematical constants
    final_fitness: float = term_one + term_two + 20.0 + np.exp(1.0)
    
    return final_fitness


def rosenbrock_function(x: np.ndarray) -> float:
    """
    Evaluates the Rosenbrock function (also known as the Valley or Banana function).

    This function is unimodal, but the global minimum lies in a narrow, parabolic 
    valley. Finding the valley is trivial, but converging to the exact minimum 
    is difficult for many algorithms.

    Search space bounds: [-10, 10]
    Global optimum: F(1) = 0

    Args:
        x (np.ndarray): The candidate solution vector representing coordinates.

    Returns:
        float: The evaluated fitness value (objective to minimize).
    """
    # Isolate the current and adjacent coordinate pairs using vector slicing
    current_elements: np.ndarray = x[:-1]
    next_elements: np.ndarray = x[1:]
    
    # Apply the Rosenbrock formula simultaneously across all paired dimensions
    squared_differences: np.ndarray = 100.0 * (next_elements - current_elements**2)**2
    distance_from_optimum: np.ndarray = (1.0 - current_elements)**2
    
    # Sum the evaluated vector elements to obtain the scalar fitness value
    final_fitness: float = float(np.sum(squared_differences + distance_from_optimum))
    
    return final_fitness


def sphere_function(x: np.ndarray) -> float:
    """
    Evaluates the Sphere model function.

    The Sphere function is strictly convex, continuous, and unimodal. It serves 
    as a baseline to measure the convergence speed of an optimization algorithm 
    without the interference of local optima.

    Search space bounds: [-600, 600]
    Global optimum: F(0) = 0

    Args:
        x (np.ndarray): The candidate solution vector representing coordinates.

    Returns:
        float: The evaluated fitness value (objective to minimize).
    """
    # Square every element in the coordinate vector and aggregate them
    final_fitness: float = float(np.sum(x**2))
    
    return final_fitness


def schwefel_1_2_function(x: np.ndarray) -> float:
    """
    Evaluates the Schwefel 1.2 function (also known as the Quadric function).

    This function is continuous, convex, and unimodal. It involves cumulative 
    sums, making it non-separable, which challenges algorithms that optimize 
    dimensions independently.

    Search space bounds: [-40, 60]
    Global optimum: F(0) = 0

    Args:
        x (np.ndarray): The candidate solution vector representing coordinates.

    Returns:
        float: The evaluated fitness value (objective to minimize).
    """
    # Calculate the cumulative sum of the vector elements efficiently
    cumulative_sums: np.ndarray = np.cumsum(x)
    
    # Square the resulting cumulative values and sum them to resolve the nested loop
    final_fitness: float = float(np.sum(cumulative_sums**2))
    
    return final_fitness


def trid_function(x: np.ndarray) -> float:
    """
    Evaluates the Trid function.

    The Trid function has no local minimum except the global one. Its variables 
    are highly interdependent, making it a challenging optimization problem 
    for algorithms lacking strong variable-correlation mechanisms.

    Search space bounds: [-d^2, d^2]
    Global optimum: F(x) = -d(d+4)(d-1)/6

    Args:
        x (np.ndarray): The candidate solution vector representing coordinates.

    Returns:
        float: The evaluated fitness value (objective to minimize).
    """
    # Compute the first mathematical term evaluating the distance from one
    first_term: float = float(np.sum((x - 1.0)**2))
    
    # Slice the coordinate vector to compute the product of adjacent variables
    current_elements: np.ndarray = x[1:]
    previous_elements: np.ndarray = x[:-1]
    
    # Compute the second mathematical term tracking dimension interdependency
    second_term: float = float(np.sum(current_elements * previous_elements))
    
    # Subtract the interdependency term from the primary distance term
    final_fitness: float = first_term - second_term
    
    return final_fitness