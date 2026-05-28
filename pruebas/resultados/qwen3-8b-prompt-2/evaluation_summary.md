# Evaluacion RAG

## Resumen

- **num_questions**: 24
- **configured_llm_provider**: ollama
- **configured_llm_model**: qwen3:8b
- **top_k**: 6
- **use_testset_hints**: True
- **attach_page_context**: True
- **generation_max_tokens**: 1200
- **result_llm_providers**: ['ollama']
- **result_llm_models**: ['qwen3:8b']
- **wall_time_s**: 10267.535
- **recorded_pipeline_time_s**: 10267.512
- **avg_time_per_response_s**: 427.813
- **avg_retrieval_time_s**: 0.3047
- **avg_generation_time_s**: 427.5078
- **avg_answer_ground_truth_similarity**: 0.8358
- **avg_answer_context_similarity**: 0.859
- **avg_ground_truth_context_similarity**: 0.822
- **avg_same_tema_ratio**: 1.0
- **avg_same_pdf_ratio**: 0.993
- **same_page_hit_rate**: 0.958
- **insufficient_context_answers**: 0
- **insufficient_context_rate**: 0.0
- **avg_context_count**: 7.2083
- **avg_context_chars**: 4399.6667
- **avg_answer_words**: 231.9167
- **avg_prompt_tokens_ollama**: 2488.125
- **avg_completion_tokens_ollama**: 863.2083
- **avg_ollama_total_duration_s**: 427.485
- **avg_input_tokens_openai**: None
- **avg_output_tokens_openai**: None
- **avg_total_tokens_openai**: None
- **avg_cpu_user_delta_s**: 2.1888
- **avg_cpu_system_delta_s**: 0.0446
- **avg_rss_peak_end_mb**: 1614.7187
- **prompt_variant**: pedagogico_con_citas
- **prompt_version**: prompt-2
- **prompt_description**: Prompt pedagogico con citas: variante del prompt de rag_answer.py que mantiene el uso exclusivo del contexto, pero fuerza una respuesta mas desarrollada, estructurada y trazable con citas por idea o paso.

## Peores respuestas por similitud answer-ground_truth

- 0.0 | insuficiente=False | ¿Qué sucede con la formulación original al añadir un camino adicional al dimensionar una red, según el texto?
- 0.8234 | insuficiente=False | Para lograr altas capacidades de análisis de eventos de seguridad, integrar múltiples dispositivos y facilitar auditorías de seguridad y uso
- 0.8427 | insuficiente=False | ¿Qué técnica analítica es más adecuada para establecer la capacidad de un enlace inexistente para un servicio nuevo, cuando se tienen valore
- 0.8465 | insuficiente=False | ¿Cuál es la principal implicación que tiene la relación estrecha entre las redes y el negocio en el contexto actual de la globalización y el
- 0.8529 | insuficiente=False | ¿Cuál es el objetivo principal al realizar el dimensionamiento de una red?
- 0.8576 | insuficiente=False | ¿Cuál es el propósito principal de incluir información como el nombre de la universidad, el tema y el año académico en un material de estudi
- 0.8622 | insuficiente=False | ¿Cuál es el enfoque principal que abarca el tema de 'Diseño & Planificación de Redes y Servicios' en el contexto de la Ingeniería de Diseño 
- 0.8622 | insuficiente=False | ¿Cuál es el propósito principal del fragmento de código proporcionado en el contexto de un problema de enrutamiento de redes?
