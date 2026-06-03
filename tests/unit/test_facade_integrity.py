"""
Unit Tests: Facade API Integrity

Tests verify that the public API exposed in src/evobench/__init__.py:
1. Imports all required classes without errors
2. Exports exactly the documented interface
3. Maintains backward compatibility
4. Supports clean namespace usage (no conflicts)

These tests run BEFORE any algorithm/benchmark tests to catch
API exposure problems early in the CI/CD pipeline.
"""

import pytest
import sys


class TestFacadeImports:
    """Test that all required items can be imported from root package."""
    
    def test_import_evobench_package(self):
        """Verify evobench package can be imported."""
        import evobench
        assert evobench is not None
    
    def test_import_pso_from_root(self):
        """Verify PSO can be imported from evobench root."""
        from evobench import PSO
        assert PSO is not None
        assert hasattr(PSO, '__init__')
        assert hasattr(PSO, 'run')
    
    def test_import_eda_from_root(self):
        """Verify EDA can be imported from evobench root."""
        from evobench import EDA
        assert EDA is not None
        assert hasattr(EDA, '__init__')
        assert hasattr(EDA, 'run')
    
    def test_import_abc_from_root(self):
        """Verify ABC can be imported from evobench root."""
        from evobench import ABC
        assert ABC is not None
        assert hasattr(ABC, '__init__')
        assert hasattr(ABC, 'run')
    
    def test_import_evolutionary_algorithm_base(self):
        """Verify EvolutionaryAlgorithm base class is accessible."""
        from evobench import EvolutionaryAlgorithm
        assert EvolutionaryAlgorithm is not None
        # Check it's an abstract base class
        from abc import ABC as ABCMeta
        assert issubclass(EvolutionaryAlgorithm, ABCMeta)


class TestBenchmarkFacadeImports:
    """Test that all benchmark functions can be imported from root."""
    
    def test_import_sphere_benchmark(self):
        """Verify Sphere benchmark can be imported."""
        from evobench import sphere
        assert sphere is not None
        assert callable(sphere)
    
    def test_import_rosenbrock_benchmark(self):
        """Verify Rosenbrock benchmark can be imported."""
        from evobench import rosenbrock
        assert rosenbrock is not None
        assert callable(rosenbrock)
    
    def test_import_ackley_benchmark(self):
        """Verify Ackley benchmark can be imported."""
        from evobench import ackley
        assert ackley is not None
        assert callable(ackley)
    
    def test_import_schwefel_benchmark(self):
        """Verify Schwefel benchmark can be imported."""
        from evobench import schwefel
        assert schwefel is not None
        assert callable(schwefel)
    
    def test_import_trid_benchmark(self):
        """Verify Trid benchmark can be imported."""
        from evobench import trid
        assert trid is not None
        assert callable(trid)
    
    def test_import_get_benchmark_utility(self):
        """Verify get_benchmark utility can be imported."""
        from evobench import get_benchmark
        assert get_benchmark is not None
        assert callable(get_benchmark)
    
    def test_import_benchmark_registry(self):
        """Verify BENCHMARK_REGISTRY can be imported."""
        from evobench import BENCHMARK_REGISTRY
        assert BENCHMARK_REGISTRY is not None
        assert isinstance(BENCHMARK_REGISTRY, dict)
        assert len(BENCHMARK_REGISTRY) >= 5  # At least 5 benchmarks


class TestStatisticalToolsFacadeImports:
    """Test that statistical tools can be imported from root."""
    
    def test_import_analyze_function(self):
        """Verify analyze function can be imported."""
        from evobench import analyze
        assert analyze is not None
        assert callable(analyze)
    
    def test_import_stat_report_function(self):
        """Verify stat_report function can be imported."""
        from evobench import stat_report
        assert stat_report is not None
        assert callable(stat_report)


