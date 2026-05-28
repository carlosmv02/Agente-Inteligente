# Evaluacion RAG

## Resumen

- **num_questions**: 24
- **configured_llm_provider**: openai
- **configured_llm_model**: gpt-5-mini
- **result_llm_providers**: ['openai']
- **result_llm_models**: ['gpt-5-mini']
- **wall_time_s**: 125.324
- **recorded_pipeline_time_s**: 125.306
- **avg_time_per_response_s**: 5.221
- **avg_retrieval_time_s**: 0.1117
- **avg_generation_time_s**: 5.109
- **avg_answer_ground_truth_similarity**: 0.879
- **avg_answer_context_similarity**: 0.8301
- **avg_ground_truth_context_similarity**: 0.822
- **avg_same_tema_ratio**: 1.0
- **avg_same_pdf_ratio**: 0.993
- **same_page_hit_rate**: 0.958
- **insufficient_context_answers**: 0
- **insufficient_context_rate**: 0.0
- **avg_context_count**: 7.2083
- **avg_context_chars**: 4399.6667
- **avg_answer_words**: 50.5
- **avg_prompt_tokens_ollama**: None
- **avg_completion_tokens_ollama**: None
- **avg_ollama_total_duration_s**: None
- **avg_input_tokens_openai**: 2215.875
- **avg_output_tokens_openai**: 250.3333
- **avg_total_tokens_openai**: 2466.2083
- **avg_cpu_user_delta_s**: 0.8721
- **avg_cpu_system_delta_s**: 0.0075
- **avg_rss_peak_end_mb**: 1565.6933
- **prompt_variant**: estricto
- **prompt_version**: prompt-1
- **prompt_description**: Prompt estricto: responde solo con informacion presente en el contexto y declara insuficiencia cuando no haya soporte suficiente.

## Peores respuestas por similitud answer-ground_truth

- 0.7252 | insuficiente=False | ¿Cuál es el objetivo principal del 'Dimensionamiento de Red' dentro del contexto de las redes?
- 0.7627 | insuficiente=False | ¿Cuál es el propósito principal de incluir la 'Teoría de Colas' en el proceso de Diseño y Planificación de Redes?
- 0.7745 | insuficiente=False | ¿Cuál es el objetivo principal al realizar el dimensionamiento de una red?
- 0.7968 | insuficiente=False | ¿Qué implica el 'dimensionamiento con 6 caminos' en el contexto de un ejercicio de Diseño y Dimensionamiento de Redes (DDR)?
- 0.8057 | insuficiente=False | ¿Cuál es el propósito principal de incluir información como el nombre de la universidad, el tema y el año académico en un material de estudi
- 0.8599 | insuficiente=False | ¿Qué técnica analítica es más adecuada para establecer la capacidad de un enlace inexistente para un servicio nuevo, cuando se tienen valore
- 0.8733 | insuficiente=False | ¿Cuándo es más recomendable utilizar un direccionamiento de red dinámico (como DHCP) en lugar de uno estático?
- 0.8745 | insuficiente=False | ¿Qué representa el cambio de notación a 'Flujo-Camino-Demanda' (FCD) en el contexto del Diseño y Dimensionamiento de Redes?
