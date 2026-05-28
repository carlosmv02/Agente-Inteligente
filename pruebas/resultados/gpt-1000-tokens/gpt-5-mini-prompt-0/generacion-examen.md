RAG listo
- Vector DB: /app/chroma_ddr
- Embeddings: intfloat/multilingual-e5-base
- LLM provider: openai
- OpenAI model: gpt-5-mini
Escribe una pregunta y pulsa Enter. Escribe 'exit' para salir.

PREGUNTA: generame un examen del estilo de examenes de convocatorias anteriores
                                                                               [*] Recuperando contexto de la base de datos...
[DEBUG] Iniciando retrieve_context...
[DEBUG] Consulta de examen detectada: True
[+] Contexto recuperado
[*] Generando respuesta...

RESPUESTA:

UNIVERSIDAD DE GRANADA
Diseño y Dimensionado de Redes (DDR) — Convocatoria: Febrero 2026
Duración: 90 minutos
Nombre, Apellidos y DNI: _______________________________________

1. (0,5 ptos) Explique brevemente las diferencias principales entre direccionamiento IP estático y dinámico (DHCP). En su respuesta indique dos ventajas y dos inconvenientes prácticos de cada enfoque en el contexto de una red empresarial. (Respuesta concisa)

2. (1 ptos) Se dispone de una red con varios enlaces susceptibles de congestión. Defina y compare de forma breve (máx. 10 líneas cada uno) los siguientes criterios de optimización empleados en dimensionado de redes: minimización de coste CAPEX total, minimización de la máxima utilización de enlace (min-max link utilization), y diseño para robustez frente a fallos de enlace. Indique un escenario práctico donde cada criterio sea el más adecuado.

3. (0,5 ptos) Indique qué técnica analítica o de optimización (p. ej. teoría de colas, optimización lineal entera, Diseño de Experimentos, simulación de eventos discretos) es la más adecuada para cada uno de los siguientes problemas y justifique en una frase:
a) Dimensionar el número de servidores front-end para minimizar la latencia percibida por usuarios, pudiendo ensayar distintas configuraciones en laboratorio.
b) Calcular la capacidad mínima de un nuevo enlace intercontinental sin posibilidad de pruebas en red real, con requisitos de QoS para distintos niveles de tráfico.
c) Re-diseñar las capacidades de los enlaces en una red existente con series temporales de tráfico monitorizado durante varios años.

4. (2 ptos) A partir de la topologia de la Figura 1 y contemplando las siguientes consideraciones:

- Solo están permitidos enlaces directos entre nodos adyacentes según la Figura 1; no se permiten enlaces adicionales entre nodos no representados en la figura.
- Los enlaces se implementan mediante módulos de 10 Gbps; cada enlace puede equiparse con un número entero de módulos (0,1,2,...). Cada módulo tiene coste CAPEX unitario distinto según el tipo (ver OPC 4).
- Objetivo: minimizar CAPEX total sujeto a que la utilización máxima de cualquier enlace no supere 85% bajo las rutas de enrutamiento de menor número de saltos y considerando protección 1+1 (tráfico duplicado por un camino alternativo en caso de fallo de enlace).
- Además, al menos dos nodos de la topología deben quedar conectados por rutas con disponibilidad calculada ≥ 99.95% en el diseño final (considere disponibilidad por módulo y por enlace según OPC 4).

Disene la red [objetivo: minimo coste CAPEX con protección y restricción de utilización] incluyendo:

a) La formulacion matematica abstracta [programación lineal entera mixta (MILP) con variables enteras para módulos y variables continuas para flujos], indicando numero de variables de cada tipo y numero de restricciones de cada tipo para la topologia de abajo, asi como las entradas y salidas, siguiendo los ejemplos vistos en clase. (1 pto)

b) Especificar de forma concreta las restricciones de igualdad/desigualdad siguientes o discutir una modificacion puntual de la formulacion:
   - capacidad enlace >= suma de flujos asignados (incluyendo duplicado por protección) para cada enlace,
   - utilización enlace = flujo/capacidad <= 0.85,
   - variables de módulos enteras y capacidad calculada como 10 Gbps × nº módulos,
   - disponibilidad de ruta calculada a partir de disponibilidades de enlaces (asuma independencia) y requisito >= 99.95% para al menos el par de nodos especificado. (0.5 ptos)