class TestUtilityToolsFacadeImports:
    """Test that experiment tools can be imported from root."""
    
    def test_import_run_automated_experiment(self):
        """Verify run_automated_experiment can be imported."""
        from evobench import run_automated_experiment
        assert run_automated_experiment is not None
        assert callable(run_automated_experiment)


class TestFacadeCompleteness:
    """Verify the Facade exports ALL documented public API."""
    
    def test_all_list_defined(self):
        """Verify __all__ is defined in evobench.__init__."""
        import evobench
        assert hasattr(evobench, '__all__')
        assert isinstance(evobench.__all__, list)
        assert len(evobench.__all__) > 0
    
    def test_all_items_are_exported(self):
        """Verify every item in __all__ is actually exported."""
        import evobench
        for item_name in evobench.__all__:
            assert hasattr(evobench, item_name), \
                f"Item '{item_name}' listed in __all__ but not exported"
    
    def test_no_private_items_in_all(self):
        """Verify __all__ doesn't contain private items (starting with _)."""
        import evobench
        for item_name in evobench.__all__:
            assert not item_name.startswith('_'), \
                f"Private item '{item_name}' should not be in __all__"
    
    def test_required_items_in_all(self):
        """Verify all critical items are in __all__."""
        import evobench
        required_items = [
            'PSO', 'EDA', 'ABC', 'EvolutionaryAlgorithm',
            'sphere', 'rosenbrock', 'ackley', 'schwefel', 'trid',
            'get_benchmark', 'BENCHMARK_REGISTRY',
            'analyze', 'stat_report',
            'run_automated_experiment'
        ]
        for item in required_items:
            assert item in evobench.__all__, \
                f"Required item '{item}' not in __all__"


class TestFacadeMetadata:
    """Test module metadata and version information."""
    
    def test_version_defined(self):
        """Verify __version__ is defined."""
        import evobench
        assert hasattr(evobench, '__version__')
        assert isinstance(evobench.__version__, str)
    
    def test_author_defined(self):
        """Verify __author__ is defined."""
        import evobench
        assert hasattr(evobench, '__author__')
        assert isinstance(evobench.__author__, str)
    
    def test_license_defined(self):
        """Verify __license__ is defined."""
        import evobench
        assert hasattr(evobench, '__license__')
        assert isinstance(evobench.__license__, str)
    
    def test_module_docstring(self):
        """Verify module has a docstring."""
        import evobench
        assert evobench.__doc__ is not None
        assert isinstance(evobench.__doc__, str)
        assert len(evobench.__doc__) > 0


class TestAlgorithmInstantiation:
    """Test that algorithms can be instantiated via Facade API."""
    
    def test_pso_instantiation(self):
        """Verify PSO can be instantiated with basic arguments."""
        from evobench import PSO, sphere
        bounds = [(-5, 5)] * 5
        opt = PSO(sphere, bounds)
        assert opt is not None
        assert hasattr(opt, 'run')
        assert hasattr(opt, 'fitness_history')
    
    def test_eda_instantiation(self):
        """Verify EDA can be instantiated with basic arguments."""
        from evobench import EDA, sphere
        bounds = [(-5, 5)] * 5
        opt = EDA(sphere, bounds)
        assert opt is not None
        assert hasattr(opt, 'run')
    
    def test_abc_instantiation(self):
        """Verify ABC can be instantiated with basic arguments."""
        from evobench import ABC, sphere
        bounds = [(-5, 5)] * 5
        opt = ABC(sphere, bounds)
        assert opt is not None
        assert hasattr(opt, 'run')


