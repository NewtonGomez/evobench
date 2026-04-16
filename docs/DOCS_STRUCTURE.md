# Documentation Architecture for evobench

## Directory Structure (to implement)

```
docs/
├── index.md                          # Documentation homepage (landing page)
├── conf.py                           # Sphinx/MkDocs configuration file
├── mkdocs.yml                        # Alternative: MkDocs configuration
│
├── getting-started/                  # User onboarding and quick introduction
│   ├── index.md                      # Getting Started landing page
│   ├── installation.md               # Installation instructions (pip, from source, requirements)
│   ├── quickstart.md                 # 5-minute quick example
│   └── concepts.md                   # Core concepts (population, fitness, generations, etc.)
│
├── guide/                            # Practical tutorials and how-to guides
│   ├── index.md
│   ├── basic-workflow.md             # Step-by-step: define algorithm → configure → run
│   ├── custom-algorithms.md          # How to implement your own evolutionary algorithm
│   ├── benchmarks-guide.md           # Available benchmark functions and when to use them
│   ├── hyperparameter-tuning.md      # Guide to exploring hyperparameter spaces
│   ├── statistical-analysis.md       # Post-hoc analysis, significance testing, visualization
│   └── reproducibility.md            # Ensuring reproducible experiments
│
├── reference/                        # Complete API documentation (auto-generated from docstrings)
│   ├── index.md
│   ├── api-overview.md               # Quick reference to all modules
│   ├── base.md                       # EvolutionaryAlgorithm abstract base class
│   ├── algorithms/
│   │   ├── index.md                  # Algorithms module overview
│   │   ├── pso.md                    # Particle Swarm Optimization API
│   │   ├── eda.md                    # Estimation of Distribution Algorithm API
│   │   └── abc.md                    # Artificial Bee Colony API
│   ├── benchmarks.md                 # Benchmark functions reference
│   ├── tools/
│   │   ├── experiment-engine.md      # Experiment orchestration API
│   │   ├── operators.md              # Genetic operators API
│   │   └── statistics.md             # Statistical utilities API
│   └── exceptions.md                 # Error types and troubleshooting
│
├── theory/                           # Theoretical background (optional but recommended)
│   ├── index.md
│   ├── evolutionary-algorithms.md    # Brief intro to EA fundamentals
│   ├── benchmark-functions.md        # Mathematical properties of test functions
│   │                                 # (similar to docs/benchmarks.md in the code)
│   ├── statistical-testing.md        # Theory behind ANOVA, Kruskal-Wallis, effect sizes
│   └── convergence-analysis.md       # Analyzing convergence curves and early stopping
│
├── examples/                         # Complete, runnable example scripts
│   ├── index.md
│   ├── comparison-study.md           # Compare 3 algorithms on Sphere
│   ├── parameter-sensitivity.md      # Analyze algorithm behavior across hyperparams
│   ├── statistical-benchmarking.md   # Full workflow with significance testing
│   ├── custom-benchmark.md           # Define and test a custom objective function
│   └── reproducing-paper.md          # Example: reproduce results from published paper
│
├── developer/                        # Contribution and development resources
│   ├── index.md
│   ├── contributing.md               # Code of conduct, PR process, dev setup
│   ├── architecture.md               # Project structure, design patterns, philosophy
│   ├── testing.md                    # How to write and run tests
│   ├── adding-algorithms.md          # Step-by-step: add a new baseline algorithm
│   ├── adding-benchmarks.md          # Step-by-step: add a new test function
│   ├── documentation.md              # How to maintain and update docs
│   └── release-process.md            # Version bumping, changelog, publication
│
├── changelog/                        # Release notes and migration guides
│   ├── index.md
│   ├── v0.1.0.md                     # Initial release notes
│   ├── v0.2.0.md                     # Future: discrete optimization (placeholder)
│   └── migration-guide.md            # Breaking changes between versions
│
├── faq/                              # Frequently asked questions
│   ├── technical-faq.md              # Algorithm selection, tuning, troubleshooting
│   ├── performance-faq.md            # Optimization, parallel execution
│   └── research-faq.md               # Reporting results, citation, publication
│
└── assets/                           # Diagrams, images, css overrides
    ├── architecture.png              # System architecture diagram
    ├── workflow.png                  # Experiment workflow flowchart
    ├── custom-style.css              # Custom Sphinx/MkDocs styling
    └── logo.svg                      # Project logo (if applicable)
```

---

## File Descriptions

### **getting-started/** — Onboarding and Core Concepts
- **impact**: New users first read this section
- **index.md**: Overview of documentation structure; where to start
- **installation.md**: Multiple installation methods, system requirements, troubleshooting
- **quickstart.md**: 5-10 minute example producing working output
- **concepts.md**: Terminology (population, generation, fitness landscape, convergence)

### **guide/** — Practical How-To Instructions
- **impact**: Users learning by doing
- **basic-workflow.md**: End-to-end workflow: define problem → select algorithm → configure → run → analyze
- **custom-algorithms.md**: Complete template and best practices for inheriting `EvolutionaryAlgorithm`
- **benchmarks-guide.md**: When to use Sphere vs. Ackley vs. Rosenbrock; difficulty levels
- **hyperparameter-tuning.md**: Systematic approaches to hyperparameter exploration
- **statistical-analysis.md**: Post-experiment analysis, significance testing, visualization techniques
- **reproducibility.md**: Seeding, version pinning, results validation

