# Hardware del Proyecto TONTO

## Propósito General

El hardware de TONTO sigue una **estrategia thin-client**: la Raspberry Pi es un cliente ligero que captura entrada del usuario y reproduce respuestas, delegando toda la lógica conversacional y procesamiento al backend.

---

## Inventario Actual

### 1. **Raspberry Pi 3 Model B v1.2** (Controlador Principal)

| Aspecto          | Detalle                                                                                  |
| ---------------- | ---------------------------------------------------------------------------------------- |
| **Propósito**    | Ejecuta cliente Python. Captura entrada de usuario y reproduce audio de respuestas.      |
| **Rol**          | Thin-client: sin lógica de negocio, sin almacenamiento persistente.                      |
| **Comunicación** | HTTP/REST al backend (Go/Python en Windows u otro servidor).                             |
| **Limitaciones** | CPU modesta (quad-core 1.2 GHz), 1 GB RAM, sin GPU. Suficiente para cliente, no para IA. |
| **Ventaja**      | Económica, bajo consumo eléctrico, forma compacta.                                       |

**Rol esperado:** Punto de entrada del niño. Recibe comandos de voz/texto, envía al backend, reproduce respuestas.

---

### 2. **Arduino Uno** (I/O Futuro - Por Definir)

| Aspecto               | Detalle                                                         |
| --------------------- | --------------------------------------------------------------- |
| **Propósito**         | TBD - Posible control de periféricos (LEDs, botones, sensores). |
| **Comunicación**      | Serial USB a Raspberry Pi.                                      |
| **Decisión Temporal** | No integrado en MVP. Reservado para expansión post-MVP.         |
| **Razón**             | Simplicidad sobre características iniciales.                    |

**Estado:** En inventario, sin uso planificado antes de MVP estable.

---

### 3. **Starter Kit Arduino** (Componentes Varios)

| Aspecto               | Detalle                                                     |
| --------------------- | ----------------------------------------------------------- |
| **Contenido**         | LEDs, resistencias, botones, sensores, cables, proto-board. |
| **Uso Potencial**     | Apoyo futuro a Arduino Uno.                                 |
| **Decisión Temporal** | Inventario de respaldo. No crítico para MVP.                |

---

## Hardware Pendiente (Probable)

### 1. **Micrófono USB**

- **Propósito:** Entrada de voz clara del usuario.
- **Requerimiento:** Mejor que micrófono integrado (si existiera) o entrada por texto.
- **Prioridad:** Alta (si se implementa entrada de voz).
- **Decisión:** Evaluar costo/calidad. Preferir modelo simple (no array de micrófonos).

### 2. **Mini Speaker / Altavoz Compacto**

- **Propósito:** Reproducción de audio (respuestas TTS del backend).
- **Requerimiento:** Audio claro para niño. Amplitud suficiente sin ser estridentes.
- **Prioridad:** Media-Alta (si se implementa TTS).
- **Decisión:** USB o conector jack de 3.5 mm. Evaluar opciones económicas.

### 3. **Pantalla HDMI Compacta**

- **Propósito:** Mostrar feedback visual (animaciones, contexto conversacional, modo "listening").
- **Requerimiento:** Pantalla pequeña (7-10 pulgadas) con HDMI.
- **Prioridad:** Baja. Funcionalidad MVP es conversacional (voz/texto), no visual.
- **Decisión:** Evaluar solo si hay presupuesto tras MVP estable.

---

## Hardware Descartado (Por Ahora)

### ❌ Cámaras

- **Razón:** Añaden complejidad (visión, privacy). MVP es conversacional, no visual.
- **Futuro:** Posible en expansión si se requiere reconocimiento de gestos.

### ❌ Sensores Ambientales (temperatura, humedad, luz, etc.)

- **Razón:** Fuera del scope de asistente conversacional infantil.
- **Futuro:** Opcional si se expande a monitoreo del entorno.

### ❌ Pantalla Integrada en Raspberry

