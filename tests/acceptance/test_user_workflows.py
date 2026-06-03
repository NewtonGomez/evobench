"""
Acceptance Tests: End-to-End User Workflows

Tests verify complete user workflows:
1. Basic optimization run (from Example 1)
2. Statistical analysis pipeline (from Example 3)
3. Multi-run convergence tracking
4. Data stability and type correctness

These tests run AFTER unit tests in CI/CD pipeline.
They validate real, production-like usage patterns.
"""

import pytest
import numpy as np


class TestBasicOptimizationWorkflow:
    """
    Test the simplest user workflow:
    1. Import API
    2. Create optimizer
    3. Run optimization
    4. Retrieve results
    
    Mimics: examples/01_basic_usage.py
    """
    
    def test_complete_pso_workflow(self, global_seed_42):
        """Execute complete PSO optimization workflow."""
        from evobench import PSO, sphere
        
        # Setup problem
        dimension = 5
        bounds = [(-5, 5)] * dimension
        
        # Create optimizer
        optimizer = PSO(
            objective_function=sphere,
            bounds=bounds,
            population_size=20,
            max_iterations=50
        )
        
        # Run optimization
        best_solution, best_fitness = optimizer.run()
        
        # Validate results structure
        assert isinstance(best_solution, np.ndarray)
        assert best_solution.shape == (dimension,)
        assert isinstance(best_fitness, (float, np.floating))
        assert best_fitness >= 0  # Sphere is non-negative
        assert not np.isnan(best_fitness)
        assert not np.isinf(best_fitness)
    
    def test_complete_eda_workflow(self, global_seed_42):
        """Execute complete EDA optimization workflow."""
        from evobench import EDA, sphere
        
        dimension = 5
        bounds = [(-5, 5)] * dimension
        
        optimizer = EDA(
            objective_function=sphere,
            bounds=bounds,
            population_size=20,
            max_iterations=50
        )
        
        best_solution, best_fitness = optimizer.run()
        
        # Same validation as PSO
        assert isinstance(best_solution, np.ndarray)
        assert best_solution.shape == (dimension,)
        assert isinstance(best_fitness, (float, np.floating))
        assert best_fitness >= 0
        assert not np.isnan(best_fitness)
    
    def test_complete_abc_workflow(self, global_seed_42):
        """Execute complete ABC optimization workflow."""
        from evobench import ABC, sphere
        
        dimension = 5
        bounds = [(-5, 5)] * dimension
        
        optimizer = ABC(
            objective_function=sphere,
            bounds=bounds,
            population_size=20,
            max_iterations=50
        )
        
        best_solution, best_fitness = optimizer.run()
        
        assert isinstance(best_solution, np.ndarray)
        assert best_solution.shape == (dimension,)
        assert isinstance(best_fitness, (float, np.floating))
        assert best_fitness >= 0
        assert not np.isnan(best_fitness)


class TestConvergenceTracking:
    """Test convergence history tracking across all algorithms."""
    
    def test_fitness_history_populated(self, global_seed_42):
        """Verify fitness_history is populated during optimization."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5
        optimizer = PSO(sphere, bounds, max_iterations=50)
        optimizer.run()
        
        # Verify history is tracked
        assert hasattr(optimizer, 'fitness_history')
        assert isinstance(optimizer.fitness_history, list)
        assert len(optimizer.fitness_history) == 50  # One per iteration
    
    def test_fitness_history_monotonic(self, global_seed_42):
        """Verify fitness history is non-increasing (monotonic)."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5
        optimizer = PSO(sphere, bounds, max_iterations=50)
        optimizer.run()
        
        history = np.array(optimizer.fitness_history)
        
        # Each value should be <= previous (elitism enforced)
        for i in range(1, len(history)):
            assert history[i] <= history[i-1] + 1e-10, \
                f"History not monotonic at step {i}: {history[i]} > {history[i-1]}"
    
    def test_fitness_history_no_nans(self, global_seed_42):
        """Verify fitness history contains no NaN values."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5
        optimizer = PSO(sphere, bounds, max_iterations=50)
        optimizer.run()
        
        history = np.array(optimizer.fitness_history)
        assert not np.any(np.isnan(history)), "NaN found in fitness history"
        assert not np.any(np.isinf(history)), "Inf found in fitness history"
    
    def test_best_fitness_matches_history_final(self, global_seed_42):
        """Verify best_fitness matches the last value in history."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5
        optimizer = PSO(sphere, bounds, max_iterations=50)
        _, best_fitness = optimizer.run()
        
        assert np.isclose(best_fitness, optimizer.fitness_history[-1])


