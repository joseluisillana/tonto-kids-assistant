# #110 — alternativas para reducir exposición accidental

Fecha: 2026-10-06. Estado: exploración documental, sin cambio de credenciales.

## Decisión vigente

El operador elige conservar el workflow actual y reducir primero exposiciones
accidentales. El agente mantiene desarrollo, tests, backend y validación SSH.
No adoptar separación de identidades, runtime operado solo por humano ni mediador.
La propuesta de aislamiento anterior queda diferida, no aprobada.

Decisión posterior: el operador descarta sustituir .env por variable host.
Primera implementación autorizada: diagnósticos seguros, conservando la
provisión actual. La comparación se conserva como historial de alternativas.
Esta fase no garantiza impedir acceso deliberado por shell, Docker o código.

## Comparación

| Opción | Qué mejora | Riesgo que conserva | Impacto operativo |
| --- | --- | --- | --- |
| `.env` actual + diagnósticos seguros | Evita volcados accidentales desde comandos oficiales | Clave en archivo y entorno del backend | Mínimo; misma provisión |
| Referencia a variable del host | Quita el valor literal de `.env` | Compose la expande; entorno host/contenedor accesible | Provisionar variable en el proceso que ejecuta Compose |
| Archivo externo usado como `env_file` | Quita la clave del árbol del repo y del contexto de build | Sigue expandida por Compose y en entorno del backend | Configurar ruta y actualizar scripts |
| Secreto Compose desde archivo externo | No inyecta valor como variable del backend; acceso por servicio | Archivo host y montaje legibles con acceso suficiente; Docker exec/código pueden leerlo | Python lee archivo; provisionar ruta una vez |
| Secreto Compose desde variable del host | Entrega archivo al backend sin valor literal en `.env` | Variable del host sigue accesible; no garantiza aislamiento | Variable disponible en cada arranque; compatibilidad por validar |

## Variable del host: respuesta concreta

El backend ya usa `os.environ.get("OPENAI_API_KEY")` en chat y STT. No lee
`.env` directamente: Compose carga el archivo y suministra la variable al
contenedor. Para prescindir de su valor en `.env`, podría declararse en Compose:

```yaml
services:
  backend:
    environment:
      - OPENAI_API_KEY
```

Esto pasa la variable disponible para Compose al contenedor; no implica que
Python pueda consultar el entorno de cualquier otro proceso del host. Evitar
mantener una fuente literal conflictiva en `.env` y definir validación de ausencia.
El arranque requiere que los helpers/Codex desktop reciban la variable. Conserva
el código Python, pero valor sigue en entorno del contenedor y puede aparecer
en diagnósticos. Aún no se cambia configuración real.

Ejemplo conceptual de `.env`, sin valor real:

```dotenv
OPENAI_API_KEY=${TONTO_HOST_OPENAI_API_KEY}
```

Compose admite interpolación en valores sin comillas o con comillas dobles;
comillas simples conservarían la referencia literalmente. El valor debe estar
exportado al proceso que ejecuta Compose. Los archivos `.env` no constituyen un
gestor de secretos ni recuperan variables de cualquier sesión del host.
El backend recibe el valor resuelto; un dump completo de Compose podría mostrarlo.
Conservar la regla de no ejecutar dumps incluso si se adopta esta opción.
No sugerir introducir la clave mediante un comando literal que quede en el
historial ni almacenarla en un perfil shell con valor visible.

Codex desktop y una terminal abierta pueden tener entornos distintos. Verificar
presencia booleana con fixtures; no leer ni imprimir la variable real. No elegir
esta opción hasta concretar cómo la suministra el operador a los helpers.

## Secreto como archivo: alternativa recomendada para evaluar después

Ejemplo conceptual; aún no aplicado:

```yaml
services:
  backend:
    environment:
      OPENAI_API_KEY_FILE: /run/secrets/openai_api_key
    secrets:
      - openai_api_key
secrets:
  openai_api_key:
    file: ${TONTO_OPENAI_SECRET_FILE}
```

`TONTO_OPENAI_SECRET_FILE` contiene una ruta, nunca la clave. El operador crea
el archivo fuera del repo con permisos apropiados y configura la ruta. No copiar
ni mover secretos desde herramientas del agente. Compose concede el montaje al
backend; web/UI y tareas de setup/tests no deben recibirlo.

Python debe implementar lectura explícita de `OPENAI_API_KEY_FILE` para chat
y STT; Docker no implementa automáticamente esa convención. Leer directamente
en Python, sin exportar luego el valor a una variable de entorno. Errores seguros
si falta archivo, es ilegible o está vacío. Definir precedencia/rechazo si se
configuran simultáneamente archivo y variable; no resolverlo silenciosamente.

Compose local no convierte el archivo en un vault cifrado ni aísla del daemon.
No afirmar que todos sus diagnósticos estén libres de valores sin pruebas de
canarios contra la versión instalada, errores, trazas y comandos pertinentes.

Los comandos `tonto.sh` y helpers SSH pueden conservarse. La preparación inicial
de la credencial cambia; Raspberry no necesita almacenar la clave del backend
ni instalar paquetes. El consumo por archivo es una opción pendiente, no una
decisión ya aceptada. No añade una dependencia Python.

## Orden recomendado con mínimo impacto

1. Mantener por ahora provisión actual. Eliminar materialización completa de
   Compose en limpieza y definir diagnósticos acotados; acotar errores HTTP/STT.
2. Excluir secretos de build/export y de servicios/tareas que no los necesitan.
   Separar configuración de tests/setup de la del runtime sin perder comandos.
3. Validar con canarios ficticios; conservar funcionamiento de helpers y demo.
4. Decidir después si vale la pena consumo por archivo externo. Variable del
   host es una mejora de almacenamiento, pero no resuelve el incidente Compose.

## Fuentes primarias consultadas

- [Interpolación Compose](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/): expansión y entorno del proceso.
- [Uso de secretos](https://docs.docker.com/compose/how-tos/use-secrets/): archivo `/run/secrets`, concesión por servicio y convención `_FILE`.
- [Fuentes de secretos](https://docs.docker.com/reference/compose-file/secrets/): `file` o `environment`; soporte Compose.

Exploración basada en documentación y código público. Sin prueba con claves
reales, cambio de runtime ni validación de compatibilidad local de las opciones.


## Migration provenance

Original source: `docs/agent-secrets-credential-options.md` at baseline 818e88e. Relocated 2026-10-06;
original content/language retained with path references adjusted. Historical
commands, approvals and pending notes retain their original context.
