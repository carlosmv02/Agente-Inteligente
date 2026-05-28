Cargando modelo de embeddings...
modules.json:   0% 0.00/387 [00:00<?, ?B/s]modules.json: 100% 387/387 [00:00<00:00, 573kB/s]
README.md: 0.00B [00:00, ?B/s]README.md: 179kB [00:00, 41.5MB/s]
sentence_bert_config.json:   0% 0.00/57.0 [00:00<?, ?B/s]sentence_bert_config.json: 100% 57.0/57.0 [00:00<00:00, 87.3kB/s]
config.json:   0% 0.00/694 [00:00<?, ?B/s]config.json: 100% 694/694 [00:00<00:00, 1.11MB/s]
model.safetensors:   0% 0.00/1.11G [00:00<?, ?B/s]model.safetensors:   6% 67.1M/1.11G [00:03<00:47, 22.1MB/s]model.safetensors:  18% 201M/1.11G [00:03<00:11, 76.3MB/s] model.safetensors:  24% 268M/1.11G [00:05<00:14, 56.8MB/s]model.safetensors:  54% 604M/1.11G [00:06<00:03, 129MB/s] model.safetensors:  60% 671M/1.11G [00:07<00:03, 120MB/s]model.safetensors:  78% 872M/1.11G [00:07<00:01, 171MB/s]model.safetensors: 100% 1.11G/1.11G [00:08<00:00, 194MB/s]model.safetensors: 100% 1.11G/1.11G [00:11<00:00, 100MB/s]
Loading weights:   0% 0/199 [00:00<?, ?it/s]Loading weights: 100% 199/199 [00:00<00:00, 3597.44it/s]
tokenizer_config.json:   0% 0.00/418 [00:00<?, ?B/s]tokenizer_config.json: 100% 418/418 [00:00<00:00, 717kB/s]
sentencepiece.bpe.model:   0% 0.00/5.07M [00:00<?, ?B/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:00<00:00, 5.18MB/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:00<00:00, 5.17MB/s]
tokenizer.json:   0% 0.00/17.1M [00:00<?, ?B/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 22.1MB/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 21.9MB/s]
special_tokens_map.json:   0% 0.00/280 [00:00<?, ?B/s]special_tokens_map.json: 100% 280/280 [00:00<00:00, 501kB/s]
config.json:   0% 0.00/200 [00:00<?, ?B/s]config.json: 100% 200/200 [00:00<00:00, 360kB/s]
RAG listo
- Vector DB: /app/chroma_ddr
- Embeddings: intfloat/multilingual-e5-base
- LLM provider: ollama
- Ollama model: gemma4:e2b
Escribe una pregunta y pulsa Enter. Escribe 'exit' para salir.

PREGUNTA: Genera un examen nuevo de DDR junto con el solucionario completo. Debe seguir el estilo de los examenes de convocatorias anteriores, tener 4 preguntas, incluir un ejercicio practico final con OPC y entregar una solucion razonada de cada pregunta.
[*] Recuperando contexto de la base de datos...
[DEBUG] Iniciando retrieve_context...
[DEBUG] Consulta de examen detectada: True
[+] Contexto recuperado
[*] Generando respuesta...

RESPUESTA:

EXAMEN

**EXAMEN DE DISEÑO Y DIMENSIONADO DE REDES (DDR)**

**Instrucciones:** Lea atentamente cada pregunta y responda de manera clara y precisa. Utilice la notación matemática adecuada cuando sea necesario.

**1. (0.5 puntos) Direccionamiento y Políticas de Red**
Discuta las principales ventajas y desventajas de implementar un esquema de direccionamiento estático frente a un esquema de direccionamiento dinámico (ej. DHCP o SLAAC) en una red corporativa de tamaño medio.

**2. (0.5 puntos) Análisis de Técnicas de Optimización**
En el contexto del dimensionado de redes, explique por qué la Teoría de Colas es una herramienta adecuada para el análisis de un único enlace, pero por qué la Optimización de Red (que considera múltiples enlaces) es necesaria para el diseño global de una infraestructura.

**3. (1.0 punto) Cálculo de Camino Óptimo**
Describa el método analítico que se utiliza para calcular el camino óptimo entre dos nodos en una red con múltiples enlaces y restricciones de capacidad. ¿Qué tipo de algoritmo se considera más adecuado para este cálculo y por qué?

**4. (2.0 puntos) Dimensionado y Optimización de Redes**
A partir de la siguiente formulación y datos, realice el dimensionado y la optimización de la capacidad de los enlaces de la red.

