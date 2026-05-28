Cargando modelo de embeddings...
modules.json:   0% 0.00/387 [00:00<?, ?B/s]modules.json: 100% 387/387 [00:00<00:00, 537kB/s]
README.md: 0.00B [00:00, ?B/s]README.md: 179kB [00:00, 36.7MB/s]
sentence_bert_config.json:   0% 0.00/57.0 [00:00<?, ?B/s]sentence_bert_config.json: 100% 57.0/57.0 [00:00<00:00, 80.0kB/s]
config.json:   0% 0.00/694 [00:00<?, ?B/s]config.json: 100% 694/694 [00:00<00:00, 1.03MB/s]
model.safetensors:   0% 0.00/1.11G [00:00<?, ?B/s]model.safetensors:  12% 134M/1.11G [00:03<00:22, 44.2MB/s]model.safetensors:  18% 201M/1.11G [00:03<00:14, 61.3MB/s]model.safetensors:  24% 268M/1.11G [00:05<00:19, 44.0MB/s]model.safetensors:  72% 805M/1.11G [00:07<00:02, 136MB/s] model.safetensors: 100% 1.11G/1.11G [00:09<00:00, 150MB/s]model.safetensors: 100% 1.11G/1.11G [00:12<00:00, 92.5MB/s]
Loading weights:   0% 0/199 [00:00<?, ?it/s]Loading weights: 100% 199/199 [00:00<00:00, 3576.30it/s]
tokenizer_config.json:   0% 0.00/418 [00:00<?, ?B/s]tokenizer_config.json: 100% 418/418 [00:00<00:00, 674kB/s]
sentencepiece.bpe.model:   0% 0.00/5.07M [00:00<?, ?B/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:00<00:00, 5.30MB/s]sentencepiece.bpe.model: 100% 5.07M/5.07M [00:00<00:00, 5.30MB/s]
tokenizer.json:   0% 0.00/17.1M [00:00<?, ?B/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 22.8MB/s]tokenizer.json: 100% 17.1M/17.1M [00:00<00:00, 22.8MB/s]
special_tokens_map.json:   0% 0.00/280 [00:00<?, ?B/s]special_tokens_map.json: 100% 280/280 [00:00<00:00, 410kB/s]
config.json:   0% 0.00/200 [00:00<?, ?B/s]config.json: 100% 200/200 [00:00<00:00, 405kB/s]
RAG listo
- Vector DB: /app/chroma_ddr
- Embeddings: intfloat/multilingual-e5-base
- LLM provider: ollama
- Ollama model: mistral:7b
Escribe una pregunta y pulsa Enter. Escribe 'exit' para salir.

PREGUNTA: Genera un examen nuevo de DDR junto con el solucionario completo. Debe seguir el estilo de los examenes de convocatorias anteriores, tener 4 preguntas, incluir un ejercicio practico final con OPC y entregar una solucion razonada de cada pregunta.
[*] Recuperando contexto de la base de datos...
[DEBUG] Iniciando retrieve_context...
[DEBUG] Consulta de examen detectada: True
[+] Contexto recuperado
[*] Generando respuesta...

RESPUESTA:

 EXAMEN
-----------------------
1. (0,5 ptos) Investiga la empresa antes de la entrevista con el cliente.
2. Siguientes entrevistas
3. (0,5 ptos) Discuta el direccionamiento estático frente al dinámico
4. (2 ptos) A partir de la topologia de la Figura 1 y contemplando las siguientes consideraciones:
   - Los enlaces entre nodos A y B, C y D no pueden ser utilizados.
   - El módulo en el nodo E debe tener una capacidad mínima de 20 Gbps.
   - La red debe minimizar el coste OPEX/CAPEX.

Disena la red incluyendo:
   a) La formulación matemática abstracta, indicando número de variables de cada tipo y número de restricciones de cada tipo para la topología de abajo, asi como las entradas y salidas, siguiendo los ejemplos vistos en clase. (1 pto)
   b) Especificar de forma concreta las restricciones de igualdad/desigualdad concretas o discutir una modificación puntual de la formulación. (0.5 ptos)
   c) Realice la solución programada en Octave, entregando tanto script como solución en el enlace habilitado para tal efecto. En la respuesta especifique explícitamente la asignación de las opciones y el resultado en términos del número de módulos o decisión de diseño. (0.5 ptos)

SOLUCIONARIO
-----------------------
1. Antes de la entrevista con el cliente, investiga la empresa para obtener información sobre su historia, productos y servicios, estructura organizacional, mercado y competidores. Esto te permitirá entender mejor las necesidades y expectativas del cliente y prepararte para ofrecer una solución adecuada.
2. Siguientes entrevistas: Durante las siguientes etapas de la relación con el cliente, es importante mantener un diálogo abierto y constructivo, compartir información relevante sobre los avances en el proyecto y responder a cualquier pregunta o duda que tenga el cliente. Además, es importante seguir investigando la empresa para estar al tanto de cualquier cambio en su situación y adaptar la solución ofrecida según sea necesario.
3. (0,5 ptos) Direccionamiento estático frente al dinámico: El direccionamiento estático es un método en el que los dispositivos de red se configuran con direcciones IP fijas y no pueden cambiar sin una intervención manual. Por otro lado, el direccionamiento dinámico permite que los dispositivos obtengan automáticamente direcciones IP a partir de un servidor DHCP. El uso del direccionamiento estático es más apropiado en redes pequeñas y controladas, mientras que el direccionamiento dinámico es más útil en redes grandes y dinámicas.
4. A partir de la topología de la Figura 1 y contemplando las siguientes consideraciones:
   - Los enlaces entre nodos A y B, C y D no pueden ser utilizados.
   - El módulo en el nodo E debe tener una capacidad mínima de 20 Gbps.
   - La red debe minimizar el coste OPEX/CAPEX.

Disena la red incluyendo:
   a) La formulación matemática abstracta es un problema de optimización lineal con variables binarias, donde cada variable representa si se utiliza o no un módulo en cada nodo. Las restricciones incluyen las capacidades de los enlaces y el requisito de que el módulo en el nodo E tenga una capacidad mínima de 20 Gbps. La función objetivo es minimizar el coste OPEX/CAPEX, que puede ser representado por una matriz de costes de cada módulo.
   b) Las restricciones concretas son:
      - El enlace entre nodos A y B no se utiliza (x1 = 0).
      - El enlace entre nodos C y D no se utiliza (x2 = 0).
      - El módulo en el nodo E tiene una capacidad mínima de 20 Gbps (y5 >= 20).
   c) La solución programada en Octave puede ser realizada utilizando la función linprog, que resuelve problemas de optimización lineal. El script incluye la definición de las variables, restricciones y función objetivo, así como la llamada a la función linprog para obtener la solución. La asignación de las opciones es AABD, donde A representa la topología, B la matriz de tráfico, C el tipo de formulación y D los costes/robustez/parametros adicionales. El resultado esperado es un número de módulos que minimice el coste OPEX/CAPEX y cumpla con las restricciones especificadas.

============================================================

PREGUNTA: exit