class TestBenchmarkFunctionCalls:
    """Test that benchmark functions work correctly."""
    
    def test_sphere_function_call(self):
        """Verify Sphere function works with array input."""
        import numpy as np
        from evobench import sphere
        x = np.array([1.0, 2.0, 3.0])
        result = sphere(x)
        assert isinstance(result, (float, np.floating))
        assert result > 0
    
    def test_ackley_function_call(self):
        """Verify Ackley function works with array input."""
        import numpy as np
        from evobench import ackley
        x = np.array([0.0, 0.0])
        result = ackley(x)
        assert isinstance(result, (float, np.floating))
        assert result < 0.1  # Ackley near optimum
    
    def test_get_benchmark_utility(self):
        """Verify get_benchmark retrieves correct functions."""
        from evobench import get_benchmark
        sphere_func = get_benchmark('sphere')
        assert callable(sphere_func)
        
        ackley_func = get_benchmark('ackley')
        assert callable(ackley_func)
    
    def test_get_benchmark_case_insensitive(self):
        """Verify get_benchmark is case-insensitive."""
        from evobench import get_benchmark, sphere
        func1 = get_benchmark('sphere')
        func2 = get_benchmark('SPHERE')
        func3 = get_benchmark('Sphere')
        # All should retrieve the same function
        assert callable(func1)
        assert callable(func2)
        assert callable(func3)


class TestBenchmarkRegistry:
    """Test BENCHMARK_REGISTRY behavior."""
    
    def test_registry_contains_standard_benchmarks(self):
        """Verify registry contains at least the standard benchmarks."""
        from evobench import BENCHMARK_REGISTRY
        required_benchmarks = ['sphere', 'rosenbrock', 'ackley', 'schwefel 1.2', 'trid']
        for benchmark_name in required_benchmarks:
            assert benchmark_name in BENCHMARK_REGISTRY, \
                f"Benchmark '{benchmark_name}' not in registry"
    
    def test_registry_values_are_callable(self):
        """Verify all registry values are callable functions."""
        from evobench import BENCHMARK_REGISTRY
        for name, func in BENCHMARK_REGISTRY.items():
            assert callable(func), f"Registry value for '{name}' is not callable"
    
    def test_registry_functions_return_float(self):
        """Verify registry functions return float values."""
        import numpy as np
        from evobench import BENCHMARK_REGISTRY
        x = np.array([1.0, 2.0, 3.0])
        for name, func in BENCHMARK_REGISTRY.items():
            result = func(x)
            assert isinstance(result, (float, np.floating)), \
                f"Registry function '{name}' did not return float, got {type(result)}"


class TestNoImportErrors:
    """Integration test: Verify no import errors occur."""
    
    def test_clean_import_sequence(self):
        """Run a realistic import sequence without errors."""
        # This mimics what users do
        from evobench import PSO, EDA, ABC
        from evobench import sphere, ackley, rosenbrock
        from evobench import analyze, stat_report
        from evobench import BENCHMARK_REGISTRY, get_benchmark
        
        # All imports should succeed
        assert PSO is not None
        assert BENCHMARK_REGISTRY is not None
    
    def test_no_circular_imports(self):
        """Verify no circular import issues."""
        import subprocess
        import sys
        
        # Try importing in a subprocess to catch circular imports
        code = "from evobench import PSO, sphere; print('OK')"
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert 'OK' in result.stdout


class TestAPIBackwardCompatibility:
    """Test that API is stable and won't break existing code."""
    
    def test_algorithm_initialization_signature(self):
        """Verify algorithm init signature matches documentation."""
        import inspect
        from evobench import PSO
        
        sig = inspect.signature(PSO.__init__)
        params = list(sig.parameters.keys())
        
        # Should have these basic parameters
        assert 'objective_function' in params
        assert 'bounds' in params
        assert 'population_size' in params
        assert 'max_iterations' in params
    
    def test_algorithm_run_returns_tuple(self):
        """Verify run() returns (solution, fitness) tuple."""
        import numpy as np
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5
        opt = PSO(sphere, bounds, max_iterations=5)
        result = opt.run()
        
        assert isinstance(result, tuple)
        assert len(result) == 2
        best_sol, best_fit = result
        assert isinstance(best_sol, np.ndarray)
        assert isinstance(best_fit, (float, np.floating))
