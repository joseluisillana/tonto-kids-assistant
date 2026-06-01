# Audio Pipeline Phase 3 Browser Manual Validation

## Objetivo

Esta spec define la validacion manual final de Fase 3 contra el backend real:

```text
browser microphone -> WAV PCM 16 kHz mono -> POST /chat/audio -> transcript -> response text -> browser speech
```

La ejecucion completa de esta guia debe producir evidencia suficiente para cerrar el desarrollo de `specs/audio-pipeline-phase-3-web-loop.md` y, en consecuencia, cerrar la feature de Fase 3 Web Voice Loop.

Esta validacion no sustituye la ruta fisica Raspberry. Es una validacion web del contrato real `POST /chat/audio` y del backend STT activo.

**Estado de cierre:** validacion completada satisfactoriamente el 2026-06-01 contra backend real. La evidencia queda registrada en `docs/project-journal/week-03.md`. El unico incidente operativo relevante fue un `422 Audio did not contain recognizable speech` causado por tener seleccionado un microfono incorrecto en el navegador; se resolvio seleccionando el input fisico correcto.

## Alcance

Incluido:

- Validar el cliente web implementado contra un backend real arrancado localmente.
- Validar captura real desde microfono del navegador.
- Confirmar que la web genera y envia WAV PCM 16-bit, 16 kHz, mono.
- Confirmar que el request usa `POST /chat/audio` sin endpoint nuevo.
- Confirmar `transcript` real de STT, `response` educativa y reproduccion audible en navegador.
- Confirmar que `/chat` de texto sigue funcionando como fallback.
- Registrar evidencia suficiente en `docs/project-journal/week-03.md`.
- Actualizar docs/specs de estado para marcar Fase 3 como completa, parcial o bloqueada.

Fuera de alcance:

- Cambios de codigo durante la validacion, salvo correcciones posteriores si la validacion falla.
- Nuevas dependencias.
- Backend transcoding de `webm`, `ogg` u otros formatos.
- Selector visible o subida manual de WAV en la UI.
- STT local, backend TTS, streaming, persistencia, auth o UI avanzada.
- Revalidacion de Raspberry, que vive en sus specs de Fase 2A/2B.

## Precondiciones

- Rama de trabajo adecuada, no `main`, salvo decision explicita.
- Dependencias locales instaladas con los scripts oficiales.
- `OPENAI_API_KEY` configurada en el entorno local sin registrarla en docs ni logs.
- Backend STT activo con `OPENAI_STT_MODEL=gpt-4o-mini-transcribe` o el valor documentado vigente.
- Backend de conversacion activo con `OPENAI_MODEL` configurado.
- Navegador con soporte de:
  - `navigator.mediaDevices.getUserMedia`
  - Web Audio API
  - `window.speechSynthesis`
- Microfono funcional disponible para el navegador.
- Permiso de microfono disponible para la URL local usada.
- Microfono correcto seleccionado en los ajustes del navegador para la URL local usada. Si el navegador tiene otro input activo, el pipeline puede enviar WAV valido pero sin voz reconocible.

## Entorno Recomendado

- Windows host de desarrollo.
- Backend local FastAPI.
- Web local Vite.
- Navegador recomendado: Chrome o Edge actual.

Registrar el navegador exacto usado. Si se usa otro navegador, registrar diferencias observadas.

## Preparacion

Desde PowerShell, en la raiz del repositorio:

```powershell
git branch --show-current
git status --short --branch
.\scripts\setup-dev.ps1
.\scripts\test.ps1 -Target python
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
```

Configurar entorno sin imprimir secretos:

```powershell
if (-not $env:OPENAI_API_KEY) { throw "OPENAI_API_KEY is not set" }
$env:OPENAI_STT_MODEL = "gpt-4o-mini-transcribe"
$env:OPENAI_MODEL = "gpt-4o-mini"
"OPENAI_API_KEY configured"
"OPENAI_STT_MODEL=$env:OPENAI_STT_MODEL"
"OPENAI_MODEL=$env:OPENAI_MODEL"
```

Arrancar backend y web:

```powershell
.\scripts\dev.ps1 -Service all
```

Si el script muestra URLs distintas a las esperadas, usar las URLs reales emitidas por el script y registrarlas como evidencia.

## Caso 1: Salud del Backend

