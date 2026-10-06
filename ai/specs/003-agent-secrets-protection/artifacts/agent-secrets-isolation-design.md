# #110 — diseño de aislamiento para revisión

Estado: propuesta DRAFT, 2026-10-06. No desplegada ni aprobada.

**SUPERSEDIDA como propuesta activa:** el operador decide conservar el workflow
actual y reducir exposiciones accidentales. Este diseño queda como alternativa
diferida. Propuesta vigente en `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-credential-options.md` y spec
#110 actualizada; no trasladar runtime/SSH a operación exclusivamente humana.
Spec: `ai/specs/003-agent-secrets-protection/spec.md`.
Plan: `ai/specs/003-agent-secrets-protection/plan.md`.

## Evidencia disponible

- Codex CLI disponible: 0.160.0, comprobado con `codex --version` y ayuda.
  No se ha leído su configuración personal, autenticación ni entorno completo.
- El perfil suministrado a esta sesión permite lectura de la raíz del host y
  escritura en el checkout y temporales; ofrece escalación. Por tanto no cumple
  el requisito de negar lectura de secretos. No se intentó abrirlos para probarlo.
- Hay autorizaciones persistentes para Docker exec y Compose run en esta sesión.
  No se han usado para inspeccionar credenciales. Son vías a retirar o limitar
  externamente en un perfil protegido; no basta modificar AGENTS.md.
- OpenCode no se encuentra en el PATH de esta shell. Sus permisos efectivos no
  se han evaluado; ausencia del ejecutable no demuestra aislamiento.
- Fuente oficial consultada:
  [Sandbox de Codex](https://learn.chatgpt.com/docs/sandboxing).
  Distingue límites técnicos y aprobaciones; documenta `workspace-write` como
  lectura de archivos y escritura dentro del workspace. No se presupone que
  una opción concreta de denegación de lectura esté disponible en esta instalación.
- Docker, SSH, conectores y navegador: no se han ejecutado pruebas negativas
  contra controles nuevos. Estado de aislamiento: no evaluado.

## Alternativas

| Opción | Operación | Límite | Propuesta |
| --- | --- | --- | --- |
| Solo instrucciones y helpers | Conserva flujo actual | Shell, Docker y código modificable permiten elusión | Endurecimiento parcial |
| Entorno sin secretos + operación humana | Agente desarrolla y prueba; humano ejecuta demo real | Menor automatización; requiere separar permisos y código | Primera fase recomendada |
| Entorno sin secretos + mediador externo | Agente pide acciones concretas al operador técnico | Requiere instalar/controlar un componente y su perímetro | Fase posterior si la operación humana resulta insuficiente |

## Diseño recomendado: primera fase

Dos dominios de ejecución, administrados por el operador. Puede materializarse
como entorno aislado o identidades separadas, pero la elección concreta debe
demostrar los criterios siguientes antes de considerarse aceptada.

**Dominio de desarrollo del agente:** checkout sin credenciales reales, fixtures
ficticias, dependencias y comandos oficiales adaptados para tests sin secretos.
No incluye el home del operador, claves SSH, configuración de otros servicios,
socket del daemon que gestiona el runtime real, procesos de ese runtime ni
volúmenes con secretos. Una shell aislada no basta si otro conector del mismo
chat conserva acceso al host: todos los canales deben tener el mismo perímetro.
Si requiere Docker para tests, usar un daemon aislado sin recursos ni acceso al
host del runtime; verificarlo, no asumir que cambiar el nombre de proyecto aísla.

**Dominio de runtime del operador:** credenciales fuera del checkout accesible
al agente y protegidas por un control que este no puede modificar. Ubicación
exacta por decidir; no proponer mover archivos con una lectura previa de valores.
Backend sigue consumiendo configuración mediante mecanismo aprobado por el
operador. La inyección por entorno no se considera segura frente a un agente con
acceso al proceso/daemon; la frontera es el dominio, no el nombre de la variable.

**Código que consume secretos:** copia revisada y promovida por el humano,
inmutable para el agente durante la demo. Sin bind mount del checkout editable,
reload, scripts/hooks/imports modificables ni dependencia mutable compartida.
El operador revisa cambios antes de promoverlos; un commit o imagen fijada por
sí solos no garantizan que el código sea seguro. Probar también modificación de
dependencias, configuración Compose, comandos de arranque y destinos HTTP.

**Operación inicial:** el humano arranca/para backend y ejecuta SSH/preflight/demo
con los scripts oficiales desde su dominio. El agente prepara cambios y pruebas
con mocks. Salud y respuestas API solo se devuelven tras acotar errores y validar
que no hay exposición. No devolver logs, inspect o shells del runtime.
La API de producto y la arquitectura conversacional permanecen iguales.

**Administración:** el agente no puede cambiar usuarios/permisos/política, montar
el dominio real ni obtener excepciones que otorguen acceso a secretos. El humano
administra fuera de la sesión protegida. Las escalaciones persistentes existentes
se revisan al crear el nuevo perfil; este documento no las modifica.

## Si posteriormente se necesita mediación automática

Interfaz cerrada: backend start/stop/status/health y acciones Raspberry preflight,
demo-text/demo-voice/demo-touch. Sin argumentos shell, rutas arbitrarias, env
arbitrario, logs brutos ni Docker exec. El componente y sus acciones quedan fuera
del checkout editable; entradas y salidas validadas y errores seguros.
Debe ejecutar únicamente código promovido por el operador. No implementar un
servicio propio ni añadir dependencia sin revisar una necesidad demostrada.

## Matriz de pruebas antes de cambiar secretos reales

| Caso | Resultado esperado en el perfil protegido |
| --- | --- |
| Lectura, escritura y copia de canario por shell y herramientas de archivos | Denegadas por control externo |
| Symlink/ruta alternativa al dominio del operador | Sin acceso |
| Compose inspect/exec/montaje contra runtime real | Sin acceso al daemon ni al recurso |
| Procesos, entorno y memoria del runtime | Sin acceso |
| Cambiar código/reload/dependencias de la demo real | No puede afectar la copia promovida |
| Cambiar controles o ejecutar escalación previamente autorizada | No abre acceso al dominio real |
| Conector o navegador con recursos del host | Denegación equivalente o canal deshabilitado |
| Setup/tests/build con secretos ausentes | Pasan en dominio de desarrollo |
| Demo real tras promoción humana | Contratos y voz conservados |

Harness con canarios solo en entorno ficticio y salida de caso/resultado, sin
valores ni volcados. Ejecutarlo dentro del perfil protegido real, incluyendo
herramientas distintas de la shell. No crear una prueba artificial que solo
simule permisos y declararla evidencia del escritorio actual.

## Decisión solicitada

Adoptar como objetivo inicial desarrollo/tests aislados sin secretos y operación
humana del runtime y SSH. Autorizar después el spike de materialización del
entorno con canarios; elegir identidad/entorno disponible sin instalar nada ni
cambiar la máquina antes de revisar la solución concreta. Mantener mediador
automático como alternativa futura. Hasta entonces, #110 sigue DRAFT.

Este documento es un diseño y una evaluación preliminar, no una prueba de
aislamiento, ni una instrucción para desactivar accesos de esta sesión.


## Migration provenance

Original source: `docs/agent-secrets-isolation-design.md` at baseline 818e88e. Relocated 2026-10-06;
original content/language retained with path references adjusted. Historical
commands, approvals and pending notes retain their original context.
