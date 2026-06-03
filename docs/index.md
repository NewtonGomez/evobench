# evobench: Standardized Benchmarking for Evolutionary Algorithms

**evobench** is a Python library designed for the rigorous benchmarking of evolutionary algorithms and metaheuristics in continuous optimization.

## Key Features
* **Implemented Baselines Algorithms**: PSO (Particle Swarm Optimization), EDA (Estimation of Distribution Algorithm), and ABC (Artificial Bee Colony).
* **Benchmark Functions**: A comprehensive suite including Sphere, Ackley, Rosenbrock, Schwefel 1.2, and Trid.
* **Statistical Analysis**: An automated decision flow that includes normality tests (Shapiro-Wilk) and comparative testing (ANOVA/Kruskal-Wallis).
* **Extensible Architecture**: Built upon the `EvolutionaryAlgorithm` abstract base class to facilitate the seamless creation of new optimizers.

## Documentation Content
* [**Getting Started**](getting-started/SETUP_CONFIG.md): Installation and initial setup guides.
* [**API Reference**](reference/index.md): Detailed documentation for classes, methods, and modules.
* [**Theory & Stats**](theory/index.md): Mathematical foundations and statistical methodology.
* [**Examples Gallery**](EXAMPLES_GALLERY.md): Practical guides and implementation use cases.

## Authors
Developed by **Enrique Gómez Linares** and **Victoria Galván Delgadillo**.

---
*MIT License | [GitHub Repository](https://github.com/NewtonGomez/evobench)*