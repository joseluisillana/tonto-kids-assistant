# #110 — reducción de exposiciones accidentales de secretos

Estado: PR 1/2/3 integradas; PR 4 validada localmente, 2026-10-06.
Baseline PR 4: main b254ded. Rama: fix/issue-110-safe-notebooklm-export.
Tracking: https://github.com/joseluisillana/tonto-kids-assistant/issues/110.
Plan: docs/plans/agent-secrets-protection-implementation-plan.md.

## Alcance elegido

Mantener workflow actual, almacenamiento en .env y operación automatizada de
backend/SSH. El operador descarta sustituir .env por variable host. Aislamiento,
mediador y otras formas de provisión quedan diferidos. El historial de opciones
vive en docs/agent-secrets-credential-options.md y el diseño de aislamiento
anterior queda como alternativa no aprobada.

No se garantiza impedir acceso deliberado del agente por archivos, shell,
Docker o código modificable. Esta reparación no completa el objetivo universal
original de #110 ni autoriza cerrar la issue.

## Entregas bajo esta spec

| Entrega | Alcance | Estado |
| --- | --- | --- |
| PR 1 | Spec/plan, limpieza y errores/logs chat/STT seguros | Integrada en #116, main 8ef12ed; CI aprobada |
| PR 2 | Setup/tests sin credenciales reales, mismos comandos | Integrada en #117, main 0222d39; CI aprobada |
| PR 3 | Exclusión de secretos en builds y montajes innecesarios | Integrada en #118, main b254ded; CI aprobada |
| PR 4 | Exportación NotebookLM con fuentes/destinos seguros | Implementada y validada localmente; pendiente revisión/integración |

Las PRs siguientes actualizan esta spec y su plan antes de implementar su fase.
Revisar diagnósticos restantes dentro de la entrega relacionada o una PR propia
si el hallazgo es independiente. Cada PR parcial usa Part of #110. Integrar una
entrega y actualizar desde main antes de empezar la siguiente. No implementar
las fases pendientes como parte de PR 1.

## Baseline y tracking

#108 integra migración Linux/Docker y #115; #107 cerrada. #88 y #114 separados.
DevExpert no se opera en real (D025); adaptadores conservados con tests mocks.
El incidente original está en docs/agent-secrets-protection-draft.md. No volver
a leer la clave ni declarar rotación no verificada.

## Requisitos de la primera reparación

- Limpieza down/stop consulta metadatos con --no-env-resolution y
  --no-interpolate antes de seleccionar el nombre. No captura configuración
  expandida ni carga valores de env_file en la salida. Conserva resolución de
  identidad de Compose, overrides, detección de residuales, alias y volúmenes.
- No devolver stdout/stderr arbitrarios de comandos Docker en limpieza.
  Errores reportan operación y exit code; residuales reportan estado sin volcado.
- Chat y STT no leen ni devuelven cuerpos HTTP fallidos ni razones de red.
  Mostrar proveedor y código HTTP upstream cuando exista; mantener 502/504.
  Suprimir cadenas de excepciones que podrían reintroducir detalles en trazas.
- Proveedor inválido no devuelve el valor recibido. Éxitos y contratos API,
  memoria de proceso, configuración y cliente permanecen iguales.
- Log WARNING por fallo con JSON de campos permitidos: evento, proveedor,
  operación chat/stt, categoría y código HTTP upstream opcional validado.
  Campos desconocidos se sustituyen por unknown. No recibir ni registrar body,
  excepción, claves, URLs, headers, modelos arbitrarios, conversación, audio o
  session_id. Sin exc_info/stack_info y sin archivos persistentes nuevos;
  usar logging estándar del proceso (stderr con configuración habitual).
  Es minimización previa, no redacción posterior de texto libre ni hash de claves.
- Añadir canarios ficticios en Docker simulado, errores HTTP/red/timeout/JSON,
  configuración inválida, trazas y respuestas de endpoints reales con HTTP mock.
  Al fallar el harness imprime solo caso/resultado, nunca el valor.

## Requisitos de PR 2 — tareas sin inyección de credenciales

- Setup/test/build usan `docker-compose.tasks.yml` explícito y `--env-file
  /dev/null`, sin heredar archivos/overrides de runtime ni COMPOSE_ENV_FILES.
  Servicios backend/UI/web sin env_file, credenciales, puertos ni depends_on.
- No crear, leer ni modificar .env en setup/test/build (incluido setup host).
  Retirar OPENAI_API_KEY y DEVEXPERT_API_KEY heredadas del proceso de tareas.
- Mismos comandos, cachés locales, imágenes y volumen backend-venv. Proyecto
  por directorio como Compose por defecto; COMPOSE_PROJECT_NAME exportado se
  respeta. Si antes se definía solo dentro de .env, exportarlo para compartir
  volumen con runtime. COMPOSE_FILE/overrides del runtime no se usan para tareas.
