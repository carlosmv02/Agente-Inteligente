Cargando modelo de embeddings...
modules.json:   0% 0.00/387 [00:00<?, ?B/s]modules.json: 100% 387/387 [00:00<00:00, 578kB/s]
README.md: 0.00B [00:00, ?B/s]README.md: 179kB [00:00, 38.7MB/s]
sentence_bert_config.json:   0% 0.00/57.0 [00:00<?, ?B/s]sentence_bert_config.json: 100% 57.0/57.0 [00:00<00:00, 82.4kB/s]
config.json:   0% 0.00/694 [00:00<?, ?B/s]config.json: 100% 694/694 [00:00<00:00, 1.20MB/s]
model.safetensors:   0% 0.00/1.11G [00:00<?, ?B/s]model.safetensors:  12% 134M/1.11G [00:03<00:23, 40.8MB/s]model.safetensors:  24% 268M/1.11G [00:03<00:10, 81.4MB/s]model.safetensors:  30% 335M/1.11G [00:04<00:10, 76.5MB/s]model.safetensors:  42% 469M/1.11G [00:06<00:07, 82.0MB/s]model.safetensors:  72% 805M/1.11G [00:07<00:01, 154MB/s] model.safetensors:  78% 872M/1.11G [00:08<00:01, 139MB/s]model.safetensors:  96% 1.07G/1.11G [00:08<00:00, 187MB/s]model.safetensors: 100% 1.11G/1.11G [00:08<00:00, 184MB/s]model.safetensors: 100% 1.11G/1.11G [00:11<00:00, 97.8MB/s]
Loading weights:   0% 0/199 [00:00<?, ?it/s]Loading weights: 100% 199/199 [00:00<00:00, 3614.79it/s]
tokenizer_config.json:   0% 0.00/418 [00:00<?, ?B/s]tokenizer_config.json: 100% 418/418 [00:00<00:00, 674kB/s]
sentencepiece.bpe.model:   0% 0.00/5.07M [00:00<?, ?B/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:00<00:00, 5.57MB/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:00<00:00, 5.57MB/s]
tokenizer.json:   0% 0.00/17.1M [00:00<?, ?B/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 23.9MB/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 23.9MB/s]
special_tokens_map.json:   0% 0.00/280 [00:00<?, ?B/s]special_tokens_map.json: 100% 280/280 [00:00<00:00, 453kB/s]
config.json:   0% 0.00/200 [00:00<?, ?B/s]config.json: 100% 200/200 [00:00<00:00, 408kB/s]
RAG listo
- Vector DB: /app/chroma_ddr
- Embeddings: intfloat/multilingual-e5-base
- LLM provider: openai
- OpenAI model: gpt-5-mini
Escribe una pregunta y pulsa Enter. Escribe 'exit' para salir.

PREGUNTA: Genera un examen nuevo de DDR junto con el solucionario completo. Debe seguir el estilo de los examenes de convocatorias anteriores, tener 4 preguntas, incluir un ejercicio practico final con OPC y entregar una solucion razonada de cada pregunta.
[*] Recuperando contexto de la base de datos...
[DEBUG] Iniciando retrieve_context...
[DEBUG] Consulta de examen detectada: True
[+] Contexto recuperado
[*] Generando respuesta...

RESPUESTA:

EXAMEN

1. (0.5 pt) Explique brevemente las ventajas e inconvenientes del direccionamiento IP estático frente al dinámico (DHCP) en el contexto de una red de campus universitario que aloja aulas, laboratorios y oficinas administrativas. En su respuesta considere aspectos de escalabilidad, seguridad, gestión y tolerancia a fallos.

2. (0.5 pt) En el diseño de redes, ¿qué diferencias principales hay entre aplicar Teoría de Colas y aplicar Optimización de Red? Para cada caso indique un ejemplo de problema típico donde aquella técnica es preferible y por qué.

