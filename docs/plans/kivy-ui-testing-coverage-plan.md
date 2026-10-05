# Kivy UI Testing Coverage — Implementation Plan

## Objective and source

Implementar `specs/kivy-ui-testing-coverage.md` con Kivy real bajo Xvfb,
conservando los checks de backend/web. Tracking: #105, part of #81.

Contexto: `AGENTS.md`, `docs/ai-assisted-workflow.md`, `docs/roadmap.md`,
`docs/specs.md`, `docs/project-journal/post-mvp-touch-ui.md`,
`specs/kivy-ui-docker-emulation.md` y `specs/raspberry-touch-ui.md`.

## Implementation

1. Confirmar rama y estado; preservar el trabajo previo. Crear/reutilizar #105.
2. Comprobar proveedores instalados y construir un widget real en ui-emulator.
   La comprobación ha confirmado SDL2, Xvfb y xauth; no hay window_headless.
3. Retirar el hook Kivy global de conftest. Sustituir mocks de Kivy y pruebas
   basadas en __new__ por constructores reales en los dos módulos de tests.
4. Cubrir estados, destinos de animación, cancelación de eventos, configuración,
   bindings, guards y callbacks de UI. Simular únicamente audio/HTTP/workers.
   Avanzar Clock para callbacks/animaciones y cancelar eventos en teardown.
5. Ejecutar test ui en ui-emulator con xvfb-run y un volumen temporal para
   /tmp/.X11-unix que sustituya el socket del host. Configurar SDL2, Mesa software,
   audio/clipboard dummy, KIVY_NO_ARGS y directorios temporales en el script.
   Preparar permisos 1777 del socket en client/Dockerfile.ui y reconstruir la
   imagen desde el target. Conservar un padre Bash para xvfb-run y propagar el
   resultado de pytest; ejecutarlo como PID 1 bloquea la señal de arranque.
6. Excluir los dos módulos UI de test python; ejecutar python → ui → web en
   test all. Actualizar ayuda e instrucciones de pruebas.
7. Ejecutar test all, build web, bash -n y git diff --check. Registrar resultados
   reales en el diario y cambiar el estado de la spec solo tras verificar.
8. Preparar commit Conventional Commit y PR referenciando #105 y Part of #81.
   No cerrar la épica ni implementar #88.

## Acceptance and verification

Los tests deben fallar si los constructores leen mal la URL, si se elimina un
binding, si los callbacks arrancan un worker cuando la UI está ocupada o si las
animaciones/eventos no respetan los estados. No comparar píxeles ni depender de
hardware/proveedores. No cambiar código de producto ni añadir dependencias.

```bash
./tonto.sh test ui
./tonto.sh test all
./tonto.sh build web
bash -n tonto.sh
git diff --check
git status --short --branch
```

## Implementation prompt

```text
Complete specs/kivy-ui-testing-coverage.md on feature/kivy-ui-testing-coverage.
Read AGENTS.md, the required current-state docs, ai-assisted-workflow, the spec
and this plan. Check branch/status before writes. Preserve inherited changes.
Use real Kivy widgets in the existing ui-emulator with SDL2/Xvfb and an isolated
X11 socket volume. Do not mock Kivy or bypass constructors. Test state targets,
event cleanup, constructors, environment configuration and interaction callbacks.
Mock external audio/HTTP and worker execution only, at their usage location.
Do not edit product code or introduce dependencies. Keep test python independent
of Kivy display and include test ui in test all. Run the official commands above,
record evidence and prepare a focused commit/PR for #105, Part of #81.
Report any checks that cannot run. Raspberry kiosk validation remains #88.
```

## Workflow isolation

Una rama y una PR para esta cobertura; sin agentes paralelos. Si main cambia,
reconciliar antes de integrar. Archivos compartidos: tonto.sh y documentación.
