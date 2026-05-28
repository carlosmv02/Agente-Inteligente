"""
genera_examen.py
----------------
Logica especializada para generar examenes nuevos de DDR desde rag_answer.py.

La generacion se separa del flujo normal porque los modelos locales suelen
fallar cuando se les pide en una sola llamada un examen completo y su solucion.
Para la variante con solucionario se hacen dos pasos:
  1. Generar solo el enunciado.
  2. Generar el solucionario usando el enunciado ya fijado.
"""

from __future__ import annotations

import os
import re
import math
import random
import hashlib
import unicodedata
from typing import Callable


DEFAULT_EXAM_ONLY_TOKENS = 3200
DEFAULT_EXAM_SOLUTION_TOKENS = 6200


def normalize_text(text: str) -> str:
    text = (text or "").lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def is_exam_generation_request(question: str) -> bool:
    q = normalize_text(question)
    return (
        "examen" in q
        and any(token in q for token in [
            "genera", "generame", "crear", "crea", "nuevo",
            "aleatoria", "aleatorio"
        ])
    )


def is_exam_generation_with_solution_request(question: str) -> bool:
    q = normalize_text(question)
    wants_solution = any(token in q for token in [
        "solucion", "soluciones", "solucionario", "resuelto",
        "resuelta", "resolver"
    ])
    return is_exam_generation_request(question) and wants_solution


def exam_only_budget() -> int:
    return int(os.environ.get("RAG_EXAM_ONLY_MAX_TOKENS", str(DEFAULT_EXAM_ONLY_TOKENS)))


def exam_solution_budget() -> int:
    return int(os.environ.get(
        "RAG_EXAM_SOLUTION_MAX_TOKENS",
        os.environ.get("RAG_EXAM_WITH_SOLUTION_MAX_TOKENS", str(DEFAULT_EXAM_SOLUTION_TOKENS)),
    ))


def response_budget(question: str) -> int | None:
    if is_exam_generation_with_solution_request(question):
        return exam_solution_budget()
    if is_exam_generation_request(question):
        return exam_only_budget()
    return None


def exam_question_4_template(include_solution: bool = False) -> str:
    final_rule = (
        "Si se pide solucionario, incluye la solucion razonada, pero no escribas un script completo .m."
        if include_solution
        else "No escribas la solucion ni el codigo."
    )
    return f"""
PLANTILLA OBLIGATORIA PARA LA PREGUNTA 4:

4. (2 ptos) A partir de la topologia de la Figura 1 y contemplando las siguientes consideraciones:

- Se dispone de una topologia concreta con nodos, enlaces y capacidades/modulos.
- Existe una matriz de trafico concreta en Gbps.
- Se deben incluir opciones OPC 1, OPC 2, OPC 3 y OPC 4.
- El objetivo debe ser de diseno/dimensionado: minimo coste, minima congestion,
  robustez, OPEX + CAPEX o una combinacion clara.

Disene la red incluyendo:

a) La formulacion matematica abstracta, indicando variables, funcion objetivo,
   restricciones, entradas y salidas. (1 pto)
b) Las restricciones de igualdad/desigualdad principales o una modificacion
   puntual de la formulacion. (0.5 ptos)
c) La solucion programada en octave/matlab, entregando script y resultados.
   En el examen escrito se debe indicar la asignacion de OPC y el resultado
   en terminos de modulos, capacidades, coste o decision de diseno. (0.5 ptos)

RESTRICCIONES DE ESTA PLANTILLA:
- No generes variantes segun DNI.
- No incluyas tablas de asignacion por DNI.
- No pidas deducir opciones a partir de letras del DNI.
- {final_rule}
- La pregunta 4 debe ser resoluble: evita datos incompatibles salvo que el
  objetivo sea explicitamente detectar inviabilidad.
""".strip()


def canonical_question_4() -> str:
    """Pregunta 4 cerrada para asegurar un ejercicio resoluble y comparable."""
    return """
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

c) Indique como implementaria la solucion en Octave/Matlab, entregando el script .m
   y los resultados. En la respuesta escrita debe aparecer la asignacion de OPC 1
   a OPC 4 y el resultado final en terminos de modulos, capacidades, utilizacion
   y coste total. (0.5 ptos)
""".strip()


def canonical_question_4_solution() -> str:
    """Solucion exacta de la pregunta 4 canonica."""
    return """
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

El problema tambien puede escribirse como el siguiente entero lineal:

minimizar 1^T m
sujeto a L <= 8.5 m
m entero
0 <= m <= 4

Como las rutas estan fijadas por R1 y cada restriccion solo depende del modulo
del propio enlace, el optimo se obtiene enlace a enlace mediante:
m_e = ceil(L_e / 8.5)

Esto prueba la optimalidad de la solucion anterior: ningun enlace puede tener
menos modulos que ceil(L_e / 8.5), y la solucion propuesta alcanza exactamente
ese minimo en todos los enlaces.

Script Octave/Matlab orientativo:

```matlab
% Enlaces en este orden: AB, BC, CD, DA, AC
enlaces = {'AB', 'BC', 'CD', 'DA', 'AC'};

L = [9, 19, 19, 8, 13];   % cargas agregadas en Gbps
C = 10;                  % Gbps por modulo
u_max = 0.85;            % utilizacion maxima

m = ceil(L ./ (u_max * C));
capacidad = C .* m;
utilizacion = L ./ capacidad;
coste_total = sum(m);

fprintf('Enlace  Carga  Modulos  Capacidad  Utilizacion\\n');
for i = 1:length(enlaces)
    fprintf('%s      %.1f     %d       %.1f       %.3f\\n', ...
        enlaces{i}, L(i), m(i), capacidad(i), utilizacion(i));
end

fprintf('Coste total = %d unidades\\n', coste_total);

if any(utilizacion > u_max + 1e-12)
    error('La solucion no cumple la utilizacion maxima');
end
```

La salida esperada del script es:
- m = [2, 3, 3, 1, 2].
- capacidad = [20, 30, 30, 10, 20] Gbps.
- utilizacion = [0.45, 0.633, 0.633, 0.80, 0.65].
- coste_total = 11.
""".strip()


