"""
Shared pytest fixtures for evobench testing.

This module provides:
- Standard benchmark functions and bounds
- Reproducible random number generators
- Mock objective functions for fast testing
- Common optimizer configurations
"""

import pytest
import numpy as np
from numpy.random import Generator, PCG64



# FIXTURES: Standard Benchmark Functions and Bounds


@pytest.fixture
def sphere_bounds():
    """Standard bounds for Sphere function ([-5, 5]^10)."""
    return [(-5, 5)] * 10


@pytest.fixture
def ackley_bounds():
    """Standard bounds for Ackley function ([-32.768, 32.768]^10)."""
    return [(-32.768, 32.768)] * 10


@pytest.fixture
def rosenbrock_bounds():
    """Standard bounds for Rosenbrock function ([-10, 10]^10)."""
    return [(-10, 10)] * 10



# FIXTURES: Reproducible Random Number Generators


@pytest.fixture
def rng_seed_42():
    """NumPy random generator with seed 42 (modern API)."""
    return Generator(PCG64(seed=42))


@pytest.fixture
def global_seed_42():
    """Set global random seed to 42 for reproducibility."""
    np.random.seed(42)
    yield
    # Teardown: restore default state (optional)
    np.random.seed(None)



# FIXTURES: Mock Objective Functions (Fast Evaluation)


@pytest.fixture
def mock_objective_fast():
    """
    Fast mock objective function: sum of squares.
    
    Returns deterministic values for testing, no randomness involved.
    Used for unit tests where speed is critical.
    """
    def objective(x):
        """Mock objective: sphere-like function."""
        return float(np.sum(x**2))
    
    return objective


@pytest.fixture
def mock_objective_with_nans():
    """
    Mock objective that produces NaN for specific inputs.
    
    Used to test robustness against numerical errors.
    """
    def objective(x):
        if np.any(np.isnan(x)):
            return float('nan')
        if np.sum(x**2) > 1e6:  # Very large values → NaN
            return float('nan')
        return float(np.sum(x**2))
    
    return objective


@pytest.fixture
def mock_objective_stochastic():
    """
    Mock objective with random noise.
    
    Used to test algorithm behavior under noisy evaluations.
    """
    def objective(x):
        base = float(np.sum(x**2))
        noise = np.random.normal(0, 0.01 * max(base, 1.0))
        return base + noise
    
    return objective



# FIXTURES: Standard Optimizer Configurations


@pytest.fixture
def pso_config():
    """Standard PSO configuration for testing."""
    return {
        'population_size': 30,
        'max_iterations': 50,
        'inertia_weight': 0.7,
        'cognitive_constant': 1.5,
        'social_constant': 1.5
    }


@pytest.fixture
def eda_config():
    """Standard EDA configuration for testing."""
    return {
        'population_size': 30,
        'max_iterations': 50,
        'selection_ratio': 0.5
    }


@pytest.fixture
def abc_config():
    """Standard ABC configuration for testing."""
    return {
        'population_size': 30,
        'max_iterations': 50,
        'limit': 20
    }



# FIXTURES: Population and Data Matrices


@pytest.fixture
def small_population():
    """Small population matrix for unit tests (10 individuals, 5 dimensions)."""
    return np.random.rand(10, 5)


@pytest.fixture
def medium_population():
    """Medium population matrix for integration tests (50 individuals, 10 dimensions)."""
    return np.random.rand(50, 10)


@pytest.fixture
def fitness_vector_small():
    """Fitness vector for small population (10 values)."""
    return np.random.rand(10)


@pytest.fixture
def fitness_vector_medium():
    """Fitness vector for medium population (50 values)."""
    return np.random.rand(50)



# FIXTURES: Convergence History (for testing analysis)


@pytest.fixture
def convergence_history_perfect():
    """Ideal convergence: monotonic decrease."""
    return [10.0 - i * 0.1 for i in range(100)]


@pytest.fixture
def convergence_history_realistic():
    """Realistic convergence with plateaus and noise."""
    history = []
    value = 10.0
    for i in range(100):
        # Exponential decay with random plateau
        decay = 0.05 if np.random.rand() > 0.3 else 0.0
        noise = np.random.normal(0, 0.05)
        value = max(0.01, value - decay + noise)
        history.append(value)
    return history


@pytest.fixture
def convergence_history_multirun():
    """Multiple convergence histories (5 runs, 100 generations each)."""
    histories = []
    for _ in range(5):
        history = []
        value = 10.0
        for i in range(100):
            decay = 0.05 if np.random.rand() > 0.3 else 0.0
            noise = np.random.normal(0, 0.05)
            value = max(0.01, value - decay + noise)
            history.append(value)
        histories.append(history)
    return np.array(histories)



# FIXTURES: Real Benchmark Functions (for integration tests)


@pytest.fixture
def real_sphere():
    """Real Sphere benchmark function."""
    from evobench import sphere
    return sphere


@pytest.fixture
def real_ackley():
    """Real Ackley benchmark function."""
    from evobench import ackley
    return ackley


@pytest.fixture
def real_rosenbrock():
    """Real Rosenbrock benchmark function."""
    from evobench import rosenbrock
    return rosenbrock



# FIXTURES: Real Algorithm Instances (for integration tests)


@pytest.fixture
def pso_instance(mock_objective_fast, sphere_bounds, pso_config):
    """Instantiated PSO optimizer."""
    from evobench import PSO
    return PSO(mock_objective_fast, sphere_bounds, **pso_config)


@pytest.fixture
def eda_instance(mock_objective_fast, sphere_bounds, eda_config):
    """Instantiated EDA optimizer."""
    from evobench import EDA
    return EDA(mock_objective_fast, sphere_bounds, **eda_config)


@pytest.fixture
def abc_instance(mock_objective_fast, sphere_bounds, abc_config):
    """Instantiated ABC optimizer."""
    from evobench import ABC
    return ABC(mock_objective_fast, sphere_bounds, **abc_config)



# SESSION-LEVEL FIXTURES (Run once per test session)


@pytest.fixture(scope="session")
def session_random_state():
    """Session-level random state snapshot."""
    return np.random.RandomState(42)


@pytest.fixture(scope="session")
def session_constants():
    """Session-level constants for all tests."""
    return {
        'DIMENSION': 10,
        'POPULATION_SIZE': 30,
        'MAX_ITERATIONS': 50,
        'TOLERANCE': 1e-6,
        'SEED': 42
    }
