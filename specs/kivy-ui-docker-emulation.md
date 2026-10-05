# Kivy UI Docker Emulation

**Status:** Draft
**Date:** 2026-10-05

## 1. Contexto

Durante el desarrollo de la interfaz táctil basada en Kivy (Spike Fase 2) para la Raspberry Pi, se habilitó la posibilidad de emular la UI en el entorno local (host del desarrollador) utilizando una ventana SDL2 (`KIVY_WINDOW=sdl2`). Sin embargo, esto requiere instalar las dependencias gráficas de Kivy y bibliotecas del sistema (como `libsdl2-dev`, `libgl1`, etc.) directamente en el host del desarrollador.

Para mantener el host limpio y garantizar que cualquier desarrollador pueda probar la UI de manera reproducible, se necesita un mecanismo de emulación basado en contenedores (Docker) que encapsule todas las dependencias necesarias.

## 2. Objetivos

* Proveer un entorno de emulación para la UI Kivy sin requerir instalaciones gráficas nativas en el host del desarrollador.
* Integrar este entorno con el flujo de trabajo existente (script `tonto.sh`).
* Mantener la compatibilidad para el desarrollo headless y con display (X11 forwarding o VNC) en los sistemas operativos soportados (Linux, y opcionalmente WSL2/Windows).

## 3. Solución Propuesta

Se propone crear un entorno Docker específico o extender el actual para ejecutar aplicaciones gráficas utilizando **X11 Forwarding** o un servidor VNC ligero. 

### 3.1. Enfoque: X11 Forwarding
Este enfoque permite que la aplicación Kivy corriendo dentro de un contenedor Docker proyecte su ventana directamente en el servidor gráfico del host.
1. Se añadirá un nuevo servicio en `docker-compose.yml` (ej. `ui-emulator` o similar) o se extenderá el entorno de tests.
2. Se configurarán las variables de entorno necesarias (`DISPLAY`, y los sockets de X11 en `/tmp/.X11-unix`).
3. El `tonto.sh` obtendrá un nuevo comando (ej. `./tonto.sh dev ui`) para levantar este servicio y permitir las validaciones de UI de forma aislada.

## 4. Criterios de Aceptación (DoD)

1. **Aislamiento:** La UI basada en Kivy puede ejecutarse sin instalar dependencias de Kivy en el entorno virtual local ni librerías SDL nativas en el host.
2. **Integración:** El script `tonto.sh` incluye una forma estandarizada de levantar el emulador (ej. `./tonto.sh dev ui`).
3. **Documentación:** Se actualiza la documentación de setup (`docs/raspberry-pi-setup.md` o análoga) con los pasos para habilitar permisos del servidor X si fuera necesario (`xhost +local:docker`).
4. **Validación:** El emulador levanta con éxito la ventana 800x480 de prueba (`spikes/ui_kivy/main.py`) desde un contenedor Docker en un host Linux de prueba.

## 5. Riesgos y Alternativas

* **WSL2 / macOS:** El reenvío de X11 puede ser complejo o requerir herramientas de terceros (como VcXsrv en Windows o XQuartz en macOS). Si esto se vuelve un bloqueante excesivo, se evaluará fallback a una imagen con un VNC/NoVNC web-based, permitiendo ver la UI desde un navegador web local (`http://localhost:6080`).
