import numpy as np
from evobench.benchmarks import sphere_function, ackley_function
from evobench.algorithms.eda import EstimationOfDistributionAlgorithm as EDA
from evobench.algorithms.pso import ParticleSwarmOptimization as PSO
from evobench.algorithms.bee import ArtificialBeeColony as ABC # Alias seguro
from evobench.tools.statistics import analyze, stat_report 
from evobench.tools.plotter import plot_all



def run_terna_experiment():
    dimension = 10
    bounds = np.array([[-10, 10]] * dimension)

    num_runs = 30   
    
    # Configuración de la terna
    algorithms = [
        {"name": "EDA", "class": EDA, "params": {"selection_ratio": 0.5}},
        {"name": "PSO", "class": PSO, "params": {"inertia_weight": 0.7}},
        {"name": "ABC", "class": ABC, "params": {"limit": 20}}
    ]
    all_results = []
    al_names = [alg["name"] for alg in algorithms]

    for alg_info in algorithms:
        print(f"Running {alg_info['name']}({num_runs} runs)")
        alg_fitness_results = []
        for _ in range(num_runs):
            model = alg_info["class"](
                objective_function=ackley_function,
                bounds=bounds,
                **alg_info["params"]
            )
            best_pos, best_fit = model.run()
            alg_fitness_results.append(best_fit)

        all_results.append(alg_fitness_results)
        print(f"{alg_info['name']} - Best Fitness: {best_fit:.4e} - Best Pob: {best_pos}")
   
#    for _ in range(2):
#        for alg_info in algorithms:
#            # Instanciación dinámica usando la clase base común
#            model = alg_info["class"](
#                objective_function=ackley_function,
#                bounds=bounds,
#                **alg_info["params"]
#            )
#            best_pos, best_fit = model.run()
#            pob.append(best_pos)
#            print(f"{alg_info['name']} - Best Fitness: {best_fit:.4e} - Best Pob: {best_pos}")
            
    # crear experimentos 
    print("STATISTICS:")
    result = analyze("Ackley", all_results, al_names)
    stat_report(result)

    plot_all("Ackley", al_names, all_results)

if __name__ == "__main__":
    run_terna_experiment()