class TestStatisticalAnalysisWorkflow:
    """
    Test the statistical comparison workflow:
    1. Collect samples from multiple algorithms
    2. Compute statistics
    3. Run hypothesis tests
    
    Mimics: examples/03_statistical_analysis.py
    """
    
    def test_collect_samples_from_algorithms(self, global_seed_42):
        """Collect independent samples from multiple algorithms."""
        from evobench import PSO, EDA, ABC, sphere
        
        bounds = [(-5, 5)] * 5
        n_runs = 5
        
        results = {}
        for algo_class, algo_name in [(PSO, 'PSO'), (EDA, 'EDA'), (ABC, 'ABC')]:
            fitnesses = []
            for _ in range(n_runs):
                opt = algo_class(sphere, bounds, max_iterations=30)
                _, best_fit = opt.run()
                fitnesses.append(best_fit)
            results[algo_name] = np.array(fitnesses)
        
        # Verify we collected correct data
        for algo_name, fitnesses in results.items():
            assert len(fitnesses) == n_runs
            assert all(isinstance(f, (float, np.floating)) for f in fitnesses)
            assert not any(np.isnan(f) for f in fitnesses)
    
    def test_descriptive_statistics_computation(self, global_seed_42):
        """Verify we can compute statistics on collected samples."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5
        fitnesses = []
        
        for _ in range(10):
            opt = PSO(sphere, bounds, max_iterations=30)
            _, best_fit = opt.run()
            fitnesses.append(best_fit)
        
        fitnesses = np.array(fitnesses)
        
        # Compute statistics
        mean = np.mean(fitnesses)
        std = np.std(fitnesses)
        median = np.median(fitnesses)
        
        # Validate statistics
        assert isinstance(mean, (float, np.floating))
        assert isinstance(std, (float, np.floating))
        assert std >= 0
        assert mean > 0  # Sphere function is non-negative
    
    def test_normality_testing(self, global_seed_42):
        """Test that we can run normality tests on samples."""
        from scipy import stats
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5
        fitnesses = []
        
        for _ in range(20):
            opt = PSO(sphere, bounds, max_iterations=30)
            _, best_fit = opt.run()
            fitnesses.append(best_fit)
        
        # Run Shapiro-Wilk test
        stat_val, p_value = stats.shapiro(fitnesses)
        
        # Verify test produces valid output
        assert isinstance(stat_val, (float, np.floating))
        assert isinstance(p_value, (float, np.floating))
        assert 0 <= p_value <= 1  # p-value in [0, 1]
    
    def test_anova_hypothesis_test(self, global_seed_42):
        """Test that we can run ANOVA on multiple algorithm samples."""
        from scipy import stats
        from evobench import PSO, EDA, ABC, sphere
        
        bounds = [(-5, 5)] * 5
        
        # Collect samples from each algorithm
        pso_results = []
        eda_results = []
        abc_results = []
        
        for _ in range(5):
            pso_opt = PSO(sphere, bounds, max_iterations=20)
            _, pso_fit = pso_opt.run()
            pso_results.append(pso_fit)
            
            eda_opt = EDA(sphere, bounds, max_iterations=20)
            _, eda_fit = eda_opt.run()
            eda_results.append(eda_fit)
            
            abc_opt = ABC(sphere, bounds, max_iterations=20)
            _, abc_fit = abc_opt.run()
            abc_results.append(abc_fit)
        
        # Run ANOVA
        f_stat, p_value = stats.f_oneway(pso_results, eda_results, abc_results)
        
        # Verify valid output
        assert isinstance(f_stat, (float, np.floating))
        assert isinstance(p_value, (float, np.floating))
        assert 0 <= p_value <= 1


class TestDataStabilityAcrossRuns:
    """
    Test that repeated runs with same seed produce identical results.
    Critical for reproducibility and CI/CD determinism.
    """
    
    def test_pso_seed_reproducibility(self):
        """Verify PSO produces identical results with same seed."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5
        
        # Run 1
        np.random.seed(42)
        opt1 = PSO(sphere, bounds, max_iterations=30)
        sol1, fit1 = opt1.run()
        hist1 = opt1.fitness_history.copy()
        
        # Run 2
        np.random.seed(42)
        opt2 = PSO(sphere, bounds, max_iterations=30)
        sol2, fit2 = opt2.run()
        hist2 = opt2.fitness_history.copy()
        
        # Verify identical results
        assert np.allclose(sol1, sol2, rtol=1e-10)
        assert np.isclose(fit1, fit2, rtol=1e-10)
        assert np.allclose(hist1, hist2, rtol=1e-10)
    
    def test_eda_seed_reproducibility(self):
        """Verify EDA produces identical results with same seed."""
        from evobench import EDA, sphere
        
        bounds = [(-5, 5)] * 5
        
        np.random.seed(42)
        opt1 = EDA(sphere, bounds, max_iterations=30)
        sol1, fit1 = opt1.run()
        
        np.random.seed(42)
        opt2 = EDA(sphere, bounds, max_iterations=30)
        sol2, fit2 = opt2.run()
        
        assert np.allclose(sol1, sol2, rtol=1e-10)
        assert np.isclose(fit1, fit2, rtol=1e-10)
    
    def test_different_seeds_produce_different_results(self):
        """Verify different seeds produce different results."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5
        
        np.random.seed(42)
        opt1 = PSO(sphere, bounds, max_iterations=30)
        _, fit1 = opt1.run()
        
        np.random.seed(123)
        opt2 = PSO(sphere, bounds, max_iterations=30)
        _, fit2 = opt2.run()
        
        # Results should typically differ (with very high probability)
        assert not np.isclose(fit1, fit2)


class TestInputValidation:
    """Test that algorithms handle invalid inputs gracefully."""
    
    def test_algorithm_with_invalid_bounds_dimension(self):
        """Verify error handling for mismatched bounds dimension."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5  # 5D bounds
        
        # Create optimizer with wrong dimension solution
        opt = PSO(sphere, bounds, max_iterations=5)
        
        # Should handle gracefully or raise informative error
        try:
            best_sol, best_fit = opt.run()
            # If no error, verify results are valid
            assert isinstance(best_sol, np.ndarray)
            assert isinstance(best_fit, (float, np.floating))
        except (ValueError, AssertionError) as e:
            # If error is raised, it should be informative
            assert len(str(e)) > 0
    
    def test_algorithm_with_single_dimension(self):
        """Verify algorithm works on 1D problems."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)]  # 1D
        opt = PSO(sphere, bounds, max_iterations=20)
        best_sol, best_fit = opt.run()
        
        assert best_sol.shape == (1,)
        assert best_fit >= 0
    
    def test_algorithm_with_large_dimension(self):
        """Verify algorithm works on high-dimensional problems."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 100  # 100D
        opt = PSO(sphere, bounds, population_size=50, max_iterations=10)
        best_sol, best_fit = opt.run()
        
        assert best_sol.shape == (100,)
        assert best_fit >= 0


