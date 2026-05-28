Cargando modelo de embeddings...
modules.json:   0% 0.00/387 [00:00<?, ?B/s]modules.json: 100% 387/387 [00:00<00:00, 695kB/s]
README.md: 0.00B [00:00, ?B/s]README.md: 179kB [00:00, 43.4MB/s]
sentence_bert_config.json:   0% 0.00/57.0 [00:00<?, ?B/s]sentence_bert_config.json: 100% 57.0/57.0 [00:00<00:00, 122kB/s]
config.json:   0% 0.00/694 [00:00<?, ?B/s]config.json: 100% 694/694 [00:00<00:00, 1.35MB/s]
model.safetensors:   0% 0.00/1.11G [00:00<?, ?B/s]model.safetensors:   6% 67.1M/1.11G [00:03<00:55, 19.0MB/s]model.safetensors:  72% 805M/1.11G [00:08<00:02, 109MB/s]  model.safetensors:  78% 872M/1.11G [00:08<00:02, 116MB/s]model.safetensors: 100% 1.11G/1.11G [00:08<00:00, 169MB/s]model.safetensors: 100% 1.11G/1.11G [00:11<00:00, 98.6MB/s]
Loading weights:   0% 0/199 [00:00<?, ?it/s]Loading weights: 100% 199/199 [00:00<00:00, 3135.03it/s]
tokenizer_config.json:   0% 0.00/418 [00:00<?, ?B/s]tokenizer_config.json: 100% 418/418 [00:00<00:00, 696kB/s]
sentencepiece.bpe.model:   0% 0.00/5.07M [00:00<?, ?B/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:00<00:00, 5.12MB/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:00<00:00, 5.11MB/s]
tokenizer.json:   0% 0.00/17.1M [00:00<?, ?B/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 45.1MB/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 45.0MB/s]
special_tokens_map.json:   0% 0.00/280 [00:00<?, ?B/s]special_tokens_map.json: 100% 280/280 [00:00<00:00, 461kB/s]
config.json:   0% 0.00/200 [00:00<?, ?B/s]config.json: 100% 200/200 [00:00<00:00, 337kB/s]
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

Como profesor experto en Diseño y Dimensionado de Redes (DDR), procedo a redactar el

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

El script .m debe:
1. Definir el vector de enlaces E = [AB, BC, CD, DA, AC].
2. Definir el vector de cargas L = [9, 19, 19, 8, 13].
3. Definir C = 10 y u_max = 0.85.
4. Calcular m = ceil(L / (u_max * C)).
5. Calcular capacidad = 10 * m.
6. Calcular utilizacion = L ./ capacidad.
7. Mostrar m, capacidad, utilizacion y coste total sum(m).

Como las rutas estan fijadas por R1 y la funcion objetivo minimiza la suma de modulos, la formula m_e = ceil(L_e / 8.5) produce directamente el optimo entero para este caso.

============================================================

PREGUNTA: exit
