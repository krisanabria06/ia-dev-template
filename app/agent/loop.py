"""Loop ReAct para responder consultas basadas en el PRD."""

from __future__ import annotations

import json
import os
from typing import Any

from app.agent.logger import log_step
from app.agent.tools import TOOLS_SCHEMA, buscar_regla_prd

MAX_STEPS = 5
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
SYSTEM_PROMPT = """Sos un agente RAG del Historial de Transacciones LegacyPay.
Solo respondés sobre las reglas contenidas en el PRD; si te preguntan otra cosa,
decís exactamente 'fuera de alcance'. No ejecutás acciones destructivas y no
inventás resultados. Usá la tool buscar_regla_prd para recuperar evidencia.
En cada turno respondé únicamente JSON válido con las claves thought, action y
action_input. action debe ser 'buscar_regla_prd' o 'final'. Si action es 'final',
action_input debe tener la clave 'respuesta'.
"""


def _parse_decision(raw: str) -> tuple[str, dict[str, Any]]:
    """Valida la decisión JSON del LLM y sus acciones permitidas."""
    try:
        decision = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("El LLM no devolvió JSON válido.") from error
    if not isinstance(decision, dict):
        raise ValueError("La decisión del LLM debe ser un objeto JSON.")
    action = decision.get("action")
    action_input = decision.get("action_input", {})
    if action not in {"buscar_regla_prd", "final"}:
        raise ValueError(f"Acción no permitida: {action!r}.")
    if not isinstance(action_input, dict):
        raise ValueError("action_input debe ser un objeto JSON.")
    if action == "buscar_regla_prd" and not isinstance(
        action_input.get("termino"), str
    ):
        raise ValueError("buscar_regla_prd requiere action_input.termino.")
    if action == "final" and not isinstance(action_input.get("respuesta"), str):
        raise ValueError("final requiere action_input.respuesta.")
    return action, action_input


def run_agent(query: str, llm_client: Any) -> str:
    """Ejecuta el loop ReAct hasta obtener una respuesta o agotar el presupuesto."""
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    for step in range(1, MAX_STEPS + 1):
        response = llm_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=TOOLS_SCHEMA,
            temperature=0,
        )
        raw = response.choices[0].message.content or ""
        try:
            action, action_input = _parse_decision(raw)
        except ValueError as error:
            return f"Error de decisión del agente: {error}"

        if action == "final":
            return str(action_input["respuesta"])

        result = buscar_regla_prd(action_input["termino"])
        log_step(step, action, action_input, result)
        messages.extend(
            [
                {"role": "assistant", "content": raw},
                {"role": "user", "content": f"Observation: {result}"},
            ]
        )

    return "Error: se alcanzó MAX_STEPS sin una respuesta final."