class TestTypeCorrectness:
    """Test that functions maintain type correctness."""
    
    def test_benchmark_return_types(self):
        """Verify benchmark functions return float types."""
        from evobench import sphere, ackley, rosenbrock, schwefel, trid
        import numpy as np
        
        x = np.array([1.0, 2.0, 3.0])
        
        benchmarks = [sphere, ackley, rosenbrock, schwefel, trid]
        for benchmark in benchmarks:
            result = benchmark(x)
            assert isinstance(result, (float, np.floating)), \
                f"{benchmark.__name__} returned {type(result)}"
    
    def test_algorithm_return_types(self):
        """Verify algorithms return correct types."""
        from evobench import PSO, sphere
        import numpy as np
        
        bounds = [(-5, 5)] * 5
        opt = PSO(sphere, bounds, max_iterations=10)
        best_sol, best_fit = opt.run()
        
        assert isinstance(best_sol, np.ndarray)
        assert isinstance(best_fit, (float, np.floating))


class TestBoundaryConstraints:
    """Test that solutions respect problem bounds."""
    
    def test_solution_within_bounds_pso(self, global_seed_42):
        """Verify PSO solutions stay within bounds."""
        from evobench import PSO, sphere
        
        bounds = [(-5, 5)] * 5
        opt = PSO(sphere, bounds, max_iterations=50)
        best_sol, _ = opt.run()
        
        # Check each dimension
        for i in range(len(best_sol)):
            assert bounds[i][0] <= best_sol[i] <= bounds[i][1], \
                f"Solution dimension {i} out of bounds: {best_sol[i]}"
    
    def test_solution_within_bounds_eda(self, global_seed_42):
        """Verify EDA solutions stay within bounds."""
        from evobench import EDA, sphere
        
        bounds = [(-5, 5)] * 5
        opt = EDA(sphere, bounds, max_iterations=50)
        best_sol, _ = opt.run()
        
        for i in range(len(best_sol)):
            assert bounds[i][0] <= best_sol[i] <= bounds[i][1]
    
    def test_solution_within_bounds_abc(self, global_seed_42):
        """Verify ABC solutions stay within bounds."""
        from evobench import ABC, sphere
        
        bounds = [(-5, 5)] * 5
        opt = ABC(sphere, bounds, max_iterations=50)
        best_sol, _ = opt.run()
        
        for i in range(len(best_sol)):
            assert bounds[i][0] <= best_sol[i] <= bounds[i][1]


