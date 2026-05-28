Cargando modelo de embeddings...
RAG listo
- Vector DB: /app/chroma_ddr
- Embeddings: intfloat/multilingual-e5-base
- LLM provider: ollama
- Ollama model: gemma4:e2b
Escribe una pregunta y pulsa Enter. Escribe 'exit' para salir.

PREGUNTA: [*] Recuperando contexto de la base de datos...
[DEBUG] Iniciando retrieve_context...
[DEBUG] Consulta de examen detectada: True
[+] Contexto recuperado
[*] Generando respuesta...

RESPUESTA:

EXAMEN

1. (0.5 ptos) Explique por que es necesario caracterizar por separado la infraestructura fisica y la logica de una red antes de proponer un nuevo diseno.

2. (0.5 ptos) Defina que representa una matriz de trafico en DDR y explique como se utiliza para pasar de requisitos de usuarios a necesidades de capacidad en enlaces.

3. (1.0 pto) Formule conceptualmente la restriccion de capacidad de una red usando una notacion de flujo-camino-demanda. Indique datos de entrada, variables de decision y salidas esperadas.

4. (2.0 puntos) Dimensionado de enlaces con trafico encaminado y coste minimo

A partir de la topologia de la Figura 1 y de la matriz de trafico indicada, dimensione la capacidad de los enlaces mediante modulos de 10 Gbps.

Figura 1. Topologia fisica T2:
- Nodos: A, B, C, D.
- Enlaces bidireccionales:
- e1 = A-B.
- e2 = B-C.
- e3 = C-D.
- e4 = A-D.
- e5 = B-D.
- No existen enlaces fisicos adicionales fuera de los indicados.

OPC 1: Topologia T2, definida por los enlaces anteriores.

OPC 2: Matriz de trafico M2, en Gbps:
- A -> B: 4.
- B -> A: 5.
- A -> C: 9.
- C -> A: 6.
- B -> C: 6.
- C -> B: 5.
- C -> D: 7.
- D -> C: 6.
- A -> D: 4.
- D -> A: 3.
- B -> D: 8.
- D -> B: 5.

OPC 3: Encaminamiento nominal R2:
- A -> B usa la ruta A-B.
- B -> A usa la ruta B-A.
- A -> C usa la ruta A-B-C.
- C -> A usa la ruta C-B-A.
- B -> C usa la ruta B-C.
- C -> B usa la ruta C-B.
- C -> D usa la ruta C-D.
- D -> C usa la ruta D-C.
- A -> D usa la ruta A-D.
- D -> A usa la ruta D-A.
- B -> D usa la ruta B-D.
- D -> B usa la ruta D-B.

OPC 4: Dimensionado por modulos:
- Cada modulo aporta 10 Gbps de capacidad al enlace donde se instala.
- Cada enlace puede tener un numero entero de modulos m_e entre 0 y 4.
- La utilizacion maxima permitida por enlace es 0.8.
- El coste de cada modulo es 1 unidad.
- El objetivo es minimizar el coste total, es decir, minimizar el numero total de modulos instalados.

Se pide:

a) Formule el problema como una programacion lineal entera, indicando variables, funcion objetivo, restricciones, entradas y salidas. (1 pto)

b) Calcule la carga agregada de cada enlace fisico bajo R2 y determine el numero minimo de modulos necesarios por enlace. Compruebe la utilizacion final de cada enlace. (0.5 ptos)

c) Indique como implementaria la solucion en Octave/Matlab y que resultados debe devolver el script .m. (0.5 ptos)

SOLUCIONARIO

1. Respuesta orientativa:
La caracterización separada de la infraestructura física y la lógica de una red es fundamental en el diseño y dimensionado de redes por las siguientes razones:

**Infraestructura Física:** Se refiere a los componentes tangibles de la red (cableado, dispositivos, capacidad de los enlaces, topología física, ubicación de los nodos). Caracterizar esto permite evaluar la viabilidad de la implementación, identificar limitaciones físicas (ej. distancia, tipo de medio, capacidad máxima del enlace), determinar los costes de instalación y asegurar que la infraestructura existente puede soportar la nueva demanda.

**Infraestructura Lógica:** Se refiere a cómo se organizan los servicios, los protocolos, las direcciones, las políticas de seguridad y el flujo de datos (rutas, direccionamiento IP, QoS, políticas de tráfico). Caracterizar esto permite entender los requisitos de comunicación, las políticas de servicio requeridas por los usuarios y cómo se deben gestionar los flujos de información.