3. (1.0 pt) Describa las consideraciones principales al diseñar una política de enrutamiento (routing) para una red autónoma que debe soportar telemetría en tiempo real y cargas M2M (Machine-to-Machine). Incluya brevemente el papel de controladores y la necesidad de automatización/telemetría en la toma de decisiones de enrutamiento.

4. (2.0 pt) A partir de la topología de la Figura 1 y contemplando las siguientes consideraciones:

- Solo se permiten enlaces entre nodos adyacentes indicados en la figura; no está permitida la creación de enlaces adicionales.
- Cada enlace puede equiparse con módulos de capacidad de 10 Gbps; cada nodo puede instalar hasta 4 módulos por interfaz.
- Coste por módulo: CAPEX = 1.000 €; coste operativo proporcional a utilización: OPEX anual = 100 € por módulo multiplicado por la fracción de utilización media.
- Se exige robustez frente a la pérdida de un enlace: el diseño debe garantizar que, ante la falla de cualquier único enlace, el tráfico total redirigido no exceda la capacidad instalada en ningún enlace (reserva para protección tipo 1+1 no requerida, pero rutas alternativas posibles).

Disene la red minimizando CAPEX+OPEX esperado, incluyendo:

a) La formulacion matematica abstracta (programación entera mixta), indicando número de variables de cada tipo y número de restricciones de cada tipo para la topologia de la Figura 1, así como las entradas y salidas. (1 pto)

b) Especificar de forma concreta las restricciones de igualdad/desigualdad principales aplicadas al problema y discutir una posible modificación puntual de la formulación para penalizar alta utilización. (0.5 pt)

c) Realice la solucion programada en octave/matlab, entregando tanto script (.m) como solución en el enlace habilitado para tal efecto. En la respuesta especifique explícitamente la asignación de las opciones y el resultado en términos del número de módulos por enlace y coste total estimado. (0.5 pt)

Si se usan opciones, deben aparecer como:

- OPC 1: Topología: elegir entre A o B (ver abajo)
- OPC 2: Matriz de tráfico: conjunto de dos alternativas (T1, T2)
- OPC 3: Tipo de formulación: [Minimizar CAPEX+OPEX con protección por rerouting]

Figura 1 (topologías disponibles):

Topología A: cuatro nodos en anillo (1—2—3—4—1) y diagonales entre 1–3 y 2–4 permitidas.
Topología B: cinco nodos en línea con un hub central: 1—2—3—4—5 y adicional 3—6 (donde 6 es un servidor regional).

Matriz de tráfico (Gbps) opciones:

T1 (para A): origen-destino (symmetric) demandas (Gbps): 1↔2: 8, 1↔3: 12, 1↔4: 6, 2↔3: 10, 2↔4: 4, 3↔4: 9.
T2 (para B): flows towards hub 3: 1→3: 6, 2→3: 10, 4→3: 8, 5→3: 5, 6↔3: 20 (symmetric where appropriate).

OPC 3: Formulación: Minimización de CAPEX+OPEX con rerouting tras falla (programación entera mixta).

SOLUCIONARIO

1. (0.5 pt) Respuesta

Ventajas del direccionamiento estático:
- Control preciso de asignaciones IP: facilita reglas basadas en IP, segmentación y auditoría.
- Predecible para servicios que requieren IP fija (servidores, impresoras).
Inconvenientes:
- Mala escalabilidad: gestión manual costosa en redes grandes.
- Mayor propensión a errores humanos y conflictos de direcciones.
- Dificultad para movilidad y cambios frecuentes (dispositivos móviles, BYOD).

Ventajas del direccionamiento dinámico (DHCP):
- Escalable y automatizable: asigna IPs sin intervención manual.
- Facilita movilidad y reutilización eficiente del espacio de direcciones.
- Integración con control de acceso (DHCP snooping, asignación basada en políticas).
Inconvenientes:
- Menor control directo sobre IPs para elementos críticos (aunque pueden reservarse).
- Dependencia del servidor DHCP (necesidad de alta disponibilidad).
- Riesgos de seguridad si no se implementa autenticación/filtrado (p. ej. DHCP spoofing).

