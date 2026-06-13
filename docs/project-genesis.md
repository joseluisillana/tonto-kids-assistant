# Project Genesis Prompt

Prompt autónomo para reconstruir TONTO Kids Assistant desde cero mediante desarrollo asistido por IA. Contiene la identidad del proyecto, arquitectura, stack, alcance, contratos, fases, workflow de agentes, reglas de código, testing, documentación, y entregables.

---

## IDENTIDAD DEL PROYECTO

Crea un asistente educativo físico para niños llamado **TONTO Kids Assistant**. Es un proyecto demo-first, orientado a validar un bucle de conversación por voz reproducible con hardware accesible.

**Actor principal**: un niño de 6-10 años que habla en español con el asistente.
**Interacción**: el niño habla → el asistente responde con voz en español, de forma educativa y amigable.
**Meta del MVP**: demostración funcional en 6 semanas, priorizando claridad, depurabilidad y una demo real sobre diseño de plataforma.

---

## ARQUITECTURA

### Topología
```
[Raspberry Pi 3] ──HTTP/JSON──> [Backend Python/FastAPI] <──HTTP/JSON── [Web Validación]
     │                                │                                    │
  arecord (captura)            OpenAI STT + Chat                     Browser mic
  espeak (TTS local)           Orquestación                          Web Speech API
```

### Principios de arquitectura
1. **Monolito ligero**: backend FastAPI único. Nada de microservicios.
2. **Cliente Raspberry ultra-fino**: solo I/O local (captura audio, reproduce TTS). Cero dependencias Python externas. Sin IA local, sin STT local, sin orquestación. Usa solo stdlib de Python.
3. **HTTP/JSON simple**: sin streaming, sin WebSockets, sin protobuf.
4. **Estado solo en memoria**: sin base de datos, sin persistencia. Historial de sesión rotativo (últimos 8 mensajes).
5. **Formato de audio**: WAV PCM 16-bit 16kHz mono. Sin formatos comprimidos, sin transcodificación en backend.
6. **Sin overengineering**: nada de colas, brokers, workers en background, injection de dependencias, orquestación de contenedores.

### Estructura del monorepo
```
backend/          # Python + FastAPI (orquestación, STT, chat)
client/           # Python stdlib (cliente Raspberry Pi)
web/              # React + TypeScript + Vite (cliente de validación)
shared/           # Modelos compartidos (si se necesitan)
docs/             # Documentación, specs, journal, planes
specs/            # Especificaciones detalladas
scripts/          # Scripts PowerShell de automatización
tests/            # Tests Python
```

---

## STACK TECNOLÓGICO

### Backend
- Python 3.11+ con FastAPI y uvicorn
- `python-multipart` para uploads de audio
- `urllib.request` de stdlib para llamadas HTTP a OpenAI (sin librerías HTTP externas)
- OpenAI API: `gpt-4o-mini` para chat, `gpt-4o-mini-transcribe` para STT (configurable por variable de entorno)

### Cliente Raspberry Pi
- Python 3 (stdlib exclusivamente)
- `arecord` para captura de audio (ALSA)
- `espeak` para TTS local, afinado a `-v es -s 135 -g 8`

### Web (cliente de validación)
- React 19 + TypeScript + Vite 7 + Tailwind CSS 4
- Sin librería de routing (pushState simple)
- Sin librería de state management (solo React state + hooks)
- Captura de micrófono: `getUserMedia` + `AudioContext` + `ScriptProcessor` (sin MediaRecorder para evitar webm)
- Encoding WAV manual en JS (sin librería externa)
- Speech output: Web Speech API (`speechSynthesis`)

---

## ALCANCE DEL MVP Y EXCLUSIONES EXPLÍCITAS

### Dentro del MVP
- Bucle de conversación por texto vía `POST /chat`
- Bucle de conversación por voz vía `POST /chat/audio` (WAV)
- Captura de audio con `arecord` en Raspberry Pi
- STT con OpenAI (gpt-4o-mini-transcribe)
- Chat educativo con OpenAI (gpt-4o-mini), instrucciones en español para niños
- TTS local con `espeak` en Raspberry
- Cliente web de validación con captura de micrófono y reproducción de voz
- Indicador visual de escucha en terminal (Raspberry) y en UI (web)
- Script de arranque de demo en Raspberry
- Scripts PowerShell para setup, dev, test, build
- Agent Capability Pack para operaciones de backend y SSH a Raspberry
- Tests Python y web
- Documentación completa: specs, arquitectura, roadmap, journal semanal, planes