**Necesidad de la Separación:**
1. **Viabilidad y Restricciones:** La infraestructura física establece los límites de lo que es posible (ej. la capacidad máxima de un cable). La lógica define lo que se desea lograr (ej. la ruta óptima). Un diseño debe respetar ambas restricciones.
2. **Dimensionamiento Realista:** El dimensionamiento de capacidad (lógica) debe basarse en la capacidad real disponible (física). Si se ignora la física, se proponen soluciones lógicamente óptimas que son físicamente imposibles.
3. **Optimización de Costes:** La infraestructura física influye directamente en el coste de la implementación. La lógica ayuda a optimizar el uso de esa infraestructura.
4. **Diseño Integral:** Un diseño de red exitoso requiere que la capa física soporte la capa lógica. Separarlas permite abordar los problemas de capacidad, coste y rendimiento de manera modular y sistemática.

2. Respuesta orientativa:
Una matriz de tráfico en el contexto de Diseño y Dimensionado de Redes (DDR) representa la cuantificación de la demanda de datos (flujos) que se espera que transiten entre diferentes pares de nodos (enlaces) dentro de una red.

**Definición:** Es una tabla o estructura que detalla el volumen de tráfico (medido en bits por segundo, Gbps, o Mbps) que se mueve en cada dirección entre cada par de enlaces definidos en la topología.

**Utilidad para pasar de requisitos de usuarios a necesidades de capacidad:**
La matriz de tráfico es el puente esencial entre la demanda del usuario (requisitos) y el dimensionamiento de la infraestructura (necesidades de capacidad).

1. **Cuantificación de la Demanda:** Traduce los requisitos de servicio de los usuarios (ej. "el usuario X necesita una tasa de transferencia de Y") en flujos de datos concretos entre los puntos de la red.
2. **Identificación de Cuellos de Botella:** Al analizar la matriz, se puede identificar qué enlaces están experimentando el mayor tráfico y cuáles tienen la mayor demanda potencial. Esto permite localizar los puntos críticos de la red.
3. **Planificación de Capacidad:** Permite calcular la carga agregada real en cada enlace. Esto es crucial para determinar si la capacidad actual del enlace es suficiente para soportar la demanda proyectada, permitiendo así dimensionar la capacidad necesaria (el *oversizing* o sobredimensionamiento) de los enlaces para garantizar el rendimiento deseado (QoS).
4. **Toma de Decisiones:** Facilita la toma de decisiones sobre dónde invertir en nuevas capacidades, qué enlaces deben ser actualizados o si se requiere una reconfiguración de la topología.

3. Respuesta orientativa:
La restricción de capacidad de una red se formula conceptualmente utilizando la notación de flujo-camino-demanda, que es la base de los problemas de flujo máximo y mínimo en redes.

**Formulación Conceptual:**
El objetivo es asegurar que la capacidad total disponible en cada enlace sea mayor o igual a la demanda total de flujo que utiliza ese enlace, considerando las restricciones de capacidad y el encaminamiento.

**Datos de Entrada (Inputs):**
*   **Topología de la Red ($G=(V, E)$):** Conjunto de nodos ($V$) y enlaces ($E$).
*   **Matriz de Tráfico ($T$):** La demanda de flujo ($f_{ij}$) en cada enlace $(i, j)$.
*   **Capacidad de los Enlaces ($C_{ij}$):** La capacidad máxima teórica de cada enlace.
*   **Encaminamiento Nominal ($R$):** La ruta específica que se utiliza para transportar cada flujo.
*   **Capacidad de los Módulos ($M$):** La capacidad de un módulo de instalación (ej. 10 Gbps).

**Variables de Decisión (Decision Variables):**
*   **Número de Módulos por Enlace ($m_e$):** La cantidad entera de módulos instalados en cada enlace $e \in E$.

**Salidas Esperadas (Outputs):**
*   **Carga Agregada ($L_e$):** La suma de todos los flujos que utilizan un enlace $e$.
*   **Utilización Final ($\rho_e$):** La relación entre la carga agregada y la capacidad del enlace ($L_e / C_e$).
*   **Coste Total ($Cost$):** La suma de los costes de los módulos instalados ($\sum m_e \times \text{Coste del módulo}$).

**Formulación Matemática Abstracta (Ejemplo de Restricción):**
Para cada enlace $e \in E$, la restricción de capacidad debe asegurar que la capacidad instalada sea suficiente para la carga agregada:
$$\sum_{f \in F} x_{f, e} \le C_e$$
Donde $x_{f, e}$ es la cantidad de flujo $f$ que utiliza el enlace $e$.

