# Estabilidad de setup y cachés tras migración

Estado: propuesta para revisión, 2026-10-05. Part of #107.
Problemas: P-107-05 y P-107-06. Sin implementación ni dependencias nuevas.

## Diagnóstico

`tonto.sh setup` instala Python en el volumen backend-venv y luego borra
el .venv del host para crear otro para el IDE. Si falta ensurepip o falla pip,
el script solo advierte y puede terminar con éxito. Según README el entorno
host es auxiliar del IDE; no es requisito del flujo Docker.
Pip del contenedor intenta usar /.cache/pip sin permisos. Npm usa /tmp/.npm,
que se pierde al retirar el contenedor. Ninguna ruta cumple la política local.
CI ya llama setup/test/build de tonto.sh y no usa setup-python/setup-node.
La spec ci-local-cache-alignment describe el workflow anterior; su issue #89
está cerrada y no autoriza restaurar ese workflow.

## Comportamiento propuesto

- `./tonto.sh setup` prepara Python Docker y web sin borrar ni modificar .venv
  del host. Exit 0 significa que todos los pasos obligatorios terminaron bien.
- `./tonto.sh setup host` prepara explícitamente el entorno opcional del IDE.
  Comprueba python3/venv, conserva un entorno existente y devuelve exit no cero
  si falla. Informa de la precondición sin instalar paquetes de sistema.
- Backend configura PIP_CACHE_DIR=/app/.cache/pip. Web monta únicamente
  .cache/npm del repo en /app/.cache/npm y configura npm_config_cache allí.
  Preparar directorios como usuario del host; no ampliar permisos de todo el repo.
- Mantener backend-venv y comandos oficiales. Fallos Docker/pip/npm obligatorios
  se propagan; ningún mensaje final de éxito oculta un fallo.
- Alinear cache de construcción del emulador y distinguirla de la caché runtime;
  no introducir caché global nueva ni cambiar arquitectura.
- CI conserva setup/test/build actuales. Primero verificar rutas y permisos;
  persistencia entre runners mediante una Action de caché sería otra decisión.

## Aceptación

1. Setup Docker funciona en entorno limpio y no requiere Python host.
2. .venv host existente no se borra ni se modifica por setup Docker.
3. Fallos obligatorios producen exit no cero; setup host fallido también.
4. Pip y npm reportan las rutas locales configuradas y escriben como UID/GID host.
5. Segunda ejecución reutiliza las cachés; no hay advertencia de caché deshabilitada.
6. test all, build all y CI pasan; down conserva dependencias y cachés.
7. Registro P-107-05/06 actualizado con evidencia; punto 7 sigue abierto si
   P-107-07 aún no se resuelve o acepta explícitamente.

## Fuera de alcance

Cambios de producto, secretos, instalación global, dependencias nuevas, audio
físico, restauración de Actions antiguas y reparación automática de npm audit.
Las vulnerabilidades P-107-07 requieren auditoría actual, evaluación por advisory
con fuentes oficiales y propuesta de versiones antes de tocar manifest/lockfile.

Plan: docs/plans/linux-setup-cache-stability-implementation-plan.md.
