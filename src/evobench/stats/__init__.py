"""
Statistical Analysis Module for Evolutionary Benchmarking

This module provides the statistical infrastructure to compare the performance
of multiple evolutionary algorithms across benchmark functions.
"""

from .analyzer import analyze
from .reporter import stat_report
from .post_hoc import dunn_test, tukeyHSD_test

# Esto (opcional) le dice a Python qué funciones exportar si alguien usa: from stats import *
__all__ = ["analyze", "stat_report", "dunn_test", "tukeyHSD_test"]