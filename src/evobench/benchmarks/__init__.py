"""
Evolutionary Benchmarking Registry Module

This module acts as a central hub for all optimization test functions. 
It utilizes a registry pattern to map string identifiers directly to 
their corresponding mathematical implementations.
"""

# We use relative imports (with the dot) to tell Python: 
# "Look inside the current folder"
from .unimodal import (
    rosenbrock_function as rosenbrock,
    sphere_function as sphere,
    schwefel_1_2_function as schwefel,
    trid_function as trid
)
from .multimodal import ackley_function as ackley

# Central dictionary mapping string names to function references
# Note: Using lowercase keys is a good practice for robustness
BENCHMARK_REGISTRY = {
    "sphere": sphere,
    "rosenbrock": rosenbrock,
    "ackley": ackley,
    "schwefel 1.2": schwefel,
    "trid": trid
}

def get_benchmark(name: str):
    """
    Retrieves the callable mathematical function based on its registry name.

    Args:
        name: The string identifier of the benchmark function.

    Returns:
        callable: The requested benchmarking function.
    """
    # Normalize the input name to lowercase to match the registry keys
    search_name = name.lower()
    
    if search_name not in BENCHMARK_REGISTRY:
        raise ValueError(f"Benchmark '{name}' is not implemented in the registry.")
        
    return BENCHMARK_REGISTRY[search_name]

# List of publicly available objects when using 'from evobench.benchmarks import *'
# Fixed the typos and ensured names match the aliases defined above
__all__ = [
    "rosenbrock", 
    "sphere", 
    "schwefel", 
    "trid", 
    "ackley", 
    "get_benchmark"
]