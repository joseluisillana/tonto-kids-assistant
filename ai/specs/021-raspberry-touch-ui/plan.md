# Raspberry Touch UI Implementation Plan

## Objective

Proveer un plan de ejecución detallado para implementar el spec `ai/specs/021-raspberry-touch-ui/spec.md`, dotando a la Raspberry Pi de una interfaz visual táctil con cara animada y manteniendo el rol de "thin client".

## Source Spec

- Spec: `ai/specs/021-raspberry-touch-ui/spec.md`
- Related docs:
  - `docs/specs.md`
  - `docs/roadmap.md`
  - `docs/future-work.md`
  - `docs/hardware.md` (a crear/actualizar durante Fase 1)

## Scope

Included:
- Configuración física de la pantalla Waveshare 5".
- Spikes de tecnología para elegir el stack de renderizado de UI y motor para la cara animada.
- Fase de diseño conceptual de la cara (generación de imágenes / selección de referencias).
- Implementación de un cliente ligero que mantenga el contrato actual de STT/TTS (`POST /chat/audio`).
- Modo texto ocultable.
- Kiosk mode al arranque de la Raspberry.
- Creación de issues de tracking en GitHub (Fase 0).

Excluded:
- Reescritura del backend a otro lenguaje/framework.
- Cloud deployment.
- Integración de wake word u otras formas de hardware (ej. LEDs/Arduino) en este flujo de trabajo.

## Implementation Plan

1. **Fase 0:** Ejecutar `gh issue create` para crear el Parent Issue y los 7 Phase Issues listados en la spec. Linkearlos en los PRs.
2. **Fase 1:** Seguir instrucciones del operador humano para la conexión del hardware. Validar HDMI y touch. Documentar comandos en `docs/hardware.md`.
3. **Fase 2:** Crear un script de prueba rápida o esqueleto web/local en la Raspberry Pi. Validar los FPS y uso de CPU. Tomar y registrar la decisión en `docs/decisions.md`.
4. **Fase 3:** Proponer y elegir el diseño visual de la cara (imágenes estáticas generadas o recolectadas como referencia visual del estilo gráfico).
5. **Fase 4:** Seleccionar librería técnica (ej. CSS, Canvas, Pygame, Tkinter) de acuerdo a la Fase 2, y programar la animación de los estados de la cara basada en el diseño visual.
6. **Fase 5:** Armar la UI principal interactiva con botón de "Hablar". Conectar la captura de audio y envío al backend. Añadir botón toggle para modo texto.
7. **Fase 6:** Sincronizar el estado del cliente (idle, recording, uploading, speaking) con la cara animada de la Fase 4.
8. **Fase 7:** Automatizar el arranque en `.config/autostart/` o como servicio `systemd`. Validar que el script `main.py` de terminal siga sirviendo de fallback.

## Acceptance Criteria

- El Parent Issue y Phase Issues existen en GitHub.
- La pantalla táctil reacciona adecuadamente y los componentes están documentados para reemplazo/reproducción.
- La decisión del stack técnico es pública y justificada.
- Existe un diseño visual de referencia claro.
- El cliente permite grabar audio tocando la pantalla y devuelve respuesta audible.
- La cara cambia de estado visualmente.
- El texto es visible si el control opcional está activado.
- El sistema arranca directamente a la interfaz táctil sin teclado ni ratón.

## Verification

```bash
./tonto.sh test python
git status --short --branch
```
(Además, pruebas funcionales manuales en el hardware físico para cada fase).

## Implementation Prompt

```text
Implement the spec in specs/raspberry-touch-ui.md.

Before editing:
- Read AGENTS.md.
- Read docs/ai-assisted-workflow.md.
- Read the source spec and this implementation plan.
- Run git branch --show-current and git status --short --branch.

Task:
- Implement the next uncompleted phase described in the spec.
- Document any decisions and update the post-mvp-touch-ui.md journal.
- Commit the changes and open a PR referring to the corresponding Phase Issue in GitHub.

Verification:
- Run the applicable local tests or ask the user to run the hardware validation.

Delivery:
- Summarize changed files, behavior implemented, and validation status.
```

## Workflow Isolation

- Branch: `docs/raspberry-touch-ui-spec` (actual) y luego `feature/raspberry-touch-ui-phase-X` para las implementaciones.
- **Worktree (CRITICAL PARA AGENTES):** Si este trabajo se ejecuta en paralelo a otras especificaciones, el agente **DEBE** aislar la implementación creando un Git worktree dedicado (ej. `git worktree add ../tonto-worktrees/touch-ui-phase-X -b feature/raspberry-touch-ui-phase-X main`) tal y como indica `docs/ai-assisted-workflow.md`. Nunca operar en la misma rama o worktree que otro agente.
- Parallel-safe: La Fase 0 debe ejecutarse primero, luego el resto de forma estrictamente secuencial al depender fuertemente de validación de hardware y pruebas físicas.
- GitHub tracking: Requerido (Fase 0).

## Notes / Assumptions

- Asumimos que la Raspberry Pi 3 B+ tiene energía suficiente para la pantalla Waveshare 5" y el micrófono por USB sin reiniciar. Si se detectan caídas de tensión (lightning bolt symbol), se documentará la necesidad de un hub alimentado en la Fase 1.


## Migration provenance

Original source: `docs/plans/raspberry-touch-ui-implementation-plan.md` at baseline 818e88e. Relocated 2026-10-06;
original content/language retained with path references adjusted. Historical
commands, approvals and pending notes retain their original context.

## Record maintenance after migration

For future work, read [spec.md](spec.md), this plan and [journal.md](journal.md).
Revise the plan before implementation; preserve historical prompts as evidence,
not authorization to execute outdated commands. Mandatory root/common workflow,
Linux/Docker operation and D025 govern current work. Maintain the local journal
and synchronize definition status/updated with the parent INDEX.md in the same
change. No secrets, credentials, tokens, connection strings, PII or real customer
data; sensitive configuration uses parameter names only.
