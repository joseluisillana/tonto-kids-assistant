# Preparacion del Cliente Raspberry Pi

## Objetivo

Esta guia permite reinstalar y recuperar desde cero la Raspberry Pi 3 usada como cliente fisico de TONTO hasta el estado validado en Semana 1.

La Raspberry Pi debe quedar preparada como cliente ligero:

- conectada a la red local por Wi-Fi,
- accesible por SSH,
- operable desde VSCode Remote SSH,
- con audio local validado,
- con `espeak` disponible para TTS,
- con el repositorio del proyecto clonado,
- lista para ejecutar el cliente Python cuando el backend este disponible.

No cubre speech-to-text, wake word, Arduino, persistencia, autenticacion, despliegue automatico ni modelos locales.

## Referencias

- Raspberry Pi Imager y customisation: https://www.raspberrypi.com/documentation/installation/
- VSCode Remote SSH: https://code.visualstudio.com/docs/remote/ssh

## Hardware Base

- Raspberry Pi 3.
- Tarjeta SDHC.
- Fuente de alimentacion estable para Raspberry Pi.
- Altavoz o salida de audio conectada a la Raspberry Pi.
- Red Wi-Fi local.
- Ordenador de desarrollo con VSCode y cliente SSH.

## Convenciones del Proyecto

Usar estos valores para que la preparacion sea reproducible:

| Campo | Valor |
| --- | --- |
| Hostname | `tonto-pi` |
| Usuario | `tonto-pi-user` |
| Zona horaria | `Europe/Madrid` |
| Pais Wi-Fi | `ES` |
| Teclado | Espanol |
| Repo | `https://github.com/joseluisillana/tonto-kids-assistant.git` |

No documentar contrasenas reales, claves privadas SSH ni credenciales Wi-Fi. En esta guia aparecen siempre como placeholders.

## 1. Grabar Raspberry Pi OS

1. Descargar Raspberry Pi Imager desde la pagina oficial de Raspberry Pi.
2. Abrir Raspberry Pi Imager.
3. Confirmar version usada como referencia del proyecto:

```text
Raspberry Pi Imager v2.0.7
Fecha de referencia: 2026-05-15
```

4. Seleccionar el dispositivo:

```text
Device: Raspberry Pi 3
```

5. Seleccionar el sistema operativo:

```text
Operating system: Raspberry Pi OS Lite (64-bit)
```

6. Seleccionar la tarjeta:

```text
Storage: SDHC Card
```

7. Abrir la configuracion de customisation antes de escribir la imagen.

## 2. Configurar Customisation en Imager

### Hostname

Configurar:

```text
Hostname: tonto-pi
```

Esto permite intentar conectar despues con:

```bash
ssh tonto-pi-user@tonto-pi.local
```

### Localisation

Configurar:

```text
Time zone: Europe/Madrid
Keyboard layout: Spanish
Wi-Fi country: ES
```

### User

Configurar:

```text
Username: tonto-pi-user
Password: <CONTRASENA_LOCAL_DE_LA_RASPBERRY>
```

La contrasena debe guardarse fuera del repositorio.

### Wi-Fi

Configurar la red local:

```text
SSID: <NOMBRE_DE_LA_WIFI>
Password: <CONTRASENA_DE_LA_WIFI>
Hidden SSID: solo si la red no publica el SSID
```

Usar una red Wi-Fi de 2.4 GHz para Raspberry Pi 3. La Wi-Fi integrada de Raspberry Pi 3 no se conecta a redes que solo emiten en 5 GHz. Si el router usa el mismo nombre para 2.4 GHz y 5 GHz, confirmar que el SSID esta disponible tambien en 2.4 GHz o crear un SSID separado para 2.4 GHz antes de grabar la imagen.

Este paso es obligatorio para una instalacion headless. La Raspberry necesita conectividad en el primer arranque para poder entrar por SSH.

### Remote Access

Habilitar SSH:

```text
Enable SSH: yes
Authentication: usuario configurado en Imager
```

Para Semana 1 basta con SSH habilitado para el usuario `tonto-pi-user`. Si mas adelante se decide exigir autenticacion solo por clave publica, actualizar esta guia y registrar la decision.

### Raspberry Pi Connect

No configurar Raspberry Pi Connect para Semana 1.