### Explícitamente FUERA del MVP
- Wake word
- Integración con Arduino / LEDs físicos
- Persistencia / base de datos
- Autenticación / cuentas de usuario
- Multi-usuario
- Modelos de IA locales
- STT local o modelos de audio locales
- Transcodificación de webm/ogg en backend
- Subida manual de WAV desde UI de producto
- Multi-agente
- Streaming de audio
- Go backend (legacy/postergado)

---

## CONTRATOS DE API

### `GET /health`
```json
{"status": "ok"}
```

### `POST /chat`
**Request**: `{"session_id": "string", "message": "string"}`
**Response**: `{"success": true, "response_text": "string"}`

### `POST /chat/audio`
**Request**: multipart/form-data
- `audio`: archivo WAV (PCM 16-bit, mono, 16kHz)
- `session_id`: string
- `duration_ms`: int
- `sample_rate_hz`: int (16000)
- `channels`: int (1)
- `device_id`: string (opcional)
- `language`: string (default "es")

**Validaciones**:
- Formato WAV: cabecera RIFF, PCM=1, mono, 16kHz, 16-bit
- Tamaño máximo: 512KB
- Duración: 250ms mínima, 10s máxima

**Response**: `{"session_id": "string", "transcript": "string", "response": "string"}`
**Errores**: 400 (inválido), 413 (demasiado grande), 415 (formato no soportado), 422 (sin voz reconocida), 502/504 (error upstream)

---

## COMPORTAMIENTO DEL ASISTENTE (PROMPT DE SISTEMA OPENAI)

El asistente debe responder:
- **En español**, lenguaje adaptado a niños de 6-10 años
- **2-3 frases** como máximo
- **Respuesta directa primero**, luego ejemplo simple si aplica
- **Sin listas, sin markdown, sin enumeraciones**
- **Cuidado factual**: no inventar datos científicos incorrectos
- **Saludos y despedidas naturales**, acordes a la edad
- **Tokens máximos de salida**: 300

---

## FASES DE IMPLEMENTACIÓN (6 SEMANAS)

### Semana 1-2: Fundación
- Setup del monorepo y scripts de automatización
- Backend FastAPI con `/health` y `POST /chat`
- Integración con OpenAI para chat
- Cliente Raspberry con bucle de texto (`--mode text`)
- TTS con `espeak`
- Tests básicos

### Semana 3: Pipeline de Voz
- **Fase 1**: Captura de audio con `arecord` en Raspberry (WAV)
- **Fase 2A**: `POST /chat/audio` en backend + STT con OpenAI
- **Fase 2B**: Automatización del cliente Raspberry (`--mode voice`)
- **Fase 3**: Cliente web con captura de micrófono y bucle de voz

### Semana 4: Estabilidad de Demo
- Baseline de demo reproducible (3 turnos de voz)
- Resiliencia: timeouts separados, manejo de URLError
- Calibración de conversación: prompt afinado, todas las pruebas pasando
- Indicadores de escucha: terminal (Raspberry) y UI (web)
- Decisión explícita de postergar Arduino/LEDs

### Semana 5: Experiencia de Demo
- **Fase 0**: Kickoff
- **Fase 1**: Runbook de demo y script de arranque (`demo-raspberry.sh`)
- **Fase 2**: Pulido de UX conversacional (límite de tokens, validación con preguntas reales)
- **Extra**: Agent Capability Pack (`agent-backend.ps1`, `agent-raspberry.ps1`)
- **Fase 3**: Resiliencia a errores (siguiente hito)

### Semana 6: Entrega Final

---

## WORKFLOW DE DESARROLLO ASISTIDO POR IA

### Herramientas
- **Codex / OpenCode**: asistente principal de proyecto
- **GitHub Copilot**: asistente en editor
- **NotebookLM**: síntesis y análisis de documentación
- **GitHub CLI (`gh`)**: operaciones de PRs e issues

