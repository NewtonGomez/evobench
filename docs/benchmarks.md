# Funciones de Prueba Benchmarking para Optimización Continua

Las funciones de prueba (benchmark functions) son fundamentales en la investigación de algoritmos de optimización. Estas funciones poseen características matemáticas conocidas que permiten evaluar de manera rigurosa el desempeño, velocidad de convergencia y capacidades de exploración/explotación de los algoritmos metaheurísticos.

Las cinco funciones implementadas en este módulo representan diferentes clases de problemas de optimización continua:

1. **Funciones unimodales**: Un único óptimo global sin mínimos locales (Sphere, Schwefel 1.2)
2. **Funciones multimodales**: Múltiples óptimos locales que pueden atrapar a los algoritmos (Ackley)
3. **Funciones con valles estrechos**: Óptimo global difícil de alcanzar (Rosenbrock)
4. **Funciones altamente interdependientes**: Variables que no pueden optimizarse de forma independiente (Trid)

### Características Deseables de una Función Benchmark

- **Propiedades matemáticas conocidas**: Óptimo global teórico documentado
- **Separabilidad variada**: Algunas separables, otras completamente acopladas
- **Diferentes grados de multimodalidad**: Desde 0 (unimodal) hasta n (altamente multimodal)
- **Escalabilidad dimensional**: Funciones que pueden evaluarse en diferentes dimensiones
- **Comportamiento diverso**: Rangos de valores, curvatura, pendientes distintas


## Función Sphere (Esfera)

### Descripción Teórica

La función Sphere es la más simple de todas las funciones benchmark. Es estrictamente convexa, continua y unimodal, lo que significa que posee un único óptimo global y ningún mínimo local. Sirve como línea base fundamental para medir la velocidad de convergencia de un algoritmo de optimización sin la interferencia de trampas de mínimos locales.

Desde el punto de vista geométrico, la función representa un paraboloide n-dimensional simétrico alrededor del origen.

### Modelo Matemático

$$F(\mathbf{x}) = \sum_{i=1}^{d} x_i^2$$

Donde:
- $\mathbf{x} = (x_1, x_2, \ldots, x_d)$ es el vector de coordenadas candidato
- $d$ es la dimensionalidad del problema
- Cada componente $x_i$ contribuye de manera completamente independiente (función separable)

### Características

| Propiedad | Valor |
|-----------|-------|
| **Dimensionalidad** | n (escalable) |
| **Espacio de búsqueda** | [-600, 600]^n |
| **Óptimo global** | $\mathbf{x}^* = (0, 0, \ldots, 0)$ |
| **Valor fitness en óptimo** | $F(\mathbf{x}^*) = 0$ |
| **Separabilidad** | Totalmente separable |
| **Multimodalidad** | Unimodal |
| **Convexidad** | Estrictamente convexa |

### Utilidad en Benchmarking

Esta función es útil para:
- Validar que el algoritmo puede converger a un óptimo conocido
- Medir la velocidad de convergencia en problemas simples
- Verificar correctitud de implementación básica
- Servir como caso de prueba fundamental antes de evaluar funciones complejas


## Función Rosenbrock

### Descripción Teórica

La función Rosenbrock es una función desafiante que ha sido ampliamente utilizada en la literatura de optimización. Aunque es unimodal (posee un único óptimo global sin mínimos locales), presenta una característica distintiva: el óptimo global se encuentra dentro de un valle parabólico angosto y curvilíneo.

El desafío computacional radica en que encontrar el valle es trivial para muchos algoritmos, pero converger al mínimo exacto dentro del valle es excepcionalmente difícil. Esta característica la convierte en un excelente indicador de la capacidad de refinamiento o explotación de un algoritmo.

### Modelo Matemático

$$F(\mathbf{x}) = \sum_{i=1}^{d-1} \left[ 100(x_{i+1} - x_i^2)^2 + (1 - x_i)^2 \right]$$

Donde:
- $\mathbf{x} = (x_1, x_2, \ldots, x_d)$ es el vector de coordenadas candidato
- $d$ es la dimensionalidad del problema (típicamente d ≥ 2)
- Cada término utiliza pares consecutivos de variables (no separable)

### Características

| Propiedad | Valor |
|-----------|-------|
| **Dimensionalidad** | n (escalable, mínimo d=2) |
| **Espacio de búsqueda** | [-10, 10]^n |
| **Óptimo global** | $\mathbf{x}^* = (1, 1, \ldots, 1)$ |
| **Valor fitness en óptimo** | $F(\mathbf{x}^*) = 0$ |
| **Separabilidad** | No separable |
| **Multimodalidad** | Unimodal |
| **Convexidad** | No convexa (tiene curvatura variable) |
| **Condicionamiento** | Mal condicionada (alto número de condición) |

### Estructura de la Función

La función consta de dos términos por cada variable (excepto la última):