### **reference/** — Complete API Documentation
- **impact**: Developers need precise behavior documentation
- **api-overview.md**: One-page overview of all public functions and classes
- **base.md**: Contract for implementing algorithms; abstract methods and properties
- **algorithms/**: Detailed docstrings for PSO, EDA, ABC (auto-generated from source)
- **benchmarks.md**: Signature, mathematical formula, optimal value, domain for each test function
- **tools/**: Full API for experiment_engine, operators, statistics modules

### **theory/** — Scientific Background
- **impact**: Researchers and PhD students needing theoretical grounding
- **evolutionary-algorithms.md**: EA taxonomy, selection pressure, exploration vs. exploitation
- **benchmark-functions.md**: Mathematical properties, separability, multimodality, hard searchability
- **statistical-testing.md**: Why ANOVA/Kruskal-Wallis, assumptions, interpretation
- **convergence-analysis.md**: Reading convergence plots, detecting stagnation, early stopping criteria

### **examples/** — Runnable Code Samples
- **impact**: Learners by example; copy-paste starting point
- **comparison-study.md**: PSO vs. ABC vs. EDA on Sphere (10D, 20 runs)
- **parameter-sensitivity.md**: Systematic grid search over PSO inertia weights
- **statistical-benchmarking.md**: Complete pipeline: run → analyze → report
- **custom-benchmark.md**: Define objective function with custom bounds
- **reproducing-paper.md**: "How I reproduced Figure 3 from [Citation]"

### **developer/** — Contributor Resources
- **impact**: Community contributors and maintainers
- **contributing.md**: Code of conduct, fork/PR workflow, coding standards (PEP 8)
- **architecture.md**: Design principles, folder structure, naming conventions
- **testing.md**: pytest setup, fixture examples, coverage targets
- **adding-algorithms.md**: Template for new baseline algorithm (with tests)
- **adding-benchmarks.md**: Template for new test function (with validation)
- **documentation.md**: Docstring format (Google/NumPy style), Sphinx directives
- **release-process.md**: Versioning scheme (semver), changelog format, PyPI publication

### **changelog/** — Version History
- **impact**: Users deciding whether to upgrade
- **v0.1.0.md**: Initial release; features, known issues, thanks
- **v0.2.0.md** (template): Planned discrete optimization support
- **migration-guide.md**: Breaking changes and upgrade instructions between major versions

### **faq/** — Common Questions
- **impact**: Reduces duplicate GitHub issues
- **technical-faq.md**: "Which algorithm should I choose?", "Why is my algorithm slow?", "How do I handle NaN?"
- **performance-faq.md**: "Can I parallelize?", "Memory requirements?", "Max dimensions?"
- **research-faq.md**: "How do I cite evobench?", "Can I publish results?", "What about my proprietary algorithm?"

### **assets/** — Visual and Styling Resources
- **architecture.png**: UML or dependency diagram
- **workflow.png**: Flowchart showing experiment flow
- **custom-style.css**: Brand colors, fonts, responsive design tweaks

---

## Recommended Build System

### Option 1: **Sphinx** (for academic/scientific projects)
```yaml
# conf.py configuration
project = 'evobench'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx_rtd_theme']
html_theme = 'sphinx_rtd_theme'  # Read the Docs theme
```

**Advantages**: Auto-generated API docs, mature ecosystem, integrates with ReadTheDocs

---

### Option 2: **MkDocs** (for modern, faster documentation)
```yaml
# mkdocs.yml configuration
site_name: evobench
theme:
  name: material
  palette:
    primary: blue
    accent: orange
plugins:
  - search
  - mermaid2
nav:
  - Home: index.md
  - Getting Started: getting-started/index.md
  - Guide: guide/index.md
  - API Reference: reference/index.md
  - Examples: examples/index.md
  - Developer: developer/index.md
```

**Advantages**: Simpler Markdown, Material theme is visually modern, fast build times

---

## Content Ownership & Update Frequency

| Section | Owner | Update Frequency | Automation |
|---------|-------|------------------|-----------|
| getting-started/ | Core team | Per minor release | Manual |
| guide/ | Core + Contributors | As needed | Manual |
| reference/ API docs | Automated | Per commit | Sphinx `autodoc` |
| theory/ | Core team | Per major release | Manual |
| examples/ | Community | Per request | Manual review |
| developer/ | Core team | Per major release | Manual |
| changelog/ | Release manager | Per version | Manual |
| faq/ | Community | Continuous | GitHub issues → FAQ |

---

## Testing & Validation of Documentation

1. **Docstring tests**: `pytest --doctest-modules` on all `.py` files
2. **Code examples**: Run all examples in `examples/` directory as part of CI/CD
3. **Link checking**: Use `sphinx-linkcheck` or `markdown-link-check`
4. **Build validation**: Ensure Sphinx/MkDocs builds without warnings
5. **Spell checking**: Use `pyspelling` or similar tools

---

## Migration Path (Existing → Documented)

Once implemented, integrate the theory and examples already present in your codebase:

1. Move `docs/benchmarks.md` → `docs/theory/benchmark-functions.md`
2. Convert notebook examples → `docs/examples/*.md`
3. Docstrings in source code (base.py, algorithms/) → `docs/reference/` (auto-generated)
4. README.md sections → `docs/getting-started/` and consolidate

---

**Notes**:
- This structure scales from 5KB to 500KB of documentation
- All links are relative (supports offline building)
- Supports versioning (multiple language translations in future)
- Can be deployed to GitHub Pages, ReadTheDocs, or any static host
