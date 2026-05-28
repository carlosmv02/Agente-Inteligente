# Evaluacion RAG

## Resumen

- **num_questions**: 24
- **configured_llm_provider**: ollama
- **configured_llm_model**: qwen3:4b
- **top_k**: 6
- **use_testset_hints**: True
- **attach_page_context**: True
- **generation_max_tokens**: 1200
- **result_llm_providers**: ['ollama']
- **result_llm_models**: ['qwen3:4b']
- **wall_time_s**: 9441.394
- **recorded_pipeline_time_s**: 9441.374
- **avg_time_per_response_s**: 393.391
- **avg_retrieval_time_s**: 0.2685
- **avg_generation_time_s**: 393.1217
- **avg_answer_ground_truth_similarity**: 0.0754
- **avg_answer_context_similarity**: 0.0724
- **avg_ground_truth_context_similarity**: 0.822
- **avg_same_tema_ratio**: 1.0
- **avg_same_pdf_ratio**: 0.993
- **same_page_hit_rate**: 0.958
- **insufficient_context_answers**: 0
- **insufficient_context_rate**: 0.0
- **avg_context_count**: 7.2083
- **avg_context_chars**: 4399.6667
- **avg_answer_words**: 8.6667
- **avg_prompt_tokens_ollama**: 2488.125
- **avg_completion_tokens_ollama**: 1186.4583
- **avg_ollama_total_duration_s**: 393.0986
- **avg_input_tokens_openai**: None
- **avg_output_tokens_openai**: None
- **avg_total_tokens_openai**: None
- **avg_cpu_user_delta_s**: 1.8854
- **avg_cpu_system_delta_s**: 0.07
- **avg_rss_peak_end_mb**: 1568.0288
- **prompt_variant**: pedagogico_con_citas
- **prompt_version**: prompt-2
- **prompt_description**: Prompt pedagogico con citas: variante del prompt de rag_answer.py que mantiene el uso exclusivo del contexto, pero fuerza una respuesta mas desarrollada, estructurada y trazable con citas por idea o paso.

## Peores respuestas por similitud answer-ground_truth

- 0.0 | insuficiente=False | ¿Cuál es la principal implicación que tiene la relación estrecha entre las redes y el negocio en el contexto actual de la globalización y el
- 0.0 | insuficiente=False | ¿Qué concepto central promueve el texto sobre la evolución de las redes modernas?
- 0.0 | insuficiente=False | ¿Cuál es el enfoque principal que abarca el tema de 'Diseño & Planificación de Redes y Servicios' en el contexto de la Ingeniería de Diseño 
- 0.0 | insuficiente=False | ¿Cuál es el propósito principal de incluir la 'Teoría de Colas' en el proceso de Diseño y Planificación de Redes?
- 0.0 | insuficiente=False | ¿Cuándo es más recomendable utilizar un direccionamiento de red dinámico (como DHCP) en lugar de uno estático?
- 0.0 | insuficiente=False | ¿Cuál es el propósito principal de considerar los 'Objetivos', 'Ámbito', 'Restricciones' e 'Intersección' al inicio de un proyecto de Diseño
- 0.0 | insuficiente=False | ¿Qué representa el cambio de notación a 'Flujo-Camino-Demanda' (FCD) en el contexto del Diseño y Dimensionamiento de Redes?
- 0.0 | insuficiente=False | ¿Cuál es el objetivo principal al abordar un 'Ejemplo de Routing' en el contexto de Diseño y Dimensionamiento de Redes?
