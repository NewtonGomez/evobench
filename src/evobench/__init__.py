"""
evobench: Comprehensive Benchmarking Suite for Evolutionary Algorithms

A Python framework for testing, comparing, and analyzing evolutionary algorithms
and metaheuristics. Includes three baseline implementations (PSO, EDA, ABC),
benchmark functions (Sphere, Rosenbrock, Ackley, Schwefel, Trid), and built-in
statistical analysis tools.

Basic Usage:
    >>> from evobench import PSO, sphere
    >>> bounds = [(-5, 5)] * 10
    >>> optimizer = PSO(sphere, bounds, max_iterations=100)
    >>> best_solution, best_fitness = optimizer.run()
    >>> print(f"Best fitness: {best_fitness:.6e}")

For advanced usage, reproducibility, and statistical comparison, see:
    - docs/getting-started/SETUP_CONFIG.md
    - docs/guide/PERFORMANCE_AND_REPRODUCIBILITY.md
    - docs/reference/index.md
"""

__version__ = "0.1.0"
__author__ = "Enrique Gómez Linares, Victoria Galván Delgadillo"
__license__ = "MIT"

# ============================================================================
# ALGORITHM EXPORTS
# ============================================================================
from evobench.algorithms import PSO, EDA, ABC

from evobench.base import EvolutionaryAlgorithm

# ============================================================================
# BENCHMARK FUNCTION EXPORTS
# ============================================================================
from evobench.benchmarks import (
    sphere,
    rosenbrock,
    ackley,
    schwefel,
    trid,
    get_benchmark,
    BENCHMARK_REGISTRY,
)

# ============================================================================
# STATISTICAL ANALYSIS EXPORTS
# ============================================================================
from .stats import analyze, stat_report

# ============================================================================
# UTILITIES EXPORTS
# ============================================================================
from .tools import run as run_automated_experiment

# ============================================================================
# PUBLIC API DEFINITION
# ============================================================================
__all__ = [
    # Core algorithms
    "PSO",
    "EDA",
    "ABC",
    "EvolutionaryAlgorithm",
    # Benchmark functions (individual)
    "sphere",
    "rosenbrock",
    "ackley",
    "schwefel",
    "trid",
    # Benchmark utilities
    "get_benchmark",
    "BENCHMARK_REGISTRY",
    # Statistical analysis
    "analyze",
    "stat_report",
    # Experiment tools
    "run_automated_experiment",

]