c) Realice la solucion programada en octave/matlab, entregando tanto script como solucion en el enlace habilitado para tal efecto. En la respuesta especifique explicitamente la asignacion de las opciones y el resultado en terminos del numero de modulos o decision de diseno. (0.5 ptos)

Figura 1: Topología (nodos y enlaces)
- Nodos: A, B, C, D, E (cinco nodos)
- Enlaces (bidireccionales, sin enlaces adicionales permitidos): A–B, A–C, B–C, B–D, C–E, D–E

OPCIONES (deben aparecer en la respuesta entregada por el alumno tal cual):

- OPC 1: Topologia seleccionada: A (usar la Figura 1 dada)
- OPC 2: Matriz de tráfico (Gbps) entre pares demanda origine→destino (sólo mostrar demandas origen≠destino; el tráfico no es simétrico). Seleccione UNA de las siguientes matrices y indique explícitamente la elección:
  A) [A→B:2, A→C:1, A→D:0.5, A→E:1.5; B→A:1, B→C:0.5, B→D:2, B→E:0.5; C→A:0.5, C→B:0.5, C→D:0.5, C→E:3; D→A:0.2, D→B:1.5, D→C:0.3, D→E:1; E→A:1, E→B:0.2, E→C:0.8, E→D:0.1]
  B) [A→B:3, A→C:2, A→D:1, A→E:2; B→A:2, B→C:1, B→D:3, B→E:1; C→A:1, C→B:1, C→D:1, C→E:4; D→A:0.5, D→B:2, D→C:0.5, D→E:1.5; E→A:1.5, E→B:0.5, E→C:1, E→D:0.2]
  C) [A→B:1, A→C:0.5, A→D:0.2, A→E:0.8; B→A:0.8, B→C:0.3, B→D:1, B→E:0.3; C→A:0.4, C→B:0.4, C→D:0.4, C→E:2; D→A:0.1, D→B:0.7, D→C:0.2, D→E:0.5; E→A:0.6, E→B:0.2, E→C:0.5, E→D:0.1]

- OPC 3: Tipo de formulacion/capacidades (seleccione UNA):
  A) Modulos homogéneos de 10 Gbps, ilimitados por enlace (enteros).
  B) Modulos de 10 Gbps o 40 Gbps; 40 Gbps equivale a 4×10 Gbps pero con descuento en coste (ver OPC 4).
  C) Modulos de 10 Gbps y posibilidad de multiplexación estadística modelada por factor de overbooking α (indicar α en la entrega).

- OPC 4: Costes y disponibilidades (seleccione UNA configuración de costes/disponibilidades):
  A) Costes: 10 Gbps módulo = 1.0 u; Disponibilidad por módulo = 0.9999; coste de mantenimiento OPEX despreciable.
  B) Costes: 10 Gbps módulo = 1.0 u; 40 Gbps módulo = 3.6 u; Disponibilidad por 10G módulo = 0.9998; por 40G módulo = 0.99995; mantenimiento anual 0.05 u por módulo (puede incluirse en objetivo).
  C) Costes: 10 Gbps módulo = 1.2 u; Disponibilidad por módulo = 0.99995; penalización por utilización >75% = coste adicional proporcional (detallar en la entrega).

Instrucciones finales:
- En la entrega del ejercicio 4 indique explícitamente: OPC 1, OPC 2, OPC 3 y OPC 4 escogidas (p. ej. OPC 1:A, OPC 2:B, OPC 3:B, OPC 4:A).
- Entregue el script .m con la formulación MILP y el fichero de resultados (salida numérica) en el enlace habilitado; en el examen escrito indique de forma clara el número de módulos por enlace resultante y la comprobación de las restricciones (utilizaciones, disponibilidad). No incluya código en el examen teórico que se evalúe aquí.