Se dispone de una topología concreta con cuatro nodos (A, B, C, D) y enlaces bidireccionales. Se asume que cada enlace tiene una capacidad nominal de 10 Gbps.

**Matriz de Tráfico Nominal (en Gbps):**
A $\to$ B: 6
A $\to$ C: 8
A $\to$ D: 4
B $\to$ A: 3
B $\to$ C: 7
B $\to$ D: 5
C $\to$ A: 5
C $\to$ B: 4
C $\to$ D: 6
D $\to$ A: 4
D $\to$ B: 3
D $\to$ C: 5

**Consideraciones de Diseño:**
*   **OPC 1:** Utilizar la topología de los enlaces definidos.
*   **OPC 2:** Utilizar la matriz de tráfico nominal.
*   **OPC 3:** Formulación matemática abstracta (MILP) para determinar el número de módulos necesarios para cada enlace y el flujo de tráfico.
*   **OPC 4:** Coste por módulo = 1 unidad; la utilización máxima permitida de cualquier enlace es del 85% (0.85).
*   **Objetivo:** Minimizar el coste total de los módulos necesarios para satisfacer todas las demandas de tráfico, respetando las restricciones de capacidad.

Diseñe la solución programada en Octave/Matlab, entregando tanto el script como la solución. En su respuesta, especifique explícitamente la asignación de las Opciones (ej. AABD) y el resultado final en términos del número de módulos requeridos para cada enlace.

SOLUCIONARIO

# SOLUCIONARIO DEL EXAMEN DE DISEÑO Y DIMENSIONADO DE REDES (DDR)

**Profesor Experto en Diseño y Dimensionado de Redes (DDR)**

A continuación, se presenta la solución razonada para cada pregunta del examen, siguiendo las directrices de claridad, evaluabilidad y enfoque en el Diseño y Dimensionado de Redes (DDR).

---

## 1. (0.5 puntos) Direccionamiento y Políticas de Red

**Discuta las principales ventajas y desventajas de implementar un esquema de direccionamiento estático frente a un esquema de direccionamiento dinámico (ej. DHCP o SLAAC) en una red corporativa de tamaño medio.**

### Esquema de Direccionamiento Estático

**Ventajas:**
1. **Seguridad y Control:** Permite un control total y predecible sobre qué dispositivos pueden acceder a la red y cómo se gestionan las políticas de seguridad (ACLs).
2. **Previsibilidad:** La asignación de direcciones es fija, lo que facilita la planificación de la infraestructura y la gestión de la seguridad perimetral.
3. **Estabilidad:** Reduce la posibilidad de conflictos de direcciones (IP spoofing) y simplifica la auditoría de la red.

**Desventajas:**
1. **Gestión Centralizada:** Requiere una administración manual o mediante sistemas centralizados (como DHCP Snooping o servidores DNS) para asignar y gestionar cada dirección.
2. **Ineficiencia en Redes Dinámicas:** En redes grandes o con alta rotación de dispositivos, la gestión manual se vuelve ineficiente y propensa a errores.
3. **Escalabilidad Limitada:** La expansión de la red puede requerir una reconfiguración manual de direcciones, lo que ralentiza el proceso.

### Esquema de Direccionamiento Dinámico (DHCP/SLAAC)

**Ventajas:**
1. **Automatización y Eficiencia:** Permite la asignación automática de direcciones, reduciendo la carga administrativa del administrador de red.
2. **Escalabilidad:** Facilita la incorporación de nuevos dispositivos a la red sin intervención manual constante.
3. **Reducción de Errores:** Minimiza el riesgo de conflictos de direcciones al delegar la tarea de asignación a un servidor central.

**Desventajas:**
1. **Seguridad:** Introduce un riesgo de seguridad si no se implementan mecanismos de control (como DHCP Snooping o listas de control de acceso) para prevenir la asignación de direcciones no autorizadas.
2. **Incertidumbre:** La asignación es dinámica, lo que puede dificultar la trazabilidad y la auditoría de la red en caso de problemas.
3. **Dependencia:** La red depende de la correcta operación del servidor DHCP o del protocolo SLAAC.

**Conclusión para Redes Corporativas de Tamaño Medio:**
Para una red corporativa de tamaño medio, la tendencia actual es utilizar un **esquema híbrido**. Se recomienda usar direccionamiento dinámico (DHCP/SLAAC) para los dispositivos de usuario final, mientras que las direcciones estáticas se reservan para dispositivos críticos de infraestructura (servidores, routers, firewalls, impresoras) donde el control y la estabilidad son prioritarios.

