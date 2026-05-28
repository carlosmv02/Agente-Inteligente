# Evaluacion RAG

## Resumen

- **num_questions**: 24
- **configured_llm_provider**: openai
- **configured_llm_model**: gpt-5-mini
- **top_k**: 6
- **use_testset_hints**: True
- **attach_page_context**: True
- **generation_max_tokens**: 1000
- **result_llm_providers**: ['openai']
- **result_llm_models**: ['gpt-5-mini']
- **wall_time_s**: 121.582
- **recorded_pipeline_time_s**: 121.565
- **avg_time_per_response_s**: 5.065
- **avg_retrieval_time_s**: 0.0942
- **avg_generation_time_s**: 4.9703
- **avg_answer_ground_truth_similarity**: 0.8971
- **avg_answer_context_similarity**: 0.8586
- **avg_ground_truth_context_similarity**: 0.822
- **avg_same_tema_ratio**: 1.0
- **avg_same_pdf_ratio**: 0.993
- **same_page_hit_rate**: 0.958
- **insufficient_context_answers**: 1
- **insufficient_context_rate**: 0.042
- **avg_context_count**: 7.2083
- **avg_context_chars**: 4399.6667
- **avg_answer_words**: 102.9583
- **avg_prompt_tokens_ollama**: None
- **avg_completion_tokens_ollama**: None
- **avg_ollama_total_duration_s**: None
- **avg_input_tokens_openai**: 1955.875
- **avg_output_tokens_openai**: 341.7083
- **avg_total_tokens_openai**: 2297.5833
- **avg_cpu_user_delta_s**: 0.7067
- **avg_cpu_system_delta_s**: 0.0088
- **avg_rss_peak_end_mb**: 1682.36

## Peores respuestas por similitud answer-ground_truth

- 0.8286 | insuficiente=False | Para lograr altas capacidades de análisis de eventos de seguridad, integrar múltiples dispositivos y facilitar auditorías de seguridad y uso
- 0.8514 | insuficiente=False | ¿Cuál es el objetivo principal del 'Dimensionamiento de Red' dentro del contexto de las redes?
- 0.8584 | insuficiente=False | ¿Qué implica el 'dimensionamiento con 6 caminos' en el contexto de un ejercicio de Diseño y Dimensionamiento de Redes (DDR)?
- 0.8607 | insuficiente=False | ¿Cuál es el objetivo principal al realizar el dimensionamiento de una red?
- 0.8689 | insuficiente=False | ¿Qué técnica analítica es más adecuada para establecer la capacidad de un enlace inexistente para un servicio nuevo, cuando se tienen valore
- 0.8799 | insuficiente=False | ¿Qué representa el cambio de notación a 'Flujo-Camino-Demanda' (FCD) en el contexto del Diseño y Dimensionamiento de Redes?
- 0.8825 | insuficiente=False | ¿Cuál es el propósito principal de incluir información como el nombre de la universidad, el tema y el año académico en un material de estudi
- 0.884 | insuficiente=True | ¿Cuándo es más recomendable utilizar un direccionamiento de red dinámico (como DHCP) en lugar de uno estático?