- Runtime dev/SSH y carga .env conservados. No iniciar ni parar backend real.
- Tests con Compose real sobre fixtures verifican ausencia de variables y
  dependencias; stubs cubren rutas CLI/fallos/no creación de .env. Tests/build
  oficiales funcionan sin overrides temporales ni claves.
- Los bind mounts y contexto build actuales pueden seguir dando acceso al
  archivo .env; esa exclusión pertenece a PR 3. Esta fase impide inyección
  accidental, no acredita aislamiento ni ausencia de secretos del filesystem.

## Requisitos de PR 3 — contextos y montajes mínimos

- UI build usa contexto client y allowlist en client/.dockerignore: solo
  Dockerfile.ui, sin .env, claves, código ni symlinks como contenido de imagen.
  El Dockerfile instala librerías; el código se suministra por mounts.
- Retirar mounts de raíz del repo en Python/UI. Runtime backend: backend y
  shared read-only más volumen venv; UI: client/shared read-only y venv/X11.
- Tareas Python/UI montan fuentes/scripts/tests y archivos públicos requeridos
  read-only; solo dependencias y caches/fixtures son escribibles. No montar .git,
  docs, exports, secretos raíz ni home/SSH. Tests conservan rutas /app originales.
- Web runtime/tareas montan archivos de configuración públicos, src/tests y
  salidas/dependencias específicas; no carpeta web completa ni web/.env reales.
  VITE_BACKEND_URL se suministra por environment runtime como antes.
- CLI prepara directorios escribibles antes de Docker, conserva comandos,
  instalación local/volumen, reload y overrides de audio. .env runtime se consume
  como env_file por Compose, nunca como archivo montado en /app.
- Canarios ficticios: comprobar contexto build efectivo y archivos ausentes
  en contenedor, sin leer secretos reales. Setup/tests/build oficiales pasan.
- Fuentes montadas se consideran públicas: no guardar secretos dentro de ellas.
  Esta fase no bloquea código malicioso, overrides manuales, symlinks hacia
  datos dentro de otro mount autorizado ni acceso al daemon/host.

## Requisitos de PR 4 — exportación segura

- Preservar fuentes Markdown actuales, archivos individuales, INDEX y combinado,
  orden y formato. Mantener comando Bash/hook, sin dependencias nuevas.
- Solo destinos bajo exports/<subdirectorio>, incluidos absolutos equivalentes.
  Rechazar raíz repo/exports, fuentes, rutas externas y prefijos similares.
  Validar normalización y componentes existentes antes de crear/borrar/escribir.
- Rechazar symlinks en fuentes y árboles docs/specs y en ruta destino, incluidos
  links rotos o que apunten dentro del repo; no seguirlos ni leer sus destinos.
- Validar todas las fuentes antes de reemplazar export anterior. Rechazar
  archivos con múltiples hardlinks para evitar alias a protegidos. Categorías
  protegidas (.env*, claves, secrets/credentials) no son fuentes autorizadas.
- No borrar recursivamente un destino arbitrario; generar en staging privado y
  reemplazar solo el directorio de export autorizado, sin seguir enlaces.
  Mensajes de error fijos, sin contenido, paths arbitrarios ni trazas shell.
- Tests con canarios ficticios: enlaces de archivos/directorios/destino, rutas
  fuera/raíz/fuentes, hardlinks, preservación ante fallo y formato válido.
- No se escanea contenido para detectar claves copiadas manualmente en docs.
  Árbol confiable sin modificaciones concurrentes durante export; no se promete
  aislamiento del host ni protección universal frente a carreras adversarias.

## Límites generales

Compose todavía genera un modelo estructural internamente, pero sin resolver
los env_file ni interpolar valores. No elimina el comando config ni garantiza
seguridad de literales secretos introducidos en YAML: las configs públicas no
deben contener credenciales. Otros comandos Docker, logs, acceso directo y
las fuentes/cachés públicas autorizadas requieren
disciplina operativa. Exclusiones de mounts y build acordadas están implementadas;
no se evalúan otros builds u overrides externos del operador.
Los logs de fallos chat/STT de esta entrega sí están acotados; logs de otros
componentes/herramientas no quedan cubiertos por esa garantía.
No presentar esta mejora como aislamiento ni sanitización universal del host.
No se cambia la fuente de credenciales ni se introducen dependencias.

## Aceptación

Tests de limpieza cubren errores, residuales, alias, proyecto personalizado y
canarios sin salidas crudas. Tests chat/STT cubren ambos adaptadores, trazas,
endpoints y códigos, sin credenciales ni llamadas reales. Suite Python completa,
sintaxis Bash y diff check pasan. Sin cambios web/UI no se exige demo física
para este parche; registrar cualquier verificación que no pudo ejecutarse.

## Operación segura y respuesta a incidentes

No ejecutar dumps de Compose/inspect/env, trazas shell ni lecturas de secretos
para investigar. .env.example sigue público; .env.* reales no. El humano rota
credenciales y gestiona copias/historiales; registrar solo superficie/fecha/tipo.
