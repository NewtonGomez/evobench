import numpy as np

def ackley_function(x: np.ndarray) -> float:
    """
    Evaluates the Ackley function for a given continuous vector.

    The Ackley function is characterized by a nearly flat outer region and 
    a large hole at the center. It poses a risk for optimization algorithms 
    to be trapped in one of its many local minima.

    Search space bounds: [-10, 10]
    Global optimum: F(0) = 0

    Args:
        x: The candidate solution vector representing coordinates.

    Returns:
        The evaluated fitness value (objective to minimize).
    """
    # Extract the dimensionality of the search space directly from the vector length
    dimension = len(x)
    
    # Calculate the sum of squared elements for the first exponential term
    sum_of_squares = float(np.sum(x**2))
    
    # Calculate the sum of cosine evaluations for the second exponential term
    sum_of_cosines = float(np.sum(np.cos(2.0 * np.pi * x)))
    
    # Compute the first component of the Ackley mathematical equation
    term_one = -20.0 * np.exp(-0.2 * np.sqrt(sum_of_squares / dimension))
    
    # Compute the second component involving the trigonometric summation
    term_two = -np.exp(sum_of_cosines / dimension)
    
    # Aggregate all terms alongside the mathematical constants
    final_fitness = term_one + term_two + 20.0 + np.exp(1.0)
    
    return final_fitness