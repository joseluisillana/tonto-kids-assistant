# Arquitectura TONTO

## 1. Visión General

TONTO es un asistente de conversación para niños ejecutándose en una **Raspberry Pi 3 Model B v1.2** con un backend de lógica centralizado. La arquitectura sigue un modelo **thin-client** donde la Raspberry es responsable de entrada/salida física y el backend maneja inteligencia e integración con servicios externos.

```
┌─────────────────────────────────────────────────┐
│           Raspberry Pi 3 B v1.2                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Cliente TONTO (Python)                   │  │
│  │ - Captura audio (micrófono)              │  │
│  │ - Reproducción TTS (altavoz)             │  │
│  │ - Estados LED/físicos                    │  │
│  │ - Interacción física básica              │  │
│  └──────────────────────────────────────────┘  │
└─────────────────┬──────────────────────────────┘
                  │
                  │ HTTP/REST (JSON)
                  │ (WiFi/LAN)
                  ▼
┌─────────────────────────────────────────────────┐
│       Backend (Windows/Linux/Cloud)             │
│  ┌──────────────────────────────────────────┐  │
│  │ Orquestador (Python/Go)                  │  │
│  │ - Gestiona conversaciones                │  │
│  │ - Llama IA, memoria, lógica              │  │
│  │ - Retorna respuestas formateadas         │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │ Servicios Externos                       │  │
│  │ - OpenAI (IA conversacional)             │  │
│  │ - Storage (memoria de usuario)           │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 2. Componentes Principales

### 2.1 Cliente Raspberry Pi (`client/`)

**Lenguaje:** Python 3  
**Dependencias:** `requirements.txt`

**Responsabilidades:**

- **Audio input:** Captura de micrófono en tiempo real
- **Audio output:** Reproducción de síntesis de voz (TTS)
- **Estados visuales:** Control de LEDs, indicadores físicos
- **Comunicación:** Envía requests HTTP al backend, recibe respuestas JSON
- **Sesiones:** Mantiene session_id local para contexto de conversación

**Limitaciones intencionales:**

- No procesa IA
- No almacena lógica de negocio
- No gestiona memoria persistente de usuario

### 2.2 Backend (`backend/`)

**Lenguaje:** Go (inicialmente)  
**Port:** 8080 (desarrollo)

**Responsabilidades:**

- **Orquestación:** Router HTTP, gestión de requests
- **Lógica conversacional:** Estructura básica de diálogos
- **Integración IA:** Llamadas a OpenAI API
- **Memoria:** Gestión de historial de conversación
- **Formateo de respuestas:** Prepara audio, texto, acciones físicas

### 2.3 Modelos Compartidos (`shared/`)

**`models.py`** contiene estructuras de datos comunes:

- `ConversationMessage` (id, timestamp, content, role)
- `ClientRequest` (session_id, audio_data/text)
- `ServerResponse` (audio_url, text, action)
- `Session` (metadata de usuario)

---

## 3. Responsabilidades: Raspberry vs Backend

| Aspecto            | Raspberry Pi                  | Backend                |
| ------------------ | ----------------------------- | ---------------------- |
| **Audio**          | Captura/reproducción física   | Generación TTS         |
| **Entrada**        | Micrófono → Buffer → HTTP     | N/A                    |
| **Salida**         | HTTP ← Altavoz/LED            | Formato de respuesta   |
| **IA**             | N/A                           | Llamadas OpenAI        |
| **Memoria**        | Session ID local              | Base de datos usuarios |
| **Estado físico**  | Ejecuta acciones (LED, motor) | Ordena acciones        |
| **Lógica negocio** | Nada                          | Todo                   |
| **Errores**        | Manejo UI local               | Logs centralizados     |

---

## 4. Flujo Conversacional Básico

### Flujo lineal de una conversación:

```
1. Usuario activa dispositivo físico (botón)
                ↓
2. Raspberry inicia captura de audio (3-10s)
                ↓
3. POST /api/conversation/start
   Body: { session_id, audio_file }
                ↓
