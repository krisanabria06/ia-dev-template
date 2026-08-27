# Postmortem · Proyecto Final · 2026-08-27

## Qué funcionó

- El retriever lexical alcanzó el scope mínimo del Eval Set y recuperó las reglas de 90 días y PAN enmascarado.
- La separación entre loop ReAct, tool y logger permitió diagnosticar el flujo con pasos auditables.
- El mock LLM determinista hizo reproducibles las pruebas sin depender de una API real.

## Qué no funcionó

- La versión actual del PRD no contenía inicialmente las reglas que el Eval Set esperaba.
- El retriever exigía coincidencia literal y no entendía preguntas naturales completas.
- El caso adversarial espera el texto `Sin coincidencias`, mientras el mock responde `fuera de alcance`; por eso el resultado final es 2/3.

## Qué haría distinto

- Definiría el PRD canónico y el contrato de respuestas antes de escribir los evals.
- Agregaría tests unitarios del retriever para frases, sinónimos y consultas fuera de alcance.

## 3 lecciones aprendidas

1. **Sobre agentes:** el scope y el presupuesto deben ser visibles en el prompt y en el loop.
2. **Sobre RAG:** un retriever lexical alcanza para un dominio pequeño, pero necesita normalización y alias bien definidos.
3. **Sobre trabajo con IA:** ejecutar cada comando de validación descubre desajustes que una lectura superficial no muestra.