QUESTION_4_VARIANTS = [
    {
        "id": "T1",
        "title": "Dimensionado de capacidad con modulos y utilizacion maxima",
        "nodes": ["A", "B", "C", "D"],
        "links": [
            ("e1", "AB", "A-B"),
            ("e2", "BC", "B-C"),
            ("e3", "CD", "C-D"),
            ("e4", "DA", "D-A"),
            ("e5", "AC", "A-C"),
        ],
        "demands": [
            ("A", "B", 6, ["AB"], "A-B"),
            ("B", "A", 3, ["AB"], "B-A"),
            ("A", "C", 8, ["AC"], "A-C"),
            ("C", "A", 5, ["AC"], "C-A"),
            ("A", "D", 4, ["DA"], "A-D"),
            ("D", "A", 4, ["DA"], "D-A"),
            ("B", "C", 7, ["BC"], "B-C"),
            ("C", "B", 4, ["BC"], "C-B"),
            ("C", "D", 6, ["CD"], "C-D"),
            ("D", "C", 5, ["CD"], "D-C"),
            ("B", "D", 5, ["BC", "CD"], "B-C-D"),
            ("D", "B", 3, ["CD", "BC"], "D-C-B"),
        ],
        "u_max": 0.85,
        "module_capacity": 10,
        "max_modules": 4,
        "cost": 1,
    },
    {
        "id": "T2",
        "title": "Dimensionado de enlaces con trafico encaminado y coste minimo",
        "nodes": ["A", "B", "C", "D"],
        "links": [
            ("e1", "AB", "A-B"),
            ("e2", "BC", "B-C"),
            ("e3", "CD", "C-D"),
            ("e4", "AD", "A-D"),
            ("e5", "BD", "B-D"),
        ],
        "demands": [
            ("A", "B", 4, ["AB"], "A-B"),
            ("B", "A", 5, ["AB"], "B-A"),
            ("A", "C", 9, ["AB", "BC"], "A-B-C"),
            ("C", "A", 6, ["BC", "AB"], "C-B-A"),
            ("B", "C", 6, ["BC"], "B-C"),
            ("C", "B", 5, ["BC"], "C-B"),
            ("C", "D", 7, ["CD"], "C-D"),
            ("D", "C", 6, ["CD"], "D-C"),
            ("A", "D", 4, ["AD"], "A-D"),
            ("D", "A", 3, ["AD"], "D-A"),
            ("B", "D", 8, ["BD"], "B-D"),
            ("D", "B", 5, ["BD"], "D-B"),
        ],
        "u_max": 0.80,
        "module_capacity": 10,
        "max_modules": 4,
        "cost": 1,
    },
    {
        "id": "T3",
        "title": "Dimensionado de red troncal con nodo perimetral",
        "nodes": ["A", "B", "C", "D", "E"],
        "links": [
            ("e1", "AB", "A-B"),
            ("e2", "BC", "B-C"),
            ("e3", "CD", "C-D"),
            ("e4", "DE", "D-E"),
            ("e5", "AE", "A-E"),
            ("e6", "AC", "A-C"),
        ],
        "demands": [
            ("A", "B", 5, ["AB"], "A-B"),
            ("B", "A", 4, ["AB"], "B-A"),
            ("A", "C", 8, ["AC"], "A-C"),
            ("C", "A", 6, ["AC"], "C-A"),
            ("A", "E", 5, ["AE"], "A-E"),
            ("E", "A", 5, ["AE"], "E-A"),
            ("B", "D", 7, ["BC", "CD"], "B-C-D"),
            ("D", "B", 5, ["CD", "BC"], "D-C-B"),
            ("C", "E", 9, ["CD", "DE"], "C-D-E"),
            ("E", "C", 6, ["DE", "CD"], "E-D-C"),
            ("B", "E", 4, ["BC", "CD", "DE"], "B-C-D-E"),
            ("E", "B", 3, ["DE", "CD", "BC"], "E-D-C-B"),
        ],
        "u_max": 0.85,
        "module_capacity": 10,
        "max_modules": 4,
        "cost": 1,
    },
]


QUESTION_4_DIMENSIONING_OPTIONS = [
    {
        "id": "D1",
        "module_capacity": 10,
        "u_max": 0.80,
        "max_modules": 4,
        "cost": 1,
    },
    {
        "id": "D2",
        "module_capacity": 10,
        "u_max": 0.85,
        "max_modules": 4,
        "cost": 1,
    },
    {
        "id": "D3",
        "module_capacity": 20,
        "u_max": 0.70,
        "max_modules": 3,
        "cost": 2,
    },
    {
        "id": "D4",
        "module_capacity": 20,
        "u_max": 0.80,
        "max_modules": 3,
        "cost": 2,
    },
    {
        "id": "D5",
        "module_capacity": 30,
        "u_max": 0.90,
        "max_modules": 2,
        "cost": 3,
    },
    {
        "id": "D6",
        "module_capacity": 40,
        "u_max": 0.80,
        "max_modules": 2,
        "cost": 4,
    },
]


EXAM_THEORY_PROFILES = [
    {
        "id": "P1",
        "title": "Fundamentos de diseno, requisitos y disponibilidad",
        "questions": [
            {
                "points": "0.5 ptos",
                "statement": "Diferencie claramente entre diseno de red y dimensionamiento. Indique dos decisiones propias de cada fase y explique por que no deben tratarse como tareas equivalentes.",
            },
            {
                "points": "0.5 ptos",
                "statement": "Explique como los requisitos de negocio condicionan los requisitos tecnicos de una red. Incluya al menos un ejemplo relacionado con coste, disponibilidad o crecimiento futuro.",
            },
            {
                "points": "1.0 pto",
                "statement": "Analice el papel de la disponibilidad en un proyecto de DDR. Explique la relacion entre SLA, redundancia, MTBF/MTTR y coste de implantacion.",
            },
        ],
    },
    {
        "id": "P2",
        "title": "Caracterizacion, trafico y optimizacion de red",
        "questions": [
            {
                "points": "0.5 ptos",
                "statement": "Explique por que es necesario caracterizar por separado la infraestructura fisica y la logica de una red antes de proponer un nuevo diseno.",
            },
            {
                "points": "0.5 ptos",
                "statement": "Defina que representa una matriz de trafico en DDR y explique como se utiliza para pasar de requisitos de usuarios a necesidades de capacidad en enlaces.",
            },
            {
                "points": "1.0 pto",
                "statement": "Formule conceptualmente la restriccion de capacidad de una red usando una notacion de flujo-camino-demanda. Indique datos de entrada, variables de decision y salidas esperadas.",
            },
        ],
    },
    {
        "id": "P3",
        "title": "Automatizacion, telemetria y redes programables",
        "questions": [
            {
                "points": "0.5 ptos",
                "statement": "Explique que aporta la programabilidad de red frente a una configuracion manual dispositivo a dispositivo.",
            },
            {
                "points": "0.5 ptos",
                "statement": "Defina Network Telemetry y razone por que es mas adecuada que una supervision puntual cuando se quieren redes autonomas.",
            },
            {
                "points": "1.0 pto",
                "statement": "Relacione Intent Based Networking con el ciclo medir-analizar-actuar. Explique como una intencion de alto nivel puede convertirse en politicas tecnicas verificables.",
            },
        ],
    },
]


