# Hardware del Proyecto TONTO

## Objetivo

El hardware de TONTO está diseñado siguiendo una estrategia **thin-client**:

- la Raspberry Pi gestiona interacción física y audio,
- mientras que la lógica conversacional y la IA se ejecutan principalmente en un backend remoto.

El objetivo del MVP NO es construir un robot complejo ni una plataforma hardware avanzada.
El objetivo es validar una experiencia educativa conversacional funcional utilizando hardware accesible, reutilizable y fácil de mantener.

---

# Filosofía Hardware

TONTO prioriza:

- reutilizar hardware existente,
- minimizar coste y complejidad,
- evitar componentes innecesarios,
- favorecer estabilidad y facilidad de depuración,
- mantener una arquitectura simple y mantenible.

La experiencia conversacional es el producto principal.
El hardware es únicamente el medio de interacción.

---

# Inventario actual

## Raspberry Pi 3 Model B v1.2

### Rol

Cliente físico principal del sistema.

### Responsabilidades

- reproducción de audio,
- TTS local,
- captura de audio futura,
- comunicación con backend,
- control de estados físicos simples,
- ejecución del cliente TONTO.

### Estado actual

Validado y operativo:

- Raspberry Pi OS instalado,
- conexión SSH funcionando,
- desarrollo remoto mediante VSCode,
- audio output validado,
- `espeak` funcionando correctamente por salida jack.

La preparacion reproducible y los pasos de recuperacion desde una tarjeta SD limpia viven en `docs/raspberry-pi-setup.md`.

### Limitaciones conocidas

- 1 GB RAM,
- CPU limitada,
- no adecuada para modelos IA pesados,
- recursos limitados para múltiples servicios concurrentes.

### Decisión arquitectónica

La Raspberry Pi debe permanecer como:

- thin client,
- simple,
- estable,
- fácil de reiniciar y mantener.

No debe ejecutar procesamiento IA complejo localmente.

---

## Arduino Uno

### Rol

Periférico opcional para estados físicos simples.

### Uso previsto

- LEDs,
- botones,
- pequeños indicadores físicos,
- posibles expresiones visuales básicas.

### Estado actual

Disponible pero todavía no integrado en el MVP.

### Prioridad

Baja-media.

La integración Arduino solo se realizará si aporta valor claro a la experiencia final de la demo.

---

## Starter Kit Arduino

### Contenido

- LEDs,
- resistencias,
- cables,
- botones,
- sensores básicos,
- protoboard.

### Uso previsto

Apoyo experimental para pruebas rápidas de estados físicos.

### Estado actual

Disponible para prototipado rápido.

---

# Hardware pendiente probable

## Micrófono USB

### Objetivo

Permitir interacción por voz real.

### Prioridad

Alta.

### Criterios

- simple,
- económico,
- compatible Linux/Raspberry Pi,
- sin procesamiento complejo integrado.

El MVP no necesita arrays de micrófonos avanzados ni hardware especializado.

---

## Mini altavoz / speaker

### Objetivo

Mejorar claridad de reproducción de voz.

### Prioridad

Media.

### Estado actual

Audio ya validado mediante salida básica local.

---

# Hardware opcional futuro

## Pantalla HDMI compacta

### Objetivo potencial

Mostrar:

- estados simples,
- modo escucha,
- feedback visual mínimo.

### Prioridad

Baja.

TONTO es principalmente voice-first, por lo que una pantalla NO es necesaria para validar el MVP.

---

# Hardware descartado para el MVP

Las siguientes categorías quedan explícitamente fuera del alcance inicial:

- cámaras,
- visión artificial,
- aceleradores IA,
- sensores complejos,
- brazos robóticos,
- automatización doméstica avanzada,
- hardware especializado costoso,
- múltiples microcontroladores.

Razón principal:

añaden complejidad sin desbloquear directamente la experiencia conversacional del MVP.

---

# Estrategia Thin Client

La Raspberry Pi NO es el cerebro principal del sistema.

El procesamiento principal ocurre en el backend:

- conversación IA,
- memoria,
- orquestación,
- lógica del sistema.

La Raspberry únicamente:

- captura entrada,
- reproduce salida,
- controla interacción física,
- mantiene estado local mínimo.

---

# Estado actual validado

Actualmente se ha validado correctamente:

- arranque estable de Raspberry Pi 3,
- desarrollo remoto por SSH,
- integración VSCode Remote SSH validada,
- reproducción audio local,
- TTS local mediante `espeak` validado por jack con voz española,
- estructura básica del entorno de desarrollo.

Todavía pendiente:

- micrófono USB,
- captura de audio,
- pipeline voz completo,
- integración Arduino,
- estados físicos visuales.

---

# Riesgos hardware principales

## Dependencia de red

El sistema depende inicialmente de conectividad entre Raspberry y backend.

### Mitigación

- arquitectura simple,
- manejo básico de errores,
- degradación controlada.

---

## Recursos limitados Raspberry Pi 3

La Raspberry Pi tiene capacidad limitada para procesos concurrentes.

### Mitigación

- mantener cliente ligero,
- evitar procesamiento IA local,
- evitar servicios innecesarios.

---

## Complejidad hardware excesiva

Añadir demasiados componentes puede ralentizar el desarrollo y dificultar depuración.

### Mitigación

- introducir hardware únicamente si desbloquea funcionalidades del MVP,
- priorizar simplicidad sobre espectacularidad.

---

# Criterios para futuras compras

Antes de añadir nuevo hardware debe responderse:

1. ¿Desbloquea directamente una funcionalidad importante del MVP?
2. ¿Reduce complejidad o la aumenta?
3. ¿Puede reutilizarse hardware ya disponible?
4. ¿Complica depuración o estabilidad?
5. ¿Aporta realmente valor a la experiencia educativa?

Si la respuesta no es claramente positiva:
el hardware probablemente no debe añadirse todavía.

---

# Estado del MVP Hardware

## Validado

- Raspberry Pi 3 operativa,
- SSH,
- desarrollo remoto,
- TTS local,
- audio output.

## Próximas prioridades

- micrófono USB,
- captura audio,
- primer pipeline voz completo.

## No prioritario actualmente

- pantallas,
- automatización física compleja,
- sensores,
- hardware visual avanzado.

---

_Última actualización: Mayo 2026_
