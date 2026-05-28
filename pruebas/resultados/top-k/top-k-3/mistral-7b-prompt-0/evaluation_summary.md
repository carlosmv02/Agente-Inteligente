# Evaluacion RAG

## Resumen

- **num_questions**: 24
- **configured_llm_provider**: ollama
- **configured_llm_model**: mistral:7b
- **top_k**: 3
- **use_testset_hints**: True
- **attach_page_context**: True
- **generation_max_tokens**: 1200
- **result_llm_providers**: ['ollama']
- **result_llm_models**: ['mistral:7b']
- **wall_time_s**: 4384.557
- **recorded_pipeline_time_s**: 4384.534
- **avg_time_per_response_s**: 182.689
- **avg_retrieval_time_s**: 0.1107
- **avg_generation_time_s**: 182.578
- **avg_answer_ground_truth_similarity**: 0.8943
- **avg_answer_context_similarity**: 0.8568
- **avg_ground_truth_context_similarity**: 0.824
- **avg_same_tema_ratio**: 1.0
- **avg_same_pdf_ratio**: 1.0
- **same_page_hit_rate**: 0.917
- **insufficient_context_answers**: 0
- **insufficient_context_rate**: 0.0
- **avg_context_count**: 4.5
- **avg_context_chars**: 2616.75
- **avg_answer_words**: 102.2917
- **avg_prompt_tokens_ollama**: 1678.375
- **avg_completion_tokens_ollama**: 192.0
- **avg_ollama_total_duration_s**: 182.572
- **avg_input_tokens_openai**: None
- **avg_output_tokens_openai**: None
- **avg_total_tokens_openai**: None
- **avg_cpu_user_delta_s**: 0.8475
- **avg_cpu_system_delta_s**: 0.0125
- **avg_rss_peak_end_mb**: 1554.0408

## Peores respuestas por similitud answer-ground_truth

- 0.7845 | insuficiente=False | Para lograr altas capacidades de análisis de eventos de seguridad, integrar múltiples dispositivos y facilitar auditorías de seguridad y uso
- 0.8333 | insuficiente=False | ¿Qué técnica analítica es más adecuada para establecer la capacidad de un enlace inexistente para un servicio nuevo, cuando se tienen valore
- 0.8574 | insuficiente=False | ¿Cuál es la principal implicación que tiene la relación estrecha entre las redes y el negocio en el contexto actual de la globalización y el
- 0.8728 | insuficiente=False | ¿Cuándo es más recomendable utilizar un direccionamiento de red dinámico (como DHCP) en lugar de uno estático?
- 0.8738 | insuficiente=False | ¿Cuál es el propósito principal de incluir información como el nombre de la universidad, el tema y el año académico en un material de estudi
- 0.8809 | insuficiente=False | ¿Qué implica el 'dimensionamiento con 6 caminos' en el contexto de un ejercicio de Diseño y Dimensionamiento de Redes (DDR)?
- 0.8876 | insuficiente=False | ¿Cuál es el objetivo principal al realizar el dimensionamiento de una red?
- 0.889 | insuficiente=False | ¿Qué tipo de problema de optimización de redes se ejemplifica al buscar el camino más corto entre dos nodos de Internet o al optimizar los t