def select_exam_profile(question: str = "") -> dict:
    requested = os.environ.get("RAG_EXAM_PROFILE", "").strip().upper()
    if requested:
        for index, profile in enumerate(EXAM_THEORY_PROFILES, start=1):
            if requested in {profile["id"].upper(), str(index)}:
                return profile

    seed = os.environ.get("RAG_EXAM_SEED", "").strip()
    if seed:
        digest = hashlib.sha256(f"profile:{seed}".encode("utf-8")).hexdigest()
        return EXAM_THEORY_PROFILES[int(digest, 16) % len(EXAM_THEORY_PROFILES)]

    return random.SystemRandom().choice(EXAM_THEORY_PROFILES)


def _find_bank_item(items: list[dict], requested: str) -> dict | None:
    requested = (requested or "").strip().upper()
    if not requested:
        return None

    for index, item in enumerate(items, start=1):
        aliases = {str(index), item["id"].upper()}
        if requested in aliases:
            return item
    return None


def _build_question_4_variant(scenario: dict, dimensioning: dict) -> dict:
    dimension_keys = {"module_capacity", "u_max", "max_modules", "cost"}
    variant = {
        key: value
        for key, value in scenario.items()
        if key not in dimension_keys
    }
    variant.update({
        "topology_id": scenario["id"],
        "matrix_id": f"M{_variant_suffix(scenario)}",
        "routing_id": f"R{_variant_suffix(scenario)}",
        "dimension_id": dimensioning["id"],
        "module_capacity": dimensioning["module_capacity"],
        "u_max": dimensioning["u_max"],
        "max_modules": dimensioning["max_modules"],
        "cost": dimensioning["cost"],
        "combination_id": f"{scenario['id']}-{dimensioning['id']}",
    })
    return variant


def _is_valid_question_4_variant(variant: dict) -> bool:
    try:
        loads = _loads_by_link(variant)
        modules = _modules_by_link(variant, loads)
    except Exception:
        return False

    return all(
        modules[link_id] <= variant["max_modules"]
        for _, link_id, _ in variant["links"]
    )


def _question_4_combinations(
    scenario: dict | None = None,
    dimensioning: dict | None = None,
) -> list[dict]:
    scenarios = [scenario] if scenario else QUESTION_4_VARIANTS
    dimensionings = [dimensioning] if dimensioning else QUESTION_4_DIMENSIONING_OPTIONS

    combinations = []
    for scenario_item in scenarios:
        for dimensioning_item in dimensionings:
            variant = _build_question_4_variant(scenario_item, dimensioning_item)
            if _is_valid_question_4_variant(variant):
                combinations.append(variant)
    return combinations


def select_question_4_variant(question: str = "") -> dict:
    requested_scenario = (
        os.environ.get("RAG_EXAM_SCENARIO", "").strip().upper()
        or os.environ.get("RAG_EXAM_VARIANT", "").strip().upper()
    )
    requested_dimensioning = (
        os.environ.get("RAG_EXAM_DIMENSION", "").strip().upper()
        or os.environ.get("RAG_EXAM_DIMENSIONING", "").strip().upper()
        or os.environ.get("RAG_EXAM_DIMENSION_OPTION", "").strip().upper()
    )

    scenario = _find_bank_item(QUESTION_4_VARIANTS, requested_scenario)
    dimensioning = _find_bank_item(QUESTION_4_DIMENSIONING_OPTIONS, requested_dimensioning)

    if requested_scenario and scenario is None:
        raise ValueError(f"RAG_EXAM_VARIANT/RAG_EXAM_SCENARIO no valido: {requested_scenario}")
    if requested_dimensioning and dimensioning is None:
        raise ValueError(f"RAG_EXAM_DIMENSION no valido: {requested_dimensioning}")

    combinations = _question_4_combinations(scenario=scenario, dimensioning=dimensioning)
    if not combinations:
        detail = []
        if scenario:
            detail.append(scenario["id"])
        if dimensioning:
            detail.append(dimensioning["id"])
        suffix = f" ({'-'.join(detail)})" if detail else ""
        raise ValueError(f"No hay combinaciones validas para la pregunta 4{suffix}")

    seed = os.environ.get("RAG_EXAM_SEED", "").strip()
    if seed:
        digest = hashlib.sha256(f"question4:{seed}".encode("utf-8")).hexdigest()
        return combinations[int(digest, 16) % len(combinations)]

    return random.SystemRandom().choice(combinations)


def force_profile_questions() -> bool:
    value = os.environ.get("RAG_EXAM_FORCE_PROFILE", "").strip().lower()
    return value in {"1", "true", "yes", "si", "s"}


def profile_questions_1_to_3(profile: dict) -> str:
    parts = []
    for number, item in enumerate(profile["questions"], start=1):
        parts.append(f"{number}. ({item['points']}) {item['statement']}")
    return "\n\n".join(parts)


def profile_guidance(profile: dict) -> str:
    lines = [f"PERFIL TEMATICO OBLIGATORIO: {profile['id']} - {profile['title']}"]
    for number, item in enumerate(profile["questions"], start=1):
        lines.append(f"- Pregunta {number}: {item['statement']}")
    return "\n".join(lines)


def _question_heading_pattern(number: int) -> str:
    return (
        rf"^\s*(?:#+\s*)?(?:\*\*)?\s*"
        rf"(?:(?:pregunta|ejercicio|cuestion)\s+)?"
        rf"{number}\s*(?:[\).:-]|\()"
    )


def _find_question_heading(text: str, number: int) -> re.Match | None:
    return re.search(_question_heading_pattern(number), text or "", flags=re.IGNORECASE | re.MULTILINE)


def _loads_by_link(variant: dict) -> dict[str, float]:
    loads = {link_id: 0.0 for _, link_id, _ in variant["links"]}
    for _, _, amount, path, _ in variant["demands"]:
        for link_id in path:
            loads[link_id] += float(amount)
    return loads


def _modules_by_link(variant: dict, loads: dict[str, float]) -> dict[str, int]:
    step = variant["u_max"] * variant["module_capacity"]
    modules = {}
    for _, link_id, _ in variant["links"]:
        modules[link_id] = 0 if loads[link_id] <= 0 else math.ceil(loads[link_id] / step)
    return modules


def _fmt_number(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.3f}".rstrip("0").rstrip(".")