El flujo oficial del proyecto es SSH y VSCode Remote SSH.

## 3. Escribir la Tarjeta SD

1. Revisar que Imager muestra:

```text
Device: Raspberry Pi 3
Operating system: Raspberry Pi OS Lite (64-bit)
Storage: SDHC Card
Customisations applied:
- Hostname configured
- Localisation configured
- User account configured
- Wi-Fi configured
- SSH enabled
```

2. Escribir la imagen en la SDHC Card.
3. Esperar a que Imager termine y expulse la tarjeta.
4. Retirar la tarjeta de forma segura.

## 4. Primer Arranque

1. Insertar la tarjeta SD en la Raspberry Pi.
2. Conectar altavoz o salida de audio.
3. Conectar alimentacion.
4. Esperar al menos 2-3 minutos en el primer arranque.
5. Desde el ordenador de desarrollo, probar resolucion por hostname:

```powershell
ping tonto-pi.local
```

Si `tonto-pi.local` no resuelve, buscar la IP de la Raspberry en el router y usar esa IP para SSH:

```powershell
ssh tonto-pi-user@<IP_DE_LA_RASPBERRY>
```

## 5. Conectar por SSH

Desde el ordenador de desarrollo:

```powershell
ssh tonto-pi-user@tonto-pi.local
```

Si aparece una pregunta de confianza del host, aceptar solo si el hostname o la IP son los esperados.

Una vez dentro, validar identidad basica:

```bash
hostname
whoami
pwd
```

Resultado esperado:

```text
tonto-pi
tonto-pi-user
/home/tonto-pi-user
```

## 6. Preparacion Minima del Sistema

Actualizar paquetes:

```bash
sudo apt update
sudo apt upgrade
```

Instalar herramientas necesarias para Semana 1:

```bash
sudo apt install -y git python3 python3-venv python3-pip espeak
```

Validar versiones y rutas:

```bash
git --version
python3 --version
python3 -m pip --version
which espeak
```

Validar audio y TTS local:

```bash
espeak "TONTO week one audio check"
```

Debe escucharse la frase por el altavoz o salida configurada.

Si no hay audio, revisar primero:

- volumen del altavoz,
- salida fisica usada,
- alimentacion de la Raspberry,
- que `espeak` existe con `which espeak`,
- que el audio del sistema funciona fuera del cliente TONTO.

## 7. Clonar el Repositorio

Desde la Raspberry Pi:

```bash
cd ~
git clone https://github.com/joseluisillana/tonto-kids-assistant.git
cd tonto-kids-assistant
```

Confirmar que el repositorio tiene la estructura esperada:

```bash
ls
```

Debe verse, entre otros:

```text
backend
client
docs
scripts
shared
specs
tests
web
```

## 8. Preparar Entorno Python del Cliente

En Semana 1 el cliente Raspberry no requiere dependencias Python externas, pero el proyecto debe usar un entorno local para mantener la instalacion limpia y preparada para cambios futuros.

Desde la raiz del repo en la Raspberry:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r client/requirements.txt
```

Si `client/requirements.txt` no instala paquetes, es correcto para Semana 1.

No instalar paquetes Python globalmente salvo herramientas del sistema mediante `apt`.

## 9. Configurar Conexion con el Backend

El backend se ejecuta en el ordenador de desarrollo o en otro host de la red. La Raspberry debe apuntar a ese host mediante `TONTO_BACKEND_URL`.

No usar `localhost` ni `127.0.0.1` en la Raspberry salvo que el backend este corriendo en la propia Raspberry.

Ejemplo:

```bash
export TONTO_BACKEND_URL=http://<BACKEND_HOST>:8000
.venv/bin/python client/main.py
```

Tambien puede ejecutarse en una sola linea:

```bash
TONTO_BACKEND_URL=http://<BACKEND_HOST>:8000 .venv/bin/python client/main.py
```

Donde `<BACKEND_HOST>` puede ser:

- la IP local del ordenador que ejecuta el backend,
- un hostname resoluble en la red local.

Para Semana 1, esta prueba completa es opcional si el backend todavia no esta levantado. La validacion obligatoria de hardware es SSH, VSCode Remote SSH, audio y `espeak`.

## 10. Configurar VSCode Remote SSH

VSCode Remote SSH es el flujo recomendado para operar y desarrollar manualmente sobre la Raspberry durante el MVP.

En el ordenador de desarrollo:

1. Instalar VSCode.
2. Instalar la extension oficial `Remote - SSH`.
3. Confirmar que el comando SSH funciona desde una terminal local:

```powershell
ssh tonto-pi-user@tonto-pi.local
```

4. Crear o actualizar la configuracion SSH local.

En Windows suele estar en:

```text
C:\Users\<USUARIO>\.ssh\config
```

Entrada recomendada:

```sshconfig
Host tonto-pi
    HostName tonto-pi.local
    User tonto-pi-user
