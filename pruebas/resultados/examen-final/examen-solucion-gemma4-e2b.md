Cargando modelo de embeddings...
modules.json:   0% 0.00/387 [00:00<?, ?B/s]modules.json: 100% 387/387 [00:00<00:00, 571kB/s]
README.md: 0.00B [00:00, ?B/s]README.md: 179kB [00:00, 39.5MB/s]
sentence_bert_config.json:   0% 0.00/57.0 [00:00<?, ?B/s]sentence_bert_config.json: 100% 57.0/57.0 [00:00<00:00, 87.6kB/s]
config.json:   0% 0.00/694 [00:00<?, ?B/s]config.json: 100% 694/694 [00:00<00:00, 561kB/s]
model.safetensors:   0% 0.00/1.11G [00:00<?, ?B/s]model.safetensors:   6% 67.1M/1.11G [00:03<00:47, 22.1MB/s]model.safetensors:  12% 134M/1.11G [00:05<00:37, 26.1MB/s] model.safetensors:  24% 268M/1.11G [00:06<00:16, 52.5MB/s]model.safetensors:  30% 335M/1.11G [00:08<00:17, 44.8MB/s]model.safetensors: 100% 1.11G/1.11G [00:09<00:00, 189MB/s]model.safetensors: 100% 1.11G/1.11G [00:12<00:00, 89.6MB/s]
Loading weights:   0% 0/199 [00:00<?, ?it/s]Loading weights: 100% 199/199 [00:00<00:00, 4085.73it/s]
tokenizer_config.json:   0% 0.00/418 [00:00<?, ?B/s]tokenizer_config.json: 100% 418/418 [00:00<00:00, 774kB/s]
sentencepiece.bpe.model:   0% 0.00/5.07M [00:00<?, ?B/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:01<00:00, 4.96MB/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:01<00:00, 4.96MB/s]
tokenizer.json:   0% 0.00/17.1M [00:00<?, ?B/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 23.5MB/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 23.5MB/s]
special_tokens_map.json:   0% 0.00/280 [00:00<?, ?B/s]special_tokens_map.json: 100% 280/280 [00:00<00:00, 544kB/s]
config.json:   0% 0.00/200 [00:00<?, ?B/s]config.json: 100% 200/200 [00:00<00:00, 406kB/s]
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

## EXAMEN

### 1. Direccionamiento de Redes y Protocolos (0.5 ptos)
Discuta las principales ventajas y desventajas de implementar un esquema de direccionamiento estático frente a uno dinámico (ej. DHCP, SLAAC) en una red empresarial moderna.

### 2. Optimización de Rutas (0.5 ptos)
Explique la diferencia fundamental entre el algoritmo de Dijkstra y el algoritmo de Bellman-Ford en el contexto del cálculo de caminos óptimos en redes. ¿En qué escenarios es más adecuado utilizar cada uno?

### 3. Dimensionamiento de Capacidad (1.0 pto)
En el contexto del Dimensionamiento y Diseño de Redes (DDR), ¿cuál es la técnica analítica más adecuada para determinar la capacidad mínima requerida de un enlace para soportar un tráfico futuro, considerando la incertidumbre y la necesidad de optimización de recursos? Justifique su elección.

### 4. Problema de Dimensionamiento y Optimización (2.0 ptos)
Considere la siguiente topología de red y la matriz de tráfico asociada. El objetivo es dimensionar la capacidad de los enlaces para minimizar la congestión total, sujeto a las capacidades físicas de los enlaces.

**Topología:**
Se dispone de tres nodos (A, B, C) conectados por tres enlaces: A-B, B-C, A-C.

**Matriz de Tráfico (en Gbps):**
*   Tráfico A $\to$ B: 10
*   Tráfico B $\to$ C: 15
*   Tráfico A $\to$ C: 5

**Restricciones de Capacidad (Capacidad Máxima de los enlaces):**
*   Capacidad del enlace A-B: 12 Gbps
*   Capacidad del enlace B-C: 10 Gbps
*   Capacidad del enlace A-C: 8 Gbps

**Formulación Requerida:**
a) Formule la formulación matemática abstracta (variables, función objetivo y restricciones) para determinar la capacidad mínima requerida de cada enlace para satisfacer la demanda de tráfico.
b) Realice la solución programada utilizando Octave/Matlab, entregando el script y la solución.

---

## SOLUCIONARIO

### 1. Direccionamiento de Redes y Protocolos (0.5 ptos)
**Respuesta:**
**Direccionamiento Estático:**
*   **Ventajas:** Ofrece control total sobre la asignación de direcciones, lo que facilita la seguridad y la previsibilidad. Es ideal para dispositivos fijos o servidores donde la estabilidad es crítica.
*   **Desventajas:** Requiere una gestión manual intensiva. Si la red cambia o se añaden dispositivos, se debe realizar una reconfiguración manual, lo que aumenta el riesgo de errores y la administración es compleja en redes grandes y dinámicas.

**Direccionamiento Dinámico (ej. DHCP, SLAAC):**
*   **Ventajas:** Permite la automatización de la asignación de direcciones, reduciendo la carga administrativa. Es ideal para redes con muchos dispositivos que se añaden y eliminan frecuentemente.
*   **Desventajas:** Introduce una dependencia de un servidor central (DHCP) o de la configuración de la red (SLAAC). Puede generar problemas de seguridad si no se implementan mecanismos de control adecuados, y la gestión de conflictos puede ser compleja.

