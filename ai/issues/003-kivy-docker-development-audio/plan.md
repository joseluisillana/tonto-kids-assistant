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

### Preparación de versión mayor solicitada — 2026-10-07

Operador decide que PR #126 eleve 1.0.0 a 2.0.0. Preparar en esta misma rama
VERSION, web/package.json y las dos versiones raíz de web/package-lock.json,
sin alterar dependencias. README debe distinguir versión declarada del código
y release publicada. Crear docs/releases/v2.0.0.md con alcance, compatibilidad,
validación, precondiciones y límites; conservar notas y tag históricos v1.0.0.
Actualizar resumen de specs, roadmap y journal global mediante referencias.

Verificación: comparar manifiesto/lock contra HEAD, permitiendo únicamente
versiones raíz; test web y build web oficiales en Desktop, diff check y export.
Las pruebas Python/Kivy y físicas ya registradas siguen aplicando al runtime
sin cambios. Actualizar título/descripción de PR para incluir preparación 2.0.0.

Después del merge: actualizar main, verificar VERSION=2.0.0 y CI aprobada del
commit integrado, comprobar ausencia de tag remoto/local v2.0.0 y crear tag
anotado sobre ese SHA. Publicar GitHub Release con --verify-tag y las notas
versionadas, solo como operación posterior autorizada. No etiquetar la rama
de preparación ni reemplazar tags existentes. Esta petición prepara la versión;
no autoriza crear la etiqueta/release antes del merge.

### Ampliación documental solicitada — 2026-10-07

Integrar en esta misma issue y PR el comando explícito de próximos arranques:
`DOCKER_CONTEXT=desktop-linux ./tonto.sh dev ui`, desde la raíz del repositorio
y después de cerrar la ventana anterior y esperar a que termine su launcher.

Ubicaciones previstas:
- README.md: setup inicial, lista de comandos y explicación del ciclo de arranque
  Desktop. Es la guía humana de esta operación; el runbook Raspberry no es su destino.
- AGENTS.md: entrada común de operación del emulador y referencia al README.
- client/AGENTS.md: instrucción para agentes que trabajan/validan la UI.
- scripts/AGENTS.md: instrucción para agentes que operan el launcher y su limpieza.

Mantener la vía nativa diferenciada y evitar depender del contexto global elegido.
Explicar que el cierre libera puentes/puertos y conserva backend; no iniciar un
segundo launcher mientras el anterior esté activo. No cambiar comportamiento,
dependencias, servicios ni volver a ejecutar aceptación física por edición de prose.
Verificar consistencia entre las cuatro ubicaciones y git diff --check; actualizar
journal y publicar en la PR #126 de la misma rama. Estado resolved se conserva
una vez incorporada esta aclaración, con revisión/integración aún pendientes.

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
