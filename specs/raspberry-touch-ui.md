# TONTO Raspberry Touch UI con Cara Animada

## Visión General

Esta especificación define el trabajo post-MVP para convertir la Raspberry Pi de un cliente de voz por terminal a un asistente físico con interfaz visual.
Se usará una pantalla táctil HDMI Waveshare de 5" conectada a la Raspberry Pi.

La interfaz mantendrá a la Raspberry como un "thin client" (el procesamiento sigue en el backend), pero añadirá una cara animada programática, un botón para hablar y estados visuales (inactivo, escuchando, pensando, hablando, error). El modo texto (transcripción/respuesta) será opcional y estará oculto bajo un control para uso del operador o el niño.

## Fases de Ejecución

Para mantener el trabajo simple, secuencial y unitario, la implementación se divide en las siguientes fases:

### Fase 0: Tracking y Registro en GitHub
Antes de escribir código o configurar hardware, se debe registrar el trabajo en el repositorio.
- **Acción:** Crear un Parent Issue ("Raspberry Touch UI with animated assistant face") y un Phase Issue por cada una de las fases listadas abajo.
- **Objetivo:** Cumplir con la regla de coordinación mediante GitHub CLI definida en el workflow.

### Fase 1: Setup y Validación de Hardware
- **Acción:** Conectar físicamente la pantalla Waveshare 5" por HDMI y USB (para touch) a la Raspberry Pi 3.
- **Objetivo:** Verificar salida de video, calibrar el touch, comprobar que el audio (micrófono USB y altavoz) sigue funcionando sin problemas de alimentación.
- **Entregable:** Todo el proceso de configuración y comandos de prueba documentados en `docs/hardware.md` (o archivo similar) para asegurar reproducibilidad.

### Fase 2: Spike de Runtime y Stack Tecnológico
- **Acción:** Evaluar opciones para renderizar la UI en la Raspberry (ej. Chromium en modo kiosko con cliente web local vs. un cliente local ligero en Python/Tkinter/Pygame u otra opción).
- **Objetivo:** Tomar en cuenta los recursos limitados de la Raspberry Pi 3 y el estado actual de la configuración para elegir la solución más fluida y sencilla.
- **Entregable:** Decisión documentada en `docs/decisions.md` y un esqueleto (scaffold) básico del cliente validado en el hardware.

### Fase 3: Diseño Visual de la Cara Animada
- **Acción:** Proponer y elegir el diseño base visual de TONTO. Se utilizarán imágenes de ejemplo o modelos de generación de imágenes (GenAI) para visualizar conceptos y paletas.
- **Objetivo:** Tener referencias claras de cómo se verá el personaje (forma, ojos, boca, estilo flat/3D) antes de intentar animarlo.
- **Entregable:** Referencias visuales seleccionadas e incorporadas al repositorio como base de diseño.

### Fase 4: Spike y Evaluación Técnica de Animación
- **Acción:** Explorar formas de renderizar el diseño elegido de manera *programática* (no basada en videos pesados) para que sea simple pero evolucionable.
- **Objetivo:** Elegir el motor o librería adecuada (dependiendo de la decisión de la Fase 2) para dibujar los estados: idle, listening, thinking, speaking, error.
- **Entregable:** Decisión técnica y un prototipo de animación visualizado en la pantalla.

### Fase 5: Cliente Táctil Mínimo
- **Acción:** Construir la UI base con el motor elegido.
- **Elementos requeridos:**
  - Botón táctil gigante para "hablar" (reemplaza al 'Enter' del terminal).
  - Integración con el STT local (captura de micrófono) usando `POST /chat/audio`.
  - Panel oculto (modo texto) activable por un control/botón para ver la transcripción y la respuesta textual.
- **Entregable:** El cliente graba audio al tocar la pantalla y recibe respuesta textual/hablada del backend.

### Fase 6: Integración de Cara Animada y Estados
- **Acción:** Integrar el prototipo de la Fase 4 con el cliente funcional de la Fase 5.
- **Objetivo:** Que la cara responda a los estados reales de la interacción de voz (cambiar a cara de "escuchando" al grabar, "pensando" al esperar al backend, y sincronizar la cara "hablando" con la duración de la respuesta TTS).
- **Entregable:** Experiencia audiovisual integrada y fluida.

### Fase 7: Kiosk Mode, Fallback y Validación Final
- **Acción:** Configurar el autostart para que la UI cargue en pantalla completa (kiosko) al encender la Raspberry.
- **Objetivo:** Asegurar que la experiencia es "appliance-like".
- **Validación:** Comprobar que el fallback de terminal (`client/main.py`) sigue funcionando si la UI gráfica falla.

## Criterios de Éxito
- La Raspberry arranca y muestra la interfaz sin interacción del operador (teclado/ratón adicional).
- Un niño puede tocar la pantalla y hablar sin ver la terminal.
- La experiencia de terminal previa sigue funcional y documentada como Plan B.
- Todo el hardware y stack están documentados para reproducir una Raspberry idéntica.

## Detalles Técnicos de Implementación (Fases 3-6)

Durante el desarrollo de la interfaz táctil se han consolidado las siguientes decisiones técnicas:

### 1. Stack Visual (Kivy)
- El framework Kivy ha demostrado ser el más adecuado para renderizar directamente en el framebuffer de la Raspberry Pi sin entorno de escritorio, capturando eventos táctiles vía `mtdev`.
- La cara animada (`TontoFace`) se dibuja paramétricamente usando `kivy.graphics` en vez de cargar GIFs, permitiendo escalado vectorial y rendimiento nativo.

### 2. Pipeline de Audio Multiplataforma
Se ha introducido la variable de entorno `TONTO_AUDIO_MODE` para permitir desarrollo sin fricción en equipos de escritorio:
- `raspberry` (por defecto): Usa ALSA (`arecord`) para captura y `espeak` para síntesis de voz.
- `pc`: Usa `sounddevice` y `soundfile` (captura) junto con `System.Speech` de PowerShell (síntesis forzando una voz en español). Dependencias listadas en `client/requirements-pc.txt`.

### 3. Normalización y Calidad de Audio
La precisión de transcripción de OpenAI Whisper cae drásticamente con audios de bajo volumen (frecuente en micrófonos integrados). En el modo `pc`, la captura se realiza en `float32` y se aplica una **normalización matemática (95% de la amplitud máxima)** usando `numpy` antes de guardar el WAV a 16kHz en PCM_16.

### 4. Precisión de Idioma (LLM)
Las instrucciones del sistema de TONTO (`TONTO_INSTRUCTIONS`) fueron traducidas íntegramente al español para evitar desviaciones del LLM en casos donde Whisper entregue transcripciones dudosas (como toses o ruido ambiente mal interpretado como inglés).
