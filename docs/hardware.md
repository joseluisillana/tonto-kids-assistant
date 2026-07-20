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
- captura de audio,
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

La validacion de Semana 3 confirmo captura WAV mono a 16 kHz con microfono USB, subida a `POST /chat/audio`, STT backend con OpenAI `gpt-4o-mini-transcribe`, respuesta educativa y reproduccion local con `espeak`. Phase 2B automatizo ese flujo en el cliente Raspberry y Phase 3 validó el mismo contrato desde navegador.

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

### Estado actual

Validado en Semana 3 con Mini USB Microphone M-305. ALSA lo detecto como `USB PnP Sound Device`; el numero de `card` vario entre validaciones (`card 2` inicialmente y `card 1` despues), por lo que debe confirmarse con `arecord -l` antes de grabar. La grabacion funciono con `arecord -D plughw:<CARD>,<DEVICE> -f S16_LE -r 16000 -c 1 -d 10 ~/tonto-mic-check.wav` y la reproduccion local funciono con `aplay ~/tonto-mic-check.wav`.

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

## Pantalla Táctil HDMI (Waveshare 5")

### Rol

Interfaz visual principal interactiva (Touch UI) y despliegue de la cara animada de TONTO.

### Objetivo

Mostrar:

- UI táctil con botón para hablar,
- estados visuales (cara animada: idle, escuchando, pensando, hablando, error),
- panel de texto opcional para transcripción.

### Prioridad

Alta (Post-MVP Touch UI).

### Configuración (Raspberry Pi 3)

La pantalla se conecta por HDMI (video) y USB (alimentación y touch). Para configurar la resolución correcta y la funcionalidad táctil:

1. Editar el archivo de configuración de arranque:
   ```bash
   sudo nano /boot/config.txt
   ```
2. Añadir las siguientes líneas al final del archivo:
   ```ini
   max_usb_current=1
   hdmi_group=2
   hdmi_mode=87
   hdmi_cvt 800 480 60 6 0 0 0
   hdmi_drive=1
   ```
3. Reiniciar la Raspberry Pi para aplicar los cambios:
   ```bash
   sudo reboot
   ```
4. El touch (USB) debería ser Plug-and-Play usando `evdev` en Raspbian. Para calibración opcional si la precisión es pobre:
   ```bash
   sudo apt-get install xserver-xorg-input-evdev
   sudo cp -rf /usr/share/X11/xorg.conf.d/10-evdev.conf /usr/share/X11/xorg.conf.d/45-evdev.conf
   # Reiniciar el entorno gráfico
   ```

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
- captura WAV con microfono USB en Raspberry,
- cliente Raspberry `--mode voice` para captura, subida a `POST /chat/audio`, respuesta y TTS local,
- contrato web de voz Phase 3 contra `POST /chat/audio` desde navegador,
- estructura básica del entorno de desarrollo.

Todavía pendiente:

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
- audio output,
- micrófono USB Mini USB Microphone M-305 detectado por ALSA,
- captura y reproduccion local de WAV con `arecord` y `aplay`,
- pipeline de voz de Semana 3: Raspberry `--mode voice` -> `POST /chat/audio` -> STT backend -> respuesta -> `espeak`,
- validacion web Phase 3 del mismo contrato de audio desde navegador.

## Próximas prioridades

- seleccionar el siguiente hito del MVP antes de añadir nuevo comportamiento,
- mejorar experiencia demo y estados físicos solo si desbloquean la demo final.

## No prioritario actualmente

- pantallas,
- automatización física compleja,
- sensores,
- hardware visual avanzado.

---

_Última actualización: Junio 2026_
