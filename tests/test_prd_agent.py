from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from app.agent.loop import run_agent
from app.agent.tools import buscar_regla_prd


class FakeCompletions:
    def __init__(self, contents: list[str]) -> None:
        self.contents = iter(contents)

    def create(self, **_: object) -> SimpleNamespace:
        content = next(self.contents)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
        )


class FakeClient:
    def __init__(self, contents: list[str]) -> None:
        self.chat = SimpleNamespace(completions=FakeCompletions(contents))


def decision(action: str, action_input: dict[str, str]) -> str:
    return json.dumps({"thought": "test", "action": action, "action_input": action_input})


def test_agent_returns_final_answer() -> None:
    client = FakeClient([decision("final", {"respuesta": "respuesta"})])
    assert run_agent("pregunta", client) == "respuesta"


def test_agent_uses_prd_evidence() -> None:
    client = FakeClient(
        [
            decision("buscar_regla_prd", {"termino": "90 días"}),
            decision("final", {"respuesta": "respuesta basada en evidencia"}),
        ]
    )
    assert "evidencia" in run_agent("rango", client)
    assert "90 días" in buscar_regla_prd("rango máximo del historial")


@pytest.mark.parametrize("raw", ["no json", json.dumps({"action": "other"})])
def test_agent_rejects_invalid_decision(raw: str) -> None:
    assert "Error de decisión" in run_agent("pregunta", FakeClient([raw]))


def test_agent_stops_at_step_budget() -> None:
    raw = decision("buscar_regla_prd", {"termino": "90 días"})
    assert "MAX_STEPS" in run_agent("pregunta", FakeClient([raw] * 5))
