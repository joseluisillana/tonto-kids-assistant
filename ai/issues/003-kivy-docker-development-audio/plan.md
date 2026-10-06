# Emulador Kivy en Docker — plan de investigación y reparación

## Objective and source record

Fuente: `ai/issues/003-kivy-docker-development-audio/issue.md`.
Leer issue.md, este plan y journal.md antes de actuar. Alcanzar desarrollo
gráfico y de voz reproducible en Docker, partiendo de main sin soluciones previas.

## Included and excluded scope

Incluye arranque Docker, acceso a pantalla/audio, captura PC, reproducción,
diagnóstico y estados de fallo, checks y documentación necesaria.
Excluye sustituir Docker por ejecución host, migrar framework UI, modificar
proveedores/backend sin evidencia, soporte Windows/macOS y funciones nuevas.

## Proposed steps

1. Establecer baseline limpio y registrar versiones, contexto Docker, daemon,
   límites del sandbox, servicio de audio y dispositivos. Examinar requisitos
   del emulador y contratos actuales antes de proponer cambios.
2. Reproducir captura fallida y aislar causas sin proveedor: enumeración de
   dispositivos, error concreto, selección de entrada, formato solicitado y
   duración. Separar captura, estados UI, HTTP y reproducción.
3. Evaluar acceso directo ALSA y acceso al servidor del escritorio según el
   entorno real. Comprobar bibliotecas/plugins, configuración, permisos,
   identidad y autenticación. No elegir una vía por la mera presencia de un socket.
4. Probar secuencialmente conexión utilizable, enumeración de entrada, WAV real
   de seis segundos y reproducción audible desde Docker. Mantener experimentos
   acotados, reversibles y sin cambios persistentes no aprobados.
5. Comparar alternativas por reproducibilidad, complejidad, dependencias,
   compatibilidad con el daemon elegido y efecto sobre Raspberry. Presentar
   opción recomendada, evidencia, limitaciones y permisos necesarios.
6. Tras resolver aprobaciones de dependencias/arquitectura, actualizar este
   plan y los contratos afectados antes de implementar el mínimo cambio.
7. Verificar arranque repetido, tres turnos reales, texto, errores y recuperación;
   mantener journal, metadata e índice sincronizados y preparar revisión.

## Affected files

Fase actual: solo este registro y `ai/issues/INDEX.md`.
Posibles archivos posteriores, sujetos al resultado: scripts/ui-emulator.sh,
client/Dockerfile.ui, docker-compose.yml, client/main.py, client/touch_ui.py,
tests de CLI/cliente/UI y documentación de operación/specs relacionadas.

## Dependencies and approvals

El operador autoriza issue nueva e investigación; exige Docker para desarrollo.
Confirma Docker Desktop Linux (desktop-linux) como entorno de aceptación.
La UI actual en Engine nativo no satisface ese requisito. El estudio debe
incluir transporte de pantalla y audio a través de la frontera de su VM.
No hay autorización implícita para paquetes nuevos, cambios de arquitectura o
reactivación de proveedores. Solicitar lo requerido después de concretar propuesta.

## Acceptance or resolution criteria

Los criterios de issue.md gobiernan el cierre. La investigación termina con
una decisión fundamentada, sin declarar resuelto el funcionamiento de voz.

## Verification

Documentación actual: referencias y `git diff --check`.
Tras implementación: `./tonto.sh test python`, `./tonto.sh test ui` y sintaxis
Bash cuando corresponda. Ampliar checks por impacto, sin inventar comandos.
Aceptación manual: ventana real, escucha, señal WAV, STT, respuesta y TTS audible;
las pruebas de widgets bajo Xvfb y los mocks no prueban hardware.

## Workflow isolation and integration

- Branch actual: fix/kivy-docker-desktop-audio, desde la rama de estudio basada en main.
- Worktree dedicado: no requerido sin trabajo paralelo; obligatorio si aparece.
- Parallel-safe: no compartir checkout con otro trabajo concurrente.
- Riesgos: scripts/UI/índice pueden cambiar en otras entregas; reconciliar desde
  main antes de integrar, sin incorporar parches de investigaciones ajenas.
- Integración: documentación de estudio primero, reparación y evidencia después.
- GitHub tracking: no asociado; esta es una issue local definida en ai/.

## Implementation prompt

Leer AGENTS.md, workflow y locales aplicables, y los tres archivos del registro
003-kivy-docker-development-audio. Ejecutar inicialmente solo la investigación
de los pasos 1–5. Usar helpers oficiales y diagnósticos seguros. Partir de main,
sin consultar ni reutilizar la investigación de otras ramas. No implementar una
solución por suposición. Registrar evidencia y propuesta de línea de trabajo,
incluidas dependencias/aprobaciones, y mantener índice/metadata sincronizados.
Docker y validación física de voz son requisitos; no sustituirlos por host/mocks.

## Implementación autorizada, 2026-10-07

El operador pide continuar después de validar UI/audio real. Implementar la vía
Desktop comprobada: puentes socat en loopback, configuración ALSA-PulseAudio en
imagen y renderizado software. No instalar paquetes host. Usar socat existente
como precondición explícita. Mantener Engine nativo con montaje directo actual.
No modificar permisos X11 automáticamente. Launcher debe retirar procesos y
override al salir normalmente, fallar o recibir señal. Añadir checks de puentes
y parámetros, tests de fallo/limpieza, diagnóstico UI directo ante fallo de captura.
Actualizar spec/plan del emulador, README e instrucciones de scripts. Verificar
con tareas oficiales sin credenciales; después backend y UI en desktop-linux.

## Assumptions and blockers

### Resultado de ensayo, 2026-10-07

Docker Desktop conectado a puente socat ligado a loopback del PC: con
libasound2-plugins y default ALSA de tipo pulse dentro de una imagen temporal,
PortAudio enumera entrada y valida 16 kHz mono. Captura física de seis segundos
genera WAV correcto con señal; operador confirma espeak audible. No se ha
integrado en cliente/main ni Kivy, ni enviado voz al backend. Propuesta siguiente:
probar UI real con transporte gráfico apropiado para Desktop y diseñar el
launcher con lifecycle/limpieza del puente y confianza local explícitos antes
de implementar. Esta propuesta aún no es una reparación aceptada.

### Resultado de UI real, 2026-10-07

Cliente sin cambios inicia SDL2/X11 y llvmpipe en Desktop mediante puente local
de pantalla. Tres turnos de voz completos aceptados por el operador; HTTP 200
en audio y prueba de texto exitosa. Recreación de UI con la misma configuración
abre ventana y conserva entrada válida. Backend del ensayo permanece en Engine
nativo: falta validar stack completo en Desktop y launcher oficial.

Línea propuesta para implementación: detección explícita de contexto/daemon;
preflight de recursos del host sin confundir sandbox y VM; puentes locales
gestionados para pantalla/audio en Desktop, con cierre garantizado; plugin y
default ALSA dentro de imagen; renderizado por software comprobado; política
de acceso local documentada sin desactivar control X11. Revisar plan/spec del
emulador antes de implementar. Mantener flujo Raspberry separado y probar
ausencia de recursos, errores y recuperación, además del arranque feliz.

Hardware, pantalla y servidor accesibles son precondiciones a precisar.
Restricciones del sandbox pueden necesitar permisos específicos y no son prueba
de fallo del host. Docker Desktop y Engine nativo no son intercambiables para
acceso a recursos; el entorno soportado debe definirse con el operador si limita
su requisito. Conexión y captura demostradas en imagen mínima; integración UI,
transcripción, recuperación y launcher definitivo siguen pendientes.