Conclusión aplicada a la red de campus:
- Uso híbrido: DHCP para usuarios finales y laboratorios; estático o reservas DHCP para infraestructuras críticas (servidores, equipos de red, servicios administrativos). Implementar alta disponibilidad del/los servidores DHCP y medidas de seguridad (snooping, ACLs).

2. (0.5 pt) Respuesta

Teoría de Colas:
- Enfocada a modelar comportamiento temporal de solicitudes (colas, servicio, tiempos de espera, utilización).
- Aplicable cuando interesa latencia, pérdida o retardo, y hay aleatoriedad en llegadas/servicio.
- Ejemplo típico: dimensionar capacidad de un enlace único dedicado a un servicio (ej. enlace de acceso a Internet) para garantizar retardo medio y probabilidad de pérdida aceptable: se modela como M/M/1 o M/G/1 según supuesto.

Optimización de Red:
- Enfocada a asignación de recursos estáticos/planificación (ruteo, capacidad, ubicación de servidores) minimizando coste o maximizando rendimiento sujeto a restricciones de capacidad.
- Ejemplo típico: diseño de la capacidad de una red troncal con múltiples enlaces y rutas, minimizando CAPEX dado un conjunto de demandas: se usa programación lineal/entera.

Diferencia clave: teoría de colas es estocástica y temporal para métricas de desempeño; optimización de red es determinista/estructural para asignación de recursos y dimensionado.

3. (1.0 pt) Respuesta

Consideraciones principales para política de enrutamiento en red autónoma con telemetría y M2M:

- Requisitos de QoS: telemetría y M2M suelen necesitar baja latencia y alta disponibilidad; priorización y clasificación de tráfico (DiffServ) deben integrarse con decisiones de ruteo.
- Rutas determinísticas vs adaptativas: para telemetría crítica puede preferirse paths reservados o segment routing con garantías; para carga M2M masiva conviene balanceo activo y control centralizado.
- Papel de controladores (SDN): un controlador central (o distribuido) permite visibilidad global, cálculo de rutas optimizadas según telemetría (latencia actual, congestión). Debe soportar políticas de intento/rollback y evitar flapping.
- Automatización y telemetría: closed-loop: telemetría recoge métricas (utilización, latencia, errores) y el controlador reajusta rutas o capacidades automáticamente. Es esencial la calidad y frecuencia de telemetría (tradeoff overhead vs reacción).
- Resiliencia y consistencia: la automatización debe considerar consistencia transaccional al desplegar cambios de ruteo para evitar bucles o pérdidas transitorias.
- Seguridad y aislamiento: asegurar que el control automatizado esté autenticado/firmado; políticas de acceso para evitar cambios no autorizados.
- Escalabilidad: diseño jerárquico del control (controladores locales y globales) para reducir latencias de decisión y sobrecarga.

Resumen: integrar políticas estáticas para tráfico crítico y políticas dinámicas basadas en telemetría para el resto, usando controladores SDN con mecanismo de fallback y suficientes medidas de seguridad y observabilidad.

4. (2.0 pt) Solución (se sigue la plantilla; OPCs seleccionados abajo)

Selección de opciones para este solucionario: OPC 1 = A (topología en anillo con diagonales), OPC 2 = T1 (matriz de tráfico para A), OPC 3 = Minimización CAPEX+OPEX con rerouting.

a) Formulación matemática abstracta (Programación Entera Mixta, MIP). (1 pto)

