from evobench.algorithms.eda import EstimationOfDistributionAlgorithm as EDA
from evobench.algorithms.pso import ParticleSwarmOptimization as PSO
from evobench.algorithms.bee import ArtificialBeeColony as ABC
from evobench.tools.statistics import analyze, stat_report
from evobench.tools.plotter import plot_all

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

from numpy import random

if __name__ == "__main__":
    # Define the dimensionality of the search space for the optimization problems
    dimension = 10
    # Initialize the configuration dictionary for the automated experimental setup
    experiment_config = {
        # Set the number of decision variables for the optimization algorithms
        "dimensions": dimension,
        # Specify the maximum number of iterations (generations) per algorithm run
        "max_iterations": 200,
        # Define the number of candidate solutions (agents) evaluated per generation
        "population_size": 100,
        # Determine the total number of independent executions to ensure statistical robustness
        "independent_runs": 30,
        # Define the list of continuous benchmark functions used to evaluate the algorithms
        "benchmarks": [
            {
                # Identify the benchmark function by its standard academic name
                "name": "Ackley", 
                # Provide the callable function reference for fitness evaluation
                "func": ackley_function, 
                # Define the continuous search space boundaries for all dimensions
                "bounds": [[-10.0, 10.0]] * dimension
            },
            {
                # Configure the Rosenbrock function evaluation setup
                "name": "Rosenbrock",
                # Pass the callable Rosenbrock objective function
                "func": rosenbrock_function,
                # Set the valid parameter range constraints across the specified dimensions
                "bounds": [[-10.0, 10.0]] * dimension
            },
            {
                # Configure the Sphere function evaluation setup
                "name": "Sphere",
                # Pass the callable Sphere objective function
                "func": sphere_function,
                # Define the corresponding expanded search space limits for the Sphere landscape
                "bounds": [[-600.0, 600.0]] * dimension
            },
            {
                # Configure the Schwefel 1.2 function evaluation setup
                "name": "Schwefel 1.2",
                # Pass the callable Schwefel 1.2 objective function
                "func": schwefel_1_2_function,
                # Assign the asymmetric search space boundaries specific to this problem
                "bounds": [[-40.0, 60.0]] * dimension
            },
            {
                # Configure the Trid function evaluation setup
                "name": "Trid",
                # Pass the callable Trid objective function
                "func": trid_function,
                # Dynamically calculate and assign scaled bounds based on the dimensionality squared
                "bounds": [[-float(dimension**2), float(dimension**2)]] * dimension
            }
        ],
        
        # Define the suite of optimization algorithms and their specific hyperparameters
        "algorithms": [
            # Configure the Estimation of Distribution Algorithm (EDA) with a 50% selection pressure
            {"name": "EDA", "class": EDA, "params": {"selection_ratio": 0.5}},
            # Configure Particle Swarm Optimization (PSO) with customized inertia and social coefficients
            {"name": "PSO", "class": PSO, "params": {"inertia_weight": 0.7, "social_constant": 1.5}},
            # Configure Artificial Bee Colony (ABC) algorithm with a defined trial limit for abandonment
            {"name": "BEE", "class": ABC, "params": {"limit": 20}}
        ]
    }

    # Define the target filepath for reading and storing the experiment's JSON results
    json_path = "test_results.json"
    # Initialize the random number generator with a fixed seed to ensure experimental reproducibility
    random.seed(20260415) 
    # Execute the core automation engine and output the generated configuration results to the specified JSON file
    run_automated_experiment(experiment_config, output_file=json_path)
    # Parse the JSON file to retrieve a collection of all evaluated benchmark functions
    benchmarks = get_evaluated_benchmarks(json_path)
    # Output the detected benchmarks to the console for monitoring and logging purposes
    print(f"Benchmarks detected: {benchmarks}\n")
    # Iterate through each identified benchmark function to process and evaluate its respective data
    for bench_func in benchmarks:
        # Extract the dictionary mapping algorithms to their fitness results for the current benchmark
        data = unpack_fitness_results(json_path, bench_func)
        # Extract the names of the evaluated algorithms into a list to serve as data labels
        alg_names = list(data.keys())
        # Directly extract the corresponding fitness result datasets for all algorithms into a flat list
        all_data = list(data.values())
        # Perform comparative statistical analysis on the algorithm datasets for the current benchmark
        result = analyze(bench_func, all_data, alg_names)
        # Output a formatted statistical report summarizing the analysis outcomes
        stat_report(result)
        # Render visual plots comparing algorithm performance for the current benchmark
        plot_all(bench_func, alg_names, all_data)
        