def _module_word(count: int) -> str:
    return "modulo" if count == 1 else "modulos"


def _matlab_cell(values: list[str]) -> str:
    return "{" + ", ".join(f"'{value}'" for value in values) + "}"


def _variant_suffix(variant: dict) -> str:
    match = re.search(r"(\d+)$", variant["id"])
    return match.group(1) if match else variant["id"][-1]


def _option_names(variant: dict) -> tuple[str, str, str, str]:
    suffix = _variant_suffix(variant)
    return (
        variant.get("topology_id", variant["id"]),
        variant.get("matrix_id", f"M{suffix}"),
        variant.get("routing_id", f"R{suffix}"),
        variant.get("dimension_id", f"D{suffix}"),
    )


def _traffic_matrix_table(variant: dict) -> str:
    nodes = variant["nodes"]
    traffic = {
        (src, dst): amount
        for src, dst, amount, _, _ in variant["demands"]
    }
    header = "| Origen \\ Destino | " + " | ".join(nodes) + " |"
    separator = "|---" * (len(nodes) + 1) + "|"
    rows = [header, separator]
    for src in nodes:
        values = []
        for dst in nodes:
            if src == dst:
                values.append("-")
            else:
                values.append(_fmt_number(traffic.get((src, dst), 0)))
        rows.append(f"| {src} | " + " | ".join(values) + " |")
    return "\n".join(rows)


def _links_table(variant: dict) -> str:
    rows = [
        "| Codigo | Enlace fisico bidireccional | Identificador usado en la solucion |",
        "|---|---|---|",
    ]
    for edge_code, link_id, label in variant["links"]:
        rows.append(f"| {edge_code} | {label} | {link_id} |")
    return "\n".join(rows)


def _routes_table(variant: dict) -> str:
    rows = [
        "| Demanda | Trafico (Gbps) | Ruta nominal | Enlaces fisicos usados |",
        "|---|---:|---|---|",
    ]
    for index, (src, dst, amount, path, route) in enumerate(variant["demands"], start=1):
        rows.append(
            f"| d{index}: {src} -> {dst} | {_fmt_number(amount)} | {route} | {', '.join(path)} |"
        )
    return "\n".join(rows)


def _load_breakdown_lines(variant: dict, loads: dict[str, float]) -> str:
    lines = []
    for _, link_id, _ in variant["links"]:
        terms = []
        labels = []
        for src, dst, amount, path, _ in variant["demands"]:
            if link_id in path:
                terms.append(_fmt_number(amount))
                labels.append(f"{src}->{dst}")
        expression = " + ".join(terms) if terms else "0"
        label_text = ", ".join(labels) if labels else "sin demandas"
        lines.append(
            f"- L_{link_id} = {expression} = {_fmt_number(loads[link_id])} Gbps "
            f"({label_text})."
        )
    return "\n".join(lines)


def _matlab_nested_cell(paths: list[list[str]]) -> str:
    lines = ["{"]
    for path in paths:
        lines.append(f"    {_matlab_cell(path)};")
    lines.append("}")
    return "\n".join(lines)


def _question_4_matlab_script(
    variant: dict,
    loads: dict[str, float],
    modules: dict[str, int],
) -> str:
    edge_ids = [link_id for _, link_id, _ in variant["links"]]
    topo_opc, matrix_opc, route_opc, dim_opc = _option_names(variant)
    origins = [src for src, _, _, _, _ in variant["demands"]]
    destinations = [dst for _, dst, _, _, _ in variant["demands"]]
    demand_values = [_fmt_number(amount) for _, _, amount, _, _ in variant["demands"]]
    paths = [path for _, _, _, path, _ in variant["demands"]]
    expected_modules = [str(modules[link_id]) for link_id in edge_ids]
    expected_loads = [_fmt_number(loads[link_id]) for link_id in edge_ids]

    return "\n".join([
        "% Script completo para la pregunta 4",
        "% Calcula cargas por enlace, modulos, capacidades, utilizaciones y coste.",
        "clear; clc;",
        "",
        f"asignacion_opc = 'OPC1={topo_opc}, OPC2={matrix_opc}, OPC3={route_opc}, OPC4={dim_opc}';",
        f"enlaces = {_matlab_cell(edge_ids)};",
        f"origen = {_matlab_cell(origins)};",
        f"destino = {_matlab_cell(destinations)};",
        f"h = [{', '.join(demand_values)}];     % Gbps por demanda",
        "rutas = " + _matlab_nested_cell(paths) + ";",
        "",
        f"C_mod = {variant['module_capacity']};",
        f"u_max = {variant['u_max']};",
        f"coste_modulo = {variant['cost']};",
        f"max_modulos = {variant['max_modules']};",
        "",
        "L = zeros(1, length(enlaces));",
        "for d = 1:length(h)",
        "    for r = 1:length(rutas{d})",
        "        enlace_ruta = rutas{d}{r};",
        "        idx = find(strcmp(enlaces, enlace_ruta));",
        "        if isempty(idx)",
        "            error('La demanda %d usa un enlace inexistente: %s', d, enlace_ruta);",
        "        end",
        "        L(idx) = L(idx) + h(d);",
        "    end",
        "end",
        "",
        "m = ceil(L ./ (u_max * C_mod));",
        "if any(m > max_modulos)",
        "    error('La solucion requiere mas modulos de los permitidos');",
        "end",
        "",
        "capacidad = C_mod .* m;",
        "utilizacion = zeros(size(L));",
        "usados = capacidad > 0;",
        "utilizacion(usados) = L(usados) ./ capacidad(usados);",
        "coste_total = coste_modulo * sum(m);",
        "",
        "fprintf('Asignacion de opciones: %s\\n', asignacion_opc);",
        "fprintf('Enlace  Carga(Gbps)  Modulos  Capacidad(Gbps)  Utilizacion\\n');",
        "for i = 1:length(enlaces)",
        "    fprintf('%-6s %10.1f %8d %15.1f %12.3f\\n', ...",
        "        enlaces{i}, L(i), m(i), capacidad(i), utilizacion(i));",
        "end",
        "fprintf('Coste total = %.0f unidades\\n', coste_total);",
        "",
        f"L_esperada = [{', '.join(expected_loads)}];",
        f"m_esperado = [{', '.join(expected_modules)}];",
        "assert(all(abs(L - L_esperada) < 1e-9));",
        "assert(all(m == m_esperado));",
        "assert(all(utilizacion <= u_max + 1e-12));",
    ])


