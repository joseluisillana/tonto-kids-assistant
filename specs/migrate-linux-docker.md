# Migración a scripts compatibles con Linux y Docker

## Objetivo

Sustituir los scripts de operación actuales basados en PowerShell (`*.ps1`) por una alternativa basada en Bash. Toda la ejecución de las operaciones de desarrollo deberá realizarse a través de contenedores Docker sin necesidad de instalar dependencias de desarrollo (Node, Python, etc.) en el host.

## Estado actual

- **Bloqueo (BLOCKER):** Confirmada la alternativa (Script Bash) y la disponibilidad de Docker en el host. Pendiente validar la Spec y el Plan antes de proceder a la implementación.
- **Fase de la Spec:** DRAFT / ANALYSIS.
- **Alternativa seleccionada:** Script Bash único o "Wrapper" (`tonto.sh`).

## Análisis y Contexto del Proyecto

### ¿Qué hace TONTO Kids Assistant?
TONTO es un asistente físico educativo diseñado para niños. El MVP valida un loop conversacional muy rápido y reproducible utilizando hardware accesible. Cuando un niño interactúa (habla), el asistente captura el audio, el backend lo transcribe a texto (STT), genera una respuesta educativa segura y comprensible usando un modelo de lenguaje, y finalmente la reproduce en voz alta usando TTS.

### Componentes del Sistema
- **Cliente Físico (Raspberry Pi 3):** Un cliente "fino" en Python. Se encarga únicamente del I/O: graba audio desde un micrófono USB, lo envía al backend, recibe la respuesta y la reproduce localmente mediante `espeak`. No hace IA local pesada.
- **Backend (Python / FastAPI):** Orquesta la lógica principal. Recibe texto o audio (WAV), consulta APIs de Inferencia (OpenAI o DevExpert) para el STT y el Chat, gestiona una memoria corta temporal, y devuelve la respuesta.
- **Cliente Web de Validación (React + TS + Vite):** Interfaz usada en desarrollo para validar el loop de voz de manera ágil usando el micrófono y altavoces del navegador, sin depender siempre de la Raspberry conectada físicamente.
- **Scripts de Operación (`scripts/*.ps1`):** Herramientas para arrancar el entorno, lanzar tests y preparar la aplicación, los cuales actualmente se ejecutan de manera nativa en el host Windows.

## Mapa de Scripts Actual y Transición a Docker

El siguiente diagrama ilustra cómo los scripts de PowerShell actuales, que instalan dependencias y corren procesos directamente en el PC, van a ser mapeados a un script de Bash (`tonto.sh`) que delegará la ejecución en contenedores Docker aislados.

```mermaid
flowchart TD
    subgraph Host Actual (Windows / PowerShell)
        A1[setup-dev.ps1] -->|Crea .venv & node_modules| A2(Host Filesystem)
        B1[dev.ps1 -Service all] -->|Lanza uvicorn & vite| B2(Host Processes)
        C1[test.ps1 / build.ps1] -->|Lanza pytest & npm| C2(Host Processes)
    end

    subgraph Host Futuro (Linux / Bash + Docker)
        D1[tonto.sh setup] -.->|docker compose build| D2(Docker Images)
        E1[tonto.sh dev all] -.->|docker compose up| E2(Docker Containers)
        F1[tonto.sh test / build] -.->|docker compose run| F2(Docker Ephemeral Containers)
    end

    A1 ====> D1
    B1 ====> E1
    C1 ====> F1
```

### Tabla de Equivalencias a Implementar

| Operación Actual (PowerShell) | Propuesta Bash + Docker (`tonto.sh`) | Dónde se ejecuta |
| --- | --- | --- |
| `.\scripts\setup-dev.ps1` | `./tonto.sh setup` | Docker (construye imágenes base con pip/npm) |
| `.\scripts\dev.ps1 -Service backend` | `./tonto.sh dev backend` | Contenedor Docker (Expone el puerto 8000) |
| `.\scripts\dev.ps1 -Service web` | `./tonto.sh dev web` | Contenedor Docker (Expone el puerto 5173) |
| `.\scripts\test.ps1 -Target all` | `./tonto.sh test all` | Contenedores efímeros Docker para pytest/npm test |
| `.\scripts\build.ps1 -Target web` | `./tonto.sh build web` | Contenedor efímero Docker para npm run build |

## Requisitos y Restricciones

- **NO** modificar el código fuente de los servicios (backend, web, clientes) ni sus assets.
- Todas las operaciones deben ejecutarse en contenedores mediante `docker` o `docker compose`. El host Linux solo requiere tener Bash y Docker.
- Los comandos y la forma de trabajar de los agentes deben documentarse en `AGENTS.md` cuando se implementen.