### Convenciones Git
- **Ramas**: `<type>/<short-kebab-description>` donde type ∈ {`feature/`, `fix/`, `docs/`, `chore/`, `experiment/`}
- **Nunca editar en `main`**: siempre crear rama primero
- **Una rama por item de trabajo**, vida corta y enfocada
- **Commits convencionales**: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`
- **Worktrees separados** para agentes paralelos: `git worktree add ../worktree-name -b branch-name`
- **No usar prefijos de herramienta** en ramas (nada de `codex/`, `opencode/`) a menos que se pida explícitamente

### Flujo de trabajo diario
1. Leer AGENTS.md, docs/specs.md, docs/roadmap.md, último journal semanal antes de actuar
2. Verificar rama actual con `git branch --show-current` y `git status`
3. Si estás en `main`, crear rama nueva con el tipo y descripción adecuados
4. Implementar cambios pequeños y directos
5. Ejecutar tests: `.\scripts\test.ps1 -Target python` o `-Target web` o `-Target all`
6. Actualizar docs/specs si el comportamiento, arquitectura, o alcance cambian
7. Si una spec se crea o modifica materialmente, crear plan de implementación en `docs/plans/`
8. Hacer commit y push; crear PR con `gh`

### Specs → Plan → Implementación
Toda spec nueva o modificada materialmente sigue este ciclo:
1. **Spec** en `specs/`: define qué, contrato, criterios de aceptación, exclusiones
2. **Plan** en `docs/plans/`: define cómo, pasos, y prompt de implementación listo para handoff
3. **Implementación**: siguiendo el plan
4. **Evidencia de validación**: tests pasando, validación humana si aplica

### Scripts obligatorios (no inventar comandos ad-hoc)
| Comando | Propósito |
|---------|-----------|
| `.\scripts\setup-dev.ps1` | Crear .venv, instalar dependencias Python y web |
| `.\scripts\dev.ps1 -Service backend\|web\|all` | Iniciar servicios |
| `.\scripts\test.ps1 -Target python\|web\|all` | Ejecutar tests |
| `.\scripts\build.ps1 -Target web\|all` | Build de producción |
| `.\scripts\agent-backend.ps1 start\|stop\|status\|health` | Ciclo de vida del backend |
| `.\scripts\agent-raspberry.ps1 preflight\|exec` | Operaciones SSH a Raspberry |

### Entorno local
- Python: `.venv/` local al repo, nunca global
- Web: `node_modules/` dentro de `web/`, nunca global
- Cachés: `.cache/` local, no depender de cachés de perfil de usuario
- Windows: PowerShell scripts oficiales
- Raspberry: bash scripts

---

## REGLAS DE CODIFICACIÓN

1. **Código pequeño, directo, inspeccionable**
2. **Python plano con patrones FastAPI ya presentes**
3. **Backend como monolito ligero** para el MVP
4. **Cliente Raspberry como script Python simple**
5. **Estructuras de datos tipadas** donde clarifiquen contratos
6. **Nombres claros** sobre abstracciones ingeniosas
7. **Manejar casos de fallo obvios**: timeouts de backend, TTS no disponible
8. **Añadir tests enfocados** al cambiar comportamiento
9. **No cambiar arquitectura o alcance silenciosamente**
10. **No reescribir archivos no relacionados**
11. **No implementar features de alcance futuro** a menos que se pida explícitamente
12. **No añadir dependencias** sin preguntar primero. Si se propone una, explicar por qué es necesaria ahora, qué alternativa más simple se consideró, dónde se usará, y si afecta al setup de Raspberry

---

## ESTRATEGIA DE TESTING

### Tests Python (pytest + httpx)
Ubicados en `tests/`, ejecutados con `.\scripts\test.ps1 -Target python`.
- `conftest.py`: fixtures con TestClient, generador de WAV, tmp_path local al repo
- `test_audio.py`: validación de WAV, campos requeridos, límites de tamaño, formato, errores STT
- `test_client.py`: HTTP client, timeouts, errores, captura de audio, espeak, indicador de escucha
- `test_openai_client.py`: payload de OpenAI, instrucciones, historial, límite de tokens
- `test_stt_client.py`: STT, modelo custom, errores HTTP, timeouts

### Tests Web (Node test runner)
Ubicados en `web/tests/`, ejecutados con `.\scripts\test.ps1 -Target web`.
- `audio-utils.test.mjs`: encoding WAV, downsampling, recorte de silencio, normalización
- `backendClient.test.mjs`: request/response del cliente backend

---

## DOCUMENTACIÓN A MANTENER

| Archivo | Propósito |
|---------|-----------|
| `AGENTS.md` | Instrucciones persistentes para asistentes IA |
| `README.md` | Orientación de alto nivel del proyecto |
| `docs/architecture.md` | Decisiones de arquitectura |
| `docs/roadmap.md` | Hitos y fases del MVP |
| `docs/specs.md` | Índice de specs activas |
| `docs/ai-assisted-workflow.md` | Flujo de trabajo de desarrollo asistido por IA |
| `docs/project-journal/week-NN.md` | Diario semanal de progreso |
| `specs/*.md` | Especificaciones detalladas por feature |
| `docs/plans/*.md` | Planes de implementación por spec |

---

## VARIABLES DE ENTORNO

```bash
OPENAI_API_KEY=           # Clave de API de OpenAI
OPENAI_STT_MODEL=         # Modelo STT (default: gpt-4o-mini-transcribe)
TONTO_BACKEND_URL=        # URL del backend (Raspberry: http://<ip>:8000)
TONTO_AUDIO_DEVICE=       # Dispositivo ALSA (default: plughw:1,0)
TONTO_RECORD_SECONDS=     # Duración de grabación (default: 6)
TONTO_TTS_COMMAND=        # Comando TTS (default: espeak)
TONTO_TTS_ARGS=           # Args TTS (default: -v es -s 135 -g 8)
```

---

## CONFIGURACIONES DE ENTORNO

### `.env` (raíz)
```
OPENAI_API_KEY=sk-...
TONTO_BACKEND_URL=http://192.168.1.100:8000
```

### `backend/requirements.txt`
```
fastapi
python-multipart
uvicorn
```

### `client/requirements.txt`
```
# Sin dependencias externas - solo stdlib
```

### `requirements-dev.txt`
```
pytest
httpx
```

### `web/package.json`
Dependencias: `react`, `react-dom`
DevDeps: `@tailwindcss/vite`, `@types/react`, `@vitejs/plugin-react`, `typescript`, `vite`

---

## CI Y AUTOMATIZACIÓN

- CI pipeline en `.github/workflows/ci.yml`
- Git hooks: pre-commit que ejecuta exportación de docs para NotebookLM
- CI, humanos, y agentes comparten los mismos scripts de superficie
- Usar `gh` CLI para PRs, issues, checks, merges

---

## ENTREGABLES POR FASE

### Semana 1-2
- [x] Monorepo con estructura definida
- [x] Scripts de setup, dev, test, build
- [x] Backend FastAPI funcional con `/health` y `POST /chat`
- [x] Integración OpenAI para chat
- [x] Cliente Raspberry con bucle de texto
- [x] TTS con espeak funcional
- [x] Tests pasando

### Semana 3
- [x] Captura WAV con arecord validada
- [x] `POST /chat/audio` con validación WAV y STT
- [x] Cliente Raspberry `--mode voice` funcional
- [x] Cliente web con captura de micrófono y bucle de voz
- [x] Indicadores de escucha

### Semana 4
- [x] Demo baseline reproducible
- [x] Manejo de timeouts y URLError
- [x] Prompt calibrado, tests pasando
- [x] Indicadores de escucha (Raspberry + web) validados

### Semana 5
- [x] Runbook de demo y script de arranque
- [x] UX conversacional pulida (validado desde Raspberry real)
- [x] Agent Capability Pack implementado
- [ ] Resiliencia a errores (Fase 3 - pendiente)

### Semana 6
- [ ] Ensayo de demo
- [ ] Cierre y entrega final

---

## INSTRUCCIONES FINALES PARA EL AGENTE

1. **Lee siempre el contexto del repo** antes de hacer cambios.
2. **Respeta el milestone actual** y mantén el alcance estrecho.
3. **Pregunta antes de añadir dependencias** o cambiar arquitectura.
4. **Si hay conflicto entre documentación y código**, pausa y haz la decisión explícita.
5. **Ante la duda, elige el cambio reversible más pequeño** que avance el MVP.
6. **Optimiza para claridad, depurabilidad y una demo real**.
7. **No expongas un upload manual de WAV** en la UI de producto/demo.
8. **Mantén estado solo en memoria** si es que se necesita estado.
9. **No añadas ni restaures Go** a menos que se reactive explícitamente.
10. **Si las instrucciones del usuario contradicen AGENTS.md**, sigue la instrucción más reciente del usuario y actualiza los docs si la decisión es persistente.
