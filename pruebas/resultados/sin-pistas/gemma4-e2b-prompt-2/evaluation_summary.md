# Evaluacion RAG

## Resumen

- **num_questions**: 24
- **configured_llm_provider**: ollama
- **configured_llm_model**: gemma4:e2b
- **top_k**: 6
- **use_testset_hints**: False
- **attach_page_context**: True
- **generation_max_tokens**: 1200
- **result_llm_providers**: ['ollama']
- **result_llm_models**: ['gemma4:e2b']
- **wall_time_s**: 2823.618
- **recorded_pipeline_time_s**: 2823.602
- **avg_time_per_response_s**: 117.65
- **avg_retrieval_time_s**: 0.1171
- **avg_generation_time_s**: 117.5324
- **avg_answer_ground_truth_similarity**: 0.8563
- **avg_answer_context_similarity**: 0.9011
- **avg_ground_truth_context_similarity**: 0.8287
- **avg_same_tema_ratio**: 0.5139
- **avg_same_pdf_ratio**: 0.4375
- **same_page_hit_rate**: 0.458
- **insufficient_context_answers**: 0
- **insufficient_context_rate**: 0.0
- **avg_context_count**: 6.0
- **avg_context_chars**: 3804.1667
- **avg_answer_words**: 201.7083
- **avg_prompt_tokens_ollama**: 2021.0
- **avg_completion_tokens_ollama**: 948.75
- **avg_ollama_total_duration_s**: 117.5072
- **avg_input_tokens_openai**: None
- **avg_output_tokens_openai**: None
- **avg_total_tokens_openai**: None
- **avg_cpu_user_delta_s**: 0.9146
- **avg_cpu_system_delta_s**: 0.0221
- **avg_rss_peak_end_mb**: 1555.6954
- **prompt_variant**: pedagogico_con_citas
- **prompt_version**: prompt-2
- **prompt_description**: Prompt pedagogico con citas: variante del prompt de rag_answer.py que mantiene el uso exclusivo del contexto, pero fuerza una respuesta mas desarrollada, estructurada y trazable con citas por idea o paso.

## Peores respuestas por similitud answer-ground_truth

- 0.7856 | insuficiente=False | Para lograr altas capacidades de análisis de eventos de seguridad, integrar múltiples dispositivos y facilitar auditorías de seguridad y uso
- 0.8176 | insuficiente=False | ¿Cuál es el objetivo principal del 'Dimensionamiento de Red' dentro del contexto de las redes?
- 0.8265 | insuficiente=False | ¿Qué técnica analítica es más adecuada para establecer la capacidad de un enlace inexistente para un servicio nuevo, cuando se tienen valore
- 0.8289 | insuficiente=False | ¿Qué sucede con la formulación original al añadir un camino adicional al dimensionar una red, según el texto?
- 0.83 | insuficiente=False | ¿Cuál es el objetivo principal al realizar el dimensionamiento de una red?
- 0.8321 | insuficiente=False | ¿Qué concepto central promueve el texto sobre la evolución de las redes modernas?
- 0.8362 | insuficiente=False | ¿Cuál es el concepto clave que resume la transición de las necesidades de negocio a la planificación técnica en el Diseño y Dimensionamiento
- 0.839 | insuficiente=False | ¿Cuál es el objetivo principal al formular un problema de dimensionamiento de red (FCD) y qué implica la naturaleza de este problema?
