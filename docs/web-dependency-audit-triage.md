# Propuesta de análisis y actualización web — P-107-07

2026-10-05, Part of #107. Propuesta; no se cambian package.json ni lockfile.
Tras npm ci: audit 7 vulnerabilidades (2 low, 1 moderate, 4 high), exit 1.
Audit omit-dev: cero, exit 0. Consulta previa del árbol instalado: 14; no se
extrapola ese resultado al árbol limpio ni se afirma la causa de la diferencia.

## Primera evaluación

El árbol de desarrollo contiene Babel 7.29.0, esbuild 0.27.7, PostCSS 8.5.14 y
Vite 7.3.3. No basta audit producción cero para cerrar el riesgo de desarrollo.

- Babel: lectura de mapas al compilar código malicioso; la fuente indica que
  compilar código de confianza no está afectado. Parche 7.29.6.
  https://github.com/advisories/GHSA-4x5r-pxfx-6jf8
- PostCSS: lectura de mapas con CSS controlado por atacante; parche 8.5.23
  para el advisory revisado. Revisar también el advisory previo del informe.
  https://github.com/advisories/GHSA-fxqj-rqcc-2cmp
- Browserslist: crecimiento de memoria en procesos largos con consultas
  externas variables; parche 4.28.7 para el advisory revisado. Revisar además
  el advisory de custom stats antes de fijar la versión final.
  https://github.com/advisories/GHSA-c83g-rgw3-j3cx
- Vite: bypass revisado requiere Windows/NTFS y servidor expuesto; Linux Docker
  no satisface esa condición según el entorno actual. Parche de rama 7: 7.3.5.
  Esto no autoriza ignorar otros advisories ni aceptar riesgo automáticamente.
  https://github.com/advisories/GHSA-fx2h-pf6j-xcff
- esbuild, nanoid y baseline-browser-mapping: informe identifica archivos en
  servidor Windows, bucles en generadores y terminación por entrada inválida.
  La evaluación completa de cada advisory y disponibilidad de versiones
  corregidas sigue pendiente; no se consideran ya mitigados.

## Propuesta de ejecución separada

1. Revisar todos los advisories actuales en fuentes oficiales y el árbol npm ls.
2. Proponer actualización dentro de majors existentes y rangos compatibles:
   Vite 7 corregido y transitivas corregidas Babel/PostCSS/Browserslist/esbuild/
   nanoid/baseline. Verificar versiones publicadas antes de fijarlas; no introducir
   overrides o cambios de major sin discutir necesidad/compatibilidad.
3. Actualizar lockfile de forma controlada, sin audit fix --force, y repetir npm ci,
   audit dev/prod, test all, build all y smoke web texto/voz. Sin dependencias nuevas.
4. Registrar riesgo residual y solicitar aceptación explícita si no puede
   eliminarse. Solo entonces cerrar P-107-07 y punto 7.

Los parches citados son candidatos derivados de advisories, no una combinación
ya validada. Este documento es triage inicial, no implementación aprobada.