Datos / Entradas:
- G = (V,E): topología A con V = {1,2,3,4}, E = { (1,2),(2,3),(3,4),(4,1),(1,3),(2,4) }.
- Demanda d_{ij} (Gbps) para pares i<j, simétrica según T1: d_{12}=8, d_{13}=12, d_{14}=6, d_{23}=10, d_{24}=4, d_{34}=9.
- Capacidad por módulo: C_mod = 10 Gbps.
- Coste CAPEX por módulo: c_cap = 1000 €.
- Coste OPEX anual por módulo: c_opex_unit = 100 € * utilización_media (fracción).
- Restricción de módulos por interfaz: m_max = 4 (capacidad máxima por enlace = 4 * C_mod = 40 Gbps).
- Protección: ante falla de cualquier único enlace, el rerouting del tráfico no debe exceder capacidad instalada en ningún enlace.

Variables:
- Integer variables m_e ∈ Z_{\ge 0}, para cada enlace e ∈ E: número de módulos instalados en enlace e.
  (Tipo entero; dominio 0..4).
  Número de variables de este tipo: |E| = 6.
- Continuous flow variables f_{ij}^{e} ≥ 0: flujo (Gbps) del par origen-destino (i→j y j→i) que utiliza enlace e en la solución nominal (sin fallo). Podemos modelar solo un sentido y multiplicar por 2 si simétrico, pero tomaremos pares i<j y rutas arbitrarias: para cada demand pair (p) y cada enlace e definimos f_{p,e} ≥ 0. Número de pares P = 6, por tanto variables de flujo nominal: P * |E| = 36 continuas.
- Auxiliary variables u_e ∈ [0,1]: utilización media del enlace e = (total_flow_on_e) / (m_e * C_mod) (se contabiliza en OPEX). Número: |E| = 6.
- Variables de flujo en escenario de fallo: f_{p,e}^{(k)} ≥ 0 para cada demanda p y cada enlace e bajo la consideración de falla del enlace k ∈ E. Estas variables modelan rerouting en cada single-link-failure escenario. Número aproximado: P * |E| * |E| = 6*6*6 = 216 (aunque para enlace k we may exclude flows over failed link). Estas son continuas.

Función objetivo:
Minimizar coste total anualizado:
Min Z = sum_{e∈E} ( c_cap * m_e ) + sum_{e∈E} c_opex_unit * u_e * m_e
donde utilización u_e = (sum_p f_{p,e}) / (m_e * C_mod), care con m_e=0: se fuerza u_e=0 si m_e=0 mediante restricciones.

Para evaluación práctica, se puede aproximar OPEX computando utilización por enlace con flujos nominales.

Restricciones principales:
1) Capacidad nominal por enlace:
for all e: sum_p f_{p,e} ≤ m_e * C_mod
Número: |E| = 6 desigualdades.

2) Flujo conserva para cada demanda p and node v (balance de flujo) en escenario nominal:
for each demand pair (s,t) and for each node v:
sum_{e out of v} f_{p,e} - sum_{e into v} f_{p,e} = b_{p,v}
donde b_{p,v} = +d_p si v = s; -d_p si v = t; 0 otherwise.
Número de ecuaciones: P * |V| = 6 * 4 = 24 igualdades.

3) Capacidad bajo fallo de enlace k (resiliencia):
Para every failed link k, for all e != k:
sum_p f_{p,e}^{(k)} ≤ m_e * C_mod
Además, flows cannot traverse failed link:
for all p: f_{p,k}^{(k)} = 0
Número: |E|*(|E|-1) desigualdades ≈ 6*5 = 30 per scenario aggregated; total set across all scenarios.

4) Balance de flujo en fallo scenario k:
for each demand p and node v, with traffic must still be routed (single-path not required; split allowed):
sum_{e out of v} f_{p,e}^{(k)} - sum_{e into v} f_{p,e}^{(k)} = b_{p,v}
Number: P * |V| * |E| equations nominally (but many redundant); effectively 6*4*6 = 144 equalities.