4. Backend procesa audio:
   - Extrae texto (Whisper/API externa)
   - Envía a OpenAI
   - Obtiene respuesta IA
   - Genera TTS de respuesta
                ↓
5. Response JSON:
   {
     "tts_url": "https://...",
     "text": "...",
     "action": "led_blink"
   }
                ↓
6. Raspberry recibe, reproduce audio, ejecuta acción
                ↓
7. Fin conversación (timeout o botón)
```

### Endpoints iniciales:

- `POST /api/conversation/start` - Inicia conversación
- `GET /api/conversation/{session_id}` - Historial
- `POST /api/session/create` - Nuevo usuario/sesión

---

## 5. Arquitectura Thin-Client

### Principios:

1. **Raspberry es dispositivo sin estado:** No toma decisiones lógicas.
2. **Backend es fuente de verdad:** Todo lo importante vive aquí.
3. **HTTP/REST es interfaz:** Simple, stateless, repetible.
4. **Idempotencia:** Requests pueden reintentarse sin efectos secundarios.

### Ventajas:

- Raspberry puede ser reemplazada sin perder datos
- Backend escalable independientemente
- Fácil testing de lógica en backend
- Hardware limitado (Pi 3) no es bottleneck

### Limitaciones aceptadas:

- Latencia de red es unavoidable
- Backend es punto único de fallo para IA
- Sesiones ephemeral en Raspberry (OK para MVP)

---

## 6. Integración Futura: Arduino

**Timing:** Post-MVP (no incluido en primer release)

### Conexión física:

```
Raspberry Pi
    ├── GPIO (pines libres)
    └── USB Serial
         │
         ↓
    Arduino (opcional)
    ├── Motores
    ├── Sensores
    └── Actuadores adicionales
