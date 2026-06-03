from evobench.benchmarks import ackley, rosenbrock
from evobench.algorithms import EDA, PSO, ABC
from evobench.stats import analyze, stat_report
from evobench.tools.plotter import plot_all
from evobench.tools import xe

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
                "func": ackley, 
                # Define the continuous search space boundaries for all dimensions
                "bounds": [[-10.0, 10.0]] * dimension
            },

            {
                # Configure the Rosenbrock function evaluation setup
                "name": "Rosenbrock",
                # Pass the callable Rosenbrock objective function
                "func": rosenbrock,
                # Set the valid parameter range constraints across the specified dimensions
                "bounds": [[-10.0, 10.0]] * dimension
            },
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
    xe.run_automated_experiment(experiment_config, output_file=json_path)
    # Parse the JSON file to retrieve a collection of all evaluated benchmark functions
    benchmarks = xe.get_evaluated_benchmarks(json_path)
    # Output the detected benchmarks to the console for monitoring and logging purposes
    print(f"\n\nBenchmarks detected: {benchmarks}\n")
    # Iterate through each identified benchmark function to process and evaluate its respective data
    for bench_func in benchmarks:
        # Extract the dictionary mapping algorithms to their fitness results for the current benchmark
        data = xe.unpack_fitness_results(json_path, bench_func)
        # Extract the names of the evaluated algorithms into a list to serve as data labels
        alg_names = list(data.keys())
        # Directly extract the corresponding fitness result datasets for all algorithms into a flat list
        all_data = list(data.values())
        # Perform comparative statistical analysis on the algorithm datasets for the current benchmark
        result = analyze(bench_func, all_data, alg_names)
        # Output a formatted statistical report summarizing the analysis outcomes
        stat_report(result)
        # Render visual plots comparing algorithm performance for the current benchmark
        #plot_all(bench_func, alg_names, all_data)
        