**Resumen de la Formulación:**
*   **Entradas:** Demanda de tráfico, capacidad física, y política de encaminamiento.
*   **Variables de Decisión:** La cantidad de módulos a instalar en cada enlace.
*   **Salidas:** La carga real en cada enlace y el coste mínimo de la infraestructura.

4. (2.0 puntos) Solucion del dimensionado de capacidad con modulos

Opciones usadas:
- OPC 1: Topologia T2.
- OPC 2: Matriz de trafico M2.
- OPC 3: Encaminamiento nominal R2.
- OPC 4: Modulos de 10 Gbps, utilizacion maxima 0.8 y coste unitario 1.

a) Formulacion matematica

Conjunto de enlaces fisicos:
E = {AB, BC, CD, AD, BD}.

Variable entera:
- m_e: numero de modulos instalados en el enlace e, con m_e entero y 0 <= m_e <= 4.

Datos:
- C = 10 Gbps por modulo.
- u_max = 0.8.
- L_e: carga agregada del enlace e calculada a partir de la matriz M2 y el encaminamiento R2.

Funcion objetivo:
Minimizar:
Z = sum_{e in E} m_e

Restriccion de capacidad/utilizacion para cada enlace:
L_e <= u_max * C * m_e

Como C = 10 y u_max = 0.8:
L_e <= 8 * m_e

Salidas del script:
- Numero de modulos m_e por enlace.
- Capacidad instalada C * m_e por enlace.
- Utilizacion final L_e / (C * m_e).
- Coste total Z.

b) Calculo de cargas y modulos

Rutas usadas:
- A -> B: A-B, carga 4.
- B -> A: B-A, carga 5.
- A -> C: A-B-C, carga 9.
- C -> A: C-B-A, carga 6.
- B -> C: B-C, carga 6.
- C -> B: C-B, carga 5.
- C -> D: C-D, carga 7.
- D -> C: D-C, carga 6.
- A -> D: A-D, carga 4.
- D -> A: D-A, carga 3.
- B -> D: B-D, carga 8.
- D -> B: D-B, carga 5.

Cargas agregadas por enlace:
- L_AB = 24 Gbps.
- L_BC = 26 Gbps.
- L_CD = 13 Gbps.
- L_AD = 7 Gbps.
- L_BD = 13 Gbps.

Numero minimo de modulos:
m_e = ceil(L_e / 8)

Por tanto:
- m_AB = ceil(24 / 8) = 3 modulos.
- m_BC = ceil(26 / 8) = 4 modulos.
- m_CD = ceil(13 / 8) = 2 modulos.
- m_AD = ceil(7 / 8) = 1 modulos.
- m_BD = ceil(13 / 8) = 2 modulos.

Capacidades instaladas:
- AB: 30 Gbps.
- BC: 40 Gbps.
- CD: 20 Gbps.
- AD: 10 Gbps.
- BD: 20 Gbps.

Utilizaciones finales:
- u_AB = 24 / 30 = 0.8.
- u_BC = 26 / 40 = 0.65.
- u_CD = 13 / 20 = 0.65.
- u_AD = 7 / 10 = 0.7.
- u_BD = 13 / 20 = 0.65.

Todas las utilizaciones son menores o iguales que 0.8, por lo que la solucion cumple la restriccion.

Coste total:
Z = 3 + 4 + 2 + 1 + 2 = 12 unidades.

Resultado final:
- AB: 3 modulos.
- BC: 4 modulos.
- CD: 2 modulos.
- AD: 1 modulos.
- BD: 2 modulos.
- Coste minimo total: 12 unidades.

c) Implementacion en Octave/Matlab

El problema tambien puede escribirse como el siguiente entero lineal:

minimizar 1^T m
sujeto a L <= 8 m
m entero
0 <= m <= 4

Como las rutas estan fijadas por R2 y cada restriccion solo depende del modulo del propio enlace, el optimo se obtiene enlace a enlace mediante:
m_e = ceil(L_e / 8)

Esto prueba la optimalidad de la solucion anterior: ningun enlace puede tener menos modulos que ceil(L_e / 8), y la solucion propuesta alcanza exactamente ese minimo en todos los enlaces.

Script Octave/Matlab orientativo:

```matlab
% Enlaces en este orden
enlaces = {'AB', 'BC', 'CD', 'AD', 'BD'};

L = [24, 26, 13, 7, 13];   % cargas agregadas en Gbps
C = 10;                  % Gbps por modulo
u_max = 0.8;            % utilizacion maxima

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
- m = [3, 4, 2, 1, 2].
- capacidad = [30, 40, 20, 10, 20] Gbps.
- utilizacion = [0.8, 0.65, 0.65, 0.7, 0.65].
- coste_total = 12.

============================================================

PREGUNTA: 