1. **Término de penalización cuadrática**: $100(x_{i+1} - x_i^2)^2$
   - Penaliza desviaciones de la parábola $x_{i+1} = x_i^2$
   - Este término es mucho más grande que el siguiente (escala 100)

2. **Término de distancia al uno**: $(1 - x_i)^2$
   - Penaliza desviaciones de las coordenadas unitarias
   - Complementa la búsqueda del óptimo global

### Utilidad en Benchmarking

Esta función es útil para:
- Evaluar la capacidad de un algoritmo para navegar valles estrechos
- Medir el equilibrio entre exploración y explotación
- Detectar prematura convergencia a puntos subóptimos
- Evaluar la eficiencia en problemas no convexos


## Función Ackley

### Descripción Teórica

La función Ackley es una función multimodal con numerosos mínimos locales distribuidos uniformemente en el espacio de búsqueda. Sin embargo, la característica más distintiva es que posee una región exterior relativamente plana rodeada por un profundo agujero en el centro donde se encuentra el óptimo global.

Esta estructura imposibilita que un algoritmo localice efectivamente el óptimo global basándose únicamente en información de gradiente local. Representa un desafío típico para algoritmos que pueden quedar atrapados en mínimos locales periféricos.

### Modelo Matemático

$$F(\mathbf{x}) = -20 \exp\left(-0.2\sqrt{\frac{1}{d}\sum_{i=1}^{d} x_i^2}\right) - \exp\left(\frac{1}{d}\sum_{i=1}^{d} \cos(2\pi x_i)\right) + 20 + e$$

Donde:
- $\mathbf{x} = (x_1, x_2, \ldots, x_d)$ es el vector de coordenadas candidato
- $d$ es la dimensionalidad del problema
- $e \approx 2.71828...$ es la constante de Euler
- La función consta de dos componentes exponenciales combinadas

### Componentes de la Función

1. **Primer término exponencial**: $-20 \exp\left(-0.2\sqrt{\frac{1}{d}\sum_{i=1}^{d} x_i^2}\right)$
   - Decae exponencialmente con la distancia desde el origen
   - Crea una región plana en el exterior
   - Magnitud aproximada: -20 en el exterior, 0 en el origen

2. **Segundo término exponencial**: $-\exp\left(\frac{1}{d}\sum_{i=1}^{d} \cos(2\pi x_i)\right)$
   - Crea múltiples mínimos locales periódicos
   - La función coseno genera oscilaciones
   - Magnitud aproximada: -1 en los mínimos locales, 0 en los máximos

3. **Constantes de desplazamiento**: $20 + e$
   - Ajustan la escala de la función
   - Garantizan que el mínimo global sea exactamente 0

### Características

| Propiedad | Valor |
|-----------|-------|
| **Dimensionalidad** | n (escalable) |
| **Espacio de búsqueda** | [-10, 10]^n (típico) |
| **Óptimo global** | $\mathbf{x}^* = (0, 0, \ldots, 0)$ |
| **Valor fitness en óptimo** | $F(\mathbf{x}^*) = 0$ |
| **Separabilidad** | No separable |
| **Multimodalidad** | Altamente multimodal |
| **Número de mínimos locales** | Múltiples (aproximadamente $2^d$ regiones) |

### Utilidad en Benchmarking

Esta función es útil para:
- Evaluar la capacidad de exploración de nuevas regiones
- Detectar atrapamiento en mínimos locales
- Medir la capacidad de escapar de regiones planas
- Evaluar el equilibrio exploración vs. explotación


## Función Schwefel 1.2 (Función Cuádrica)

### Descripción Teórica

La función Schwefel 1.2, también conocida como función cuádrica, es una función continua, convexa y unimodal. Sin embargo, su característica distintiva es que **no es separable**: los elementos no pueden optimizarse de forma independiente, ya que la función incorpora sumas acumulativas que crean acoplamiento entre variables consecutivas.

Esto representa un desafío importante para algoritmos que intenten descomponer el problema en subproblemas más simples.

### Modelo Matemático

$$F(\mathbf{x}) = \sum_{i=1}^{d} \left(\sum_{j=1}^{i} x_j\right)^2$$

Donde:
- $\mathbf{x} = (x_1, x_2, \ldots, x_d)$ es el vector de coordenadas candidato
- $d$ es la dimensionalidad del problema
- La suma acumulativa crea la no-separabilidad

### Expansión Alternativa

La función puede reescribirse como:

$$F(\mathbf{x}) = \sum_{i=1}^{d} i \cdot x_i^2 + 2 \sum_{i=1}^{d} \sum_{j=i+1}^{d} (d-i+1) \cdot x_i \cdot x_j$$

Esta forma muestra explícitamente cómo todas las variables interactúan entre sí ponderadas por factores que dependen de sus índices.

### Características