### 2. Optimización de Rutas (0.5 ptos)
**Respuesta:**
**Diferencia Fundamental:**
*   **Dijkstra:** Busca el camino más corto (mínimo) entre un nodo fuente y todos los demás nodos en un grafo ponderado. Se enfoca en la minimización de la suma de los pesos de los enlaces.
*   **Bellman-Ford:** También busca el camino más corto, pero puede manejar pesos negativos (aunque no se permiten en redes físicas típicas) y es más robusto para detectar ciclos.

**Adecuación:**
*   **Dijkstra:** Es el algoritmo preferido para encontrar el camino óptimo en redes de tráfico donde los pesos (costes o latencias) son siempre positivos. Es más eficiente para este propósito.
*   **Bellman-Ford:** Es útil cuando se necesita detectar la existencia de ciclos en la red o cuando se deben considerar escenarios más complejos donde los pesos pueden variar dinámicamente, aunque es computacionalmente más costoso que Dijkstra en redes sin ciclos negativos.

### 3. Dimensionamiento de Capacidad (1.0 pto)
**Respuesta:**
La técnica analítica más adecuada para determinar la capacidad mínima requerida de un enlace para soportar una demanda de tráfico futura, considerando la incertidumbre y la necesidad de optimización de recursos, es la **Optimización de Red (Network Optimization)**, utilizando modelos basados en **Teoría de Colas (Queuing Theory)**.

**Justificación:**
1.  **Optimización de Red:** Permite considerar la interdependencia de múltiples enlaces y nodos, buscando una solución global que minimice un objetivo (ej. coste total o congestión).
2.  **Teoría de Colas:** Permite modelar el tráfico como un proceso estocástico (llegadas de paquetes) y calcular la capacidad necesaria para mantener un nivel de servicio (QoS) deseado, manejando la variabilidad y la congestión.

### 4. Problema de Dimensionamiento y Optimización (2.0 ptos)
**Respuesta:**

**Asignación de Opciones:**
*   OPC 1: A (Topología)
*   OPC 2: B (Matriz de Tráfico)
*   OPC 3: C (Formulación de Capacidad/Restricciones)
*   OPC 4: D (Objetivo: Mínima Congestión)

**a) Formulación Matemática Abstracta (1 pto)**

**Variables:**
*   $x_{AB}$: Capacidad requerida del enlace A-B (Gbps)
*   $x_{BC}$: Capacidad requerida del enlace B-C (Gbps)
*   $x_{AC}$: Capacidad requerida del enlace A-C (Gbps)

**Función Objetivo (Minimizar Congestión):**
Minimizar la suma de las diferencias entre el tráfico real y la capacidad asignada (o minimizar el exceso de tráfico sobre la capacidad).
$$ \text{Minimizar } Z = \sum_{(i, j) \in E} \max(0, T_{ij} - x_{ij}) $$
Donde $T_{ij}$ es el tráfico real en el enlace $(i, j)$, y $E$ es el conjunto de enlaces.

**Restricciones:**
1.  **Restricciones de Capacidad Física (Límite Superior):** La capacidad requerida no puede exceder la capacidad física máxima del enlace.
    $$ x_{AB} \le 12 $$
    $$ x_{BC} \le 10 $$
    $$ x_{AC} \le 8 $$
2.  **Restricciones de Demanda (Mínimo Requerido):** La capacidad debe ser suficiente para soportar el tráfico real en cada enlace.
    $$ x_{AB} \ge T_{AB} = 10 $$
    $$ x_{BC} \ge T_{BC} = 15 $$
    $$ x_{AC} \ge T_{AC} = 5 $$

**b) Solución Programada (1 pto)**

**Método:** Se utiliza la formulación de programación lineal (PL) para encontrar los valores de $x_{ij}$ que minimicen la congestión, respetando las restricciones de capacidad física y la demanda de tráfico.

**Variables y Restricciones (en términos de la matriz):**
*   $x_{AB} \ge 10$ y $x_{AB} \le 12$
*   $x_{BC} \ge 15$ y $x_{BC} \le 10$
*   $x_{AC} \ge 5$ y $x_{AC} \le 8$

**Análisis de Viabilidad:**
Existe una inconsistencia en la restricción del enlace B-C:
*   Demanda de tráfico $T_{BC} = 15$ Gbps.
*   Capacidad física máxima del enlace B-C es $10$ Gbps.

**Resultado y Conclusión:**
Dado que la demanda de tráfico ($15$ Gbps) excede la capacidad física máxima del enlace ($10$ Gbps), es **matemáticamente imposible** satisfacer la demanda de tráfico en el enlace B-C sin una modificación física de la infraestructura.

**Solución Metodológica (Asumiendo que la capacidad física es el límite):**
Si el objetivo es minimizar la congestión *dentro de las capacidades físicas existentes*, la solución es que el sistema es inviable.

**Resultado Esperado (Si se fuerza la solución):**
Si se interpreta la pregunta como encontrar la capacidad mínima *posible* que se acerca a la demanda, se debe indicar la violación de la restricción.

*   **Enlace A-B:** $x_{AB} = 10$ Gbps (Mínimo requerido)
*   **Enlace B-C:** $x_{BC}$ no puede ser satisfecho. La congestión es inevitable, ya que $15 > 10$.
*   **Enlace A-C:** $x_{AC} = 5$ Gbps (Mínimo requerido)

**Conclusión Final:**
El dimensionamiento de la red, tal como se presenta con las restricciones dadas, resulta en una **inviabilidad** para el enlace B-C, ya que la demanda de tráfico excede la capacidad física disponible. Se requiere una ampliación física del enlace B-C a al menos 15 Gbps para satisfacer la demanda.

============================================================

PREGUNTA: exit
