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

Datos del ejercicio. La pregunta queda completamente definida por las siguientes
opciones, que deben usarse sin anadir enlaces ni demandas no indicadas:

OPC 1 = T2. Topologia fisica de la Figura 1:
- Nodos: A, B, C, D.
- Enlaces permitidos, todos bidireccionales:
| Codigo | Enlace fisico bidireccional | Identificador usado en la solucion |
|---|---|---|
| e1 | A-B | AB |
| e2 | B-C | BC |
| e3 | C-D | CD |
| e4 | A-D | AD |
| e5 | B-D | BD |
- No existen enlaces fisicos adicionales fuera de los indicados.
- Cada identificador de enlace acumula el trafico de ambos sentidos. Por ejemplo,
  AB acumula trafico A -> B y B -> A si esas demandas usan el enlace A-B.

OPC 2 = M2. Matriz de trafico en Gbps:
| Origen \ Destino | A | B | C | D |
|---|---|---|---|---|
| A | - | 4 | 9 | 4 |
| B | 5 | - | 6 | 8 |
| C | 6 | 5 | - | 7 |
| D | 3 | 5 | 6 | - |

OPC 3 = R2. Encaminamiento nominal de cada demanda:
| Demanda | Trafico (Gbps) | Ruta nominal | Enlaces fisicos usados |
|---|---:|---|---|
| d1: A -> B | 4 | A-B | AB |
| d2: B -> A | 5 | B-A | AB |
| d3: A -> C | 9 | A-B-C | AB, BC |
| d4: C -> A | 6 | C-B-A | BC, AB |
| d5: B -> C | 6 | B-C | BC |
| d6: C -> B | 5 | C-B | BC |
| d7: C -> D | 7 | C-D | CD |
| d8: D -> C | 6 | D-C | CD |
| d9: A -> D | 4 | A-D | AD |
| d10: D -> A | 3 | D-A | AD |
| d11: B -> D | 8 | B-D | BD |
| d12: D -> B | 5 | D-B | BD |

OPC 4 = D2. Dimensionado por modulos:
- Cada modulo aporta 10 Gbps de capacidad al enlace donde se instala.
- Cada enlace puede tener un numero entero de modulos m_e entre 0 y 4.
- La utilizacion maxima permitida por enlace es 0.8.
- El coste de cada modulo es 1 unidad.
- El objetivo es minimizar el coste total, es decir, minimizar el numero total de modulos instalados.
- La capacidad instalada en el enlace e es C_e = 10 * m_e Gbps.
- La utilizacion final debe calcularse como u_e = L_e / C_e, donde L_e es la
  carga agregada del enlace e bajo el encaminamiento R2.

Se pide:

a) Formule el problema como una programacion lineal entera, indicando entradas,
   variables, funcion objetivo, restricciones y salidas. (1 pto)

b) Calcule la carga agregada de cada enlace fisico bajo R2, determine
   el numero minimo de modulos necesarios por enlace y compruebe la utilizacion
   final de cada enlace. (0.5 ptos)

c) Indique como implementaria la solucion en Octave/Matlab, entregando el script .m
   y los resultados. En la respuesta escrita debe aparecer la asignacion de OPC 1
   a OPC 4 y el resultado final en terminos de modulos, capacidades, utilizacion
   y coste total. (0.5 ptos)

SOLUCIONARIO

1. Respuesta orientativa: La caracterización separada de la infraestructura física y la lógica de una red es fundamental para un diseño robusto y eficiente. La infraestructura física define las limitaciones reales del sistema (capacidad de los enlaces, topología, latencia física, limitaciones de hardware, costes de instalación). La infraestructura lógica, por otro lado, define los requisitos del servicio (requisitos de QoS, políticas de seguridad, direccionamiento, requisitos de ancho de banda por aplicación, rutas deseadas).

Es necesario separarlas porque:
*   **Diseño Realista:** Permite identificar si la infraestructura física actual puede soportar los requisitos lógicos deseados. Por ejemplo, una topología física puede ser excelente, pero si los enlaces tienen una capacidad insuficiente (física), no se pueden satisfacer los requisitos de ancho de banda (lógica).
*   **Optimización:** Facilita la optimización. Se pueden optimizar los recursos físicos (dimensionamiento de enlaces) bajo las restricciones impuestas por los requisitos lógicos (tráfico y QoS).
*   **Gestión de Costes:** Permite evaluar el impacto económico de las decisiones. Los costes físicos (cableado, hardware) se combinan con los costes de servicio (ancho de banda requerido).
*   **Seguridad y Operación:** La infraestructura física establece los límites de la conectividad, mientras que la lógica define cómo se utiliza esa conectividad, asegurando que las políticas de seguridad y el direccionamiento se implementen correctamente sobre una base física viable.