| Propiedad | Valor |
|-----------|-------|
| **Dimensionalidad** | n (escalable) |
| **Espacio de búsqueda** | [-40, 60]^n |
| **Óptimo global** | $\mathbf{x}^* = (0, 0, \ldots, 0)$ |
| **Valor fitness en óptimo** | $F(\mathbf{x}^*) = 0$ |
| **Separabilidad** | Completamente no separable |
| **Multimodalidad** | Unimodal |
| **Convexidad** | Convexa |
| **Acoplamiento de variables** | Total (todas las variables acopladas) |

### Utilidad en Benchmarking

Esta función es útil para:
- Evaluar algoritmos que mantienen estructura de población/diversidad
- Medir desempeño en problemas altamente acoplados
- Detectar si el algoritmo explota correlaciones entre variables
- Evaluar convergencia en problemas mal condicionados


## Función Trid

### Descripción Teórica

La función Trid es particularmente desafiante porque sus variables están altamente interdependientes. No posee mínimos locales excepto el óptimo global, pero debido a las relaciones complejas entre variables, el espacio de búsqueda presenta topografía difícil de navegar.

Es especialmente diseñada para evaluar la capacidad de algoritmos para detectar y explotar correlaciones entre variables, así como su eficiencia en espacios donde la información de gradiente es engañosa.

### Modelo Matemático

$$F(\mathbf{x}) = \sum_{i=1}^{d} (x_i - 1)^2 - \sum_{i=2}^{d} x_i \cdot x_{i-1}$$

Donde:
- $\mathbf{x} = (x_1, x_2, \ldots, x_d)$ es el vector de coordenadas candidato
- $d$ es la dimensionalidad del problema
- El primer término mide distancia del vector unitario
- El segundo término introduce interdependencia

### Óptimo Global de Trid

El óptimo global no es trivial de calcular analíticamente:

**Coordenadas óptimas:**
$$x_i^* = i(d + 1 - i) \quad \text{para } i = 1, 2, \ldots, d$$

Esta fórmula genera un conjunto de coordenadas geométricamente específico que no es evidente.

**Valor fitness en óptimo:**
$$F(\mathbf{x}^*) = -\frac{d(d+4)(d-1)}{6}$$

### Ejemplos Numéricos

Para diferentes dimensiones:
- d=2: $\mathbf{x}^* = (2, 2)$, $F(\mathbf{x}^*) = -4$
- d=3: $\mathbf{x}^* = (3, 4, 3)$, $F(\mathbf{x}^*) = -12$
- d=10: $\mathbf{x}^* = (10, 18, 24, 28, 30, 30, 28, 24, 18, 10)$, $F(\mathbf{x}^*) = -440$

### Características

| Propiedad | Valor |
|-----------|-------|
| **Dimensionalidad** | n (escalable) |
| **Espacio de búsqueda** | [-d², d²]^n |
| **Óptimo global** | $x_i^* = i(d+1-i)$ |
| **Valor fitness en óptimo** | $F(\mathbf{x}^*) = -\frac{d(d+4)(d-1)}{6}$ |
| **Separabilidad** | No separable |
| **Multimodalidad** | Unimodal (sin mínimos locales) |
| **Interdependencia** | Altamente interdependiente |
| **Previsibilidad de gradientes** | Engañosa (gradientes no guían bien) |

### Utilidad en Benchmarking

Esta función es útil para:
- Evaluar algoritmos que exploten correlaciones de variables
- Detectar prematura convergencia con información limitada
- Medir robustez en espacios topológicamente complejos
- Evaluar aprendizaje de correlaciones durante la búsqueda


## Análisis Comparativo

### Tabla Resumen

| Característica | Sphere | Rosenbrock | Ackley | Schwefel 1.2 | Trid |
|---|---|---|---|---|---|
| **Separabilidad** | Sí | No | No | No | No |
| **Multimodalidad** | Unimodal | Unimodal | Multimodal | Unimodal | Unimodal* |
| **Convexidad** | Sí | No | No | Sí | Sí |
| **Dificultad** | Muy Baja | Media-Alta | Alta | Media | Alta |
| **Acoplamiento** | Nulo | Local | Bajo | Total | Total |

*Unimodal pero con topografía engañosa

### Recomendaciones de Uso

1. **Validación inicial**: Sphere
2. **Refinamiento y explotación**: Rosenbrock
3. **Exploración global**: Ackley
4. **Acoplamiento de variables**: Schwefel 1.2 y Trid
5. **Suite completa**: Todas en secuencia creciente de dificultad


## Referencias Teóricas

- Ackley, D. H. (1987). A connectionist machine for genetic hillclimbing. Kluwer Academic Publishers.
- Rosenbrock, H. H. (1960). An automatic method for finding the greatest or least value of a function. The Computer Journal, 3(3), 175-184.
- Schwefel, H. P. (1981). Numerical Optimization of Computer Models. John Wiley & Sons.
- Trid, F. (1974). Referenced in various optimization literature on benchmark functions.