def canonical_question_4(variant: dict | None = None) -> str:
    """Pregunta 4 parametrizada, nueva por variante pero siempre resoluble."""
    variant = variant or _build_question_4_variant(
        QUESTION_4_VARIANTS[0],
        QUESTION_4_DIMENSIONING_OPTIONS[0],
    )
    nodes = ", ".join(variant["nodes"])
    topo_opc, matrix_opc, route_opc, dim_opc = _option_names(variant)

    return f"""
4. (2.0 puntos) {variant["title"]}

Datos del ejercicio. La pregunta queda completamente definida por las siguientes
opciones, que deben usarse sin anadir enlaces ni demandas no indicadas:

OPC 1 = {topo_opc}. Topologia fisica de la Figura 1:
- Nodos: {nodes}.
- Enlaces permitidos, todos bidireccionales:
{_links_table(variant)}
- No existen enlaces fisicos adicionales fuera de los indicados.
- Cada identificador de enlace acumula el trafico de ambos sentidos. Por ejemplo,
  AB acumula trafico A -> B y B -> A si esas demandas usan el enlace A-B.

OPC 2 = {matrix_opc}. Matriz de trafico en Gbps:
{_traffic_matrix_table(variant)}

OPC 3 = {route_opc}. Encaminamiento nominal de cada demanda:
{_routes_table(variant)}

OPC 4 = {dim_opc}. Dimensionado por modulos:
- Cada modulo aporta {variant["module_capacity"]} Gbps de capacidad al enlace donde se instala.
- Cada enlace puede tener un numero entero de modulos m_e entre 0 y {variant["max_modules"]}.
- La utilizacion maxima permitida por enlace es {variant["u_max"]}.
- El coste de cada modulo es {variant["cost"]} unidad.
- El objetivo es minimizar el coste total, es decir, minimizar el numero total de modulos instalados.
- La capacidad instalada en el enlace e es C_e = {variant["module_capacity"]} * m_e Gbps.
- La utilizacion final debe calcularse como u_e = L_e / C_e, donde L_e es la
  carga agregada del enlace e bajo el encaminamiento {route_opc}.

Se pide:

a) Formule el problema como una programacion lineal entera, indicando entradas,
   variables, funcion objetivo, restricciones y salidas. (1 pto)

b) Calcule la carga agregada de cada enlace fisico bajo {route_opc}, determine
   el numero minimo de modulos necesarios por enlace y compruebe la utilizacion
   final de cada enlace. (0.5 ptos)

c) Indique como implementaria la solucion en Octave/Matlab, entregando el script .m
   y los resultados. En la respuesta escrita debe aparecer la asignacion de OPC 1
   a OPC 4 y el resultado final en terminos de modulos, capacidades, utilizacion
   y coste total. (0.5 ptos)
""".strip()


def canonical_question_4_solution(variant: dict | None = None) -> str:
    """Solucion exacta de la pregunta 4 parametrizada."""
    variant = variant or _build_question_4_variant(
        QUESTION_4_VARIANTS[0],
        QUESTION_4_DIMENSIONING_OPTIONS[0],
    )
    loads = _loads_by_link(variant)
    modules = _modules_by_link(variant, loads)
    module_capacity = variant["module_capacity"]
    u_max = variant["u_max"]
    step = module_capacity * u_max
    cost_total = sum(modules.values()) * variant["cost"]
    topo_opc, matrix_opc, route_opc, dim_opc = _option_names(variant)

    edge_ids = [link_id for _, link_id, _ in variant["links"]]
    edge_set = ", ".join(edge_ids)
    routes = "\n".join(
        f"- {src} -> {dst}: {route}, carga {_fmt_number(amount)}."
        for src, dst, amount, _, route in variant["demands"]
    )
    load_lines = _load_breakdown_lines(variant, loads)
    module_lines = "\n".join(
        f"- m_{link_id} = ceil({_fmt_number(loads[link_id])} / {_fmt_number(step)}) = "
        f"{modules[link_id]} {_module_word(modules[link_id])}."
        for _, link_id, _ in variant["links"]
    )
    capacity_lines = "\n".join(
        f"- {link_id}: {module_capacity * modules[link_id]} Gbps."
        for _, link_id, _ in variant["links"]
    )
    utilization_lines = "\n".join(
        f"- u_{link_id} = {_fmt_number(loads[link_id])} / {module_capacity * modules[link_id]} = {_fmt_number(loads[link_id] / (module_capacity * modules[link_id]))}."
        for _, link_id, _ in variant["links"]
        if modules[link_id] > 0
    )
    result_lines = "\n".join(
        f"- {link_id}: {modules[link_id]} {_module_word(modules[link_id])}."
        for _, link_id, _ in variant["links"]
    )
    matlab_modules = ", ".join(str(modules[link_id]) for link_id in edge_ids)
    matlab_capacity = ", ".join(str(module_capacity * modules[link_id]) for link_id in edge_ids)
    matlab_utilization = ", ".join(
        _fmt_number(loads[link_id] / (module_capacity * modules[link_id]))
        for link_id in edge_ids
    )
    matlab_script = _question_4_matlab_script(variant, loads, modules)

    return f"""
4. (2.0 puntos) Solucion del dimensionado de capacidad con modulos

Opciones usadas:
- OPC 1 = {topo_opc}: topologia fisica definida en el enunciado.
- OPC 2 = {matrix_opc}: matriz de trafico en Gbps.
- OPC 3 = {route_opc}: encaminamiento nominal fijado por demanda.
- OPC 4 = {dim_opc}: modulos de {module_capacity} Gbps, utilizacion maxima {u_max},
  coste unitario {variant["cost"]} y maximo {variant["max_modules"]} modulos por enlace.

a) Formulacion matematica

Conjunto de enlaces fisicos:
E = {{{edge_set}}}.

Conjunto de demandas:
D = {{d = (s,t)}} con trafico h_d y ruta nominal p_d dados en {matrix_opc} y {route_opc}.

Variable entera:
- m_e: numero de modulos instalados en el enlace e, con m_e entero y 0 <= m_e <= {variant["max_modules"]}.

Datos:
- C = {module_capacity} Gbps por modulo.
- u_max = {u_max}.
- c = {variant["cost"]}: coste unitario de cada modulo.
- delta_ed = 1 si la ruta nominal de la demanda d usa el enlace e, y 0 en caso contrario.
- L_e = sum_{{d in D}} h_d * delta_ed: carga agregada del enlace e.

Funcion objetivo:
Minimizar:
Z = c * sum_{{e in E}} m_e

Restriccion de capacidad/utilizacion para cada enlace:
sum_{{d in D}} h_d * delta_ed <= u_max * C * m_e

Como C = {module_capacity} y u_max = {u_max}:
L_e <= {_fmt_number(step)} * m_e

Restricciones de dominio:
m_e entero, 0 <= m_e <= {variant["max_modules"]}, para todo e in E.

Salidas del script:
- Numero de modulos m_e por enlace.
- Capacidad instalada C * m_e por enlace.
- Utilizacion final L_e / (C * m_e).
- Coste total Z.

b) Calculo de cargas y modulos

Rutas usadas:
{routes}

Cargas agregadas por enlace:
{load_lines}

Numero minimo de modulos:
m_e = ceil(L_e / {_fmt_number(step)})

Por tanto:
{module_lines}

Capacidades instaladas:
{capacity_lines}

Utilizaciones finales:
{utilization_lines}

Todas las utilizaciones son menores o iguales que {u_max}, por lo que la solucion cumple la restriccion.

Coste total:
Z = {variant["cost"]} * ({" + ".join(str(modules[link_id]) for link_id in edge_ids)}) = {cost_total} unidades.

Resultado final:
{result_lines}
- Coste minimo total: {cost_total} unidades.

c) Implementacion en Octave/Matlab

El problema tambien puede escribirse como el siguiente entero lineal:

minimizar c * 1^T m
sujeto a L <= {_fmt_number(step)} m
m entero
0 <= m <= {variant["max_modules"]}

Como las rutas estan fijadas por {route_opc} y cada restriccion solo depende del modulo del propio enlace, el optimo se obtiene enlace a enlace mediante:
m_e = ceil(L_e / {_fmt_number(step)})

Esto prueba la optimalidad de la solucion anterior: ningun enlace puede tener menos modulos que ceil(L_e / {_fmt_number(step)}), y la solucion propuesta alcanza exactamente ese minimo en todos los enlaces.

Script Octave/Matlab completo:

```matlab
{matlab_script}
```

La salida esperada del script es:
- m = [{matlab_modules}].
- capacidad = [{matlab_capacity}] Gbps.
- utilizacion = [{matlab_utilization}].
- coste_total = {cost_total}.
""".strip()