2. Respuesta orientativa: Una matriz de tráfico en DDR representa la relación de flujo de datos (demanda) entre todos los pares de nodos (fuentes y destinos) en la red, especificando la cantidad de tráfico (en Gbps) que se espera en cada enlace físico.

**Utilidad para pasar de requisitos de usuarios a necesidades de capacidad:**

La matriz de tráfico actúa como el puente cuantitativo entre la demanda del usuario y la capacidad requerida de la infraestructura.

1.  **Requisitos de Usuarios (Demanda):** Se parte de los requisitos de los usuarios (ej. las demandas d1 a d12 en el ejemplo) que especifican el tráfico que debe fluir entre puntos específicos.
2.  **Cálculo de Carga Agregada (Flujo):** Se utiliza la matriz de tráfico (o el encaminamiento nominal) para calcular la carga total que cada enlace físico debe soportar. Esto se logra sumando el tráfico de todas las demandas que utilizan ese enlace.
3.  **Necesidades de Capacidad:** La carga agregada calculada representa la necesidad real de capacidad del enlace. Si la carga agregada de un enlace excede la capacidad física instalada, se identifica un cuello de botella y se determina la necesidad de dimensionar o añadir capacidad (módulos) para satisfacer la demanda.

En esencia, la matriz de tráfico permite transformar los requisitos de "qué quieren los usuarios" (demanda) en "cuánto debe soportar la infraestructura" (capacidad).

3. Respuesta orientativa: La restricción de capacidad de una red se formula conceptualmente mediante la relación entre el flujo de datos, el camino elegido y la demanda total.

**Notación de Flujo-Camino-Demanda:**

La restricción de capacidad se establece asegurando que la capacidad total disponible en un enlace sea mayor o igual a la carga agregada (flujo) que transita por ese enlace, considerando el encaminamiento de las demandas.

**Datos de Entrada:**
*   Matriz de tráfico (o encaminamiento nominal) $R$: La demanda de tráfico para cada flujo $d_i$.
*   Topología física $E$: La lista de enlaces físicos disponibles.
*   Capacidad del enlace $C_e$: La capacidad máxima instalada en cada enlace $e$.
*   Función de encaminamiento $\text{Ruta}(d_i)$: La ruta específica que se utiliza para satisfacer la demanda $d_i$.

**Variables de Decisión:**
*   $m_e$: Número de módulos instalados en el enlace físico $e$. (Variables enteras).

**Salidas Esperadas:**
*   Carga agregada $L_e$: La suma del tráfico de todas las demandas que utilizan el enlace $e$.
*   Utilización final $u_e$: La relación entre la carga agregada y la capacidad instalada ($u_e = L_e / C_e$).
*   Restricción de capacidad: $L_e \le C_e$ (o $L_e / C_e \le \text{Utilización Máxima Permitida}$).

4. (2.0 puntos) Solucion del dimensionado de capacidad con modulos

Opciones usadas:
- OPC 1 = T2: topologia fisica definida en el enunciado.
- OPC 2 = M2: matriz de trafico en Gbps.
- OPC 3 = R2: encaminamiento nominal fijado por demanda.
- OPC 4 = D2: modulos de 10 Gbps, utilizacion maxima 0.8,
  coste unitario 1 y maximo 4 modulos por enlace.

a) Formulacion matematica

Conjunto de enlaces fisicos:
E = {AB, BC, CD, AD, BD}.

Conjunto de demandas:
D = {d = (s,t)} con trafico h_d y ruta nominal p_d dados en M2 y R2.

Variable entera:
- m_e: numero de modulos instalados en el enlace e, con m_e entero y 0 <= m_e <= 4.

Datos:
- C = 10 Gbps por modulo.
- u_max = 0.8.
- c = 1: coste unitario de cada modulo.
- delta_ed = 1 si la ruta nominal de la demanda d usa el enlace e, y 0 en caso contrario.
- L_e = sum_{d in D} h_d * delta_ed: carga agregada del enlace e.

Funcion objetivo:
Minimizar:
Z = c * sum_{e in E} m_e

Restriccion de capacidad/utilizacion para cada enlace:
sum_{d in D} h_d * delta_ed <= u_max * C * m_e

Como C = 10 y u_max = 0.8:
L_e <= 8 * m_e

