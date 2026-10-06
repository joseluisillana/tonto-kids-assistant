---
id: "023-web-dependency-audit-remediation"
title: "Cierre de auditoría web del punto 7"
status: done
owner: "Unknown — legacy ownership not recorded"
created: "2026-10-06"
updated: "2026-10-06"
related:
  - "specs/web-dependency-audit-remediation.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/issues/107"
  - "docs/project-journal/week-06.md#post-mvp--cierre-auditoría-web-p-107-07-2026-10-05"
  - "ai/specs/023-web-dependency-audit-remediation/plan.md"
  - "ai/specs/023-web-dependency-audit-remediation/artifacts/web-dependency-audit-triage.md"
---

# Cierre de auditoría web del punto 7

2026-10-05. Trabajo autorizado por el operador. Part of #107, P-107-07.
Rama fix/web-dependency-audit; base docs/post-migration-stability-validation.

## Objetivo y alcance

Eliminar los advisories del árbol npm de desarrollo sin alterar el producto.
Actualizar lockfile de forma compatible con package.json, conservando React 19,
Vite 7, plugin-react 5, Tailwind 4 y TypeScript 5. No añadir dependencias directas
ni usar --force. Si el resolver requiere overrides o cambiar major de una
herramienta directa, explicar y revisar esa decisión antes de proceder.
La actualización de transitivas es parte del mantenimiento autorizado.

## Aceptación

1. npm ci limpio y auditoría completa/omit-dev terminan con exit 0 y cero hallazgos.
2. Árbol npm sin dependencias inválidas; lockfile reproducible.
3. Setup, 97 tests Python, 24 Kivy, web y build pasan; CI pasa.
4. Smoke web texto y subida de voz contra backend conservan transcript/respuesta
   y manejo de estados. No convertir el smoke en aceptación física de speech.
5. P-107-07 y punto 7 COMPLETADO con logs sanitizados, versiones y URLs de CI.
6. Audibilidad web/emulador y UI touch física mantienen sus pendientes propios;
   no cerrar #107 por esta reparación.

## Evidencia y fuentes

Informe inicial: 7 hallazgos (2 low, 1 moderate, 4 high), cero producción.
Revisar todos los GHSA del audit en fuentes de los mantenedores, registrar
versiones antes/después y cualquier riesgo residual. Sin aceptación implícita
de vulnerabilidades aunque una afecte únicamente a otro SO.

Plan: docs/plans/web-dependency-audit-remediation-implementation-plan.md.

## Migration provenance and supported current state

- Original repository source: `specs/web-dependency-audit-remediation.md` at baseline 818e88e.
- First recorded Git date: 2026-10-06; actual original authoring date is unknown
  unless explicitly recorded in the preserved body.
- Last source Git date before migration: 2026-10-06.
- Migration/update date: 2026-10-06. Legacy owner/authorship is not established;
  the current owner field records that uncertainty, not a fabricated attribution.
- Status decision: Web audit repair and zero-audit result accepted in Week 06 journal and final #107 matrix.
- Evidence: [source](../../../docs/project-journal/week-06.md#post-mvp--cierre-auditoría-web-p-107-07-2026-10-05).
- Corresponding GitHub tracking issues: [GitHub issue](https://github.com/joseluisillana/tonto-kids-assistant/issues/107).

Historical headings below/above retain the original reported state. YAML status
and this provenance annotation express the supported state after evidence review.
Do not execute archived proposals or historical operating examples without a new
authorized work item. No runtime or acceptance behavior changed by relocation.

Maintain plan.md/journal.md and synchronize status/updated with the parent INDEX.md
in the same change. No secrets, credentials, tokens, connection strings, PII or
real customer data; sensitive configuration is described by parameter name only.
