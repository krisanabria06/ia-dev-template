"""Golden Set del agente RAG del Proyecto Final."""

from __future__ import annotations

import sys
from pathlib import Path

from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agent.loop import run_agent

CASES = [
    {
        "id": "rango-90-dias",
        "question": "¿cuál es el rango máximo del historial?",
        "expected_substring": "90 días",
    },
    {
        "id": "pan-solo-ultimos-4",
        "question": "¿puedo exponer el PAN completo?",
        "expected_substring": "últimos 4",
    },
    {
        "id": "fuera-de-alcance",
        "question": "¿cuál es la capital de Francia?",
        "expected_substring": "Sin coincidencias",
    },
]


def evaluate() -> None:
    """Ejecuta los casos del Golden Set contra el mock LLM local."""
    client = OpenAI(base_url="http://localhost:8001/v1", api_key="mock")
    passed = 0
    for case in CASES:
        result = run_agent(case["question"], client)
        ok = case["expected_substring"].casefold() in result.casefold()
        mark = "✅" if ok else "❌"
        status = "PASS" if ok else "FAIL"
        print(f"{mark} {case['id']}: {status}")
        if ok:
            passed += 1
    print(f"\n{passed}/{len(CASES)} casos pasaron")


if __name__ == "__main__":
    evaluate()