def _sanitize_exam_questions_1_to_3(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"(?is)\bsolucionario\b.*$", "", text).strip()
    match = _find_question_heading(text, 4)
    if match:
        text = text[:match.start()].strip()
    return text


def _has_questions_1_to_3(text: str) -> bool:
    return all(
        _find_question_heading(text or "", number)
        for number in (1, 2, 3)
    )


def _sanitize_solution_1_to_3(text: str) -> str:
    text = (text or "").strip()

    heading = re.search(r"(?im)^\s*(?:#+\s*)?SOLUCIONARIO\b.*$", text)
    if heading:
        text = text[heading.end():].strip()

    first_answer = _find_question_heading(text, 1)
    if first_answer:
        text = text[first_answer.start():].strip()

    q4 = _find_question_heading(text, 4)
    if q4:
        text = text[:q4.start()].strip()

    return text


def _extract_question(exam_text: str, number: int) -> str:
    pattern = (
        rf"(?ims){_question_heading_pattern(number)}\s*"
        rf"(.*?)(?={_question_heading_pattern(number + 1)}|\Z)"
    )
    match = re.search(pattern, exam_text or "")
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def _fallback_solution_for_question(number: int, question_text: str) -> str:
    q = normalize_text(question_text)

    if "diseno de red" in q and "dimensionamiento" in q:
        return f"""{number}. Respuesta orientativa:
El diseno de red decide la arquitectura y la combinacion de tecnologias que permiten alcanzar los objetivos de conectividad: topologia, equipos, protocolos, segmentacion, ubicacion de servicios y mecanismos de redundancia. El dimensionamiento, en cambio, fija parametros cuantitativos dentro de ese diseno: capacidad de enlaces, numero de modulos, ancho de banda, tamanos de colas o recursos necesarios para cumplir unas prestaciones.

No son tareas equivalentes porque un buen dimensionamiento sobre una arquitectura inadecuada no resuelve el problema global, y un diseno correcto sin capacidades suficientes puede incumplir requisitos de trafico, retardo o disponibilidad."""

    if "requisitos de negocio" in q:
        return f"""{number}. Respuesta orientativa:
Los requisitos de negocio expresan que necesita la organizacion: continuidad del servicio, reduccion de costes, crecimiento, movilidad, seguridad o soporte a nuevas aplicaciones. En DDR esos requisitos se traducen en requisitos tecnicos medibles, como disponibilidad, capacidad, latencia maxima, cobertura, redundancia o restricciones presupuestarias.

Por ejemplo, si el negocio exige operacion 24/7, el diseno debe incluir alta disponibilidad, rutas alternativas y equipos redundantes. Si el objetivo principal es contener costes, el dimensionamiento debe equilibrar prestaciones y CAPEX/OPEX."""

    if "disponibilidad" in q and ("sla" in q or "mtbf" in q or "mttr" in q):
        return f"""{number}. Respuesta orientativa:
La disponibilidad mide la proporcion de tiempo en que la red puede prestar el servicio requerido. En un proyecto de DDR suele expresarse mediante SLA y condiciona decisiones de redundancia, proteccion, eleccion de equipos y mantenimiento.

MTBF representa el tiempo medio entre fallos y MTTR el tiempo medio de reparacion. Una disponibilidad alta se obtiene aumentando MTBF, reduciendo MTTR o introduciendo redundancia para que un fallo no interrumpa el servicio. El inconveniente es que la redundancia aumenta coste, consumo y complejidad, por lo que debe compararse con el impacto economico de una parada."""

    if "infraestructura fisica" in q and "logica" in q:
        return f"""{number}. Respuesta orientativa:
La infraestructura fisica describe los elementos reales de la red: enlaces, equipos, ubicaciones, salas, cableado y capacidades instaladas. La dimension logica describe como se organizan los servicios sobre esa infraestructura: direccionamiento, VLAN, dominios, politicas, rutas y separacion de usuarios o aplicaciones.

Separarlas permite detectar si un problema viene de limitaciones fisicas o de una mala organizacion logica. Tambien evita proponer cambios de capacidad cuando bastaria reorganizar la red, o cambios logicos cuando el cuello de botella es fisico."""

    if "matriz de trafico" in q:
        return f"""{number}. Respuesta orientativa:
Una matriz de trafico indica la demanda entre pares origen-destino, normalmente en unidades de caudal como Mbps o Gbps. Cada elemento h_sd representa cuanto trafico debe cursarse desde el nodo s hasta el nodo d.

En DDR sirve para transformar necesidades de usuarios y aplicaciones en cargas sobre rutas y enlaces. Combinada con el encaminamiento, permite calcular la carga agregada por enlace y, a partir de ella, decidir capacidades, modulos o restricciones de utilizacion."""

    if "flujo-camino-demanda" in q or "restriccion de capacidad" in q:
        return f"""{number}. Respuesta orientativa:
En una formulacion flujo-camino-demanda se parte de demandas h_d, caminos candidatos p para cada demanda d y una matriz de incidencia que indica si el camino p usa el enlace e. Las variables suelen ser x_dp, flujo asignado de la demanda d al camino p, y en problemas de dimensionamiento tambien variables de capacidad o modulos por enlace.

La conservacion de demanda exige que la suma de flujos asignados a los caminos de cada demanda sea igual a h_d. La restriccion de capacidad impone que la suma de todos los flujos que atraviesan un enlace no supere su capacidad instalada. La salida esperada es la asignacion de flujos, la capacidad necesaria por enlace y el coste o congestion resultante."""

    if "programabilidad" in q and "manual" in q:
        return f"""{number}. Respuesta orientativa:
La programabilidad permite gestionar la red mediante APIs, controladores y automatizacion, en lugar de configurar cada dispositivo manualmente. Esto reduce errores, acelera despliegues y facilita aplicar politicas coherentes en toda la infraestructura.

Frente al enfoque manual, tambien permite adaptar configuraciones a cambios de trafico o requisitos de servicio de forma mas rapida, integrando la red con sistemas de orquestacion, telemetria y control."""

    if "direccionamiento" in q and ("dhcp" in q or "dinamico" in q or "estatico" in q):
        return f"""{number}. Respuesta orientativa:
El direccionamiento estatico asigna direcciones fijas de forma manual o controlada. Es adecuado para servidores, routers, firewalls, impresoras o equipos que deben ser localizables siempre en la misma direccion. Sus ventajas son previsibilidad, facilidad para aplicar reglas de seguridad y trazabilidad. Sus inconvenientes son la baja escalabilidad, el riesgo de errores manuales y la dificultad de gestion cuando hay muchos dispositivos.

El direccionamiento dinamico, mediante DHCP o SLAAC, automatiza la asignacion de direcciones. Es adecuado para usuarios finales, aulas, laboratorios, movilidad y redes con alta rotacion de equipos. Sus ventajas son escalabilidad, menor administracion manual y reutilizacion eficiente del espacio de direcciones. Sus inconvenientes son la dependencia del servicio de asignacion, la necesidad de medidas de seguridad como DHCP snooping y una trazabilidad que debe apoyarse en logs.

En una red empresarial moderna suele recomendarse un enfoque hibrido: direcciones estaticas o reservas para infraestructura critica y direccionamiento dinamico para equipos de usuario."""

    if "telemetry" in q or "telemetria" in q:
        return f"""{number}. Respuesta orientativa:
Network Telemetry consiste en recoger de forma continua y automatizada informacion operativa de la red, como utilizacion de enlaces, latencia, perdidas, errores, estado de colas o eventos de dispositivos. Frente a una monitorizacion manual o puntual, permite disponer de una vision casi en tiempo real del comportamiento de la infraestructura.

En redes autonomas, la telemetria alimenta los sistemas de analisis y control. Con esos datos se pueden detectar congestiones, anticipar fallos, ajustar rutas, activar politicas de calidad de servicio o lanzar acciones correctivas automaticamente. Por tanto, es un elemento clave para cerrar el ciclo medir-analizar-actuar."""

    if "intent based" in q or "ibn" in q or "programabilidad" in q or "programmability" in q:
        return f"""{number}. Respuesta orientativa:
Intent Based Networking permite expresar objetivos de alto nivel, como garantizar una latencia maxima, aislar un tipo de trafico o asegurar disponibilidad, y traducirlos automaticamente a politicas de configuracion y control sobre la red.

La programabilidad es la capacidad que permite esa traduccion: controladores, APIs y mecanismos de automatizacion convierten la intencion en reglas de encaminamiento, QoS, segmentacion o reserva de recursos. Despues, la telemetria permite comprobar si la red cumple la intencion y reajustar la configuracion si aparecen desviaciones."""

    if "colas" in q or "optimizacion" in q:
        return f"""{number}. Respuesta orientativa:
La teoria de colas es adecuada para estudiar el comportamiento de recursos individuales sometidos a trafico aleatorio, por ejemplo un enlace o servidor. Permite estimar retardo, espera, ocupacion o probabilidad de congestion a partir de tasas de llegada y servicio.

La optimizacion de red es necesaria cuando el problema afecta a varios enlaces, rutas y demandas simultaneamente. En ese caso no basta con dimensionar un enlace aislado: hay que decidir capacidades, rutas o modulos minimizando coste o congestion y respetando restricciones globales. Ambas tecnicas son complementarias: la teoria de colas analiza prestaciones locales y la optimizacion decide el diseno global."""

    if "camino" in q or "dijkstra" in q or "bellman" in q or "ruta" in q:
        return f"""{number}. Respuesta orientativa:
El calculo de caminos en redes suele modelarse como un problema de camino minimo sobre un grafo ponderado, donde los nodos representan equipos o ubicaciones y los enlaces tienen pesos asociados a coste, retardo, distancia, utilizacion o una combinacion de metricas.

Si los pesos son no negativos, Dijkstra es una opcion eficiente y habitual. Bellman-Ford es mas general y permite pesos negativos, aunque es menos eficiente y se usa sobre todo cuando esa generalidad es necesaria. Si ademas existen restricciones de capacidad o multiples demandas, el problema puede requerir una formulacion de flujo u optimizacion de red en lugar de un simple camino minimo."""

    return f"""{number}. Respuesta orientativa:
La respuesta debe identificar los conceptos principales de la pregunta, relacionarlos con el diseno y dimensionado de redes, justificar la tecnica o decision propuesta y mencionar sus limitaciones. En una respuesta completa se valoran la precision terminologica, la conexion con requisitos de capacidad/prestaciones y la claridad al distinguir entre decisiones locales y decisiones globales de diseno."""


