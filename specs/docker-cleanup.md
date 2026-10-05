# Limpieza completa de Docker

Fecha: 2026-10-05. Plan aprobado. Part of #107; resuelve P-107-01.

`./tonto.sh down` y `stop` deben detener y retirar todos los contenedores del
proyecto Compose efectivo, incluidos one-off activos creados por `run`, y sus
redes administradas. Pueden interrumpir demos/tests activos de ese proyecto.
Usar `down --remove-orphans` y verificar después por etiquetas de proyecto:
si quedan contenedores o redes, exit no cero con IDs residuales.
Propagar errores de Docker o configuración.

Obtener nombre de configuración efectiva, respetando COMPOSE_PROJECT_NAME;
nunca imprimir configuración ni secretos. No usar prune, --volumes o borrado
global ni tocar contenedores ajenos. Conservar backend-venv, .venv host y
web/node_modules. Repetir sin servicios debe devolver exit 0.

Aceptación: servicios/one-off eliminados, red ausente, puertos libres;
contenedor ajeno intacto; dependencias conservadas; alias e idempotencia pasan;
residual simulado devuelve error; arranque y tests siguen funcionando.
Actualizar puntos 2/4/6 conservando histórico.

Fuera de alcance: TTS, URL UI, setup, caches, mDNS, UI física y dependencias nuevas.
Plan: docs/plans/docker-cleanup-implementation-plan.md.
