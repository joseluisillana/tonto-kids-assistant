# Migración a scripts compatibles con Linux y Docker

## Objetivo

Sustituir la totalidad de los scripts de operación y de asistentes de IA actuales basados en PowerShell (`*.ps1`) por alternativas basadas en Bash. Toda la ejecución de las operaciones de desarrollo se realizará a través de contenedores Docker, sin instalar dependencias locales (Node, Python) en el host, garantizando que el proyecto sea ejecutable desde cualquier OS que cuente con Docker y Bash.

## Estado actual

- **Fase de la Spec:** DRAFT / ANALYSIS. (Se mantiene en borrador por petición).
- **Alternativa seleccionada:** Script Bash único o "Wrapper" (`tonto.sh`) y scripts Bash de apoyo.

## Decisiones Técnicas Confirmadas

1. **Acceso LAN para la Raspberry Pi:** 
   Se usará el mapeo de puertos estándar de Docker (`8000:8000`), el cual expone el servicio en `0.0.0.0` en la máquina host. Esto permite nativamente que la Raspberry Pi (un dispositivo físico independiente en la misma red) alcance el backend a través de la IP del host de desarrollo, sin necesidad de flags adicionales como `-AllowLan`.
2. **Volúmenes (Hot Reloading):** 
   El `docker-compose.yml` mapeará el código fuente del host (`./backend` y `./web`) dentro de los contenedores. Esto permite que los cambios de código se apliquen al instante durante el desarrollo sin necesidad de reconstruir las imágenes Docker.
3. **Manejo de Secretos y Configuración:** 
   Se empleará un fichero `.env` en la raíz del repositorio, que será cargado por `docker-compose` para inyectar variables como `OPENAI_API_KEY` o configuraciones específicas al contenedor de manera segura.
4. **Erradicación absoluta de PowerShell:** 
   Ningún script de PowerShell (`*.ps1`) debe permanecer en el repositorio. Todos los procesos (incluyendo la generación de la documentación para NotebookLM, hooks de Git, y las utilidades para los agentes IA como `agent-backend` y `agent-raspberry`) serán convertidos a Bash y adaptados para funcionar preferiblemente a través del motor Docker (a excepción de los que estrictamente necesiten ejecutarse en la Raspberry Pi de forma nativa).

## Análisis y Contexto del Proyecto

### ¿Qué hace TONTO Kids Assistant?
TONTO es un asistente físico educativo diseñado para niños. El MVP valida un loop conversacional muy rápido y reproducible utilizando hardware accesible. Cuando un niño interactúa (habla), el asistente captura el audio, el backend lo transcribe a texto (STT), genera una respuesta educativa segura y comprensible usando un modelo de lenguaje, y finalmente la reproduce en voz alta usando TTS.

### Componentes del Sistema
- **Cliente Físico (Raspberry Pi 3):** Un cliente "fino" en Python. Se encarga únicamente del I/O: graba audio desde un micrófono USB, lo envía al backend, recibe la respuesta y la reproduce localmente mediante `espeak`. No hace IA local pesada.
- **Backend (Python / FastAPI):** Orquesta la lógica principal. Recibe texto o audio (WAV), consulta APIs de Inferencia (OpenAI o DevExpert) para el STT y el Chat, gestiona una memoria corta temporal, y devuelve la respuesta.
- **Cliente Web de Validación (React + TS + Vite):** Interfaz usada en desarrollo para validar el loop de voz de manera ágil usando el micrófono y altavoces del navegador, sin depender siempre de la Raspberry conectada físicamente.

## Mapa de Scripts Actual y Transición a Docker

El siguiente diagrama ilustra cómo todos los flujos que dependían de PowerShell pasarán a Bash + Docker.

```mermaid
flowchart TD
    subgraph Host Actual (Dependiente de PowerShell)
        A1[setup-dev.ps1] -->|Crea .venv & node_modules| A2(Host Filesystem)
        B1[dev.ps1 -Service all] -->|Lanza uvicorn & vite| B2(Host Processes)
        C1[test.ps1 / build.ps1] -->|Lanza pytest & npm| C2(Host Processes)
        G1[agent-*.ps1 / export-*.ps1] -->|Herramientas de IA y Docs| G2(Host Processes)
    end

    subgraph Host Futuro (Independiente del OS - Bash + Docker)
        D1[tonto.sh setup] -.->|docker compose build| D2(Docker Images)
        E1[tonto.sh dev all] -.->|docker compose up| E2(Docker Containers)
        F1[tonto.sh test / build] -.->|docker compose run| F2(Docker Ephemeral Containers)
        H1[tonto.sh / agent-*.sh / export-*.sh] -.->|Contenedor o Bash| H2(Docker/Bash)
    end

    A1 ====> D1
    B1 ====> E1
    C1 ====> F1
    G1 ====> H1
```

### Tabla de Equivalencias a Implementar

| Operación Actual (PowerShell) | Propuesta Bash + Docker | Dónde se ejecuta |
| --- | --- | --- |
| `setup-dev.ps1` | `./tonto.sh setup` | Docker (construye imágenes) |
| `dev.ps1` | `./tonto.sh dev [backend/web]` | Contenedor Docker |
| `test.ps1` | `./tonto.sh test all` | Docker efímero |
| `build.ps1` | `./tonto.sh build web` | Docker efímero |
| `export-docs-for-notebooklm.ps1` | `scripts/export-docs.sh` (o en `tonto.sh`) | Bash (y contenedores si es necesario) |
| `agent-backend.ps1` | `scripts/agent-backend.sh` | Bash (llamando a docker) |
| `agent-raspberry.ps1` | `scripts/agent-raspberry.sh` | Bash |

## Requisitos y Restricciones

- **NO** modificar el código fuente de los servicios (backend, web, clientes) ni sus assets.
- Todas las herramientas del repositorio (sin excepción) deben migrarse a Bash.
- Los comandos y la forma de trabajar de los agentes deben documentarse en `AGENTS.md` tras finalizar la implementación.
