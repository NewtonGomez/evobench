"""
Optimization Algorithms Module.

This module provides implementations of various evolutionary and swarm-based
metaheuristics. The algorithms are exported with their standard acronyms 
for ease of use.
"""

# Importamos las clases con sus nombres completos y les asignamos el alias oficial
from .eda import EstimationOfDistributionAlgorithm as EDA
from .pso import ParticleSwarmOptimization as PSO
from .bee import ArtificialBeeColony as ABC

# Definimos exactamente qué se expone cuando alguien importa este módulo
__all__ = [
    "EDA", 
    "PSO", 
    "ABC"
]