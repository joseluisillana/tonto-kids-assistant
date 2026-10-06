# Emulador Kivy en Docker — journal

| date | human/agent author | change summary | commit/PR reference |
| --- | --- | --- | --- |
| 2026-10-07 | jose / Codex | Operador solicita issue independiente e investigación desde main; Docker obligatorio para desarrollo. Registro creado como planned, con plan de estudio, criterios de arranque/voz y límites de evidencia. Sin implementación ni cambios de servicios. | pendiente |
| 2026-10-07 | jose / Codex | Investigación iniciada; estado in-progress. Operador exige Docker Desktop Linux y participa en pruebas. Separados sandbox, host y daemons; pruebas efímeras de solo diagnóstico, sin cambios de servicios existentes. | pendiente |
| 2026-10-07 | jose / Codex | Operador autoriza imagen temporal con libasound2-plugins y puente local socat existente, sin instalación en host ni configuración permanente. Desktop conecta al puente TCP ligado exclusivamente a loopback. Pendiente validar protocolo, dispositivos y captura. | pendiente |

## Evidencia inicial y trabajo pendiente

Baseline main a95164d. Reproducción manual confirmada por el operador. Captura
real: None en 0,191 s para seis segundos, PortAudio sin dispositivos y error al
consultar -1. Texto responde. Consulta de solo lectura identifica PipeWire con
protocolo PulseAudio e inputs disponibles en escritorio; contenedor ALSA/OSS
sin dispositivos, plugin ALSA-PulseAudio ni accesos de audio configurados.

Estos datos son observaciones propias de la sesión; no se adopta una solución
de otra rama. No se ha probado una vía completa de captura/reproducción exitosa.
Pendiente: ejecutar pasos 1–5 del plan y acordar línea de reparación.

## Frontera host/daemon verificada

Engine nativo informa Linux Mint y kernel del host. Montaje de /dev de ese
daemon en contenedor efímero muestra /dev/snd y dispositivos de grupo 29.
La ausencia de esa ruta en el sandbox indujo al launcher a omitirlos: la
reproducción desde el agente no equivale a un arranque desde terminal del host.

Docker Desktop informa kernel linuxkit y sistema Docker Desktop. Montaje de
/dev desde su daemon no ofrece /dev/snd. Los bind mounts estrictos del socket
PulseAudio y directorio X11 del host fallan porque las rutas no existen para
ese daemon. No se usó -v para evitar crear rutas inexistentes. Esto demuestra
que el launcher actual no completa pantalla/audio en este entorno requerido.
El alias host.docker.internal resuelve dentro de Desktop; no acredita aún
una conexión de audio ni autenticación. La UI existente sigue en Engine nativo.

## Ensayo Desktop: conexión y enumeración

Imagen efímera tonto-audio-probe:003 (fuera del código del producto): Python
3.12, PortAudio, bibliotecas PC del proyecto, espeak y libasound2-plugins.
Configuración ALSA predeterminada de tipo pulse dentro de la imagen.
Puente socat del usuario ligado exclusivamente a loopback, hacia el socket
del servicio de audio; no se modificó configuración permanente de PipeWire.
Docker Desktop accede al puente mediante su alias del host.

Resultado: PortAudio enumera pulse y default, con entrada/salida; default [1,1].
check_input_settings acepta mono float32 a 16 kHz. El aviso de cookie ausente
no impide la conexión de este ensayo con el puente Unix del mismo usuario;
no se copiaron ni leyeron cookies. La seguridad definitiva del puente requiere
revisión explícita: el ensayo confía en procesos locales y no publica en LAN.
Reproducción espeak lanzada; aceptación humana y captura real pendientes.
Estos resultados no acreditan todavía la UI completa, latencia o transcripción.

## Aceptación física del ensayo de audio

El operador confirmó oír la frase de espeak desde Docker Desktop y estar listo
para grabar. Tras aviso hablado, captura de seis segundos mediante sounddevice
con las opciones del cliente PC, sin guardar audio en disco ni enviarlo a STT.
WAV generado en memoria: un canal, 16 kHz, ancho de muestra 2 bytes, 96.000
frames. Tiempo real 6,104 s; pico 0,09825 y RMS 0,00896 sobre float32; 96.000
muestras no nulas. Señal presente, sin acreditar inteligibilidad/transcripción.

La prueba usa un harness mínimo, no la función capture_audio ni la UI del
producto. Valida transporte, formato y reproducción; queda pendiente integrar
y validar el código real, normalización, selección de entrada, recuperación y
turnos completos. Recomendación: estudiar integración de puente local gestionado
por launcher y configuración ALSA dentro de imagen. Resolver además transporte
gráfico para Desktop, autenticación/confianza local, lifecycle y limpieza.
No instalar paquetes en host; socat ya existía. Dependencias instaladas solo
en la imagen de ensayo. Retirar puente e imagen al terminar; conservar receta
de scratch fuera del repositorio como evidencia reproducible.

Limpieza confirmada: proceso del puente terminado mediante su sesión, puerto
de loopback sin listener e imagen temporal eliminada. No quedan contenedores
del ensayo. Configuración permanente y servicios existentes preservados.
Verificación documental: git diff --check pasa. Issue continúa in-progress.