```

Si `.local` no funciona de forma estable, usar IP fija o reserva DHCP:

```sshconfig
Host tonto-pi
    HostName <IP_DE_LA_RASPBERRY>
    User tonto-pi-user
```

5. En VSCode, ejecutar `Remote-SSH: Connect to Host...`.
6. Elegir `tonto-pi`.
7. Abrir la carpeta remota:

```text
/home/tonto-pi-user/tonto-kids-assistant
```

8. Abrir una terminal integrada de VSCode. Esa terminal debe ejecutarse en la Raspberry.

Validar desde la terminal remota:

```bash
hostname
pwd
which espeak
```

## 11. Checklist de Recuperacion

Usar esta lista despues de reinstalar o recuperar la Raspberry:

- [ ] Raspberry Pi Imager instalado en el ordenador de desarrollo.
- [ ] Raspberry Pi Imager `v2.0.7` usado como referencia o version actual anotada.
- [ ] Dispositivo seleccionado: `Raspberry Pi 3`.
- [ ] Sistema seleccionado: `Raspberry Pi OS Lite (64-bit)`.
- [ ] Tarjeta seleccionada: `SDHC Card`.
- [ ] Hostname configurado: `tonto-pi`.
- [ ] Usuario configurado: `tonto-pi-user`.
- [ ] Localizacion configurada: `Europe/Madrid`, teclado espanol, pais Wi-Fi `ES`.
- [ ] Wi-Fi configurada desde Imager con un SSID disponible en 2.4 GHz.
- [ ] SSH habilitado desde Imager.
- [ ] Raspberry arranca y aparece en la red.
- [ ] `ssh tonto-pi-user@tonto-pi.local` funciona, o funciona SSH por IP.
- [ ] VSCode Remote SSH conecta con `tonto-pi`.
- [ ] `sudo apt update` y `sudo apt upgrade` ejecutados.
- [ ] `git`, `python3`, `python3-venv`, `python3-pip` y `espeak` instalados.
- [ ] `espeak "TONTO week one audio check"` se escucha.
- [ ] Repositorio clonado en `/home/tonto-pi-user/tonto-kids-assistant`.
- [ ] `.venv` creado en el repo.
- [ ] `client/requirements.txt` instalado dentro de `.venv`.
- [ ] `TONTO_BACKEND_URL` apunta al backend real cuando se prueba el cliente.
- [ ] El cliente puede arrancar con `.venv/bin/python client/main.py` cuando hay backend disponible.

## 12. Exportar a NotebookLM

Esta guia vive en `docs/`, por lo que entra automaticamente en el flujo de exportacion a NotebookLM.

Desde el ordenador de desarrollo, refrescar fuentes:

```powershell
.\scripts\export-docs-for-notebooklm.ps1
```

Comprobar que existe:

```text
exports/notebooklm/docs__raspberry-pi-setup.md
```

NotebookLM debe leer la copia exportada, pero la fuente oficial sigue siendo este archivo en `docs/`.

## Historial de Preparacion Raspberry

| Fecha | Semana | Cambio |
| --- | --- | --- |
| 2026-05-15 | Semana 1 | Se documenta preparacion reproducible con Raspberry Pi Imager v2.0.7, Raspberry Pi OS Lite 64-bit, Wi-Fi, SSH, VSCode Remote SSH, `espeak` y cliente Python minimo. |
| 2026-05-15 | Semana 1 | Se aclara que Raspberry Pi 3 debe configurarse con una red Wi-Fi disponible en 2.4 GHz; redes solo 5 GHz no sirven para el arranque headless. |
| 2026-05-15 | Semana 1 | Se corrige el usuario validado de SSH a `tonto-pi-user`. |