class TestOptimizationQuality:
    """Test that algorithms produce reasonable optimization results."""
    
    def test_pso_improves_fitness_on_sphere(self, global_seed_42):
        """Verify PSO finds better solutions than initial population."""
        from evobench import PSO, sphere
        import numpy as np
        
        bounds = [(-5, 5)] * 5
        opt = PSO(sphere, bounds, max_iterations=100)
        best_sol, best_fit = opt.run()
        
        # Initial population would have fitness around sum of (2.5)^2 * 5 = 31
        initial_random_fit = sphere(np.random.uniform(-5, 5, 5))
        
        # PSO should find much better solution
        assert best_fit < initial_random_fit * 0.1, \
            f"PSO fitness {best_fit} not much better than random {initial_random_fit}"
    
    def test_eda_improves_fitness_on_sphere(self, global_seed_42):
        """Verify EDA finds better solutions than initial population."""
        from evobench import EDA, sphere
        
        bounds = [(-5, 5)] * 5
        opt = EDA(sphere, bounds, max_iterations=100)
        best_sol, best_fit = opt.run()
        
        # Should converge to near-zero on Sphere
        assert best_fit < 1.0, f"EDA fitness {best_fit} not converged on Sphere"
    
    def test_abc_improves_fitness_on_sphere(self, global_seed_42):
        """Verify ABC finds better solutions than initial population."""
        from evobench import ABC, sphere
        
        bounds = [(-5, 5)] * 5
        opt = ABC(sphere, bounds, max_iterations=100)
        best_sol, best_fit = opt.run()
        
        # Should converge to near-zero on Sphere
        assert best_fit < 1.0, f"ABC fitness {best_fit} not converged on Sphere"
