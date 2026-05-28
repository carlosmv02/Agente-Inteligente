Cargando modelo de embeddings...
modules.json:   0% 0.00/387 [00:00<?, ?B/s]modules.json: 100% 387/387 [00:00<00:00, 683kB/s]
README.md: 0.00B [00:00, ?B/s]README.md: 179kB [00:00, 43.3MB/s]
sentence_bert_config.json:   0% 0.00/57.0 [00:00<?, ?B/s]sentence_bert_config.json: 100% 57.0/57.0 [00:00<00:00, 50.5kB/s]
config.json:   0% 0.00/694 [00:00<?, ?B/s]config.json: 100% 694/694 [00:00<00:00, 1.22MB/s]
model.safetensors:   0% 0.00/1.11G [00:00<?, ?B/s]model.safetensors:   6% 67.1M/1.11G [00:03<00:51, 20.4MB/s]model.safetensors:  18% 201M/1.11G [00:03<00:12, 71.0MB/s] model.safetensors:  24% 268M/1.11G [00:08<00:28, 29.6MB/s]model.safetensors:  84% 939M/1.11G [00:08<00:01, 159MB/s] model.safetensors: 100% 1.11G/1.11G [00:09<00:00, 162MB/s]model.safetensors: 100% 1.11G/1.11G [00:12<00:00, 89.8MB/s]
Loading weights:   0% 0/199 [00:00<?, ?it/s]Loading weights: 100% 199/199 [00:00<00:00, 4222.59it/s]
tokenizer_config.json:   0% 0.00/418 [00:00<?, ?B/s]tokenizer_config.json: 100% 418/418 [00:00<00:00, 858kB/s]
sentencepiece.bpe.model:   0% 0.00/5.07M [00:00<?, ?B/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:01<00:00, 4.66MB/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:01<00:00, 4.66MB/s]
tokenizer.json:   0% 0.00/17.1M [00:00<?, ?B/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 26.7MB/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 26.7MB/s]
special_tokens_map.json:   0% 0.00/280 [00:00<?, ?B/s]special_tokens_map.json: 100% 280/280 [00:00<00:00, 596kB/s]
config.json:   0% 0.00/200 [00:00<?, ?B/s]config.json: 100% 200/200 [00:00<00:00, 434kB/s]
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

1. (0.5 ptos) Discuta las ventajas y desventajas de implementar un esquema de direccionamiento estático frente a un esquema de direccionamiento dinámico en una red empresarial moderna.

2. (0.5 ptos) Explique el concepto de Network Telemetry y cómo esta tecnología contribuye a la toma de decisiones y la automatización en entornos de Redes Autónomas.

3. (1.0 pto) En el contexto de Intent Based Networking (IBN), analice cómo la capacidad de programabilidad (Programmability) de la red permite transformar una intención de negocio (ej. garantizar una latencia específica) en políticas de control automáticas para los dispositivos de la red.

4. (2.0 puntos) Dimensionado de capacidad con modulos y utilizacion maxima

A partir de la topologia de la Figura 1 y de la matriz de trafico indicada, dimensione la capacidad de los enlaces mediante modulos de 10 Gbps.

Figura 1. Topologia fisica T1:
- Nodos: A, B, C y D.
- Enlaces bidireccionales: e1 = A-B, e2 = B-C, e3 = C-D, e4 = D-A, e5 = A-C.
- No existen enlaces fisicos B-D ni A-D-C adicionales fuera de los indicados.

OPC 1: Topologia T1, definida por los enlaces e1..e5.

OPC 2: Matriz de trafico M1, en Gbps:
- A -> B: 6; A -> C: 8; A -> D: 4.
- B -> A: 3; B -> C: 7; B -> D: 5.
- C -> A: 5; C -> B: 4; C -> D: 6.
- D -> A: 4; D -> B: 3; D -> C: 5.

OPC 3: Encaminamiento nominal R1:
- Las demandas directas A-B, A-C, C-D y D-A usan su enlace directo.
- B -> D usa la ruta B-C-D.
- D -> B usa la ruta D-C-B.
- C -> B usa la ruta C-B.
- Las demandas en sentido inverso usan el mismo enlace fisico en sentido inverso.

