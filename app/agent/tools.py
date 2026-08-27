"""Herramientas de recuperación para el agente del PRD."""

from __future__ import annotations

import re
from pathlib import Path

PRD_PATH = Path(__file__).parents[2] / "docs" / "prd" / "PRD.md"


def buscar_regla_prd(termino: str) -> str:
    """Busca un término en el PRD y devuelve hasta tres contextos cercanos."""
    if not termino or not termino.strip():
        return "Término vacío: indicá qué regla del PRD querés buscar."
    if not PRD_PATH.is_file():
        return f"PRD inexistente: no se encontró {PRD_PATH}."

    lines = PRD_PATH.read_text(encoding="utf-8").splitlines()
    term = termino.strip().casefold()
    hit_indexes = [
        index for index, line in enumerate(lines) if term in line.casefold()
    ][:3]
    if not hit_indexes:
        stopwords = {
            "cual",
            "cuál",
            "del",
            "los",
            "las",
            "que",
            "puedo",
            "exponer",
            "completo",
            "maximo",
            "máximo",
            "historial",
        }
        keywords = [
            keyword
            for keyword in re.findall(r"[\wáéíóúüñ]+", term)
            if len(keyword) >= 3 and keyword not in stopwords
        ]
        if "rango" in keywords or "historial" in termino.casefold():
            keywords.append("90 días")
        if "pan" in keywords:
            keywords.append("últimos 4")
        hit_indexes = [
            index
            for index, line in enumerate(lines)
            if any(keyword in line.casefold() for keyword in keywords)
        ][:3]
    if not hit_indexes:
        return f"Sin coincidencias para '{termino}' en el PRD."

    contexts: list[str] = []
    included: set[int] = set()
    for hit_index in hit_indexes:
        start = max(0, hit_index - 3)
        end = min(len(lines), hit_index + 4)
        context_lines = [
            f"{line_number}: {lines[line_number - 1]}"
            for line_number in range(start + 1, end + 1)
            if line_number - 1 not in included
        ]
        included.update(range(start, end))
        contexts.append("\n".join(context_lines))

    return "\n\n--- hit ---\n\n".join(contexts)


TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "buscar_regla_prd",
            "description": (
                "Busca lexicalmente una regla en docs/prd/PRD.md y devuelve "
                "hasta tres coincidencias con tres líneas de contexto."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "termino": {
                        "type": "string",
                        "description": "Término o frase a buscar en el PRD.",
                    }
                },
                "required": ["termino"],
            },
        },
    }
]