```

### Modelo de integración:

- **Arduino como "periférico de Raspberry":**
  - Raspberry Pi mantiene comunicación serial con Arduino
  - Backend ordena acciones complejas a Raspberry
  - Raspberry traduce a comandos Arduino
  - No comunicación directa Backend ↔ Arduino

**Razón:** Mantener Raspberry como "gateway" de hardware, Backend como orquestador.

---

## 7. Principios Arquitectónicos

### 7.1 Simplicidad

- Una sola vía de comunicación (HTTP)
- Datos en JSON, sin protocol buffers
- Endpoints RESTful simples
- No event streams, queues, ni choreography (MVP)

### 7.2 Monolito Backend Inicial

- Toda lógica en único proceso
- Base de datos simple (SQLite o archivo JSON para MVP)
- Sin microservicios
- Fácil de debuggear localmente

### 7.3 Stateless Raspberry

- Reinicia sin romper nada
- Session ID es única identificación
- No almacena decisiones de negocio

### 7.4 Fallar de forma segura

- **Timeout en Raspberry:** Si backend no responde en 5s, cancela y avisa al usuario
- **Retry en Backend:** Si OpenAI falla, respuesta genérica predefinida
- **Logs centralizados:** Backend registra todo para debugging

### 7.5 MVP First

- No preparar para 1M users
- No agregar persistencia si no es necesario
- No abstracciones prematuras
- Refactor cuando el código duela

---

## 8. Decisiones de Arquitectura Tomadas

### 8.1 Thin-Client (Raspberry)

**Decisión:** Raspberry es cliente sin lógica de negocio  
**Por qué:**

- Raspberry 3 B tiene CPU/RAM limitados
- Actualizaciones de lógica sin flashear dispositivo
- Debugging centralizado
- Escalabilidad horizontal futura

### 8.2 Backend único (no microservicios)

**Decisión:** Monolito Python/Go en Windows inicialmente  
**Por qué:**

- MVP de 6 semanas, equipo pequeño
- Overhead de microservicios no justificado
- Database única, transacciones ACID simples
- Deployment simple (ejecutable single)

### 8.3 OpenAI como IA

**Decisión:** LLM externo (no local en Raspberry)  
**Por qué:**

- Raspberry no tiene GPU
- OpenAI tiene quality superior a modelos locales
- Actualizaciones automáticas
- Pay-per-use (economía MVP)

**Alternativa futura:** Reemplazar con LLM local si costo no es viable

### 8.4 HTTP/REST para comunicación

**Decisión:** No websockets, no gRPC  
**Por qué:**

- Simple de debuggear
- Herramientas estándar (curl, Postman)
- Latencia aceptable para conversación
- No requiere librerías especiales en cliente

### 8.5 JSON para datos

**Decisión:** No protocol buffers, no msgpack  
**Por qué:**

- Legible en debuggear
- Python/Go soporte nativo
- Size no es crítico en MVP

---

## 9. Decisiones Aún Abiertas

### 9.1 Storage persistente

**Pregunta:** ¿Dónde guardar historial de usuario?

**Opciones:**

- SQLite (archivo local en backend)
- JSON files (prototipo rápido)
- PostgreSQL (overkill para MVP)

**Estado:** Pendiente decisión. Usar archivo JSON para MVP.

### 9.2 Autenticación

**Pregunta:** ¿Cómo identificar sesiones?

**Opciones:**

- Device ID simple (hardware Raspberry)
- QR code en startup
- Cloud account (futura)

**Estado:** Pendiente. Usar device ID simple inicialmente.

### 9.3 TTS local vs. cloud

**Pregunta:** ¿Generar audio donde?

**Opciones:**

- Backend genera con Google TTS API (actual)
- Raspberry genera con pyttsx3 local
- Mezcla (backend text, Raspberry TTS)

**Estado:** Pendiente benchmarking. Probar backend-side inicialmente.

### 9.4 Escalabilidad de backend

**Pregunta:** ¿A qué punto pasar de monolito a componentes?

**Criterios:**

- > 5 Raspberry Pis simultáneas
- > 100 usuarios
- Latencia > 2s (bottleneck identificado)

**Estado:** No iniciamos escalabilidad hasta alcanzar límites.

### 9.5 Deployment

**Pregunta:** ¿Dónde corre el backend?

**Opciones:**

- Windows local (desarrollo)
- Linux en cloud (AWS, Digital Ocean)
- Docker container (futuro)

**Estado:** Windows local inicialmente, plan migrar a Linux simple (1 VPS).

### 9.6 Error handling y observabilidad

**Pregunta:** ¿Cómo monitorear el sistema?

**Opciones:**

- Logs en archivo simple
- Logging centralizado (ELK stack)
- Métricas Prometheus

**Estado:** Logs simples en archivo inicialmente.

---

## 10. Caminos de Evolución (Post-MVP)

### Fase 2 (Meses 2-3)

- [ ] Arduino integration
- [ ] Memoria persistente mejorada
- [ ] Múltiples Raspberry Pis (round-robin)
- [ ] Dashboard simple de uso

### Fase 3 (Meses 3-4)

- [ ] LLM local en Raspberry si OpenAI cost es issue
- [ ] WebRTC para streaming audio (si latencia es problema)
- [ ] Cache de respuestas comunes

### Fase 4 (Meses 4+)

- [ ] Microservicios si componentes saturan
- [ ] Horizontal scaling de backend
- [ ] Integración cloud
- [ ] App móvil para padres

---

## 11. Referencias Rápidas

- **Specs de hardware:** [hardware.md](hardware.md)
- **Visión de producto:** [vision.md](vision.md)
- **Roadmap:** [roadmap.md](roadmap.md)
- **Flujo conversacional detallado:** [conversation-loop.md](../specs/conversation-loop.md)
- **Audio pipeline:** [audio-pipeline.md](../specs/audio-pipeline.md)

---

## 12. Decisiones NO tomadas (anti-goals)

- ❌ Microservicios iniciales
- ❌ Autoscaling automático
- ❌ Cache distribuida
- ❌ Message queues
- ❌ Kubernetes
- ❌ Arquitectura "enterprise"
- ❌ Over-engineering

**Filosofía:** Build boring, build simple, build it works. Refactor cuando duela.