5) Link-use consistency: relation between nominal flows and utilization variables u_e:
u_e ≥ (sum_p f_{p,e}) / (m_e * C_mod) if m_e≥1; and u_e = 0 if m_e=0.
These are nonlinear; to linearize, enforce:
sum_p f_{p,e} ≤ u_e * m_e * C_mod
and u_e ≤ 1, u_e ≥ 0.
Number: |E| constraints.

6) Bounds on modules:
for all e: 0 ≤ m_e ≤ m_max, integer.
Number: |E| bounds.

Salidas esperadas:
- Valores m_e por cada enlace e (nº de módulos).
- Flujos f_{p,e} nominales.
- Coste CAPEX y OPEX estimado y utilización por enlace.
- Verificación de capacidad en todos los escenarios de fallo.

Resumen de recuento (aproximado):
- Variables enteras: 6 (m_e).
- Variables continuas: nominal flows 36 + utilizations 6 + fallback flows ~ 180 (reducción posible) ≈ ~222.
- Restricciones: ≈ 6 (capacities) + 24 (balances) + ~144 (fail balances) + 30 (fail capacities) + 6 (utilization linking) ≈ ~210 restricciones. (Números aproximados; se debe indicar en la entrega exacta según implementación).

b) Restricciones concretas y modificación puntual. (0.5 pt)

Restricciones concretas principales (expresadas como desigualdades/igualdades):

- Capacidad nominal por enlace e:
sum_{p} f_{p,e} ≤ 10 * m_e, ∀ e ∈ E.

- Balance de flujo (nominal) para demanda p=(s,t), en nodo v:
sum_{e∈δ^+(v)} f_{p,e} - sum_{e∈δ^-(v)} f_{p,e} = 
  { +d_p, if v=s; -d_p, if v=t; 0, else }.

- Capacidad en fallo k, para e ≠ k:
sum_{p} f_{p,e}^{(k)} ≤ 10 * m_e, ∀ e ≠ k.

- No uso del enlace fallado:
f_{p,k}^{(k)} = 0, ∀ p.

- Límite de módulos por enlace:
0 ≤ m_e ≤ 4, m_e ∈ Z.

- Definición de utilización:
sum_p f_{p,e} ≤ u_e * m_e * 10, ∀ e;
0 ≤ u_e ≤ 1.

Modificación puntual para penalizar alta utilización:
- Añadir término al objetivo que penalice utilizaciones críticas, p. ej. añadir α * sum_e (u_e)^2 * m_e para penalización convexa (no-lineal). Si se requiere mantener linealidad, añadir penalización lineal pesada para u_e superior a umbral u_thresh: introducir variable slack s_e ≥ 0 y restricciones s_e ≥ sum_p f_{p,e} - u_thresh * m_e * 10; penalizar s_e en objetivo con coste elevado β. Esto fuerza diseño con menor chance de congestión.

Discusión: la inclusión de penalización por utilización reduce OPEX pero puede incrementar CAPEX; su magnitud α/β decide tradeoff.

c) Solución programada en octave/matlab y resultado esperado (metodología y resultado). (0.5 pt)

Indicaciones para el script .m (entrega requerida):
- Implementar datos de G, demandas d_p.
- Variables: enteras m_e (use intlinprog o solver MIP disponible), continuas f_{p,e} y f_{p,e}^{(k)} (modelar todo en una sola MIP).
- Construir la matriz de restricciones conforme a apartado (a) y vector coste con componentes CAPEX y OPEX aproximado (puede linealizar OPEX usando u_e y sum_p f_{p,e} ≤ u_e * m_e * 10).
- Forzar m_e upper bounds 4.
- Resolver con intlinprog (o glpk if available).
- Tras obtener m_e, calcular utilización u_e = sum_p f_{p,e} / (m_e * 10) (definir 0 si m_e=0).
- Comprobar para cada fallo k que existan variables de rerouting f^{(k)} que satisfacen demandas y capacidades; si la MIP incluyó escenarios de fallo, estarán garantizadas; si no, realizar re-routing probado con un LP para cada fallo con m_e fijos.

