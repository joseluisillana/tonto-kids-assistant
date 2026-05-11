# Conversation Loop - First Functional Flow

## Objetivo Funcional

Establecer el primer flujo end-to-end completamente funcional de TONTO:

- Usuario ingresa texto manualmente
- Backend procesa y genera respuesta
- Cliente reproduce respuesta vía TTS

**Estado**: Validación inicial del pipeline completo (MVP)

---

## Flujo Completo

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │ (texto manual)
       ▼
┌─────────────────────┐
│  Cliente (Python)   │
│  main.py            │
└──────┬──────────────┘
       │ (HTTP POST)
       ▼
┌─────────────────────┐
│  Backend (Go)       │
│  main.go            │
└──────┬──────────────┘
       │ (respuesta texto)
       ▼
┌─────────────────────┐
│  Cliente (Python)   │
│  Recibe respuesta   │
└──────┬──────────────┘
       │ (texto a voz)
       ▼
┌─────────────────────┐
│  TTS (espeak)       │
│  Audio salida       │
└─────────────────────┘
```

### Pasos Detallados

1. **Input (Cliente)**
   - Usuario ingresa texto en CLI
   - Validación básica (no vacío, < 500 caracteres)

2. **Transmisión (Cliente → Backend)**
   - HTTP POST a `localhost:8080/chat`
   - Body: `{"message": "texto del usuario"}`
   - Header: `Content-Type: application/json`

3. **Procesamiento (Backend)**
   - Recibe mensaje
   - Genera respuesta (placeholder o integración OpenAI)
   - Retorna respuesta en JSON

4. **Recepción (Cliente)**
   - Parsea respuesta JSON
   - Extrae texto de respuesta

5. **Síntesis de Voz (Cliente)**
   - Invoca `espeak` con el texto
   - Reproduce audio (salida estándar del sistema)

---

## Responsabilidades

### Cliente (Python)

- `client/main.py`:
  - Interfaz de entrada de usuario (CLI simple)
  - Validación de entrada local
  - HTTP POST al backend
  - Parseo de respuesta JSON
  - Invocación de `espeak` con el texto de respuesta
  - Manejo de errores de conexión

### Backend (Go)

- `backend/main.go`:
  - Servidor HTTP en puerto 8080
  - Endpoint POST `/chat`
  - Parseo de JSON del cliente
  - Lógica de generación de respuesta (placeholder o OpenAI)
  - Respuesta en formato JSON `{"response": "texto"}`
  - Logging básico de requests

---

## Criterios de Aceptación

### Funcionalidad

- [ ] Cliente conecta exitosamente a backend en localhost:8080
- [ ] Usuario puede ingresar texto en CLI
- [ ] Backend recibe el mensaje y responde
- [ ] Cliente reproduce la respuesta mediante TTS
- [ ] El audio es audible y comprensible

### Flujo Completo

- [ ] Ciclo completo usuario → input → backend → TTS funciona sin errores
- [ ] No hay bloqueadores de conexión/red
- [ ] TTS se ejecuta sin fallos

### Confiabilidad

- [ ] Manejo de errores en conexión al backend
- [ ] Manejo de respuestas inválidas del backend
- [ ] Reintentos o notificación clara de fallos

### Performance

- [ ] Respuesta del backend < 2 segundos
- [ ] Latencia total end-to-end < 5 segundos

---

## Limitaciones Actuales

### Input

- ✋ Solo texto manual en CLI
- ✋ Sin soporte para audio/micrófono aún
- ✋ Sin procesamiento de lenguaje natural (NLP)

### Backend

- ✋ Sin integración OpenAI (placeholder de respuesta estatica)
- ✋ Sin contexto de conversación (stateless)
- ✋ Sin persistencia de historial

### TTS

- ✋ Solo espeak (sin voces personalizadas)
- ✋ Sin soporte multi-idioma (solo inglés)
- ✋ Sin ajuste de velocidad/tono

### Infra

- ✋ Sin autenticación
- ✋ Sin rate limiting
- ✋ Sin logging persistente

---

## Riesgos Técnicos

| Riesgo                     | Probabilidad | Impacto | Mitigación                                  |
| -------------------------- | ------------ | ------- | ------------------------------------------- |
| **Conexión rechazada**     | Alta         | Crítico | Validar puerto, firewall, backend corriendo |
| **Formato JSON inválido**  | Media        | Alto    | Parser robusto, logging de request/response |
| **espeak no instalado**    | Media        | Alto    | Validar disponibilidad, instrucciones setup |
| **Timeout en backend**     | Media        | Medio   | Timeout configurable, reintentos            |
| **Encoding de caracteres** | Baja         | Medio   | UTF-8 consistente cliente/backend           |

---

## Estado Actual de Implementación

### Completado

- [ ] Estructura de proyecto inicializada
- [ ] `go.mod` y `requirements.txt` definidos
- [ ] Carpetas base creadas

### En Progreso

- [ ] Backend: servidor HTTP básico en `backend/main.go`
- [ ] Cliente: loop de input en `client/main.py`

### Pendiente

- [ ] Endpoint `/chat` en backend
- [ ] Cliente: HTTP POST al backend
- [ ] Cliente: invocación de espeak
- [ ] Testing e2e del flujo completo
- [ ] Integración OpenAI backend

### Bloqueadores

- Ninguno identificado en esta fase MVP

---

## Especificación Técnica Mínima

### Backend (Go)

```
POST /chat HTTP/1.1
Content-Type: application/json

{
  "message": "string (max 500 chars)"
}

Response:
{
  "response": "string"
}
```

### Cliente (Python)

```python
1. Loop: get input from user
2. Validate (not empty, < 500 chars)
3. POST to http://localhost:8080/chat
4. Parse response JSON
5. Execute: espeak "response text"
6. Repeat or exit
```

---

## Próximos Pasos

1. **Backend MVP**: Implementar servidor HTTP + endpoint `/chat` con respuesta estática
2. **Cliente MVP**: Implementar HTTP client + validación + espeak integration
3. **Testing**: Validar ciclo completo manual
4. **OpenAI**: Integración de backend con API OpenAI (post-MVP)

---

## Referencias

- [Audio Pipeline](./audio-pipeline.md)
- [Hardware](../docs/hardware.md)
- [Architecture](../docs/architecture.md)