## Segundo ensayo: UI real en Desktop

Operador autoriza continuar con el siguiente paso. Puente X11 temporal ligado
a loopback hacia el socket del escritorio. XOpenDisplay desde un contenedor
Desktop confirma conexión. Se conserva control de acceso X11 existente, que
permite al usuario local; no se ejecutó xhost + ni se copiaron cookies.
Imagen UI de ensayo basada en la imagen existente del proyecto, con dependencias
Kivy/PC actuales y el plugin autorizado. Copias del cliente real sin cambios de
fuentes. Pendiente ventana SDL2/OpenGL, captura real y turno completo.

SDL2 inicia la ventana real 800x480 en Desktop y entra en main loop; OpenGL
usa llvmpipe por software. Título distintivo del ensayo. Hashes de main.py,
touch_ui.py y tonto_face.py coinciden exactamente con el checkout del producto.
Health HTTP desde el contenedor hacia backend existente: 200. Backend permanece
en Engine nativo; no se declara validado el stack entero en Desktop.
Avisos de portapapeles por xclip/xsel ausentes, ya presentes en baseline,
no impiden iniciar UI; no se añadieron paquetes para silenciarlos.
Solicitada aceptación humana de tres turnos de voz en la ventana Desktop.

Operador confirma los tres turnos: «ahora funciona perfectamente», con escucha,
respuesta audible y retorno al botón inicial. Logs HTTP acotados confirman tres
POST /chat/audio con 200. WAV del cliente real: mono, 16 kHz, 16 bits, 96.000
frames. Texto con send_message real desde Desktop también devuelve respuesta.
No se guardan conversaciones ni audio en el registro; WAV temporal reside solo
en el contenedor de ensayo y desaparece al retirarlo.

La recreación del contenedor con la misma configuración vuelve a abrir ventana,
entrar en main loop y aceptar entrada mono a 16 kHz, sin ajustes nuevos del host.
No se repitieron turnos de voz tras recrearlo. Estudio de viabilidad de UI/audio
completado; issue no resuelta: faltan launcher oficial, backend en Desktop,
preflight, errores/recuperación, limpieza automática y validación de aceptación
del producto reparado. No se modificaron fuentes del cliente ni scripts.

Segundo ensayo retirado: contenedor e imágenes de ensayo/importación eliminados,
ambos puentes terminados y puertos sin listener. Backend/web y ventana antigua
en Engine nativo preservados. git diff --check pasa.

## Implementación oficial, 2026-10-07

Operador solicita continuar tras aceptación física del ensayo. Rama propia
fix/kivy-docker-desktop-audio. Launcher detecta daemon Desktop, valida DISPLAY,
sockets y puertos, crea bridges locales socat con grupos setsid y limpia
contenedor/procesos/override al salir o recibir señal. Sin audio inicia UI/texto.
La configuración ALSA-PulseAudio está en imagen y se activa solo en Desktop.
Engine nativo conserva la ruta previa. Error de captura UI ya no pasa por THINKING.

Checks: suite Python oficial en Desktop, 185 passed; casos adicionales de
configuración Desktop, audio ausente, error Compose, puente fallido, terminación,
puerto ocupado y parámetros inválidos. Sintaxis Bash y git diff --check pasan.
Build oficial UI y validación stack Desktop pendientes; no declarar resuelto.

Backend nativo y emulador anterior detenidos para liberar puerto y evitar
confusión. Helper oficial inicia backend en Desktop; health OK y turno real
de texto exitoso. Web nativa ajena a la validación permanece sin cambios.

Primer test ui falla durante colección: falta Kivy en backend-venv de Desktop,
aunque Python/backend/pytest están disponibles. Imagen gráfica construida sin
error. Backend Desktop detenido temporalmente y setup oficial ejecutado en ese
contexto para preparar dependencias completas. No es fallo de widgets ni se
instalan paquetes host. Añadida recuperación de ValueError por selección de
dispositivo PC inválida y límites de duración touch iguales al CLI (1–10 s).
Pendiente repetir checks y aceptación física sobre configuración definitiva.

Setup instaló dependencias completas, pero su primera ejecución terminó con
error 127 al editarse tonto.sh durante esa ejecución; incidencia del agente,
no del script estable. Repetición con archivo estable: exit 0. Suites finales
con dependencias declaradas: 188 passed Python y 29 passed Kivy. Avisos conocidos
de Starlette/httpx e imghdr no bloquean; sintaxis Bash y diff check correctos.

Arranque oficial `DOCKER_CONTEXT=desktop-linux ./tonto.sh dev ui`: ventana
TontoTouch y main loop; backend e interfaz activos en Desktop. Override reemplaza
bind X11 por volumen anónimo, usa bridges locales y ALSA_CONFIG_PATH del producto.
Función real de captura recupera un nombre de dispositivo inexistente devolviendo
None, sin iniciar grabación ni alterar la ventana. Pendiente aceptación humana
de tres turnos de voz, texto y cierre para comprobar limpieza automática.

