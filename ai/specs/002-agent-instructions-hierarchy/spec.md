---
id: "002-agent-instructions-hierarchy"
title: "Jerarquía portable de instrucciones para agentes"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-10-06"
updated: "2026-10-06"
related:
  - "specs/agent-instructions-hierarchy.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/122"
  - "https://github.com/joseluisillana/tonto-kids-assistant/pull/123"
  - "ai/specs/002-agent-instructions-hierarchy/plan.md"
---

# Jerarquía portable de instrucciones para agentes

## Estado y objetivo

Estado: **IMPLEMENTED localmente — pendiente de revisión e integración**.
Fecha: 2026-10-06.
Seguimiento: [#122](https://github.com/joseluisillana/tonto-kids-assistant/issues/122).
Plan: [agent-instructions-hierarchy-implementation-plan.md](plan.md).

Reorganizar las instrucciones actuales mediante un `AGENTS.md` raíz como punto
de entrada y mapa arquitectónico, y `AGENTS.md` locales donde exista una
responsabilidad significativa. Conservar cada regla, condición, excepción,
capacidad y ruta de operación existente; reducir duplicidad y permitir adquirir
contexto progresivamente con cualquier agente de desarrollo.

Esta entrega implementa la jerarquía documental y conserva su matriz de origen.
La línea posterior de reorganización de Spec Driven Development queda separada.
Las dos consultas de diseño están resueltas. La matriz y los recorridos del plan
registran la validación local; la issue sigue abierta hasta integrar el trabajo.

## Fuente y adaptación del prompt

Fuente: prompt aportado por el operador, «Prompt para inicializar repositorios».
Propone descubrimiento previo, jerarquía raíz/módulos, contratos, dependencias
en ambos sentidos, comandos y CI reales, conservación de instrucciones,
neutralidad de proveedor, seguridad y revisión cruzada.

Se adapta al repositorio existente con estas condiciones:

- Los archivos son `AGENTS.md`, en Markdown, confirmado por el operador durante
  la revisión. No se introduce YAML ni un formato nuevo de instrucciones.
- La conservación incluye instrucciones no arquitectónicas: Git, permisos,
  secretos, dependencias, alcance, documentación, operación y validación.
- El inventario y la matriz de conservación son obligatorios antes de reducir
  el contenido actual. Compactar no permite perder condiciones o excepciones.
- `tonto.sh` y `scripts/` son la superficie oficial. Analizar Makefile solo si
  existe; no crear uno ni copiar los comandos ilustrativos del prompt.
- Spec, plan, índice y journal son entregables necesarios del workflow vigente,
  aunque el prompt genérico limita documentación adicional.
- Las referencias a proveedores del producto pueden ser necesarias para
  describir código real. No implican requerir un proveedor del agente de desarrollo.
- Se conserva el idioma inglés de los `AGENTS.md` existentes, según la prioridad
  del prompt. Spec, plan y evidencia pueden permanecer en español.

## Contexto observado

Baseline local: `1cf1640`, preparación de v1.0.0 integrada mediante #121.
El MVP conversacional está cerrado; UI táctil/kiosk #81/#88 y otros pendientes
siguen separados. Esta reorganización no altera ese estado ni acredita hardware.

En el baseline había un `AGENTS.md` raíz y no se localizaron locales.
`docs/ai-assisted-workflow.md` desarrollaba reglas que
también aparecen en la raíz. `.agents/skills/` contiene conocimiento operativo
que debe seguir accesible sin soporte específico de skills.

Hay discrepancias que la implementación debe registrar antes de resolver:
`AGENTS.md` y el workflow conservan referencias operativas a Windows/WSL y
DevExpert, mientras el roadmap establece Linux/Docker y D025 declara DevExpert
deprecado para validación. No borrar ese contexto ni reactivar el proveedor:
distinguir historia, adaptadores conservados y operación vigente. Las reglas
sobre Python local y tareas Docker también deben describir su ámbito real.

## Alcance

Incluye descubrimiento del código y documentación pública, inventario atómico
de instrucciones, distribución de fuentes canónicas, navegación, jerarquía de
`AGENTS.md`, neutralización del lenguaje sobre agentes y revisión documental.
Los documentos existentes pueden ajustarse solo para eliminar duplicación,
corregir rutas o separar historia y operación dentro de esta reorganización.

Excluye cambiar runtime, APIs, estructura de paquetes, build, CI, dependencias,
configuración personal, permisos, secretos, proveedores del producto o modelos.
No reorganizar `specs/`, planes, ADRs o journal ni cambiar el proceso SDD vigente.
No crear integraciones obligatorias para herramientas, nuevos wrappers ni
funcionalidades futuras. No operar voz/SSH/proveedores para validar documentación.

## Requisitos

### R1. Descubrimiento previo basado en evidencias

Antes de modificar instrucciones, revisar estructura versionada, fuentes,
entrypoints, manifiestos, README, arquitectura, decisiones, documentación local,
tests, lint/format existentes, scripts, CI, contenedores y configuración pública.
Leer roadmap, specs y última entrada del journal, y cumplir el gate Git actual.
Buscar instrucciones existentes, incluidas las específicas de herramientas y
skills. No deducir responsabilidades por nombres de carpetas ni asumir que una
ausencia en el inventario inicial prueba que no hay otras instrucciones.

Registrar evidencias de interfaces y relaciones: runtime, contratos HTTP o
modelos, configuración, operación y dependencias solo de tests. No convertir
el mapa en un inventario exhaustivo de imports. Las incertidumbres se declaran.

Delimitar el inventario mediante un listado explícito de fuentes revisadas y
exclusiones justificadas. Incluye instrucciones operativas vigentes o invocadas
por raíz, workflow y skills. No convierte cada frase de toda spec o del journal
en una regla global: esos archivos aportan contratos, alcance o decisiones para
su ámbito. El historial sirve para resolver vigencia, no para reactivar órdenes.

El descubrimiento no autoriza leer `.env`, credenciales, configuración expandida,
volcados de entorno, cuerpos crudos de errores o trazas de shell. Se mantienen
las protecciones de #110 y los helpers oficiales con salida acotada.

### R2. Conservación verificable, antes y después

Crear en el plan una matriz **por instrucción**, incluyendo reglas
contenidas en documentos enlazados y skills que gobiernen el trabajo. Cada fila
debe tener ID estable, fuente y sección original, texto o significado completo,
ámbito, condición/excepción, destino canónico, ruta de lectura obligatoria,
tratamiento y evidencia de revisión. Usar la revisión baseline para recuperar
el original; no depender del adjunto externo para ejecutar el plan.

Se permite una unidad con varias cláusulas inseparables o un ejemplo completo
si conserva íntegramente cada condición/excepción y se revisan todas sus cláusulas;
no confundir el número de unidades con el número de obligaciones normativas.

Conservar fuerza normativa y disparador además del contenido: «debe», «prefiere»,
«puede» y «solo si» no son intercambiables. La equivalencia se revisa sobre la
cadena de lectura completa y no sobre similitud de palabras. Por ejemplo,
trasladar la autorización de dependencias a `backend/AGENTS.md` perdería cobertura
en web; cambiar «preferir gh» por «exigir gh» endurecería la regla sin autorización.
Registrar la lista de fuentes antes del recuento: cubrir todas las filas de un
inventario incompleto no demuestra conservación completa.

Tratamientos válidos: conservada, trasladada, fusionada con equivalencia
demostrada, o histórica con decisión vigente enlazada. Ninguna instrucción puede
desaparecer silenciosamente. Si hay contradicción sin decisión existente,
registrarla y pedir decisión al operador antes de modificar la regla afectada.
Una regla histórica conserva contexto y trazabilidad; no se transforma en orden
operativa. Verificar también en sentido inverso: cada regla final tiene origen
o está identificada como navegación nueva exigida por esta spec.

### R3. Fuente canónica y descubribilidad

Un único lugar desarrolla cada regla. La raíz conserva los guardarraíles globales
necesarios antes de cualquier edición, en especial el gate Git, lectura del
estado vigente, seguridad y autorización de dependencias/arquitectura. Los
procedimientos largos permanecen en documentos canónicos existentes con enlaces
y un mandato explícito que indica cuándo leerlos; un enlace opcional no conserva
una obligación. Los resúmenes y enlaces pueden repetirse como navegación, sin
copiar el procedimiento ni introducir otra versión normativa.

Decisión confirmada por el operador: `docs/ai-assisted-workflow.md` mantiene el
detalle de las reglas comunes de trabajo. `AGENTS.md` conserva las reglas
críticas y exige leer el workflow antes de editar, incluidos formatters,
generadores y comandos que escriben archivos. Para procedimientos condicionados,
indica cuándo consultar su sección. No trasladar ese detalle a AGENTS.md ni
duplicarlo en archivos locales.

Las restricciones globales nunca se trasladan solo a un archivo local. Los
locales complementan la raíz y sus ancestros, sin relajar reglas globales.
Leer toda la cadena aplicable y, para cambios transversales, todos los ámbitos
afectados y sus consumidores. No asumir que una herramienta carga archivos o
skills automáticamente; la ruta manual debe ser suficiente.

La reorganización no cambia la precedencia de instrucciones de la sesión ni los
permisos del entorno. Conserva la regla existente de seguir la última indicación
explícita del operador y documentar decisiones persistentes. Entre documentos
del repositorio, un local concreta el ámbito y una decisión vigente puede
sustituir una regla histórica si se registra la evidencia. La profundidad de
una ruta o la fecha de modificación de un archivo no bastan para resolver un
conflicto; tampoco el comportamiento del código autoriza cambiar una regla.

Cada enlace obligatorio identifica disparador y sección pertinente. Leer los
consumidores afectados cuando el cambio puede alterar su contrato o comportamiento,
sin imponer la lectura de todos los archivos de cada consumidor. La raíz enlaza
los locales disponibles; cada local referencia sus ancestros y relaciones
pertinentes. Si un ámbito no tiene local, se aplica el ancestro más cercano y
las fuentes indicadas por la raíz, sin crear un archivo solo por esa ausencia.

Destino preliminar, sujeto al inventario:

| Familia actual | Ubicación y ruta prevista |
| --- | --- |
| Objetivo, límites MVP, simplicidad y no sobreingeniería | Guardarraíles en raíz; detalle vigente en arquitectura/specs enlazadas |
| Lectura de estado, discrepancias y cambios de decisiones | Obligación en raíz → roadmap, specs, journal y documentos pertinentes |
| Reglas Git, ramas, gate, worktrees, commits, PR e issues | Gate mínimo en raíz → procedimiento único en workflow; aislamiento paralelo conservado |
| Linux/Docker/Bash, venv, node_modules, caches y escalación | Resumen global → workflow/scripts; precisiones locales por ámbito |
| Dependencias y arquitectura | Autorización y explicación requeridas en raíz; ninguna relajación local |
| Secretos y límites de protección | Prohibiciones globales en raíz → spec/plan #110; conservar .env y automatización |
| Documentación, planes, handoff y SDD | Obligación global → workflow existente; sin rediseño SDD |
| Operación backend/Raspberry y skills | Ruta neutral al capability pack y SKILL.md públicos; uso manual equivalente |
| Herramientas, modelos y configuración histórica | Contexto histórico/local apropiado, sin requisito de agente/proveedor en AGENTS.md |
| Contratos, fallbacks, errores, validación e impacto | Contexto de módulo y enlaces a specs, consumidores y tests existentes |

Esta tabla es una cobertura por familias; no sustituye el inventario atómico.

### R4. Contenido de la raíz

Incluir overview, mapa conciso, arquitectura y flujo de dependencias, archivos
clave, workflows, testing, navegación a módulos y guardarraíles globales.
Explicar backend Python/FastAPI, cliente Raspberry ligero, web de validación,
HTTP/JSON, contratos compartidos, UI táctil actual y estado de artefactos Go.
Describir lo existente sin convertir propuestas futuras en arquitectura actual.

El mapa puede describir capacidades actuales, pero no duplicar el sprint, fase
activa ni estado de issues en AGENTS.md: esas fuentes siguen siendo roadmap,
specs y journal. Los límites del MVP deben conservar su ámbito temporal y
excepciones post-MVP ya autorizadas; no presentar la UI táctil existente como
prohibida por una regla histórica del MVP ni ampliar permisos a futuras UIs.

Documentar comandos reales de setup/dev/test/build y rutas a operación, limpieza,
export y validaciones disponibles. Derivar su alcance de scripts y CI. CI actual:
`./tonto.sh setup`, `./tonto.sh test all`, `./tonto.sh build all`; no atribuirles
garantías de hardware o equivalencias inexistentes. Referenciar detalle existente.

### R5. Contexto local significativo

Evaluar `backend/`, `client/`, `web/`, `shared/`, `scripts/`, `tests/`, `spikes/`,
`docs/`, `specs/` y `.agents/skills/` como candidatos, no como lista obligatoria
de archivos a crear. Justificar inclusiones y exclusiones con responsabilidades
reales; valorar submódulos solo si aportan contexto distinto.

Cada local debe describir propósito, estructura breve, archivos clave, interfaz
pública, Depends on, Used by, dependencias externas relevantes, restricciones
demostradas, impacto de cambios, testing y documentación local. Omitir secciones
vacías o declarar incertidumbres útiles. Diferenciar implementación interna y
contratos consumidos. Enlazar ancestros y módulos relacionados con rutas válidas.
Cruzar Depends on/Used by y los tests que ejercitan esas relaciones.

No generar archivos en dependencias, caches, entornos, outputs, cobertura,
temporales, binarios o fixtures triviales. No crear un AGENTS.md por carpeta
mecánicamente ni duplicar instrucciones globales para hacerlo autosuficiente.

### R6. Neutralidad y capacidades

Usar «agent» o «assistant» para reglas de desarrollo; no exigir modelo, IDE,
proveedor, extensión, CLI de agente, plugin o MCP. No crear archivos específicos
de proveedor como parte de esta tarea. Las instrucciones existentes específicas
se registran en el inventario y se conserva su información útil en una fuente
neutral o histórica.

Git, gh, Docker y Bash siguen siendo herramientas de proyecto existentes;
neutralidad no exige eliminar esa superficie. Conservar la distinción entre
agentes de desarrollo y proveedores del runtime. Mantener skills y sus recursos;
su conocimiento puede consultarse directamente por archivo. Specs y planes
siguen siendo la fuente de comportamiento, sin obligar a usar un loader de skills.

### R7. Revisión y mantenimiento

Comprobar rutas, enlaces, comandos, vigencia, ausencia de datos sensibles,
conservación y coherencia de dependencias. Conservar nombres técnicos exactos.
Cuando una modificación posterior cambie contrato, comandos o responsabilidades,
actualizar el mapa afectado y su fuente canónica en la misma entrega.
No introducir generadores, nuevas dependencias ni un framework documental.

Las instrucciones trasladadas salen de su ubicación operativa original en la
misma entrega que incorpora su destino y navegación. Conservarlas como historia
en la matriz/baseline no exige duplicarlas en todos los archivos finales.
Antes de integrar, comparar el diff contra el baseline vigente y verificar que
no haya cambios concurrentes sin inventariar; una migración parcial no acredita
conservación total. Git permite revertir la entrega documental sin tocar producto.

El export NotebookLM actual selecciona raíz y Markdown de docs/specs, además de
web/README; no incorpora automáticamente todos los nuevos AGENTS.md locales.
Registrar esta limitación. La navegación operativa del repositorio no depende
del export y esta spec no autoriza ampliar el script ni afirmar que NotebookLM
recibe el nuevo mapa completo.

## Criterios de aceptación

1. La matriz cubre el 100 % de las instrucciones originales inventariadas, con
   condiciones/excepciones y destinos alcanzables; no quedan filas sin resolver.
2. La raíz permite localizar componentes, reglas previas a edición, estado actual,
   comandos y documentos obligatorios; los locales aportan contexto comprobable.
3. Cada regla desarrollada tiene una fuente canónica; las repeticiones restantes
   son enlaces o resúmenes que no alteran su significado.
4. Un agente sin carga automática de AGENTS.md ni skills puede seguir la ruta
   manual y cumplir las mismas reglas. No se promete compatibilidad automática
   con todos los productos ni se requiere probar cuentas externas.
5. Recorridos manuales de cambio backend/contrato compartido, cliente/audio,
   web/audio, scripts/secretos y documentación/spec encuentran obligaciones,
   consumidores, tests y fuentes pertinentes antes de editar.
6. Depends on/Used by, rutas y comandos se contrastan con fuentes públicas.
   Discrepancias vigentes resueltas por decisiones existentes o por el operador;
   contexto histórico conservado y etiquetado.
7. Ningún cambio funcional, nueva dependencia, pérdida de capacidades, modificación
   de secretos/CI ni reorganización SDD. Diff documental acotado y revisado.

Para cada recorrido del criterio 5, registrar: supuesto de cambio, cadena de
lectura, reglas aplicables e IDs de matriz, contrato/consumidores afectados,
validación pertinente y resultado. Se permite «no aplica» con justificación;
una lista de archivos sin demostrar que se encuentra la regla no es evidencia.

## Decisiones confirmadas de la revisión

- **Q1 — formato (resuelta):** el operador confirma AGENTS.md en Markdown.
  No introducir YAML.
- **Q2 — ubicación del procedimiento común (resuelta):** mantener el detalle en
  `docs/ai-assisted-workflow.md`, con reglas críticas y lectura obligatoria desde
  `AGENTS.md`. La implementación aplica esta distribución junto con la matriz
  de conservación; no requiere una nueva elección de ubicación.

## Evidencia de esta entrega

Inventario previo de 524 unidades A/W/D/R/I de cinco fuentes principales, con
original completo, destino, ruta, tratamiento y revisión. Las fuentes adicionales
con contratos/tutoriales conservados se verifican por comparación con baseline.
No se declara que las 524 unidades sean 524 reglas distintas: incluyen contexto,
pasos, ejemplos y repeticiones. Plan con decisiones de ubicación y recorridos.

Raíz y diez locales: backend, client, web, shared, scripts, tests, spikes, docs,
specs y .agents/skills. Revisión de referencias locales y secciones de destino,
neutralidad de AGENTS.md, comandos contra scripts/CI y diff documental.
No cambia runtime, dependencias, CI, secretos, scripts o directorios SDD.
No se ejecutan hardware/proveedores ni pruebas funcionales por este cambio de
documentación. Issue #122 pendiente de revisión/integración; export NotebookLM
mantiene su limitación de cobertura de archivos locales.

## Migration provenance and supported current state

- Original repository source: `specs/agent-instructions-hierarchy.md` at baseline 818e88e.
- First recorded Git date: 2026-10-06; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-10-06.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: PR #123 merged 2026-10-06 as 40342ee; supersedes the preserved local-pending heading.
- Evidence: [source](https://github.com/joseluisillana/tonto-kids-assistant/pull/123).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/122).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
