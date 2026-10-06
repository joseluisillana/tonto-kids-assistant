# Release v1.0.0 — cierre del MVP Linux/Docker

Decisión aprobada por el operador: 2026-10-06. Baseline de producto: e98f43f.
Publicación: tag anotado v1.0.0 y primera GitHub Release, tras PR y CI aprobada.
Plan: docs/plans/release-v1.0.0-implementation-plan.md.

## Alcance y compatibilidad

Se acepta como contrato público del MVP el HTTP/JSON documentado de GET /health,
POST /chat y POST /chat/audio; el audio admitido sigue siendo WAV PCM mono,
16 kHz, 16 bits. Los detalles y límites siguen en specs/audio-pipeline.md y
specs/web-validation-client.md. Backend FastAPI, Raspberry thin client y web
conservan su comportamiento; estado de conversación únicamente en memoria.

La operación soportada del host es Linux + Docker + Bash mediante tonto.sh
setup/dev/test/build/down. Desde v0.6.1 se retiró el workflow PowerShell/Windows;
los operadores deben migrar a los runbooks Linux. No se cambia almacenamiento
.env ni automatización backend/SSH en esta release. No se añaden dependencias.

VERSION declara 1.0.0 como referencia de la release del monorepo. Los metadatos
web/package.json y las dos entradas raíz de su lockfile se alinean a 1.0.0;
no cambia ninguna versión resuelta de dependencia. Los futuros cierres deben
mantenerlos alineados mediante su PR. No se introduce lectura dinámica ni
nuevos mounts; esta declaración no cambia el default de metadatos OpenAPI.

## Límites y pendientes conservados

- #81/#88: integración táctil existente; kiosk y aceptación final touch/OpenGL ES
  en Raspberry pendientes. v1.0.0 no declara terminado ese hito.
- #114: demora del control de volumen del emulador aplazada.
- #53: evaluación de proveedores futura. DevExpert deprecado para operación
  real por D025; adaptadores históricos solo cubiertos con mocks.
- #110 cerrada por reducción de exposiciones accidentales; aislamiento completo
  diferido. No se promete bloqueo universal del acceso del agente.
- Sin persistencia, cuentas, auth, wake word, modelos locales ni backend TTS.
- mDNS en esta LAN requiere alternativa IP con identidad SSH verificada;
  calidad espeak básica y avisos de deprecación existentes documentados.

## Evidencia y aceptación de publicación

Baseline e98f43f: revalidación de #110 en specs/agent-secrets-protection.md,
175 tests Python, 25 Kivy, web/build/setup y scripts aprobados; PR #120 y CI main
37452016616 success. Validación física anterior de migración en
specs/migrate-linux-docker-validation.md; no se presenta como revalidación física
posterior a #110. Esta preparación solo cambia documentación y versión.

Publicar exige: metadatos alineados, lockfile sin cambios de dependencias,
./tonto.sh test web y ./tonto.sh build web aprobados, export y diff check limpios,
CI completa del commit de la PR (setup/test all/build all) aprobada y merge.
Comprobar además CI main aprobada, ausencia del tag v1.0.0 y main sincronizada;
crear tag anotado sobre el SHA integrado, push y gh release create --verify-tag
con docs/releases/v1.0.0.md. No mover tags históricos ni cerrar pendientes.

### Validación de preparación (2026-10-06)

./tonto.sh test web: exit 0, TypeScript y suite web aprobados.
./tonto.sh build web: exit 0, TypeScript/Vite, 43 módulos.
Comparación JSON del lockfile con e98f43f: solo cambian las dos versiones raíz;
ningún paquete, integridad, URL o rango de dependencia cambia. VERSION y ambos
manifest/lock alineados a 1.0.0. Export y diff check aprobados antes del commit.
CI completa de PR y main se verificará como gate de publicación en GitHub.