Elección concreta y resultado razonado (OPC asignadas):
- OPC 1: Topología A.
- OPC 2: Matriz T1.
- OPC 3: Formulación MIP minimizar CAPEX+OPEX con rerouting.

Resultado esperado razonado (estimación, no cálculo exacto sin ejecutar el solver):
- Calculemos la demanda total agregada que atraviesa enlaces para estimar módulos requeridos:
  El tráfico entre nodos se distribuye por rutas posiblemente balanceadas. En topología A con diagonales, muchos destinos tomarán caminos cortos. Suma de todas demandas (considerando ambas direcciones) = 2 * (8+12+6+10+4+9) = 2*49 = 98 Gbps totales bidireccionales. En steady-state los enlaces compartirán ese tráfico; máximo acumulado por enlace probablemente alrededor de ~30 Gbps en el peor caso si muchos pares atraviesan el mismo enlace.

- Dado módulos de 10 Gbps y límite 4 módulos (40 Gbps), es plausible que m_e = 3 en uno o dos enlaces (capacidad 30 Gbps) y m_e = 2 en otros, para acomodar 98 Gbps total con redomento y redundancia para fallos. Estimación de configuración posible:
  Ejemplo factible (estimado): m_(1,2)=3, m_(2,3)=3, m_(3,4)=2, m_(4,1)=2, m_(1,3)=2, m_(2,4)=2.
  Esto da capacidades: 30,30,20,20,20,20 → suma capacidad instalada = 140 Gbps (bidireccional sumada por enlaces).
- CAPEX estimado = 11 módulos * 1000 € = 11.000 €.
  (Aquí, total módulos = 3+3+2+2+2+2 =14; CAPEX = 14.000 €; mixta estimación depende de asignación final.)
- OPEX estimado: suponer utilización media global ~ 98/140 ≈ 0.7 → OPEX anual ≈ 100 € * 14 * 0.7 = 980 €.

Verificación de robustez:
- Con fallo de un enlace, el tráfico se rerutea por caminos alternativos; dado que capacidad instalada por enlace máxima llega a 30-20 Gbps, debemos comprobar que la carga adicional sobre cualquier enlace tras rerouting no supere su capacidad. En el ejemplo, los enlaces con 30 Gbps tienen margen 10 Gbps antes de saturar (capacidad 30). Si rerouting de una caída añade más de 10 Gbps a uno de estos enlaces, la solución no sería válida; por eso en la MIP se impone la restricción explícita de capacidad en escenarios de fallo.

Conclusión y entregables:
- El estudiante debe entregar un script .m que implemente la MIP anteriormente descrita para OPCs seleccionadas (A, T1, formulation MIP) y que devuelva m_e por enlace, flujos nominales y valores de coste CAPEX y OPEX, más comprobación de todos escenarios de fallo.
- El solucionario presente da la metodología y una estimación razonada; el cálculo numérico exacto requiere ejecutar el solver MIP con los datos concretos y producir el vector m_e final y los costes. Si el solver devuelve por ejemplo m = [3,3,2,2,2,2] (orden según E), entonces:
  - Número módulos = 14; CAPEX = 14.000 €.
  - Calcule flujos y utilizaciones según salida del solver; OPEX anual ≈ 100 € * sum_e m_e * u_e.
- En la entrega se debe indicar explícitamente: OPC 1 = A; OPC 2 = T1; OPC 3 = Minimización CAPEX+OPEX con rerouting. Adjuntar archivo .m y un fichero de resultados con m_e y comprobación de capacidad en todos los escenarios de fallo.

Nota final: si no hay información suficiente para obtener un único vector m_e exacto sin ejecutar el solver, la solución metodológica anterior es evaluable: definición de variables, objetivo, restricciones y la estrategia de resolución con MIP y verificación por escenarios.

============================================================

PREGUNTA: exit
