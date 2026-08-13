# PRD — Agente de asistencia para consultas de negocio y herramientas básicas

## 1. Visión y problema

### Hechos proporcionados
- El repositorio es un template del diplomado IA Aplicada al Desarrollo de Software.
- El contexto narrativo del proyecto es Greenfield para LegacyPay, con coexistencia de un monolito legado.
- El repositorio incluye un agente ReAct, herramientas propias y datos de ejemplo de comerciantes y transacciones.
- El agente actual ya cuenta con herramientas para cálculo y consulta de comerciantes, y con un mecanismo para identificar acciones que requieren aprobación humana.

### Propuesta
- El producto debe permitir que un usuario formule consultas en lenguaje natural y reciba respuestas útiles, apoyadas por herramientas y datos de ejemplo del dominio LegacyPay.
- El producto debe ofrecer trazabilidad del proceso de razonamiento y ejecución, de modo que sea comprensible para un operador humano.
- El producto debe poder detenerse de forma explícita cuando una acción sensible requiera confirmación humana, sin ejecutar la acción automáticamente.

## 2. Alcance incluido y fuera de alcance

### Alcance incluido
- Soporte para un agente que reciba un objetivo en lenguaje natural.
- Uso de herramientas registradas para resolver tareas concretas.
- Soporte inicial para:
  - consulta de información de comerciantes,
  - ejecución de cálculos básicos,
  - registro de pasos del ciclo Reason → Act → Observe.
- Identificación de acciones sensibles que requieren aprobación humana antes de ejecutarse.

### Fuera de alcance
- Integración con sistemas reales de LegacyPay o con servicios externos productivos.
- Implementación completa de flujos de negocio de alto riesgo o de escritura operativa.
- Definición de políticas de seguridad, roles autorizados o límites regulatorios no especificados en el repositorio.
- Definición de SLA, volúmenes de uso o métricas de operación no aportadas por el contexto.

## 3. Usuarios, entidades y reglas de negocio

### Usuarios
- Usuario del agente: persona que escribe una consulta en lenguaje natural para obtener información o ejecutar una tarea simple.
- Operador humano: persona que revisa y aprueba acciones que el agente identifica como sensibles.

### Entidades
- Merchant: entidad representada por los datos de ejemplo del archivo de comerciantes. Se utilizan campos como merchant_id, name, category, status, daily_limit_usd, monthly_volume_usd, risk_level, pci_compliant, onboarded_at y avg_transaction_7d_usd.
- Transaction: entidad representada por los datos de ejemplo de transacciones. Se utilizan campos como transaction_id, merchant_id, amount_usd, timestamp, status, flag_reason e incident_ref.

### Reglas de negocio
- El agente debe responder con un formato estructurado válido para que el flujo de ejecución sea interpretable.
- Si una acción requiere aprobación humana, el agente debe detenerse y comunicarlo explícitamente.
- El agente debe usar herramientas disponibles para ejecutar tareas concretas en lugar de responder únicamente con texto general.
- Los datos usados en este alcance provienen de los ejemplos incluidos en el repositorio y no de una fuente productiva.

## 4. Historias de usuario con criterios de aceptación

### Historia 1 — Consultar información de un comerciante
- Como usuario del agente, quiero consultar los datos básicos de un comerciante mediante su identificador, para obtener información relevante sin revisar manualmente el archivo de datos.

#### Criterios de aceptación
- Si el comerciante existe en los datos disponibles, la respuesta debe incluir la información correspondiente del registro.
- Si el comerciante no existe, la respuesta debe indicar que no se encontró información para ese identificador.
- La respuesta debe ser comprensible y estar basada en los datos proporcionados.

### Historia 2 — Ejecutar un cálculo simple
- Como usuario del agente, quiero pedir una operación aritmética sencilla, para obtener el resultado sin usar otra herramienta manualmente.

#### Criterios de aceptación
- El agente debe usar la herramienta de cálculo disponible cuando la consulta lo requiera.
- La respuesta debe devolver el resultado de la operación solicitada.
- Si la entrada no es válida, el agente debe informar el error de forma clara.

### Historia 3 — Detener una acción sensible
- Como operador humano, quiero que el agente identifique acciones sensibles y se detenga antes de ejecutarlas, para conservar control sobre operaciones críticas.

#### Criterios de aceptación
- Si la acción seleccionada está en la lista de acciones que requieren aprobación, el agente debe detenerse.
- La respuesta debe indicar que la acción requiere aprobación humana.
- No debe ejecutar la acción automáticamente.

## 5. Restricciones no funcionales

### Hechos proporcionados
- El entorno de desarrollo actual usa Python, FastAPI, Streamlit, pytest y un mock local de LLM.
- El agente ya implementa un límite de pasos para evitar bucles infinitos.

### Propuesta
- El flujo debe ser ejecutable en el entorno de desarrollo del repositorio sin requerir dependencias adicionales no justificadas.
- La ejecución debe mantener trazabilidad suficiente para inspeccionar el razonamiento y la observación de cada paso.
- El sistema debe manejar respuestas inválidas del modelo sin bloquear el flujo de forma inesperada.
- No se definen SLA, volúmenes ni exigencias regulatorias en este PRD porque no están especificadas en el contexto.

## 6. Preguntas abiertas
- PREGUNTA ABIERTA: ¿Qué roles específicos están autorizados para cada acción sensible del producto?
- PREGUNTA ABIERTA: ¿Qué consultas de negocio deben priorizarse en una siguiente iteración del agente?
- PREGUNTA ABIERTA: ¿Qué datos del dominio LegacyPay deben exponerse en una versión posterior si se integra con una fuente de verdad real?
- PREGUNTA ABIERTA: ¿Qué nivel de detalle de trazabilidad necesita el operador humano para revisar las decisiones del agente?
