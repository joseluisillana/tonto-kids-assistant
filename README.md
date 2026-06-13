# TONTO Kids Assistant

_T.O.N.T.O — Thinking Oriented Natural Tutor Organism_

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
│     Raspberry Pi     │──────────────────────────────────────►│      Windows PC      │
│    Thin Client v1.2  │                                       │      Backend IA      │
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

- **Hardware confirmado**: Audio output validado y `espeak` funcionando.
- **Desarrollo**: VSCode Remote SSH, acceso por SSH remoto.
- **Responsabilidades actuales**: entrada manual de texto, llamadas HTTP al backend, TTS local, manejo básico de errores y loop de voz automatizado con `client/main.py --mode voice`.
- **Responsabilidades futuras**: wake word, control físico/Arduino y otras capacidades fuera del MVP inmediato.
- **Tecnología**: Python estándar para el primer loop; dependencias de audio/GPIO se añadirán solo cuando entren en alcance.

### Backend (Windows PC)

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
- **Hardware**: Raspberry Pi 3B v1.2; Arduino Uno queda futuro para estados físicos
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
├── shared/           # Código compartido
│   ├── models.py     # DTOs y modelos
│   └── config.py     # Configuración común
├── docs/             # Documentación técnica
│   ├── README.md     # Índice documental
│   ├── specs.md      # Specs activas
│   └── decisions.md  # Decisiones técnicas
├── scripts/          # Automatización
│   ├── setup-dev.ps1 # Setup local aislado
│   ├── dev.ps1       # Servidores locales
│   ├── test.ps1      # Tests y checks
│   ├── build.ps1     # Builds reproducibles
│   └── export-docs-for-notebooklm.ps1
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

**Semana 4 - Kickoff documental preparado**. El siguiente hito queda faseado en `specs/week-04-demo-stability.md` y `docs/plans/week-04-demo-stability.md`: primero validar la demo actual varias veces, después corregir solo bloqueos reales, calibrar conversación/memoria corta si hace falta, y decidir explícitamente si Arduino/LEDs aportan suficiente valor para entrar en el MVP.

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
- PC Windows con Python 3.9+
- VSCode con Remote SSH extension
- Cuenta OpenAI API (para desarrollo)

### Setup Inicial

1. **Clona y configura**

   ```powershell
   git clone <repo-url>
   cd tonto-kids-assistant
   .\scripts\setup-dev.ps1
   ```

2. **Levanta el backend**

   ```powershell
   $env:TONTO_INFERENCE_PROVIDER="openai"
   $env:OPENAI_API_KEY="<your-openai-api-key>"
   .\scripts\dev.ps1 -Service backend
   ```

   Para usar DevExpert Inference en lugar de OpenAI:

   ```powershell
   $env:TONTO_INFERENCE_PROVIDER="devexpert"
   $env:DEVEXPERT_API_KEY="<your-devexpert-api-key>"
   .\scripts\dev.ps1 -Service backend
   ```

   Para permitir que la Raspberry Pi acceda al backend desde la misma red:

   ```powershell
   .\scripts\dev.ps1 -Service backend -AllowLan
   ```

   En ese modo usa la IP LAN del PC Windows en `TONTO_BACKEND_URL`, por ejemplo `http://192.168.1.91:8000`.

3. **Levanta el cliente web de validación**

   ```powershell
   .\scripts\dev.ps1 -Service web
   ```

4. **O levanta backend y web juntos**

   ```powershell
   .\scripts\dev.ps1 -Service all
   ```

5. **Verifica comunicación**
   - Backend en `http://127.0.0.1:8000`
   - Backend para Raspberry en LAN con `.\scripts\dev.ps1 -Service backend -AllowLan`
   - Cliente conecta y recibe audio
   - Web principal en `http://127.0.0.1:5173/`
   - Panel tecnico en `http://127.0.0.1:5173/admin`

### Comandos Oficiales

Usa estos comandos en vez de instalar dependencias o lanzar herramientas a mano:

```powershell
.\scripts\setup-dev.ps1
.\scripts\dev.ps1 -Service backend
.\scripts\dev.ps1 -Service backend -AllowLan
.\scripts\dev.ps1 -Service web
.\scripts\dev.ps1 -Service all
.\scripts\test.ps1 -Target all
.\scripts\build.ps1 -Target all
.\scripts\export-docs-for-notebooklm.ps1
.\scripts\install-git-hooks.ps1
```

Python usa siempre el entorno virtual local `.venv/`. Las dependencias web viven en `web/node_modules/`. No instales paquetes Python o npm globales para trabajar en el MVP.

`.\scripts\install-git-hooks.ps1` se ejecuta una vez por clon. Instala un hook local que actualiza la exportación para NotebookLM antes de cada commit.

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
