# TONTO Kids Assistant

_T.O.N.T.O — Thinking Oriented Natural Tutor Organism_

TONTO es un agente educativo físico con interacción por voz diseñado para acompañar a un niño en su aprendizaje diario mediante conversación natural, personalidad persistente y memoria contextual.

Es un producto AI-first moderno que combina hardware físico accesible con modelos de IA avanzados para crear experiencias de aprendizaje inmersivas y personalizadas.

Nace como proyecto para la formación AI Expert de DevExpert.io, por ello, la IA forma está presente en el núcleo tanto del producto como del proceso de desarrollo.

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
- **IA como núcleo**: IA guía diseño de producto y acelera desarrollo (Copilot/Codex).
- **Spec Driven Development**: Especificaciones claras pero adaptables, validadas por prototipos.
- **Anti-scope-creep**: Solo features que contribuyen al MVP core. No "nice-to-haves".

## Objetivos del MVP (6 semanas)

Prototipo que demuestre conversación educativa básica:

- **Conversación básica**: Input voz → procesamiento IA → output voz.
- **Memoria simple**: Recordar contexto de sesión actual.
- **Estados físicos**: LEDs que reflejan estado de conversación.
- **Wake word**: Activación por voz ("Hey TONTO") o física (wake button).
- **Personalidad básica**: Respuestas adaptadas a edad del niño.

**No incluye**: Personalidad persistente compleja, aprendizaje estructurado, multi-idioma.

## Arquitectura Actual

```
┌─────────────────┐    HTTP APIs    ┌─────────────────┐
│   Raspberry Pi  │◄──────────────►│   Windows PC    │
│   (Thin Client) │                │   (Backend IA)  │
│   v1.2          │                │ Python/FastAPI  │
│                 │                │                 │
│ • Audio I/O     │                │ • OpenAI API    │
│ • Wake Word     │                │ • Memoria       │
│ • TTS (espeak)  │                │ • Orquestación  │
│ • LEDs/Arduino  │                │ • Personalidad  │
│ • GPIO Control  │                │                 │
└─────────────────┘                └─────────────────┘
        ▲                                  ▲
        │                                  │
        └──────── Web Validation Client ───┘
```

### Cliente (Raspberry Pi 3 Model B v1.2)

- **Hardware confirmado**: Audio output validado, espeak funcionando, Arduino Uno para estados físicos.
- **Desarrollo**: VSCode Remote SSH, acceso por SSH remoto.
- **Responsabilidades**: Captura audio, wake word, TTS, control GPIO/Arduino.
- **Tecnología**: Python con bibliotecas de audio (pyaudio, speech_recognition) y GPIO (RPi.GPIO).

### Backend (Windows PC)

- **Decisión MVP**: Python inicialmente para iteración rápida (FastAPI, OpenAI).
- **Responsabilidades**: Llamadas OpenAI, gestión memoria, orquestación respuestas.
- **Tecnología**: Python con FastAPI para APIs, integración OpenAI.

### Cliente Web de Validación

- **Objetivo**: Probar el backend desde navegador sin depender siempre de la Raspberry Pi.
- **Responsabilidades**: Entrada manual de texto, visualización de respuestas, panel tecnico de demo y soporte para CI/despliegue frontend.
- **Tecnología**: React + TypeScript + Vite, con Tailwind CSS como base visual.

## Stack Tecnológico Confirmado

