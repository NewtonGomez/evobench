# Changelog

Todos los cambios relevantes de este proyecto serán documentados en este archivo.

El formato está basado en las buenas prácticas de *Keep a Changelog* y en la semántica observada en los mensajes de commit del repositorio.

---

## [2026-04-16]

### Changed
- Se actualizó `BENCHMARKS.md` para definir con mayor claridad las características de las funciones benchmark.  
  **Autor:** NewtonGomez
- Se modificó la vista del análisis estadístico hacia un enfoque más minimalista.  
  **Autor:** NewtonGomez
- Se agregaron dependencias en `pyproject.toml`.  
  **Autor:** NewtonGomez

### Refactored
- Se modularizó la arquitectura del proyecto para mejorar mantenibilidad, escalabilidad y claridad estructural.  
  **Autor:** NewtonGomez
- Se reubicó y dividió `benchmarks.py` en el paquete `benchmarks/`, separando funciones unimodales y multimodales.  
  **Autor:** NewtonGomez
- Se implementó `BENCHMARK_REGISTRY` junto con la utilidad `get_benchmark` para el mapeo dinámico de funciones benchmark.  
  **Autor:** NewtonGomez
- Se modularizó `statistics.py` en el paquete `stats/`, incorporando los módulos `core_tests`, `reporter` y `analyzer`.  
  **Autor:** NewtonGomez
- Se actualizaron los archivos `__init__.py` en algoritmos, benchmarks y estadísticas para exponer una API tipo *Facade* más limpia.  
  **Autor:** NewtonGomez
- Se estandarizaron las convenciones de nombres utilizando alias para algoritmos (`PSO`, `EDA`, `ABC`) y nombres cortos para benchmarks (`sphere`, `ackley`).  
  **Autor:** NewtonGomez
- Se mejoró `stat_report` con significancia resaltada mediante colores ANSI y umbral alfa dinámico.  
  **Autor:** NewtonGomez
- Se mantuvo `base.py` en la raíz del proyecto como contrato global de arquitectura.  
  **Autor:** NewtonGomez
- Se depuraron los *type hints* locales y se reforzó la documentación interna con docstrings y comentarios detallados en inglés.  
  **Autor:** NewtonGomez

---

## [2026-04-15]

### Added
- Se añadió `experiment_engine.py` para automatizar la ejecución de experimentos, serialización JSON y desempaquetado dinámico de datos (`get_evaluated_benchmarks`, `unpack_fitness_results`).  
  **Autor:** NewtonGomez
- Se implementó `roulette_wheel_selection_index()` en el módulo de operadores para devolver enteros escalares en lugar de arreglos de NumPy.  
  **Autor:** NewtonGomez

### Fixed
- Se corrigió la lógica de selección en `bee.py` (Artificial Bee Colony), resolviendo el error de valor ambiguo (`ValueError`) durante la fase de *Onlooker Bee*.  
  **Autor:** NewtonGomez

### Changed
- Se actualizó el runner de experimentos, migrando de `run_experiments.py` a `run_experiments_2.py`, utilizando el nuevo motor de experimentación, configurando las 5 funciones benchmark con sus respectivos límites y reorganizando imports conforme a PEP 8.  
  **Autor:** NewtonGomez
- Se reescribió la lógica de `plotter.py` para evitar superposición de barras entre algoritmos.  
  **Autor:** galvandvictoria-alt
- Se implementó una lógica condicional para la función `trid`.  
  **Autor:** galvandvictoria-alt
- Se mejoraron los comentarios en `run_experiments.py`.  
  **Autor:** NewtonGomez
- Se removió un comentario en el algoritmo ABC para permitir la visualización de histogramas y boxplots.  
  **Autor:** galvandvictoria-alt
- Se realizó una actualización general sin detalle explícito en el mensaje de commit.  
  **Autor:** galvandvictoria-alt
- Se realizó otra actualización general sin detalle explícito en el mensaje de commit.  
  **Autor:** galvandvictoria-alt

### Documentation
- Se añadió la documentación inicial del proyecto en `README.md`, incluyendo visión general, instalación y guía rápida.  
  **Autor:** NewtonGomez
- Se estableció la arquitectura base del directorio `docs/` para futura integración con MkDocs o Sphinx.  
  **Autor:** NewtonGomez
- Se agregó el archivo `LICENSE` con licencia MIT para definir los derechos de uso de código abierto.  
  **Autor:** NewtonGomez

### Merged
- Se integraron cambios desde la rama principal del repositorio remoto.  
  **Autor:** galvandvictoria-alt
- Se integraron cambios adicionales desde la rama principal del repositorio remoto.  
  **Autor:** galvandvictoria-alt