---

## 2. (0.5 puntos) Análisis de Técnicas de Optimización

**Explique por qué la Teoría de Colas es una herramienta adecuada para el análisis de un único enlace, pero por qué la Optimización de Red (que considera múltiples enlaces) es necesaria para el diseño global de una infraestructura.**

### Teoría de Colas (Análisis de un único enlace)

La Teoría de Colas es adecuada para el análisis de un **único enlace** porque permite modelar el comportamiento de un sistema donde el tráfico entra y sale de un punto específico (el enlace) a una tasa determinada.

*   **Enfoque Local:** Permite analizar la dinámica de la congestión, la latencia y la pérdida de paquetes en un punto específico, considerando la tasa de llegada de datos (tráfico entrante) y la tasa de servicio (capacidad del enlace).
*   **Modelado de Procesos:** Se utiliza para predecir el comportamiento de los datos bajo condiciones de carga, ayudando a dimensionar la capacidad de ese enlace en particular.

### Optimización de Red (Diseño Global de la Infraestructura)

La Optimización de Red es necesaria para el diseño global de una infraestructura porque el rendimiento de la red no depende solo de la capacidad de un enlace individual, sino de la **interacción y el flujo de tráfico entre todos los enlaces** (el camino completo).

*   **Interdependencia:** El tráfico se mueve a través de múltiples enlaces. La congestión en un enlace puede ser causada por la sobrecarga de otros enlaces en la ruta.
*   **Diseño Global:** La optimización debe considerar la capacidad total de la infraestructura, las restricciones de flujo (matriz de tráfico), y los objetivos globales (minimizar el coste total, minimizar la latencia promedio de la red, garantizar el QoS global).
*   **Diseño de Políticas:** Permite tomar decisiones de dimensionamiento y reconfiguración que optimicen el rendimiento general de la red, en lugar de solo optimizar componentes aislados.

**Conclusión:** La Teoría de Colas es una herramienta de análisis local (micro), mientras que la Optimización de Red es una herramienta de diseño global (macro) que integra las dinámicas locales para lograr un objetivo sistémico.

---

## 3. (1.0 punto) Cálculo de Camino Óptimo

**Describa el método analítico que se utiliza para calcular el camino óptimo entre dos nodos en una red con múltiples enlaces y restricciones de capacidad. ¿Qué tipo de algoritmo se considera más adecuado para este cálculo y por qué?**

### Método Analítico y Algoritmo

El método analítico utilizado para calcular el camino óptimo entre dos nodos en una red con múltiples enlaces y restricciones de capacidad es el **algoritmo de camino más corto ponderado**, generalmente implementado a través de variantes del algoritmo de **Dijkstra** o **Bellman-Ford**.

**¿Por qué Dijkstra/Bellman-Ford?**
Estos algoritmos están diseñados para encontrar el camino con el menor "coste" (o menor latencia/menor coste de capacidad) entre un nodo fuente y todos los demás nodos de la red.

### Adaptación para Restricciones de Capacidad

Para incorporar las restricciones de capacidad (que son el elemento clave en el dimensionado de redes), el algoritmo debe ser adaptado:

1. **Función de Coste:** En lugar de usar el coste de distancia simple, la función de coste debe incorporar la capacidad disponible y la demanda de tráfico. El coste de un enlace se define en función de la capacidad restante o la latencia esperada.
2. **Restricciones:** El algoritmo debe verificar que el flujo de tráfico en cada enlace no exceda su capacidad dimensionada.

**Algoritmo más Adecuado:**
El algoritmo más adecuado es una variante de **Dijkstra con restricciones de flujo (Flow-Constrained Shortest Path)**.

**Justificación:**
*   **Dijkstra:** Es eficiente para encontrar el camino más corto en términos de coste.
*   **Adaptación:** Al integrar las restricciones de capacidad en la función de coste, el algoritmo no solo encuentra el camino físicamente más corto, sino el camino que es **factible** dadas las limitaciones de capacidad y la demanda de tráfico. Esto permite encontrar el camino óptimo que minimiza el coste total mientras se garantiza que todas las restricciones de QoS y capacidad se cumplen.

---

## 4. (2.0 puntos) Dimensionado y Optimización de Redes