OPC 4: Dimensionado por modulos:
- Cada modulo aporta 10 Gbps de capacidad al enlace donde se instala.
- Cada enlace puede tener un numero entero de modulos m_e entre 0 y 4.
- La utilizacion maxima permitida por enlace es 0.85.
- El coste de cada modulo es 1 unidad.
- El objetivo es minimizar el coste total, es decir, minimizar el numero total de modulos instalados.

Se pide:

a) Formule el problema como una programacion lineal entera, indicando variables, funcion objetivo, restricciones, entradas y salidas. (1 pto)

b) Calcule la carga agregada de cada enlace fisico bajo R1 y determine el numero minimo de modulos necesarios por enlace. Compruebe la utilizacion final de cada enlace. (0.5 ptos)

c) Indique como implementaria la solucion en Octave/Matlab y que resultados debe devolver el script .m. (0.5 ptos)

SOLUCIONARIO

1. Respuesta orientativa:
**Ventajas y Desventajas del Direccionamiento Estático vs. Dinámico**

**Esquema de Direccionamiento Estático:**
*   **Ventajas:**
    *   **Seguridad y Previsibilidad:** Ofrece un control total y predecible sobre la asignación de direcciones. Es ideal para entornos pequeños, redes estables o dispositivos IoT donde la configuración debe ser fija.
    *   **Simplicidad:** Es fácil de implementar y gestionar, reduciendo la complejidad de los protocolos de asignación.
    *   **Estabilidad:** Minimiza los errores de asignación y los conflictos de direcciones.
*   **Desventajas:**
    *   **Ineficiencia:** Puede llevar a un desperdicio de direcciones IP si no se gestiona adecuadamente (fragmentación).
    *   **Escalabilidad Limitada:** Se vuelve muy complejo de gestionar en redes grandes y dinámicas, requiriendo intervención manual para cambios.
    *   **Gestión Laboriosa:** Requiere un proceso manual de configuración y reasignación, lo que aumenta el riesgo de errores humanos.

**Esquema de Direccionamiento Dinámico:**
*   **Ventajas:**
    *   **Eficiencia y Escalabilidad:** Permite utilizar un rango de direcciones mucho más amplio, optimizando el uso del espacio de direcciones.
    *   **Automatización:** Facilita la asignación automática de direcciones mediante protocolos (como DHCP), reduciendo la carga administrativa.
    *   **Adaptabilidad:** Permite que la red se adapte automáticamente a los cambios en la topología y la demanda de tráfico.
*   **Desventajas:**
    *   **Complejidad:** Introduce una mayor complejidad en la gestión de la red, ya que requiere protocolos de asignación y monitoreo constantes.
    *   **Seguridad:** Si no se implementan mecanismos de seguridad adecuados, puede aumentar el riesgo de ataques o la asignación de direcciones no autorizadas.
    *   **Dependencia:** La red depende de la correcta operación de los servidores DHCP y de los protocolos de comunicación.

**Conclusión en Redes Empresariales Modernas:**
En una red empresarial moderna, se tiende a implementar esquemas **dinámicos** (como DHCP o soluciones basadas en SDN/SDN) para aprovechar la escalabilidad y la eficiencia. Sin embargo, para segmentos críticos, dispositivos IoT o entornos de control industrial donde la estabilidad y la seguridad son primordiales, el **direccionamiento estático** sigue siendo una opción válida, aunque requiere una gestión centralizada y robusta.

2. Respuesta orientativa:
**Concepto de Network Telemetry y su Contribución a la Automatización**

**Concepto de Network Telemetry (Teledetección de Red):**
Network Telemetry es una tecnología que permite la recopilación de datos de rendimiento, estado y métricas de la red en tiempo real y de alta granularidad. A diferencia del monitoreo tradicional (que se basa en muestreos periódicos), la telemetría proporciona una visión continua y detallada del comportamiento de la red, incluyendo el flujo de datos, la latencia, la congestión, la utilización de recursos y el estado de los enlaces.

**Contribución a la Toma de Decisiones y la Automatización en Redes Autónomas:**
La telemetría es fundamental para la transición hacia Redes Autónomas (Autonomous Networks) y sistemas de control basados en la inteligencia artificial (AI/ML). Su contribución se manifiesta de la siguiente manera:

