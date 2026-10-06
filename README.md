# TONTO Kids Assistant

_T.O.N.T.O — Thinking Oriented Natural Tutor Organism_

Versión del proyecto: **1.0.0**, declarada en `VERSION` y alineada con los
metadatos del paquete web. Cierre del MVP conversacional Linux/Docker validado.
Contrato y alcance: [spec de release](ai/specs/022-release-v1.0.0/spec.md);
[cambios y limitaciones](docs/releases/v1.0.0.md). Kiosk y aceptación física
final de la UI táctil (#88) siguen pendientes.

TONTO es un agente educativo físico diseñado para acompañar a un niño en su aprendizaje diario mediante conversación natural.

Es un producto AI-first moderno que combina hardware físico accesible con modelos de IA avanzados para crear experiencias de aprendizaje inmersivas y personalizadas.

Nace como proyecto para la formación AI Expert de DevExpert.io. Por ello, la IA está presente en el núcleo del producto y también en el proceso de desarrollo.

Este README es el documento fundacional operativo para el desarrollador principal del proyecto. Está pensado para orientar las decisiones técnicas diarias, el backlog inicial y las pruebas en hardware real.

## Visión Producto

Imagina un compañero de aprendizaje que no solo responde preguntas, sino que recuerda conversaciones anteriores, adapta su personalidad al niño, y guía el aprendizaje de manera natural a través de la voz.

TONTO transforma el aprendizaje en una conversación continua, haciendo que la educación sea accesible, divertida y profundamente personalizada.

## Visión Técnica

Un sistema distribuido donde un thin client físico (Raspberry Pi) maneja I/O, audio y hardware, un backend central procesa IA/orquestación, y un cliente web de validación permite probar el backend desde navegador durante el desarrollo.

La comunicación es online-first con degradación offline básica.

El foco está en conversación natural persistente que adapta el aprendizaje al niño.

## Filosofía Técnica

- **MVP de 6 semanas**: Prototipo funcional demostrable en 6 semanas, no producto completo.
- **Demo-first development**: Cada semana produce una demo tangible, no documentación.
- **Thin client + heavy backend**: Raspberry Pi como I/O puro, backend como cerebro IA.
- **Online-first con degradación offline**: IA requiere conectividad, pero fallback básico offline.
- **IA como núcleo**: IA guía diseño de producto y acelera desarrollo (Copilot/Codex/OpenCode).
- **Spec Driven Development**: Especificaciones claras pero adaptables, validadas por prototipos.
- **Anti-scope-creep**: Solo features que contribuyen al MVP core. No "nice-to-haves".

## Objetivos del MVP (6 semanas)

El MVP final de 6 semanas busca demostrar una conversación educativa básica sobre hardware real.

El milestone inmediato ya validó el primer loop texto → backend → IA → respuesta → TTS local. Semana 3 queda completada: voz real con Raspberry, Fase 2B automatizada con `client/main.py --mode voice`, TTS ajustado a `espeak -v es -s 135 -g 8` y Fase 3 web validada el 2026-06-01 con microfono de navegador → WAV PCM 16 kHz mono → `POST /chat/audio` → transcript → respuesta → speech audible en browser.

Incluye ahora:

- **Entrada manual de texto** desde Raspberry Pi o cliente web de validación.
- **Entrada de voz validada inicialmente** mediante captura WAV en Raspberry y `POST /chat/audio`, más el loop automatizado `--mode voice` en la misma Raspberry.
- **Revalidación TTS completada** en Raspberry real: `espeak -v es -s 135 -g 8` hace las respuestas largas suficientemente entendibles para demo, aunque siguen sonando robóticas.
- **Fase web de voz completada**: el cliente web captura microfono, genera WAV compatible, usa `POST /chat/audio`, muestra evidencia y reproduce la respuesta con Web Speech API.
- **Backend Python/FastAPI** con endpoint `/chat`.
- **Integración OpenAI** para generar respuestas educativas.
- **TTS local** en Raspberry Pi mediante `espeak`.
- **Memoria de sesión en proceso** solo para contexto corto.
- **Documentación viva** en Markdown, asistida por Codex, OpenCode y NotebookLM.

Queda fuera del primer loop automatizado: wake word, Arduino/LEDs, persistencia, autenticación, multiusuario, memoria avanzada, UI de producto compleja y STT local.

## Arquitectura Actual

```
┌──────────────────────┐       HTTP /chat + /chat/audio       ┌──────────────────────┐
│     Raspberry Pi     │──────────────────────────────────────►│      Linux host      │
│    Thin Client  │                                       │      Backend IA      │
│                      │                                       │   Python/FastAPI     │
│ • Text input         │                                       │                      │
│ • arecord WAV        │                                       │ • POST /chat         │
│ • HTTP client        │                                       │ • POST /chat/audio   │
│ • TTS espeak         │                                       │ • OpenAI chat        │
│ • Thin client        │                                       │ • OpenAI STT         │
│ • No IA local        │                                       │ • Session memory     │
└──────────────────────┘                                       │ • Orquestación       │
┌──────────────────────┐       HTTP /health + /chat            │ • Personalidad       │
│ Web Validation Client│──────────────────────────────────────►│                      │
│ React/TypeScript/Vite│   Voice: mic -> WAV -> /chat/audio    └──────────────────────┘
│                      │
│ • Text validation    │
│ • UI evidence        │
│ • Audio web loop     │
│ • No Raspberry link  │
└──────────────────────┘
```

### Cliente (Raspberry Pi 3 Model B v1.2)

- **Hardware confirmado**: Pantalla táctil HDMI Waveshare 5" conectada y funcionando; Audio output validado y `espeak` funcionando.
- **Desarrollo**: VSCode Remote SSH, acceso por SSH remoto.
- **Responsabilidades actuales**: entrada manual de texto, llamadas HTTP al backend, TTS local, manejo básico de errores y loop de voz automatizado con `client/main.py --mode voice`.
- **Responsabilidades futuras**: wake word, control físico/Arduino y otras capacidades fuera del MVP inmediato.
- **Tecnología**: Python estándar para el primer loop; dependencias de audio/GPIO se añadirán solo cuando entren en alcance.

### Backend (Linux host)

- **Decisión MVP**: Python inicialmente para iteración rápida (FastAPI, OpenAI).
- **Responsabilidades**: Llamadas OpenAI, gestión memoria, orquestación respuestas.
- **Tecnología**: Python con FastAPI para APIs, integración OpenAI.

### Cliente Web de Validación

- **Objetivo**: Probar el backend desde navegador sin depender siempre de la Raspberry Pi.
- **Responsabilidades**: Entrada manual de texto, visualización de respuestas, panel técnico de demo y soporte para CI/despliegue frontend. No depende de la Raspberry; la Fase 3 web ya valida audio contra el mismo backend `POST /chat/audio`, con captura de microfono, transcript, respuesta textual y speech output del navegador.
- **Tecnología**: React + TypeScript + Vite, con Tailwind CSS como base visual.

## Stack Tecnológico Confirmado

- **Lenguajes**: Python (cliente y backend inicial)
- **Web**: React, TypeScript, Vite, Tailwind CSS
- **IA**: OpenAI API by default; DevExpert Inference is available through backend provider selection
- **Audio actual**: espeak/espeak-ng para TTS local
- **Audio actual**: STT backend con OpenAI `gpt-4o-mini-transcribe` validado manualmente desde Raspberry; DevExpert STT puede usarse mediante `TONTO_INFERENCE_PROVIDER=devexpert`; wake word queda fuera del MVP inmediato
- **Hardware**: Raspberry Pi 3B v1.2 con pantalla táctil HDMI Waveshare 5"; Arduino Uno queda futuro para estados físicos
- **Comunicación**: REST APIs (FastAPI)
- **Desarrollo**: Codex, OpenCode (WSL2/DevExpert), GitHub, GitHub Copilot, VSCode + Remote SSH
- **Documentación**: Markdown en repo como fuente oficial; NotebookLM para síntesis; Codex/OpenCode para mantenimiento asistido

**Tecnologías aparcadas**: Go para backend queda como evaluación futura, no como requisito activo del MVP ni como gate de CI.

## Estructura del Monorepo

```
tonto-kids-assistant/
├── backend/          # Backend IA (Python inicialmente)
│   ├── main.py       # API server
│   ├── requirements.txt
│   └── ...
├── client/           # Cliente Raspberry Pi
│   ├── main.py       # Audio/GPIO loop
│   ├── requirements.txt
│   └── ...
├── web/              # Cliente web de validación
│   ├── src/          # React app
│   ├── package.json
│   └── ...
├── spikes/           # Pruebas de concepto y prototipos aislados
├── shared/           # Código compartido
│   ├── models.py     # DTOs y modelos
│   └── config.py     # Configuración común
├── docs/             # Documentación técnica
│   ├── README.md     # Índice documental
│   ├── specs.md      # Specs activas
│   └── decisions.md  # Decisiones técnicas
├── scripts/          # Automatización
│   ├── agent-backend.sh # Control backend Docker
│   ├── agent-raspberry.sh # Operaciones SSH
│   ├── demo-raspberry.sh # Demo de voz
│   ├── demo-touch.sh # Demo táctil
│   └── export-docs-for-notebooklm.sh
├── tests/            # Tests automatizados
├── .gitignore
└── README.md
```

## Development Workflow

### Semana 1-2: Core Setup

1. **Spec semanal**: Actualizar `docs/specs.md` con objetivos semana.
2. **Prototype**: Implementar feature mínima viable.
3. **AI-Assisted**: Usar Copilot para boilerplate, Codex/OpenCode para cambios completos.
4. **Test físico**: Validar en Raspberry Pi real.
5. **Demo**: Grabación corta mostrando progreso.

### Semana 3-4: Integración

1. **Spec review**: Ajustar basado en prototipos previos.
2. **Backend first**: APIs funcionales antes de cliente.
3. **Offline fallback**: Básico para desconexiones.
4. **Performance check**: Latencia < 3s para conversación.

### Semana 5-6: Polish & Demo

1. **Edge cases**: Manejo de errores, audio ruidoso.
2. **Hardware polish**: Estados visuales consistentes.
3. **MVP demo**: 5 min conversación coherente.
4. **Documentación**: Specs finales, setup instructions.

## AI-Assisted Workflow

- **Codex**: inspección del repo, implementación acotada, actualización de documentación y verificación.
- **OpenCode**: CLI interactivo adicional con provider DevExpert (deepseek-v4-flash/pro) en WSL2. Implementación, revisión y verificación de tests siguiendo las mismas reglas.
- **GitHub Copilot**: asistencia dentro del editor para boilerplate y cambios pequeños.
- **NotebookLM**: investigación, síntesis y borradores a partir de fuentes exportadas del repo.
- **GitHub**: historial oficial de decisiones, código y documentación.

**Principio**: AI acelera, no reemplaza. Las decisiones estables vuelven al repo y se validan con scripts, tests o hardware real.

El flujo común para Codex, OpenCode, Copilot, Cursor, Claude u otras herramientas vive en `docs/ai-assisted-workflow.md`. TONTO usa GitHub Flow ligero, ramas `<type>/<short-kebab-description>` y Conventional Commits.

## Spec Driven Development

1. **Spec first**: Escribir requerimiento técnico claro en `docs/specs.md`.
2. **Prototype**: Implementar mínimo para validar spec.
3. **Test**: Validar en Pi, ajustar spec si necesario.
4. **Commit**: Solo specs validadas entran al repo.
5. **Iterate**: Specs evolucionan con prototipos, no planes estáticos.

## Principios Anti-Scope-Creep

- **MVP-only features**: Solo lo necesario para demo de 6 semanas.
- **No gold-plating**: Funcionalidad básica que funciona > features complejas rotas.
- **Hardware constraints**: Respeta límites de Pi 3 (CPU, memoria).
- **Offline minimal**: IA requiere internet; offline es fallback básico.
- **Single user focus**: Un niño a la vez, no multi-usuario.

## Decisiones Abiertas

- **Backend language**: Python/FastAPI para MVP; Go queda aparcado hasta que una decisión futura lo reactive.
- **Memoria futura**: solo después de validar el loop con memoria en proceso.
- **STT**: OpenAI `gpt-4o-mini-transcribe` elegido como proveedor inicial backend y validado manualmente desde Raspberry; wake word queda pendiente.
- **Estados físicos**: Arduino/LEDs fuera del primer loop.
- **Deployment**: ejecución local primero; despliegue reproducible después.

## Riesgos Técnicos Principales

- **Latencia de red**: Conversación requiere <2s respuesta; internet inestable rompe UX.
- **Audio en Pi 3**: CPU limitada puede causar delays en procesamiento voz.
- **OpenAI rate limits**: Costo y límites pueden afectar desarrollo/testing.
- **GPIO reliability**: Arduino integration puede ser inestable.
- **Offline degradation**: Sin IA, experiencia es muy limitada.

## Estado Actual del Proyecto

**Semanas 1 y 2 cerradas**: estructura monorepo, hardware base validado, backend conversacional mínimo, cliente Raspberry con TTS local, cliente web de validación y automatización local inicial.

**Semana 3 - Pipeline de voz real completada**. El proyecto cerró la captura WAV, el endpoint `POST /chat/audio`, la integración STT backend, la automatización de voz en Raspberry y la Fase 3 web. El cliente web valida el mismo contrato de audio, mantiene el loop de texto como fallback estable y reproduce de forma audible la respuesta desde navegador.

**Semana 4 - Kickoff documental preparado**. El siguiente hito queda faseado en `ai/specs/026-week-04-demo-stability/spec.md` y `ai/specs/026-week-04-demo-stability/plan.md`: primero validar la demo actual varias veces, después corregir solo bloqueos reales, calibrar conversación/memoria corta si hace falta, y decidir explícitamente si Arduino/LEDs aportan suficiente valor para entrar en el MVP.

**Hitos generales conseguidos**:

- ✅ Raspberry Pi 3B v1.2 configurado con SSH/VSCode Remote
- ✅ Audio output y `espeak` funcionando
- ✅ Backend Python/FastAPI con `/chat`
- ✅ Cliente Raspberry de texto con TTS local
- ✅ Cliente web de validación React/TypeScript/Vite
- ✅ Scripts oficiales de setup/dev/test/build
- ✅ Loop Raspberry → backend LAN → OpenAI → TTS validado manualmente
- ✅ Varias interacciones seguidas validadas en hardware real
- ✅ Captura WAV validada en Raspberry con micrófono USB
- ✅ Endpoint `POST /chat/audio` implementado con validación y STT backend inicial
- ✅ Phase 2A validada con Raspberry real: WAV manual → backend STT → respuesta → `espeak`
- ✅ Phase 2B validada inicialmente con Raspberry real: `client/main.py --mode voice` automatiza captura, subida, transcript/response y TTS local
- ✅ Phase 2B post-ajuste TTS revalidada con Raspberry real: `espeak -v es -s 135 -g 8` es suficientemente entendible para demo
- ✅ Phase 3 Web Voice Loop validada: microfono web → WAV PCM 16 kHz mono → `POST /chat/audio` → transcript → response → speech audible en navegador

**Métricas MVP**:

- Varias interacciones de texto seguidas sin crashes
- Respuesta backend en menos de 5 segundos como objetivo inicial
- TTS local reproduce la respuesta; las respuestas largas quedaron revalidadas con el ajuste `-s 135 -g 8` como suficientemente entendibles para demo
- Web validation client permite probar texto y voz contra el backend sin hardware Raspberry
- Fase 3 web completada sin cambiar el contrato backend, sin selector WAV visible y con respuesta audible mediante APIs nativas del browser

## Backlog Cerrado Semanas 1-2

- [x] Implementar endpoint `/chat` básico
- [x] Crear cliente Raspberry de texto con TTS local
- [x] Crear cliente web de validación
- [x] Añadir scripts oficiales locales
- [x] Documentar workflow Codex/OpenCode/NotebookLM/GitHub
- [x] Validar conversación end-to-end con OpenAI real
- [x] Ejecutar demo texto → backend → TTS en Raspberry
- [x] Validar múltiples turnos Raspberry → backend LAN → OpenAI → TTS

## Getting Started

### Prerrequisitos Confirmados

- Raspberry Pi 3 Model B v1.2 con Raspberry Pi OS
- Host Linux con Docker Engine y Docker Compose
- VSCode con Remote SSH extension
- Cuenta OpenAI API (para desarrollo)

### Setup Inicial

1. Clona el repositorio y ejecuta `./tonto.sh setup` en Linux con Docker Compose.
2. El operador configura proveedor y credenciales en `.env`, usando
   `.env.example` como plantilla. El runtime Compose carga ese archivo; los agentes no
   deben leer ni imprimir secretos. Consulta `docs/demo-runbook.md`.
3. Ejecuta `./tonto.sh dev all` para backend y web, o
   `./tonto.sh dev backend` para usar Raspberry/emulador.
4. Backend local: `http://127.0.0.1:8000`; web: `http://127.0.0.1:5173/`.
   Raspberry usa la IP LAN del host, por ejemplo `http://192.168.1.91:8000`.
   Docker expone el backend en la LAN; el firewall debe permitir el puerto.
5. Ejecuta `./tonto.sh dev ui` para el emulador Kivy. La captura/reproducción
   física requiere dispositivo de audio disponible en el host.

### Comandos Oficiales

Usa estos comandos en vez de instalar dependencias o lanzar herramientas a mano:

```bash
./tonto.sh setup
# Opcional: entorno Python del IDE, requiere Python/venv en el host
./tonto.sh setup host
./tonto.sh dev backend
./tonto.sh dev web
./tonto.sh dev ui
./tonto.sh dev all
./tonto.sh test python
./tonto.sh test ui
./tonto.sh test web
./tonto.sh test all
./tonto.sh build all
./tonto.sh down
./scripts/export-docs-for-notebooklm.sh
./scripts/install-git-hooks.sh
```

`down` (alias `stop`) detiene todos los contenedores del proyecto Compose,
incluidos emuladores y tests temporales en ejecución, y elimina sus redes.
Conserva los volúmenes de dependencias, `.venv` local y `web/node_modules`.
Devuelve error si quedan contenedores o redes del proyecto; no limpia otros
proyectos Docker.

`test ui` construye la imagen `ui-emulator` y ejecuta widgets Kivy reales con
SDL2 y Xvfb, sin pantalla física ni servidor X del host. Usa renderizado por
software y un socket X11 temporal aislado. `test all` ejecuta Python, UI y web;
las pruebas UI no capturan audio ni llaman al backend. Requiere ejecutar
`setup` primero para preparar el volumen de dependencias. La prueba táctil y
kiosk en Raspberry sigue siendo una validación separada.

`setup`, `test` y `build` usan `docker-compose.tasks.yml` sin `env_file` y con
`--env-file /dev/null`: no crean ni cargan `.env`, no inyectan las claves de
OpenAI/DevExpert del host y no arrancan el backend real. El archivo runtime y
sus overrides (`COMPOSE_FILE`/`COMPOSE_ENV_FILES`) se ignoran para estas tareas.
`setup host` también retira esas dos claves de su proceso. Las imágenes, cachés
y el volumen `backend-venv` se conservan. Si personalizas `COMPOSE_PROJECT_NAME`,
expórtalo en la shell para tareas y runtime; no basta definirlo solo en `.env`.
Python/UI ya no montan la raíz del repositorio: solo fuentes públicas en modo
read-only, dependencias y cachés/fixtures necesarios. Web monta src/configs
públicos, tests, node_modules y salidas concretas; no monta web/.env. La imagen
UI usa contexto client y client/.dockerignore permite solo Dockerfile.ui.
El CLI prepara directorios escribibles para que Docker no los cree como root.
La configuración runtime sigue recibiendo .env por env_file, sin montarlo como
archivo en /app. No guardar secretos dentro de fuentes/cachés autorizadas.
Esto no aísla al agente del host/daemon ni valida overrides manuales (#110).

El emulador usa `http://backend:8000` dentro de Docker y TTS español con espeak.
`dev ui` reconstruye la imagen y configura `/dev/snd` y los grupos de sus
nodos de carácter mediante un override Compose temporal en Engine nativo.
En **Docker Desktop Linux**, detecta su daemon y conecta la pantalla X11 y el
servicio de audio del usuario mediante puentes temporales en loopback. Requiere
`socat`, `setsid` (util-linux), sesión X11 local y acceso X11 ya permitido al
usuario; no instala paquetes ni modifica permisos del host. Si tu sesión no
autoriza al usuario local, habilítalo desde su terminal con
`xhost +SI:localuser:$(id -un)`; no uses `xhost +`.
PipeWire con protocolo PulseAudio o PulseAudio proporciona captura y reproducción;
el plugin ALSA está dentro de la imagen. Sin servicio de audio, UI/texto siguen
disponibles y la voz muestra error de captura.

Para Desktop, ejecuta `DOCKER_CONTEXT=desktop-linux ./tonto.sh setup` una vez y
`DOCKER_CONTEXT=desktop-linux ./tonto.sh dev ui`. Backend se inicia como dependencia
en ese mismo contexto; los puertos del backend deben estar libres. Cierra la
ventana o usa Ctrl+C para retirar contenedor UI y puentes; backend permanece.
Los puertos locales de puente son 26024 (X11) y 24713 (audio), configurables con
`TONTO_UI_X11_PORT` y `TONTO_UI_AUDIO_PORT`. No se publica en LAN; el puente confía
en los procesos locales. Un puerto ocupado se rechaza sin reutilizar el listener.
Los overrides se retiran al salir, también si el arranque falla.
Respeta `COMPOSE_FILE`/`COMPOSE_PATH_SEPARATOR` exportados en el entorno y los
archivos base/override convencionales. Si la selección de archivos Compose se
configura únicamente en `.env`, el operador debe exportarla para `dev ui`; el
helper no lee archivos de secretos. Kivy usa directorios temporales escribibles
y arranca con `python -m client.touch_ui`. En Engine nativo, sin dispositivos
de audio, síntesis a WAV y pruebas Xvfb siguen siendo posibles; la voz requiere
acceso al hardware. En Desktop no se montan dispositivos ALSA ni sockets host.
El modo PC y Raspberry usan espeak para sintetizar voz en Linux.

En Linux/Docker (vía `tonto.sh`), el `.venv` local sirve únicamente para alimentar el autocompletado del IDE, mientras que Docker maneja y aísla las dependencias reales del contenedor en un volumen propio (`backend-venv`). Las dependencias web viven en `web/node_modules/`. No instales paquetes Python o npm globales para trabajar en el MVP.

`./scripts/install-git-hooks.sh` se ejecuta una vez por clon. Instala un hook local que actualiza la exportación para NotebookLM antes de cada commit.

La exportación de NotebookLM genera fuentes individuales y `exports/notebooklm/NOTEBOOKLM_COMBINED.md`. Para refrescos normales en NotebookLM, usa el documento combinado como fuente principal.

### Desarrollo Diario

- **Spec first**: Actualiza `docs/specs.md` antes de codear
- **AI assist**: Copilot para editor, Codex/OpenCode para cambios completos, NotebookLM para síntesis
- **Test físico**: Siempre valida en Pi real
- **Commit pequeño**: Ramas cortas, Conventional Commits y specs/docs incluidas cuando aplique

## Contribución

Actualmente este proyecto es mantenido por un desarrollador principal con foco en entrega rápida.

Se trabajaa alrededor de un backlog corto con especificaciones validadas y tests reales en Raspberry Pi.

- **Issues**: Bugs o ideas técnicas específicas
- **Ramas**: Usa `<type>/<short-kebab-description>`, por ejemplo `docs/formalize-ai-git-workflow`
- **Commits**: Usa Conventional Commits, por ejemplo `docs: formalize AI-assisted Git workflow`
- **PRs**: Incluye resumen, docs/specs afectadas y verificación ejecutada
- **Reviews**: Feedback técnico honesto, no político
- **Decisiones**: El desarrollador principal valida cambios de arquitectura y dependencias

**Regla**: Si no ayuda al MVP de 6 semanas, no entra.

Las contribuciones actualmente no están permitidas.

## Licencia

MIT - Mantén simple, comparte código.

---

_Proyecto TONTO: IA + Hardware = Aprendizaje Conversacional. Iteración semanal, no metas imposibles._

### Setup y cachés Linux

`./tonto.sh setup` prepara dependencias Docker y web; conserva el `.venv` del
host. `./tonto.sh setup host` instala el entorno opcional del IDE y falla si
Python/venv/pip no están disponibles; no instala paquetes del sistema.
Las cachés pip/npm viven en `.cache/pip` y `.cache/npm` dentro del repositorio,
con permisos del usuario. CI usa el mismo flujo Docker. La reutilización entre
runners de CI no se configura en este cambio.
# Selección de micrófono del emulador

En modo PC, `TONTO_AUDIO_DEVICE` selecciona la entrada PortAudio por índice
numérico o nombre; sin valor se usa la entrada predeterminada. Pasa esta variable
al contenedor con `TONTO_AUDIO_DEVICE=5 ./tonto.sh dev ui`. Los índices dependen del equipo;
no fijes un índice de hardware en el Compose compartido.
En este equipo, 5 corresponde a DMIC hw:0,7 y admite 16 kHz; 4 no los admite.
Consulta entradas con `docker compose run --rm --no-deps ui-emulator .venv/bin/python -m sounddevice`
si la configuración del contenedor permite acceso a audio; el arranque oficial
`dev ui` incorpora ese acceso. Un dispositivo incompatible muestra error y
vuelve a permitir reintentar después de cuatro segundos.