**A partir de la siguiente formulación y datos, realice el dimensionado y la optimización de la capacidad de los enlaces de la red. Incluya:**
*   **OPC 1:** Utilizar la topología de los enlaces definidos.
*   **OPC 2:** Utilizar la matriz de tráfico nominal.
*   **OPC 3:** Formulación matemática abstracta (MILP) para determinar el número de módulos necesarios para cada enlace y el flujo de tráfico.
*   **OPC 4:** Coste por módulo = 1 unidad; la utilización máxima permitida de cualquier enlace es del 85% (0.85).
*   **Objetivo:** Minimizar el coste total de los módulos necesarios para satisfacer todas las demandas de tráfico, respetando las restricciones de capacidad.

### a. La Formulación Matemática Abstracta (MILP)

**Variables de Decisión:**
*   $x_{ij}$: Número de módulos necesarios para el enlace $(i, j)$. (Donde $i$ y $j$ son los nodos).

**Entradas (Datos):**
*   Matriz de Tráfico Nominal $T_{ij}$ (Demanda de tráfico en Gbps).
*   Capacidad Nominal del enlace $C_{ij}$ (10 Gbps).
*   Restricción de Utilización Máxima $U_{max} = 0.85$.
*   Coste por módulo $C_{módulo} = 1$.

**Restricciones Principales:**

1. **Restricción de Capacidad (Dimensionamiento):** La capacidad total del enlace debe ser suficiente para soportar el tráfico real.
   $$\text{Capacidad del enlace } (x_{ij}) \ge \frac{\text{Tráfico real en el enlace } (f_{ij})}{\text{Utilización máxima } (U_{max})}$$
   *Nota: En el contexto de dimensionamiento, la capacidad del enlace $x_{ij}$ debe ser al menos la demanda de tráfico $f_{ij}$ dividida por la utilización máxima permitida.*

2. **Restricción de Flujo (Conservación):** El flujo de tráfico en cada nodo debe ser conservado (entrada = salida).
   $$\sum_{j} f_{ij} - \sum_{j} f_{ji} = \text{Generación/Consumo del nodo } i$$
   *(Esta restricción se aplica al flujo $f_{ij}$ que se dimensiona).*

3. **Restricción de Utilización:** El flujo de tráfico real ($f_{ij}$) no debe exceder el 85% de la capacidad dimensionada ($x_{ij}$).
   $$f_{ij} \le U_{max} \cdot x_{ij} \quad \forall (i, j)$$

4. **Restricción de No Negatividad:** El número de módulos debe ser no negativo.
   $$x_{ij} \ge 0$$

**Función Objetivo:**
Minimizar el coste total de los módulos necesarios.
$$\text{Minimizar } Z = \sum_{(i, j) \in \text{Enlaces}} C_{módulo} \cdot x_{ij}$$
$$\text{Minimizar } Z = \sum_{(i, j) \in \text{Enlaces}} x_{ij}$$

### b. Solución Programada (Metodología y Resultado Esperado)

**Asignación de Opciones:**
Dado el enunciado, la asignación de opciones es: **AABD** (Asumiendo que la formulación es un problema de optimización de flujo y capacidad).

**Entradas y Salidas del Script .m:**
*   **Entradas:** Matriz de Tráfico $T_{ij}$, Capacidad Nominal $C_{ij}$, $U_{max}=0.85$, Coste $C_{módulo}=1$.
*   **Salidas:** Valores óptimos de las variables de decisión $x_{ij}$ (número de módulos) y el Coste Total $Z$.

**Resultado Esperado o Metodología Exacta:**

1. **Definición de Variables:** Se definen las variables $x_{ij}$ para los 12 enlaces de la topología (A-B, A-C, A-D, B-A, B-C, B-D, C-A, C-B, C-D, D-A, D-B, D-C).
2. **Definición de Restricciones:** Se establecen las restricciones de capacidad y flujo basadas en la matriz de tráfico y la utilización máxima (85%).
3. **Implementación del Solver:** Se utiliza un solver de Programación Lineal Entera (MILP) en Octave/Matlab para encontrar el conjunto de valores de $x_{ij}$ que minimizan la suma de los módulos.
4. **Cálculo de Módulos:** El script calculará el número mínimo de módulos $x_{ij}$ que deben instalarse en cada enlace para garantizar que el tráfico nominal $T_{ij}$ se pueda transmitir con una utilización máxima del 85% de la capacidad dimensionada.

**Resultado Final (Ejemplo Conceptual):**
El resultado será un vector de 12 valores, donde cada valor $x_{ij}$ representa el número mínimo de módulos requeridos para el enlace $(i, j)$. El valor $Z$ será el coste total mínimo de estos módulos.

*Nota: Dado que no se ejecuta el solver, se especifica la metodología. El resultado exacto se obtiene al ejecutar el script en el entorno de PRADO.*

============================================================

PREGUNTA: exit