def _fallback_solution_1_to_3(exam_text: str) -> str:
    parts = []
    for number in (1, 2, 3):
        parts.append(_fallback_solution_for_question(number, _extract_question(exam_text, number)))
    return "\n\n".join(parts)


def build_exam_prompt(
    question: str,
    context: str,
    include_solution: bool = False,
    profile: dict | None = None,
) -> str:
    profile = profile or select_exam_profile(question)
    solution_rule = (
        "Devuelve solo las preguntas 1, 2 y 3. No incluyas el solucionario."
        if not include_solution
        else "Devuelve solo las preguntas 1, 2 y 3. El ejercicio 4 y el solucionario se generaran en pasos controlados."
    )
    return f"""
Eres un profesor experto en Diseno y Dimensionado de Redes (DDR).

Genera las preguntas 1, 2 y 3 de un EXAMEN NUEVO a partir del CONTEXTO.
Debe parecer un examen real de convocatorias anteriores, pero no debe copiar
literalmente ningun examen.

REGLAS DE SALIDA:
1) {solution_rule}
2) Escribe exactamente 3 preguntas numeradas 1, 2 y 3.
3) Las preguntas deben ser teoricas o de razonamiento breve.
4) No generes la pregunta 4.
5) No uses preguntas genericas como "siguientes entrevistas" ni contenido fuera de DDR.
6) Reparte la puntuacion como 0.5, 0.5 y 1.0 puntos.
7) No expliques tus decisiones fuera del examen.
8) Termina todas las frases y no dejes apartados vacios.
9) Usa obligatoriamente el PERFIL TEMATICO indicado. Puedes reformular la
   redaccion, pero no cambies el tema central de cada pregunta.
10) Evita repetir literalmente preguntas ya generadas en ejecuciones anteriores.

CHECKLIST ANTES DE RESPONDER:
- Hay exactamente 3 preguntas.
- No aparece una pregunta 4.
- No hay variantes por DNI.
- No hay solucionario en este paso.

{profile_guidance(profile)}

CONTEXTO:
{context}

PETICION ORIGINAL:
{question}
""".strip()


