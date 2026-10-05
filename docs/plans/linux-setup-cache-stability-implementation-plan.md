# Plan del punto 7: setup y cachés

Estado: aprobado por el operador; implementación en validación. Part of #107.
Fuente: specs/linux-setup-cache-stability.md.

## Pasos

1. Crear fix/linux-setup-cache-stability desde la rama integrada de #108
   (o main si ya está fusionada). Confirmar checkout limpio y leer contexto.
2. Separar setup Docker del setup host explícito; retirar borrado automático
   del entorno IDE. Hacer explícitos errores y requisitos de cada modalidad.
3. Preparar .cache/pip y .cache/npm con permisos de usuario; configurar Compose
   y montar la caché npm sin ampliar el montaje al resto del repositorio.
4. Revisar Dockerfile.ui para asegurar que las instalaciones de build no crean
   cachés globales persistentes; no confundir capas Docker con caché pip runtime.
5. Actualizar README/ayuda y sustituir el contexto operativo obsoleto de la spec
   y plan ci-local-cache-alignment, conservando evidencia histórica fechada.
6. Añadir pruebas enfocadas del CLI con Docker simulado: errores propagados,
   setup sin Python host, selección explícita host y preservación de su .venv.
7. Validar en proyecto Compose aislado y checkout temporal sin secretos reales:
   setup limpio/repetido, rutas/permisos y caché reutilizada. No borrar volúmenes
   ni entornos existentes del operador. Evitar leer/imprimir config expandida.
8. Ejecutar ./tonto.sh test all, ./tonto.sh build all y ./tonto.sh down.
   Registrar salidas sanitizadas y CI, hacer commits y PR pequeña vinculada #107.
9. Para P-107-07, obtener auditoría actual de desarrollo y producción, analizar
   advisories/versiones y presentar propuesta separada; no usar audit fix --force.

## Validación de aceptación

Seguir criterios de la spec. No cerrar punto 7 por pasar tests: también deben
cumplirse setup, cachés y resolución/aceptación del riesgo de dependencias.
No cerrar #107 ni reabrir #89 automáticamente.

## Prompt de implementación

Lee AGENTS.md, roadmap/specs/journal y workflow; verifica rama/estado Git.
Implementa specs/linux-setup-cache-stability.md en una rama fix propia, después
de aprobación del plan. Conserva .venv host durante setup Docker y ofrece setup
host explícito. Configura cachés locales con permisos UID/GID, sin dependencias
ni instalación global. Mantén el CI Docker actual. Usa fixtures/proyecto Compose
aislado para validar entorno limpio sin destruir datos ni leer secretos. Ejecuta
checks/build/limpieza oficiales, documenta evidencia P-107-05/06 y publica PR
vinculada #107. No cambies dependencias web hasta revisar propuesta P-107-07.
