from evobench.algorithms.eda import EstimationOfDistributionAlgorithm as EDA
from evobench.algorithms.pso import ParticleSwarmOptimization as PSO
from evobench.algorithms.bee import ArtificialBeeColony as ABC

from evobench.benchmarks import (
    ackley_function, 
    rosenbrock_function, 
    sphere_function, 
    schwefel_1_2_function, 
    trid_function
)

from evobench.tools.experiment_engine import (
    run_automated_experiment, 
    unpack_fitness_results,
    get_evaluated_benchmarks
)

if __name__ == "__main__":
    dimension = 10
    experiment_config = {
    "dimensions": dimension,
    "max_iterations": 100,
    "population_size": 50,
    "independent_runs": 5,
    "benchmarks": [
        {
            "name": "Ackley", 
            "func": ackley_function, 
            "bounds": [[-10.0, 10.0]] * dimension
        },
        {
            "name": "Rosenbrock", 
            "func": rosenbrock_function, 
            "bounds": [[-10.0, 10.0]] * dimension
        },
        {
            "name": "Sphere", 
            "func": sphere_function, 
            "bounds": [[-600.0, 600.0]] * dimension
        },
        {
            "name": "Schwefel 1.2", 
            "func": schwefel_1_2_function, 
            "bounds": [[-40.0, 60.0]] * dimension
        },
        {
            "name": "Trid", 
            "func": trid_function, 
            "bounds": [[-float(dimension**2), float(dimension**2)]] * dimension
        }
    ],
    "algorithms": [
        {"name": "EDA", "class": EDA, "params": {"selection_ratio": 0.5}},
        {"name": "PSO", "class": PSO, "params": {"inertia_weight": 0.7, "social_constant": 1.5}},
        {"name": "BEE", "class": ABC, "params": {"limit": 20}}
    ]
}

    # Call the automation engine
    run_automated_experiment(experiment_config, output_file="test_results_2026.json")
    
    benchmarks = get_evaluated_benchmarks("test_results_2026.json")
    print(f"Benchmarks detected: {benchmarks}\n")
    for bench_func in benchmarks:
        data = unpack_fitness_results("test_results_2026.json", bench_func)
        print(f"{bench_func} data: {data}")