def build_solution_prompt(question: str, context: str, exam_text: str) -> str:
    return f"""
Eres un profesor experto en Diseno y Dimensionado de Redes (DDR).

Redacta el SOLUCIONARIO de las preguntas 1, 2 y 3 del examen siguiente. Usa el
CONTEXTO y el ENUNCIADO como fuentes principales. No resuelvas la pregunta 4:
su solucion exacta se anadira automaticamente.

REGLAS:
1) Empieza directamente con "1. Respuesta orientativa:".
2) Responde solo las preguntas 1, 2 y 3 con el mismo numero que en el examen.
3) Las respuestas 1, 2 y 3 deben ser claras, evaluables y ajustadas a DDR.
4) No incluyas titulo, introduccion ni una linea que diga SOLUCIONARIO.
5) No incluyas una seccion 4.
6) No escribas un script .m completo.
7) No contradigas los datos del examen.
8) Termina todas las soluciones.

CONTEXTO:
{context}

ENUNCIADO DEL EXAMEN:
{exam_text}

PETICION ORIGINAL:
{question}
""".strip()


def build_single_pass_prompt(question: str, context: str) -> str:
    if is_exam_generation_with_solution_request(question):
        variant = select_question_4_variant(question)
        profile = select_exam_profile(question)
        return f"""
Eres un profesor experto en Diseno y Dimensionado de Redes (DDR).

Genera un EXAMEN NUEVO y despues su SOLUCIONARIO. Usa el CONTEXTO como guia,
pero no copies literalmente examenes anteriores.

REGLAS:
1) La salida debe tener dos secciones: EXAMEN y SOLUCIONARIO.
2) El examen debe tener exactamente 4 preguntas numeradas 1, 2, 3 y 4.
3) Las preguntas 1, 2 y 3 deben ser teoricas o de razonamiento breve.
4) La pregunta 4 debe ser exactamente la plantilla canonica incluida abajo.
5) En el solucionario, responde cada pregunta con el mismo numero.
6) En la pregunta 4, usa exactamente la solucion canonica incluida abajo.
7) Las preguntas 1, 2 y 3 deben seguir el perfil tematico indicado.

CONTEXTO:
{context}

{profile_guidance(profile)}

PREGUNTA 4 CANONICA:
{canonical_question_4(variant)}

SOLUCION CANONICA DE LA PREGUNTA 4:
{canonical_question_4_solution(variant)}

PETICION ORIGINAL:
{question}
""".strip()
    return build_exam_prompt(question, context, include_solution=False)


def _call_step(
    call_llm: Callable[[str, int, bool], dict],
    prompt: str,
    budget: int,
    print_tokens: bool,
) -> str:
    data = call_llm(prompt, budget, print_tokens=print_tokens)
    return (data.get("response") or "").strip()


def generate_exam_answer(
    question: str,
    context: str,
    call_llm: Callable[[str, int, bool], dict],
    print_tokens: bool = False,
) -> str:
    """Genera el examen. Si se pide solucionario, lo hace en dos pasos."""
    wants_solution = is_exam_generation_with_solution_request(question)
    variant = select_question_4_variant(question)
    profile = select_exam_profile(question)

    if not wants_solution:
        generated = _call_step(
            call_llm,
            build_exam_prompt(question, context, include_solution=False, profile=profile),
            exam_only_budget(),
            print_tokens=False,
        )
        questions_1_to_3 = _sanitize_exam_questions_1_to_3(generated)
        if force_profile_questions() or not _has_questions_1_to_3(questions_1_to_3):
            questions_1_to_3 = profile_questions_1_to_3(profile)
        exam = f"{questions_1_to_3}\n\n{canonical_question_4(variant)}".strip()
        answer = f"EXAMEN\n\n{exam}".strip()
        if print_tokens:
            print(answer, end="", flush=True)
        return answer

    generated_exam = _call_step(
        call_llm,
        build_exam_prompt(question, context, include_solution=True, profile=profile),
        exam_only_budget(),
        print_tokens=False,
    )
    questions_1_to_3 = _sanitize_exam_questions_1_to_3(generated_exam)
    if force_profile_questions() or not _has_questions_1_to_3(questions_1_to_3):
        questions_1_to_3 = profile_questions_1_to_3(profile)
    exam = f"{questions_1_to_3}\n\n{canonical_question_4(variant)}".strip()

    solution_1_to_3 = _call_step(
        call_llm,
        build_solution_prompt(question, context, exam),
        exam_solution_budget(),
        print_tokens=False,
    )
    cleaned_solution_1_to_3 = _sanitize_solution_1_to_3(solution_1_to_3)
    if not _find_question_heading(cleaned_solution_1_to_3, 1):
        cleaned_solution_1_to_3 = _fallback_solution_1_to_3(exam)

    solution = (
        f"{cleaned_solution_1_to_3}\n\n"
        f"{canonical_question_4_solution(variant)}"
    ).strip()

    answer = f"EXAMEN\n\n{exam}\n\nSOLUCIONARIO\n\n{solution}".strip()
    if print_tokens:
        print(answer, end="", flush=True)
    return answer