- **Razón:** Costo vs beneficio. HDMI externa es más flexible.

### ❌ GPU / Hardware Acelerador de IA

- **Razón:** IA ejecuta en backend (OpenAI API). Raspberry no procesa modelos.
- **Decisión Arquitectónica:** Thin-client, no compute-heavy en la Pi.

---

## Decisiones de Diseño

### 1. **Thin-Client (Raspberry Pi sin IA)**

**Decisión:** Toda la inteligencia (OpenAI API) y lógica ejecuta en backend.

- ✅ **Ventaja:** Raspberry simple, económica, bajo mantenimiento.
- ✅ **Ventaja:** Backend escalable, upgrades sin tocar hardware en campo.
- ❌ **Trade-off:** Depende de conectividad red.

### 2. **Simplicidad Sobre Características**

**Decisión:** MVP con Raspberry + conexión HTTP al backend. Sin Arduino, sin pantalla, sin sensores inicialmente.

- ✅ **Ventaja:** Tiempo de desarrollo menor. Más fácil debuggear.
- ❌ **Trade-off:** Menos atractivo visualmente, funcionalidad limitada.

### 3. **Storage: Backend, No Raspberry**

**Decisión:** Raspberry sin almacenamiento persistente local. Sesiones identificadas por `session_id` vía backend.

- ✅ **Ventaja:** Stateless Raspberry. Fácil de replicar/reemplazar.
- ✅ **Ventaja:** Datos centralizados en backend (más seguro para niño).
- ❌ **Trade-off:** Requiere conexión activa al backend.

---

## Conectividad y Deployment

| Componente               | Conexión                       |
| ------------------------ | ------------------------------ |
| Raspberry Pi ↔ Backend   | Ethernet o WiFi (LAN/Internet) |
| Raspberry Pi ↔ Arduino   | Serial USB (futuro)            |
| Raspberry Pi ↔ Micrófono | USB (futuro)                   |
| Raspberry Pi ↔ Pantalla  | HDMI (futuro, opcional)        |

---

## Restricciones y Limitaciones Conocidas

| Limitación                | Impacto                                           | Mitigation                                             |
| ------------------------- | ------------------------------------------------- | ------------------------------------------------------ |
| **Raspberry Pi 1 GB RAM** | Limita procesos concurrentes, imposible IA local. | Mantener cliente simple (Python async). IA en backend. |
| **Procesador 1.2 GHz**    | TTS local sería lento.                            | TTS en backend.                                        |
| **Dependencia Red**       | Sin red = sin funcionalidad.                      | Caché local futuro (post-MVP).                         |
| **Arduino no integrado**  | Expansión I/O limitada inicialmente.              | Reservado para post-MVP.                               |
| **Sin pantalla inicial**  | Feedback visual limitado a audio.                 | UX basada en texto + voz.                              |

---

## Roadmap Hardware

### MVP (Fase 1)

- ✅ Raspberry Pi 3B v1.2 + cliente Python
- ✅ Conexión HTTP al backend
- 🔵 Entrada: teclado USB o SSH remoto
- 🔵 Salida: texto en terminal o via API

### Post-MVP (Fase 2)

- ⏳ Micrófono USB (entrada voz)
- ⏳ Mini speaker (salida audio TTS)
- ⏳ Arduino integrado (expansión I/O)

### Futuro (Fase 3+)

- ⏳ Pantalla HDMI pequeña (UI visual)
- ⏳ Sensores opcionales (según business case)

---

## Notas de Coste y Sostenibilidad

- **Raspberry Pi:** ~$50 USD (margen económico).
- **Arduino Uno + Kit:** ~$30 USD (respaldo, opcional).
- **Micrófono USB:** ~$10-20 USD.
- **Mini Speaker:** ~$15-30 USD.
- **Pantalla HDMI 7":** ~$50-100 USD (bajo prioridad).

**Filosofía:** Comenzar mínimo (solo Raspberry), agregar periféricos según validación de MVP.

---

_Última actualización: Mayo 2026_
