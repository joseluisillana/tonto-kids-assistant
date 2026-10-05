# Migración a scripts compatibles con Linux y Docker

## Objetivo

Sustituir la totalidad de los scripts de operación y de asistentes de IA actuales basados en Bash (`*.ps1`) por alternativas basadas en Bash. Toda la ejecución de las operaciones de desarrollo se realizará a través de contenedores Docker, sin instalar dependencias locales (Node, Python) en el host, garantizando que el proyecto sea ejecutable desde cualquier OS que cuente con Docker y Bash.

## Estado actual

- **Fase de la Spec:** DRAFT / ANALYSIS. (Se mantiene en borrador por petición).
- **Alternativa seleccionada:** Script Bash único o "Wrapper" (`tonto.sh`) y scripts Bash de apoyo.

## Decisiones Técnicas Confirmadas

1. **Acceso LAN para la Raspberry Pi:** 
   Se usará el mapeo de puertos estándar de Docker (`8000:8000`), el cual expone el servicio en `0.0.0.0` en la máquina host. Esto permite nativamente que la Raspberry Pi alcance el backend a través de la IP del host.
2. **Volúmenes (Hot Reloading):** 
   El `docker-compose.yml` mapeará el código fuente del host (`./backend` y `./web`) dentro de los contenedores para aplicar cambios de código al instante.
3. **Manejo de Secretos y Configuración:** 
   Se empleará un fichero `.env` en la raíz cargado por `docker-compose`.
4. **Erradicación de Bash (Estrategia Paralela):** 
   Ningún script de Bash (`*.ps1`) permanecerá en la versión final del proyecto, **PERO** durante la implementación se construirán las alternativas de Bash en paralelo. Solo cuando se haya validado su funcionamiento al 100%, se procederá con la limpieza final de los artefactos legacy de Windows 11 / Bash.
5. **Integración Continua (GitHub Actions) y Hooks:** 
   El workflow de CI actual (`ci.yml`), que está acoplado a Bash, será migrado para usar la nueva infraestructura basada en Bash y Docker. Los hooks de git (`pre-commit`) se reescribirán para invocar los nuevos scripts `.sh` sin depender de `pwsh`.
6. **Actualización de Documentación Agéntica y General:** 
   Todas las referencias en `AGENTS.md`, `README.md`, planes y cualquier otra documentación deben ser actualizadas para que los agentes y humanos sepan usar los nuevos scripts (`tonto.sh`, etc.) y descarten por completo la antigua vía Bash.

## Análisis y Contexto del Proyecto

### ¿Qué hace TONTO Kids Assistant?
TONTO es un asistente físico educativo diseñado para niños. Captura voz, la transcribe, genera respuesta y la reproduce localmente.

### Componentes del Sistema
- **Cliente Físico (Raspberry Pi 3)**
- **Backend (Python / FastAPI)**
- **Cliente Web de Validación (React + TS + Vite)**

## Mapa de Scripts Actual y Transición a Docker

```mermaid
flowchart TD
    subgraph Host Actual (Dependiente de Bash)
        A1[setup-dev.ps1 / dev.ps1] -->|Nativo| A2(Host Processes)
        B1[ci.yml / pre-commit] -->|Llama pwsh| B2(Host Processes)
        C1[agent-*.ps1 / export-*.ps1] -->|Herramientas| C2(Host Processes)
    end

    subgraph Host Futuro (Independiente del OS - Bash + Docker)
        D1[tonto.sh setup / dev] -.->|docker compose| D2(Docker)
        E1[ci.yml / pre-commit] -.->|Llama Bash| E2(Docker / Bash)
        F1[agent-*.sh / export-*.sh] -.->|Contenedor o Bash| F2(Docker / Bash)
    end

    A1 ====> D1
    B1 ====> E1
    C1 ====> F1
```

## Requisitos y Restricciones (ESTRICTOS)

- **NO** eliminar todavía ningún `.ps1` ni recursos actuales de Git/GitHub. Se construirán artefactos en paralelo (`tonto.sh`, `ci.yml` modificado u otro archivo, etc.). La fase de limpieza de `.ps1` será estrictamente **la última fase**.
- **NO** modificar el código fuente de los servicios (backend, web, clientes) ni sus assets.
- La documentación (especialmente `AGENTS.md`) es crítica y debe reflejar fielmente la nueva arquitectura para que los LLMs futuros no intenten invocar `.ps1`.

## Validaciones

Las validaciones pormenorizadas, pasos a seguir y sus evidencias para este plan se recogerán en un documento auxiliar enlazado: 
- [Ver Validaciones y Evidencias](migrate-linux-docker-validation.md)
