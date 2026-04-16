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
│   └── evobench/                 # Main package
│       ├── __init__.py
│       ├── base.py               # Abstract base class
│       ├── benchmarks.py          # Test functions
│       ├── algorithms/            # Algorithm implementations
│       │   ├── __init__.py
│       │   ├── eda.py
│       │   ├── pso.py
│       │   └── abc.py
│       └── tools/                 # Utility functions
│           ├── __init__.py
│           ├── operators.py
│           └── experiment_engine.py
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_base.py
│   ├── test_operators.py
│   └── test_benchmarks.py
├── docs/                          # Documentation (to be created)
├── examples/                      # Example scripts
├── pyproject.toml                 # Modern Python packaging
├── setup.py                       # Legacy setup script (optional)
├── setup.cfg                      # Configuration for setup tools
├── MANIFEST.in                    # Include non-Python files
├── README.md                      # Project documentation
├── LICENSE                        # MIT License
├── CONTRIBUTING.md               # Contribution guidelines
├── CHANGELOG.md                  # Version history
└── .gitignore                     # Git ignore patterns
```

---

## Configuration File: pyproject.toml

The modern approach using `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "evobench"
version = "0.1.0"
description = "Standardized benchmarking framework for evolutionary algorithms"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Enrique Gómez", email = "ing.enrique_gomez@outlook.com"},
    {name = "Victoria Galván", email = "galvand.victoria@gmail.com"}
]
keywords = [
    "evolutionary-algorithms",
    "benchmarking",
    "optimization",
    "metaheuristics",
    "research"
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "numpy>=1.19",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "pytest-cov>=2.12",
    "black>=21.0",
    "flake8>=3.9",
    "isort>=5.0",
    "mypy>=0.900",
    "pre-commit>=2.10",
]
docs = [
    "sphinx>=3.0",
    "sphinx_rtd_theme>=1.0",
    "sphinx-autodoc-typehints>=1.0",
]
sci = [
    "scipy>=1.5",
    "scikit-learn>=0.24",
    "pandas>=1.0",
]

[project.urls]
Homepage = "https://github.com/NewtonGomez/evobench"
Documentation = "https://evobench.readthedocs.io"
Repository = "https://github.com/NewtonGomez/evobench"
"Bug Tracker" = "https://github.com/NewtonGomez/evobench/issues"

[tool.setuptools]
packages = ["evobench"]

[tool.setuptools.package-data]
evobench = ["py.typed"]

[tool.black]
line-length = 100
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=evobench --cov-report=term-missing"

[tool.coverage.run]
branch = true
source = ["evobench"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

---

## Configuration File: setup.cfg

For backward compatibility:

```ini
[metadata]
name = evobench
version = 0.1.0
author = Enrique Gómez
author_email = ing.enrique_gomez@outlook.com
description = Standardized benchmarking framework for evolutionary algorithms
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/NewtonGomez/evobench
project_urls =
    Bug Tracker = https://github.com/NewtonGomez/evobench/issues
    Documentation = https://evobench.readthedocs.io
classifiers =
    Development Status :: 4 - Beta
    Intended Audience :: Science/Research
    Topic :: Scientific/Engineering
    License :: OSI Approved :: MIT License
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: 3.10
    Programming Language :: Python :: 3.11
    Programming Language :: Python :: 3.12

[options]
packages = find:
python_requires = >=3.8
install_requires =
    numpy>=1.19

[options.packages.find]
where = src

[options.extras_require]
dev =
    pytest>=6.0
    pytest-cov>=2.12
    black>=21.0
    flake8>=3.9
    isort>=5.0
    mypy>=0.900
    pre-commit>=2.10
docs =
    sphinx>=3.0
    sphinx_rtd_theme>=1.0
    sphinx-autodoc-typehints>=1.0
sci =
    scipy>=1.5
    scikit-learn>=0.24
    pandas>=1.0

[bdist_wheel]
universal = 0
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

After installation, users should be able to:

```python
# Import main algorithm classes
from evobench.algorithms import PSO, EDA, ABC

# Import benchmark functions
from evobench.benchmarks import (
    sphere_function,
    rosenbrock_function,
    ackley_function,
    schwefel_1_2_function,
    trid_function
)

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