1.  **Datos Ricos (Garbage In/Out):** La telemetría genera datos ricos y detallados (el "garbage in" de la IA). Estos datos son la materia prima necesaria para entrenar modelos de Machine Learning que pueden identificar patrones de tráfico, predecir fallos y detectar anomalías en la red con alta precisión.
2.  **Toma de Decisiones Basada en Datos:** Al proporcionar una visión en tiempo real del estado de la red, permite a los sistemas de control tomar decisiones informadas de manera proactiva. Por ejemplo, si la telemetría indica una alta latencia en un enlace específico, el sistema puede decidir automáticamente reconfigurar las rutas o ajustar la capacidad de los enlaces para mitigar el problema.
3.  **Automatización (Control Automático):** En entornos de Redes Autónomas, la telemetría alimenta los sistemas de control automático. Los datos de telemetría se utilizan como *inputs* para los algoritmos de control (como los sistemas de control de retroalimentación, como se menciona en el contexto), permitiendo que los dispositivos ajusten sus parámetros (sensores y actuadores) para alcanzar un estado deseado (Set Point). Esto se traduce en una capacidad de respuesta inmediata y la capacidad de operar con mínima interacción humana.

3. Respuesta orientativa:
**Intent Based Networking (IBN) y la Programabilidad en Redes**

**Análisis de IBN y la Programabilidad:**
Intent Based Networking (IBN) es un paradigma de gestión de redes que busca abstraer la complejidad de la configuración de la infraestructura física y lógica para centrarse en los **objetivos de negocio** (Intenciones). En lugar de configurar manualmente rutas, políticas de seguridad o QoS en cada dispositivo, el administrador define lo que la red *debe lograr* (la intención).

**El Rol de la Programabilidad (Programmability):**
La capacidad de programabilidad es el mecanismo que permite transformar esa intención de negocio en políticas de control automáticas para los dispositivos de la red.

1.  **Abstracción de la Intención:** La programabilidad permite definir la intención en términos de requisitos de alto nivel (ej. "Garantizar una latencia de 5 ms entre el servidor de base de datos y la aplicación").
2.  **Traducción a Políticas:** Los sistemas de IBN utilizan esta intención para traducir los requisitos de negocio en políticas de red concretas y ejecutables. Estas políticas definen las reglas operativas que deben seguir los dispositivos.
3.  **Control Automático (Feedback Loop):** La programabilidad permite que estas políticas se implementen mediante la automatización. Los dispositivos de la red (sensores) recopilan datos de telemetría sobre su estado actual y comparan este estado con la intención definida. Si se detecta una desviación (ej. la latencia es de 10 ms), el sistema de control (actuador) automáticamente ajusta los parámetros de la red (reconfigura el camino, ajusta la capacidad) para cumplir con la intención.

**Transformación de Intención en Control Automático:**
La programabilidad actúa como el puente entre el nivel estratégico (la intención de negocio) y el nivel operativo (la configuración de los dispositivos). Permite que la red deje de ser un sistema estático y se convierta en un sistema dinámico y reactivo. Esto facilita la implementación de un **lazo cerrado** (control automático) donde la red se auto-gestiona, asegurando que los objetivos de negocio se mantengan, independientemente de las fluctuaciones del tráfico o los fallos de la infraestructura. En esencia, la programabilidad permite que la red se adapte dinámicamente para cumplir con las reglas definidas por la intención.

4. (2.0 puntos) Solucion del dimensionado de capacidad con modulos

Opciones usadas:
- OPC 1: Topologia T1.
- OPC 2: Matriz de trafico M1.
- OPC 3: Encaminamiento nominal R1.
- OPC 4: Modulos de 10 Gbps, utilizacion maxima 0.85 y coste unitario 1.

a) Formulacion matematica

Conjunto de enlaces fisicos:
E = {AB, BC, CD, DA, AC}.

Variable entera:
- m_e: numero de modulos instalados en el enlace e, con m_e entero y 0 <= m_e <= 4.

Datos:
- C = 10 Gbps por modulo.
- u_max = 0.85.
- L_e: carga agregada del enlace e calculada a partir de la matriz M1 y el encaminamiento R1.

Funcion objetivo:
Minimizar:
Z = sum_{e in E} m_e

Restriccion de capacidad/utilizacion para cada enlace:
L_e <= u_max * C * m_e

Como C = 10 y u_max = 0.85:
L_e <= 8.5 * m_e