---

## [2026-04-14]

### Added
- Se implementó el algoritmo **Artificial Bee Colony (ABC)** en `bee.py`.  
  **Autor:** NewtonGomez
- Se incorporaron las tres fases principales del algoritmo: *Employed Bees*, *Onlooker Bees* y *Scout Bees*.  
  **Autor:** NewtonGomez
- Se añadió un mecanismo de contador de intentos (*trial counter*) para gestionar abandono y evitar estancamiento en óptimos locales mediante el hiperparámetro `limit`.  
  **Autor:** NewtonGomez
- Se integró selección proporcional al fitness (*roulette wheel*) para coordinar la fase de *Onlooker Bees*.  
  **Autor:** NewtonGomez
- Se garantizó compatibilidad con la clase base `EvolutionaryAlgorithm` y restricciones vectorizadas de frontera.  
  **Autor:** NewtonGomez
- Se mantuvo tipado estático y documentación consistente con el resto del código base.  
  **Autor:** NewtonGomez
- Se implementó `eda.py` con un **Estimation of Distribution Algorithm (EDA)** continuo basado en modelado gaussiano.  
  **Autor:** NewtonGomez
- Se integró selección por torneo para construir el conjunto élite usado en la estimación de media y desviación estándar.  
  **Autor:** NewtonGomez
- Se reforzó la integridad del espacio de búsqueda mediante *boundary clipping* vectorizado.  
  **Autor:** NewtonGomez
- Se añadió `docs/benchmarks.md` con el marco matemático para Sphere, Rosenbrock, Ackley, Schwefel 1.2 y Trid.  
  **Autor:** NewtonGomez
- Se documentaron propiedades clave como separabilidad, multimodalidad y convexidad para evaluación algorítmica.  
  **Autor:** NewtonGomez
- Se aseguró compatibilidad total con la clase base `EvolutionaryAlgorithm` y tipado estático estricto.  
  **Autor:** NewtonGomez

### Changed
- Se removió el prefijo `src` de los imports y se estandarizó la estructura del paquete usando el namespace absoluto `evobench`.  
  **Autor:** NewtonGomez
- Se integró completamente la configuración de `pyproject.toml` para soportar el layout `src`.  
  **Autor:** NewtonGomez
- Se desacopló el código fuente de la estructura física de directorios, facilitando una distribución más profesional.  
  **Autor:** NewtonGomez

### Verified
- Se verificó que todas las pruebas unitarias pasen bajo el nuevo esquema de imports.  
  **Autor:** NewtonGomez

### Tests
- Se implementaron las funciones objetivo y sus pruebas unitarias rigurosas para Ackley, Rosenbrock, Sphere, Schwefel y Trid.  
  **Autor:** NewtonGomez
- Se validó la corrección matemática comprobando mínimos globales teóricos en coordenadas espaciales precisas.  
  **Autor:** NewtonGomez
- Se añadieron pruebas estructurales para robustez ante vectores flotantes multidimensionales arbitrarios.  
  **Autor:** NewtonGomez

### Refactored
- Se añadieron *type hints* conforme a PEP 484.  
  **Autor:** NewtonGomez

---

## [2026-04-13]

### Tests
- Se añadió una suite dinámica de pruebas unitarias para operadores evolutivos de selección, cruce y mutación usando `pytest`.  
  **Autor:** NewtonGomez
- Se integró descubrimiento dinámico de funciones mediante `inspect` para probar nuevos operadores sin modificar el archivo de pruebas.  
  **Autor:** NewtonGomez
- Se agregaron *fixtures* sintéticos determinísticos para población, padres e individuos, garantizando reproducibilidad.  
  **Autor:** NewtonGomez
- Se incorporaron validaciones estrictas sobre tipos de salida (`numpy.ndarray`), integridad dimensional y cumplimiento de límites del espacio de búsqueda continuo.  
  **Autor:** NewtonGomez

### Added
- Se desarrolló la clase abstracta `EvolutionaryAlgorithm` para estandarizar inicialización y seguimiento de estado entre metaheurísticas.  
  **Autor:** NewtonGomez
- Se implementaron operadores de selección en espacio continuo: Tournament, Roulette Wheel y Boltzmann.  
  **Autor:** NewtonGomez
- Se implementaron operadores de cruce para representación real: Arithmetic, Uniform y One-Point.  
  **Autor:** NewtonGomez
- Se implementaron operadores de mutación para codificación real: Gaussian, Uniform y Non-Uniform.  
  **Autor:** NewtonGomez
- Commit inicial del proyecto.  
  **Autor:** NewtonGomez