En arranque oficial se observan cinco peticiones audio: 200, 502, 502, 200, 200;
dos textos 200. Diagnósticos seguros de los 502: provider_failure network en
operación stt de OpenAI, después de la captura/subida, sin HTTP upstream conocido.
No atribuir la causa exacta a DNS/TLS/proveedor sin evidencia. Tres comprobaciones
HTTPS sin credenciales responden 401 esperado: conectividad disponible durante
esa comprobación, sin acreditar ausencia de fallos transitorios en STT.

Cierre manual de ventana: launcher exit 0; contenedor UI retirado, puertos de
ambos bridges sin listeners, directorio temporal retirado y backend health OK.
Aceptación humana pendiente; falta un turno audio adicional exitoso tras los
dos últimos 200 y recreación del launcher para completar secuencia consecutiva.

## Resolución validada — pendiente revisión e integración

El operador confirma voz y texto correctos, con dos errores recuperables de red
en STT ajenos a la captura; cierra ventana con su botón. Launcher oficial se
recrea sin cambiar configuración. Operador confirma turno correcto tras reinicio;
HTTP audio 200 adicional completa tres envíos audio exitosos consecutivos tras
los fallos. WAV oficial: mono, 16 kHz, 16 bits, 96.000 frames. Backend y UI
permanecen activos en Desktop para uso local; los bridges pertenecen al launcher
y se retiran al cerrar, como se verificó en el primer arranque oficial.

Estado resolved: criterios técnicos y aceptación física cumplidos; revisión e
integración pendientes. No garantiza disponibilidad continua de la red/proveedor.
El diagnóstico solo establece categoría network para dos fallos STT, sin causa
exacta. No se altera backend para ocultarlos o introducir reintentos.
Validación: setup exit 0, 188 Python, 29 Kivy, sintaxis Bash y diff check pasan.
Sin paquetes instalados en host ni configuración permanente modificada.

Reparación guardada en commit 3bddad0 y publicada para revisión en
[PR #126](https://github.com/joseluisillana/tonto-kids-assistant/pull/126), borrador.
La issue local permanece resolved hasta revisión/integración; no existe una issue
GitHub duplicada. Backend y emulador oficiales siguen activos en Desktop.

## Aclaración de operación humana y de agentes — 2026-10-07

Operador exige registrar el comando explícito de próximos arranques y el cierre
previo en documentación humana e instrucciones de agentes. Plan ampliado antes
de editar. README actualizado en setup, comandos y ciclo Desktop; AGENTS raíz,
client/AGENTS y scripts/AGENTS incorporan el mismo comando desde raíz, contexto
explícito y espera de limpieza del launcher anterior. Backend permanece disponible.
Misma issue 003 y PR #126; cambio documental sin alterar código ni servicios.
Verificación de consistencia y git diff --check correctas; no requiere repetir
pruebas de runtime. Estado resolved, pendiente revisión/integración.

Intento de comparar dispositivos con compose run --device no ejecutó nada:
esa opción no está admitida por run. No se extrae evidencia de audio de ese error.
No hay dependencias nuevas ni reparación implementada. Pendiente concretar
prueba de transporte hacia el host y aprobar dependencias/arquitectura necesarias.

## Preparación v2.0.0 — 2026-10-07

Operador solicita incremento mayor en esta PR. Plan ampliado antes de cambios.
VERSION, manifest web y ambas versiones raíz del lock alineadas a 2.0.0.
Comparación JSON con HEAD confirma que solo cambian esas versiones, sin cambios
de paquetes/rangos/integridades. Tests web exit 0 y build web exit 0 (43 módulos).
README, notas versionadas, roadmap y resumen de specs distinguen código declarado
de publicación pendiente; no se modifican API ni dependencias.

Notas v2.0.0 recogen reparación Desktop e instrucciones/registros ai/ integrados
desde v1.0.0. No se encontró tag remoto v2.0.0 en la consulta acotada; etiquetar
sobre SHA integrado requiere comprobar de nuevo ausencia y CI main después del
merge. No se crea tag en esta rama ni se altera v1.0.0. Preparación incorporada
a PR #126; publicación posterior pendiente.

## Integración y publicación — 2026-10-07

Operador autoriza merge condicionado a CI y publicación de 2.0.0. CI del head
50dc1fc7b0ab3c95a1b6686789d06a7eb32de20c aprobada (runs 37547089425 y
37547085539). PR #126 integrada mediante squash como
acc9c38f19ec973c3843234cab74d8e875e78cc7. CI main de ese SHA aprobada:
https://github.com/joseluisillana/tonto-kids-assistant/actions/runs/37547339596.
Versiones raíz verificadas en 2.0.0 y etiqueta ausente antes de publicar.
Tag anotado v2.0.0 publicado y referencia remota resuelta al SHA integrado.
Release pública, sin draft/prerelease y marcada latest:
https://github.com/joseluisillana/tonto-kids-assistant/releases/tag/v2.0.0.
Publicado 2026-10-06T23:37:03Z, 2026-10-07 en Europe/Madrid.
Issue cerrada tras aceptación humana e integración; README y notas actualizados.
No se modifica el tag histórico v1.0.0 ni el contenido del commit etiquetado.
