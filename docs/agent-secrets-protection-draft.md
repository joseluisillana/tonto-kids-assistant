# Borrador: protección de secretos frente a operaciones de agentes

Estado: DRAFT / pendiente de revisión. No autoriza implementación.
Tracking: https://github.com/joseluisillana/tonto-kids-assistant/issues/110.
Fecha: 2026-10-05. Rama solicitada: fix/docker-cleanup. Contexto: #107 y PR #109.
Este documento es contexto de backlog para una issue, no una spec aprobada.

Actualización 2026-10-06: se conserva este contexto original como historial.
Spec vigente en borrador: `specs/agent-secrets-protection.md`; plan:
`docs/plans/agent-secrets-protection-implementation-plan.md`. Reconciliados con
main `a985dac` tras integrar #108 y cerrar #107. No autorizan implementación.

## Incidente comprobado

Durante el análisis de limpieza Docker se ejecutó
`docker compose config --format json` con salida capturada por exec_command.
Compose resolvió env_file .env y devolvió la configuración completa, incluyendo
services.backend.environment.OPENAI_API_KEY con su valor real. La clave quedó
en el historial de herramientas del chat. No reproducirla en esta issue, logs,
docs ni ejemplos. No se ha constatado publicación en GitHub o uso por terceros.
El commit de reparación 03b7ce8 no contiene esa salida ni el valor de la clave.
Se recomendó rotación al operador; no se ha verificado que se haya realizado.

Las skills ya indican no imprimir claves, pero esa instrucción no impidió el
incidente. .gitignore protege de commits accidentales, no de lecturas ni logs.
La versión reparada de tonto.sh captura internamente la configuración para
extraer el nombre del proyecto: revisar cómo evitar también esa materialización
completa, aunque no se imprima. No modificarla en este trabajo de borrador.

## Objetivo propuesto por el operador

Impedir que cualquier agente lea, edite, copie, exporte o revele ficheros con
secretos o valores derivados. Incluir vías indirectas: Compose, Docker inspect,
variables de entorno, trazas shell, logs, exports y herramientas conectadas.
La aplicación debe poder consumir credenciales mediante mecanismos controlados
sin que el agente reciba sus valores. Las operaciones administrativas sobre
secretos deben reservarse al operador humano.

## Superficies a inventariar sin leer su contenido

- .env, .env.* con valores reales y archivos locales de proveedores.
- Claves privadas SSH, tokens, credenciales cloud y configuración de herramientas.
- Configuración Compose expandida; Docker inspect de entornos; env/printenv;
  shell set -x; comandos cat/rg/sed sobre archivos protegidos, incluidos globos,
  recursión, enlaces simbólicos y rutas alternativas.
- Logs, informes, screenshots, exports NotebookLM, commits y mensajes de issues.
- Mantener .env.example como plantilla pública con placeholders; verificar su
  clasificación mediante reglas, sin dar permiso genérico a todos los .env.*.

## Trabajo futuro propuesto

1. Definir matriz de operaciones prohibidas/permitidas y política en AGENTS.md,
   docs/ai-assisted-workflow.md y skills pertinentes, portable a Codex/OpenCode.
2. Analizar controles técnicos efectivos de cada entorno (sandbox/permisos/tool
   guards); una instrucción Markdown por sí sola no garantiza impedir accesos.
   No prometer una prohibición universal sin validarla para cada ruta de acceso.
3. Diseñar wrappers oficiales con salida mínima para diagnóstico: nombre de
   proyecto, estado, modelo y presencia booleana de credencial; nunca valor.
   Filtrar antes de devolver datos a herramientas/modelos, no después.
4. Preservar consumo de .env por Docker/aplicación sin lectura de secretos por
   agentes; evitar configuración expandida y no depender de redacción tardía.
5. Crear spec y plan emparejado antes de implementar; evaluar dependencias o
   cambios de arquitectura y pedir decisión si fueran necesarios.
6. Añadir pruebas con secretos CANARIO ficticios: lectura directa, comandos
   indirectos, errores, trazas, exports, symlinks y logs. Ningún canario aparece
   en salidas de herramientas, archivos de evidencia ni commits.
7. Revalidar setup/dev/test/build, preflight SSH y diagnóstico de errores, con
   helpers aprobados. No bloquear el funcionamiento habitual de la demo.
8. Documentar respuesta a incidentes y rotación humana; no incluir secretos.

## Criterios de aceptación para concretar en la futura spec

- Acceso directo a archivos protegidos denegado por controles verificables.
- Diagnóstico permitido devuelve solo datos explícitamente autorizados.
- No hay fuga de canarios, incluyendo rutas indirectas y casos de error.
- .env.example utilizable; setup/dev/test/build y demo conservan funcionamiento.
- Alcance y limitaciones explícitos por tipo de agente y mecanismo de acceso.
- Evidencias sanitizadas y revisión humana antes de aceptar la protección.

## Handoff

Revisar este borrador y la issue antes de implementar. Leer instrucciones del
proyecto y aplicar gate Git. No abrir .env ni otros secretos para investigar.
Partir de archivos de ejemplo y fixtures con canarios inventados. Proponer spec
y plan con controles efectivos y límites conocidos; no instalar dependencias ni
cambiar seguridad/producto sin el alcance aprobado. No cerrar #107 ni PR #109
por completar solo este seguimiento.