Salidas del script:
- Numero de modulos m_e por enlace.
- Capacidad instalada 10 * m_e por enlace.
- Utilizacion final L_e / (10 * m_e).
- Coste total Z.

b) Calculo de cargas y modulos

Rutas usadas:
- A -> B: AB, carga 6.
- B -> A: AB, carga 3.
- A -> C: AC, carga 8.
- C -> A: AC, carga 5.
- A -> D: DA, carga 4.
- D -> A: DA, carga 4.
- B -> C: BC, carga 7.
- C -> B: BC, carga 4.
- C -> D: CD, carga 6.
- D -> C: CD, carga 5.
- B -> D: BC + CD, carga 5.
- D -> B: CD + BC, carga 3.

Cargas agregadas por enlace:
- L_AB = 6 + 3 = 9 Gbps.
- L_BC = 7 + 4 + 5 + 3 = 19 Gbps.
- L_CD = 6 + 5 + 5 + 3 = 19 Gbps.
- L_DA = 4 + 4 = 8 Gbps.
- L_AC = 8 + 5 = 13 Gbps.

Numero minimo de modulos:
m_e = ceil(L_e / 8.5)

Por tanto:
- m_AB = ceil(9 / 8.5) = 2 modulos.
- m_BC = ceil(19 / 8.5) = 3 modulos.
- m_CD = ceil(19 / 8.5) = 3 modulos.
- m_DA = ceil(8 / 8.5) = 1 modulo.
- m_AC = ceil(13 / 8.5) = 2 modulos.

Capacidades instaladas:
- AB: 20 Gbps.
- BC: 30 Gbps.
- CD: 30 Gbps.
- DA: 10 Gbps.
- AC: 20 Gbps.

Utilizaciones finales:
- u_AB = 9 / 20 = 0.45.
- u_BC = 19 / 30 = 0.633.
- u_CD = 19 / 30 = 0.633.
- u_DA = 8 / 10 = 0.80.
- u_AC = 13 / 20 = 0.65.

Todas las utilizaciones son menores o iguales que 0.85, por lo que la solucion cumple la restriccion.

Coste total:
Z = 2 + 3 + 3 + 1 + 2 = 11 unidades.

Resultado final:
- AB: 2 modulos.
- BC: 3 modulos.
- CD: 3 modulos.
- DA: 1 modulo.
- AC: 2 modulos.
- Coste minimo total: 11 unidades.

c) Implementacion en Octave/Matlab

El problema tambien puede escribirse como el siguiente entero lineal:

minimizar 1^T m
sujeto a L <= 8.5 m
m entero
0 <= m <= 4

Como las rutas estan fijadas por R1 y cada restriccion solo depende del modulo
del propio enlace, el optimo se obtiene enlace a enlace mediante:
m_e = ceil(L_e / 8.5)

Esto prueba la optimalidad de la solucion anterior: ningun enlace puede tener
menos modulos que ceil(L_e / 8.5), y la solucion propuesta alcanza exactamente
ese minimo en todos los enlaces.

Script Octave/Matlab orientativo:

```matlab
% Enlaces en este orden: AB, BC, CD, DA, AC
enlaces = {'AB', 'BC', 'CD', 'DA', 'AC'};

L = [9, 19, 19, 8, 13];   % cargas agregadas en Gbps
C = 10;                  % Gbps por modulo
u_max = 0.85;            % utilizacion maxima

m = ceil(L ./ (u_max * C));
capacidad = C .* m;
utilizacion = L ./ capacidad;
coste_total = sum(m);

fprintf('Enlace  Carga  Modulos  Capacidad  Utilizacion\n');
for i = 1:length(enlaces)
    fprintf('%s      %.1f     %d       %.1f       %.3f\n', ...
        enlaces{i}, L(i), m(i), capacidad(i), utilizacion(i));
end

fprintf('Coste total = %d unidades\n', coste_total);

if any(utilizacion > u_max + 1e-12)
    error('La solucion no cumple la utilizacion maxima');
end
```

La salida esperada del script es:
- m = [2, 3, 3, 1, 2].
- capacidad = [20, 30, 30, 10, 20] Gbps.
- utilizacion = [0.45, 0.633, 0.633, 0.80, 0.65].
- coste_total = 11.

============================================================

PREGUNTA: exit