- **Lenguajes**: Python (cliente y backend inicial)
- **Web**: React, TypeScript, Vite, Tailwind CSS
- **IA**: OpenAI API (GPT-4 para conversación)
- **Audio**: pyaudio, speech_recognition, espeak-ng
- **Hardware**: Raspberry Pi 3B v1.2, Arduino Uno
- **Comunicación**: REST APIs (FastAPI)
- **Desarrollo**: Codex, GitHub, GitHub Copilot, VSCode + Remote SSH
- **Documentación**: Markdown plano, NotebookLM para síntesis

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
│   ├── specs.md      # Specs activas
│   └── api.md        # Endpoints
├── scripts/          # Automatización
│   ├── setup-dev.ps1 # Setup local aislado
│   ├── dev.ps1       # Servidores locales
│   ├── test.ps1      # Tests y checks
│   └── build.ps1     # Builds reproducibles
├── tests/            # Tests
│   ├── test_audio.py
│   └── test_api.py
├── .gitignore
└── README.md
```

## Development Workflow

### Semana 1-2: Core Setup

1. **Spec semanal**: Actualizar `docs/specs.md` con objetivos semana.
2. **Prototype**: Implementar feature mínima viable.
3. **AI-Assisted**: Usar Copilot para boilerplate, Codex para lógica compleja.
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

- **Spec writing**: Copilot ayuda a redactar specs claras y técnicas.
- **Code generation**: Codex para APIs, lógica de audio, integración OpenAI.
- **Debugging**: AI para analizar logs y sugerir fixes.
- **Testing**: Generar test cases para edge cases.
- **Documentation**: Sintetizar cambios en specs usando NotebookLM.

**Principio**: AI acelera, no reemplaza. Validar todo en hardware real.

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
- **Memoria storage**: JSON files inicialmente, DB si necesario.
- **Wake word engine**: Picovoice vs custom (por licencia/costo).
- **TTS engine**: espeak vs Google TTS (offline vs calidad).
- **Deployment**: Docker vs native en Pi.

## Riesgos Técnicos Principales

- **Latencia de red**: Conversación requiere <2s respuesta; internet inestable rompe UX.
- **Audio en Pi 3**: CPU limitada puede causar delays en procesamiento voz.
- **OpenAI rate limits**: Costo y límites pueden afectar desarrollo/testing.
- **GPIO reliability**: Arduino integration puede ser inestable.
- **Offline degradation**: Sin IA, experiencia es muy limitada.

## Estado Actual del Proyecto

**Semana 0 completa**: Estructura monorepo, hardware validado, specs iniciales.

- ✅ Raspberry Pi 3B v1.2 configurado con SSH/VSCode Remote
- ✅ Audio output y espeak funcionando
- ✅ Arduino Uno conectado y básico GPIO
- ✅ Backend placeholder (Python) con API básica
- ✅ Cliente placeholder con audio input básico
- 🔄 Próximo: Integración OpenAI, wake word básico

**Métricas MVP**:

- Conversación de 3+ minutos sin crashes
- Wake word accuracy >80%
- Respuesta <3s desde voz a voz
- Estados físicos que reflejan conversación

## Backlog Semana 1

- [ ] Setup OpenAI API integration en backend
- [ ] Implementar endpoint /chat básico
- [ ] Cliente: Captura audio continua
- [ ] Wake word detection simple (keyword spotting)
- [ ] TTS response playback
- [ ] Test end-to-end: voz → API → voz

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
   .\scripts\dev.ps1 -Service backend
   ```

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
   - Cliente conecta y recibe audio
   - Web principal en `http://127.0.0.1:5173/`
   - Panel tecnico en `http://127.0.0.1:5173/admin`

### Comandos Oficiales

Usa estos comandos en vez de instalar dependencias o lanzar herramientas a mano:

```powershell
.\scripts\setup-dev.ps1
.\scripts\dev.ps1 -Service backend
.\scripts\dev.ps1 -Service web
.\scripts\dev.ps1 -Service all
.\scripts\test.ps1 -Target all
.\scripts\build.ps1 -Target all
```

Python usa siempre el entorno virtual local `.venv/`. Las dependencias web viven en `web/node_modules/`. No instales paquetes Python o npm globales para trabajar en el MVP.

### Desarrollo Diario

- **Spec first**: Actualiza `docs/specs.md` antes de codear
- **AI assist**: Copilot para code, Codex para logic
- **Test físico**: Siempre valida en Pi real
- **Commit pequeño**: Cambios diarios, specs incluidas

## Contribución

Actualmente este proyecto es mantenido por un desarrollador principal con foco en entrega rápida.

Se trabajaa alrededor de un backlog corto con especificaciones validadas y tests reales en Raspberry Pi.

- **Issues**: Bugs o ideas técnicas específicas
- **PRs**: Incluye spec changes y tests
- **Reviews**: Feedback técnico honesto, no político
- **Decisiones**: El desarrollador principal valida cambios de arquitectura y dependencias

**Regla**: Si no ayuda al MVP de 6 semanas, no entra.

Las contribuciones actualmente no están permitidas.

## Licencia

MIT - Mantén simple, comparte código.

---

_Proyecto TONTO: IA + Hardware = Aprendizaje Conversacional. Iteración semanal, no metas imposibles._