1. Abrir la URL web local en el navegador.
2. Confirmar que la UI muestra el backend URL usado.
3. Confirmar que `/health` aparece como disponible.
4. Registrar:
   - URL web.
   - Backend URL.
   - Estado health visible.

Criterio de paso:

- La UI puede alcanzar el backend real antes de iniciar audio.

## Caso 2: Fallback de Texto `/chat`

1. Enviar un mensaje de texto corto:

```text
Hola TONTO, dime que es una estrella en una frase.
```

2. Confirmar que la respuesta aparece en la conversacion.
3. Confirmar que el estado tecnico no queda en error.
4. Registrar la respuesta recibida.

Criterio de paso:

- El fallback `/chat` sigue funcionando despues de implementar Fase 3.

## Caso 3: Loop Principal de Voz Web

Frase recomendada:

```text
Hola TONTO, explicame que es una estrella.
```

Pasos:

1. En la UI web, iniciar un turno de voz.
2. Aceptar el permiso de microfono si el navegador lo solicita.
3. Antes de hablar, comprobar en los ajustes de sitio del navegador que el input seleccionado es el microfono fisico correcto.
4. Decir la frase recomendada de forma natural.
5. Detener y enviar el turno de voz.
6. Esperar la respuesta del backend.
7. Confirmar que la UI muestra:
   - `session_id`.
   - `device_id=web-validation-client`.
   - `language=es`.
   - `sample_rate_hz=16000`.
   - `channels=1`.
   - MIME del audio generado como WAV.
   - duracion aproximada.
   - tamano del WAV.
   - HTTP status de `/chat/audio`.
   - latencia total.
   - `transcript`.
   - `response`.
   - estado de speech output.
8. Confirmar que la respuesta se reproduce audiblemente en el navegador.
9. Confirmar que no existe selector visible de archivo WAV ni flujo visible de subida manual.

Criterios de paso:

- El request usa `POST /chat/audio`.
- El backend responde `HTTP 200`.
- El `transcript` no esta vacio.
- El `transcript` no es el placeholder `[audio input captured]`.
- El `transcript` es razonablemente cercano a la frase hablada.
- La `response` es educativa, visible y no vacia.
- La `response` se escucha en el navegador.
- El panel tecnico muestra evidencia suficiente para depuracion.

## Caso 4: Segundo Turno en la Misma Sesion

Frase recomendada:

```text
Y por que brillan?
```

Pasos:

1. Sin recargar la pagina, iniciar otro turno de voz.
2. Decir la frase recomendada.
3. Detener y enviar.
4. Confirmar que se conserva la misma sesion web salvo que la UI haya sido reiniciada.
5. Confirmar que el transcript y la respuesta corresponden al segundo turno.

Criterios de paso:

- La experiencia soporta mas de un turno corto.
- El estado vuelve a `idle` o equivalente al terminar.
- La UI no queda bloqueada tras reproducir speech.

## Caso 5: Error por Permiso Denegado

Pasos:

1. Revocar o bloquear el permiso de microfono para la URL local.
2. Intentar iniciar un turno de voz.
3. Confirmar que aparece un error legible.
4. Restaurar el permiso de microfono al terminar la prueba.

Criterio de paso:

- La UI comunica que el permiso de microfono fue denegado o no esta disponible sin romper el flujo de texto.

## Caso 6: Audio Vacio o Demasiado Corto

Pasos:

1. Iniciar un turno de voz.
2. Detenerlo inmediatamente o permanecer en silencio.
3. Enviar si la UI permite el envio.
4. Confirmar que aparece error legible o que el request no se envia con audio vacio.

Criterio de paso:

- La UI o el backend rechaza el turno vacio con una explicacion entendible.

Nota de diagnostico:

- Si el backend responde `422` con detalle equivalente a `Audio did not contain recognizable speech` pero el WAV fue aceptado, revisar primero que el navegador este usando el microfono correcto. En una validacion real el fallo se resolvio seleccionando el input correcto desde los ajustes del navegador; no era un fallo de `/chat/audio` ni del contrato WAV.

## Caso 7: Backend No Disponible

Pasos:

1. Detener el backend o apuntar temporalmente la UI a un backend URL no disponible, segun permita la configuracion actual.
2. Intentar un turno de texto o voz.
3. Confirmar que aparece error legible de backend no disponible, timeout o HTTP error.
4. Restaurar el backend real.

