# AI_USAGE.md · Proyecto Final

## Entrada 1 · 2026-08-25

**Contexto:** generación del esqueleto del agente en `app/agent/`.
**Herramienta IA:** GitHub Copilot.
**Prompt clave:** crear un agente RAG con tools, loop ReAct y logger.
**Decisión IA:** propuso el loop, `TOOLS_SCHEMA` y el registro de pasos.
**Decisión humana:** acepté con ajustes y revisé las acciones permitidas.
**Aprendizaje:** declarar el patrón ReAct en el prompt orienta la estructura de salida.

## Entrada 2 · 2026-08-25

**Contexto:** definición del alcance del agente.
**Herramienta IA:** GitHub Copilot.
**Prompt clave:** restringir respuestas al PRD de Historial de Transacciones.
**Decisión IA:** propuso un `SYSTEM_PROMPT` con una respuesta para fuera de alcance.
**Decisión humana:** acepté el scope explícito y verifiqué el comportamiento con el mock.
**Aprendizaje:** el scope debe ser una regla visible y comprobable, no una suposición.

## Entrada 3 · 2026-08-27

**Contexto:** actualización de dependencias para usar el SDK OpenAI.
**Herramienta IA:** GitHub Copilot.
**Prompt clave:** actualizar `pyproject.toml`, ejecutar `uv lock` y `uv sync`.
**Decisión IA:** recomendó promover `openai` a dependencia principal.
**Decisión humana:** acepté porque el Eval Set importa `OpenAI` sin extras opcionales.
**Aprendizaje:** las dependencias declaradas deben reflejar el camino de ejecución real.

## Entrada 4 · 2026-08-27

**Contexto:** creación del Eval Set.
**Herramienta IA:** GitHub Copilot.
**Prompt clave:** crear tres casos de outcome y scope contra el mock LLM.
**Decisión IA:** generó `evals/eval_agent.py` con resultado por caso y total.
**Decisión humana:** ajusté el path para que funcione con `python evals/eval_agent.py`.
**Aprendizaje:** un script de evaluación debe poder ejecutarse exactamente como está documentado.

## Entrada 5 · 2026-08-27

**Contexto:** fallo del retriever ante preguntas en lenguaje natural.
**Herramienta IA:** GitHub Copilot.
**Prompt clave:** hacer robusta la búsqueda lexical sin perder la abstención.
**Decisión IA:** propuso palabras significativas y alias para las reglas del PRD.
**Decisión humana:** acepté tras comprobar que pasan 2/3 casos y Francia sigue fuera de alcance.
**Aprendizaje:** los evals revelan contratos implícitos entre el mock, el retriever y el prompt.
