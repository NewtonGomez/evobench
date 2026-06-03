# Project Setup and Installation Configuration

## Overview

This file documents the setup configuration for evobench. The project uses standard Python packaging tools for distribution.

---

## Package Metadata

- **Project Name**: evobench
- **Description**: Standardized benchmarking framework for evolutionary algorithms
- **Author**: Enrique Gómez and Victoria Galván
- **License**: MIT
- **Python Requirement**: >=3.8
- **Repository**: https://github.com/NewtonGomez/evobench

---

## Installation Methods

### Method 1: Development Installation (Recommended for Contributors)

```bash
# Clone repository
git clone https://github.com/NewtonGomez/evobench.git
cd evobench

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### Method 2: Standard Installation (Users)

```bash
# Once published to PyPI
pip install evobench
```

### Method 3: Installation from Source

```bash
git clone https://github.com/NewtonGomez/evobench.git
cd evobench
pip install .
```

---

## Project Structure for Packaging

```
evobench/
├── src/
│   └── evobench/                     # Main package
│       ├── __init__.py               # Facade: exposes main APIs
│       ├── base.py                   # Abstract base class
│       ├── algorithms/               # Algorithm implementations
│       │   ├── __init__.py           # Facade: PSO, EDA, ABC
│       │   ├── eda.py
│       │   ├── pso.py
│       │   └── bee.py
│       ├── benchmarks/               # Benchmark function modules
│       │   ├── __init__.py           # Facade: sphere, ackley, rosenbrock, schwefel, trid
│       │   ├── unimodal.py           # Unimodal functions
│       │   └── multimodal.py         # Multimodal functions
│       ├── stats/                    # Statistical analysis tools
│       │   ├── __init__.py           # Facade: analyze, stat_report
│       │   ├── core_test.py          # Normality and hypothesis tests
│       │   ├── reporter.py           # Colored ANSI reporting
│       │   └── analyzer.py           # Fitness data analysis
│       └── tools/                    # Utility functions
│           ├── __init__.py
│           ├── operators.py
│           └── experiment_engine.py
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── test_base.py
│   ├── test_operators.py
│   └── test_benchmarks.py
├── docs/                             # Documentation
├── pyproject.toml                    # Modern Python packaging
├── setup.cfg                         # Configuration for setup tools
├── MANIFEST.in                       # Include non-Python files
├── README.md                         # Project documentation
├── LICENSE                           # MIT License
├── CONTRIBUTING.md                  # Contribution guidelines
├── CHANGELOG.md                      # Version history
└── .gitignore                        # Git ignore patterns
```

---

## Configuration File: pyproject.toml

The modern approach using `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "evobench"
version = "0.1.0"
authors = [
  { name = "Enrique Gómez Linares" },
  { name = "Victoria Galván Delgadillo" }
]
description = "A benchmarking suite for evolutionary algorithms and metaheuristics"
readme = "README.md"
requires-python = ">=3.9"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering :: Mathematics",
]
dependencies = [
    "numpy>=1.24.0",
    "scipy>=1.9.0",
    "matplotlib>=3.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]

[tool.setuptools.packages.find]
# Indica que el código fuente real vive dentro de la carpeta 'src'
where = ["src"]

[tool.pytest.ini_options]
# Esta línea es la que permite quitar el prefijo 'src.' de tus imports
# ya que añade 'src' automáticamente al path de búsqueda de Python
pythonpath = ["src"]
testpaths = ["tests"]
```

---

## Configuration File: MANIFEST.in

Include non-Python files in distribution:

```
include README.md
include LICENSE
include CHANGELOG.md
include CONTRIBUTING.md
recursive-include docs *.md
recursive-include examples *.py
recursive-include tests *.py
```

---

## Building and Distribution

### Build the Package

```bash
# Install build tools
pip install build

# Build distribution files
python -m build

# Output:
# dist/evobench-0.1.0-py3-none-any.whl
# dist/evobench-0.1.0.tar.gz
```

### Publish to PyPI (When Ready)

```bash
# Install twine
pip install twine

# Upload to PyPI
twine upload dist/*

# Or test first on TestPyPI
twine upload --repository testpypi dist/*
```

---

## Package Imports

After installation, users can import using the simplified Facade pattern:

```python
# Import main algorithm classes (via Facade)
from evobench.algorithms import PSO, EDA, ABC

# Import benchmark functions (via Facade, with short aliases)
from evobench.benchmarks import (
    sphere,
    rosenbrock,
    ackley,
    schwefel,
    trid
)

# Import statistical analysis tools (via Facade)
from evobench.stats import analyze, stat_report

# Alternative: Import directly from top-level Facade
from evobench import PSO, EDA, ABC, analyze, stat_report

# Import operators
from evobench.tools.operators import (
    tournament_selection,
    roulette_wheel_selection,
    arithmetic_crossover,
    gaussian_mutation
)

# Import base class for custom algorithms
from evobench.base import EvolutionaryAlgorithm
```

---

## Development Setup

### Install with Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest                          # All tests
pytest tests/test_operators.py  # Specific file
pytest -v --cov               # Verbose with coverage
```

### Code Quality Checks

```bash
# Format code
black evobench/ tests/
isort evobench/ tests/

# Lint
flake8 evobench/ tests/

# Type checking
mypy evobench/

# All checks (with pre-commit)
pre-commit run --all-files
```

---

## Version Management

### Semantic Versioning Scheme

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.Y.0): New features, backward compatible
- **PATCH** (0.0.Z): Bug fixes, backward compatible

### Update Version

1. Update `version` in `pyproject.toml`
2. Update `CHANGELOG.md` with release notes
3. Create git tag: `git tag v0.1.0`
4. Push: `git push origin v0.1.0`

---

## Next Steps for Publication

1. **Register Package Name**: Reserve on PyPI
2. **Create GitHub Repository**: Set up remote
3. **Enable CI/CD**: GitHub Actions for automatic testing
4. **Set Up ReadTheDocs**: Automatic documentation builds
5. **Publish Release**: Push to PyPI when v1.0 ready

---

## References

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI - Python Package Index](https://pypi.org/)
- [Semantic Versioning](https://semver.org/)
- [PEP 517 - Build Backend](https://www.python.org/dev/peps/pep-0517/)
- [setuptools Documentation](https://setuptools.pypa.io/)