Criterio de paso:

- El fallo no deja la UI bloqueada y el mensaje orienta la causa probable.

## Caso 8: Speech No Soportado o Fallo de Speech

Ejecutar solo si el navegador permite reproducir el escenario sin instalar dependencias.

Opciones aceptables:

- Usar un navegador sin `speechSynthesis`.
- Bloquear o cancelar la reproduccion audible si el navegador lo permite.
- Registrar que el navegador usado si soporta speech y no se pudo forzar este negativo de forma razonable.

Criterio de paso:

- Si speech no esta soportado o falla, la UI lo comunica sin invalidar el transcript ni la respuesta textual.

## Evidencia Obligatoria

Registrar en `docs/project-journal/week-03.md`, seccion `Fase 3 Web Loop Validation Evidence`:

```text
Date:
Branch:
Commit or working tree note:
Browser and version:
Web URL:
Backend URL:
Backend health:
OPENAI_STT_MODEL:
OPENAI_MODEL:
Text fallback result:
Voice phrase 1:
Voice phrase 1 duration_ms:
Voice phrase 1 WAV size:
Voice phrase 1 MIME:
Voice phrase 1 HTTP status:
Voice phrase 1 latency_ms:
Voice phrase 1 transcript:
Voice phrase 1 response:
Voice phrase 1 audible playback result:
Voice phrase 2:
Voice phrase 2 transcript:
Voice phrase 2 response:
Permission denied result:
Empty audio result:
Backend unavailable or timeout result:
Speech unsupported/failure result:
Visible WAV upload absent:
Overall result:
Blockers:
```

No registrar `OPENAI_API_KEY`, audios persistidos, capturas con secretos, ni datos personales.

## Criterios de Cierre de la Feature

La Fase 3 Web Voice Loop puede cerrarse solo si:

- Todos los casos obligatorios pasan o tienen una excepcion justificada en el journal.
- El loop principal de voz devuelve transcript real y response real desde el backend.
- La respuesta se escucha en el navegador o, si el navegador no soporta speech, queda documentado con respuesta textual valida.
- `/chat` de texto sigue funcionando.
- No hay selector visible de WAV ni flujo visible de subida manual.
- No se agrego endpoint nuevo.
- No se agrego transcoding backend ni dependencia nueva.
- La evidencia manual queda registrada en `docs/project-journal/week-03.md`.
- Se actualizan los documentos de estado listados abajo.
- Los checks finales pasan.

## Actualizacion Documental de Cierre

Despues de una validacion exitosa, actualizar en el mismo cambio:

- `docs/project-journal/week-03.md`: pegar la evidencia real.
- `specs/audio-pipeline-phase-3-web-loop.md`: marcar Fase 3 como validada o describir cualquier limitacion.
- `specs/web-validation-client.md`: marcar criterios Phase 3 como cumplidos o parcialmente cumplidos.
- `specs/audio-pipeline.md`: reflejar que la variante web fue validada contra `POST /chat/audio`.
- `docs/specs.md`: actualizar estado de Fase 3.
- `docs/roadmap.md`: marcar Fase 3 como completa, parcial o bloqueada.
- `docs/architecture.md`: reflejar solo el estado validado, sin cambiar arquitectura.
- `README.md`: refrescar el estado actual de Semana 3 si corresponde.
- `AGENTS.md`: ajustar instrucciones persistentes solo si cambia el estado activo del milestone.

## Checks Finales

Ejecutar:

```powershell
.\scripts\test.ps1 -Target python
.\scripts\test.ps1 -Target web
.\scripts\build.ps1 -Target web
git diff --check
git status --short --branch
```

## Resultado Esperado

Al completar esta guia con evidencia positiva, la spec de implementacion de Fase 3 queda cerrada como validada. Si algun criterio falla, la feature no se cierra: se registra el bloqueo, se corrige con cambios acotados y se repite esta validacion.

## Resultado de Cierre 2026-06-01

La guia queda ejecutada con resultado `PASS` por validacion humana en navegador local contra backend real. La Fase 3 Web Voice Loop y la Semana 3 quedan cerradas como satisfactorias, manteniendo las restricciones de alcance: sin endpoint nuevo, sin dependencias nuevas, sin selector WAV visible, sin backend transcoding y con `/chat` como fallback estable.