Restricciones de dominio:
m_e entero, 0 <= m_e <= 4, para todo e in E.

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
- L_AB = 4 + 5 + 9 + 6 = 24 Gbps (A->B, B->A, A->C, C->A).
- L_BC = 9 + 6 + 6 + 5 = 26 Gbps (A->C, C->A, B->C, C->B).
- L_CD = 7 + 6 = 13 Gbps (C->D, D->C).
- L_AD = 4 + 3 = 7 Gbps (A->D, D->A).
- L_BD = 8 + 5 = 13 Gbps (B->D, D->B).

Numero minimo de modulos:
m_e = ceil(L_e / 8)

Por tanto:
- m_AB = ceil(24 / 8) = 3 modulos.
- m_BC = ceil(26 / 8) = 4 modulos.
- m_CD = ceil(13 / 8) = 2 modulos.
- m_AD = ceil(7 / 8) = 1 modulo.
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
Z = 1 * (3 + 4 + 2 + 1 + 2) = 12 unidades.

Resultado final:
- AB: 3 modulos.
- BC: 4 modulos.
- CD: 2 modulos.
- AD: 1 modulo.
- BD: 2 modulos.
- Coste minimo total: 12 unidades.

c) Implementacion en Octave/Matlab

El problema tambien puede escribirse como el siguiente entero lineal:

minimizar c * 1^T m
sujeto a L <= 8 m
m entero
0 <= m <= 4

Como las rutas estan fijadas por R2 y cada restriccion solo depende del modulo del propio enlace, el optimo se obtiene enlace a enlace mediante:
m_e = ceil(L_e / 8)

Esto prueba la optimalidad de la solucion anterior: ningun enlace puede tener menos modulos que ceil(L_e / 8), y la solucion propuesta alcanza exactamente ese minimo en todos los enlaces.

Script Octave/Matlab completo:

```matlab
% Script completo para la pregunta 4
% Calcula cargas por enlace, modulos, capacidades, utilizaciones y coste.
clear; clc;

asignacion_opc = 'OPC1=T2, OPC2=M2, OPC3=R2, OPC4=D2';
enlaces = {'AB', 'BC', 'CD', 'AD', 'BD'};
origen = {'A', 'B', 'A', 'C', 'B', 'C', 'C', 'D', 'A', 'D', 'B', 'D'};
destino = {'B', 'A', 'C', 'A', 'C', 'B', 'D', 'C', 'D', 'A', 'D', 'B'};
h = [4, 5, 9, 6, 6, 5, 7, 6, 4, 3, 8, 5];     % Gbps por demanda
rutas = {
    {'AB'};
    {'AB'};
    {'AB', 'BC'};
    {'BC', 'AB'};
    {'BC'};
    {'BC'};
    {'CD'};
    {'CD'};
    {'AD'};
    {'AD'};
    {'BD'};
    {'BD'};
};

C_mod = 10;
u_max = 0.8;
coste_modulo = 1;
max_modulos = 4;

L = zeros(1, length(enlaces));
for d = 1:length(h)
    for r = 1:length(rutas{d})
        enlace_ruta = rutas{d}{r};
        idx = find(strcmp(enlaces, enlace_ruta));
        if isempty(idx)
            error('La demanda %d usa un enlace inexistente: %s', d, enlace_ruta);
        end
        L(idx) = L(idx) + h(d);
    end
end

m = ceil(L ./ (u_max * C_mod));
if any(m > max_modulos)
    error('La solucion requiere mas modulos de los permitidos');
end

capacidad = C_mod .* m;
utilizacion = zeros(size(L));
usados = capacidad > 0;
utilizacion(usados) = L(usados) ./ capacidad(usados);
coste_total = coste_modulo * sum(m);

fprintf('Asignacion de opciones: %s\n', asignacion_opc);
fprintf('Enlace  Carga(Gbps)  Modulos  Capacidad(Gbps)  Utilizacion\n');
for i = 1:length(enlaces)
    fprintf('%-6s %10.1f %8d %15.1f %12.3f\n', ...
        enlaces{i}, L(i), m(i), capacidad(i), utilizacion(i));
end
fprintf('Coste total = %.0f unidades\n', coste_total);

L_esperada = [24, 26, 13, 7, 13];
m_esperado = [3, 4, 2, 1, 2];
assert(all(abs(L - L_esperada) < 1e-9));
assert(all(m == m_esperado));
assert(all(utilizacion <= u_max + 1e-12));
```

La salida esperada del script es:
- m = [3, 4, 2, 1, 2].
- capacidad = [30, 40, 20, 10, 20] Gbps.
- utilizacion = [0.8, 0.65, 0.65, 0.7, 0.65].
- coste_total = 12.

============================================================

PREGUNTA: 