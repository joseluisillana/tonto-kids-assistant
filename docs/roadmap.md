# Roadmap del MVP - 6 semanas

Este roadmap describe un plan práctico para llevar el proyecto a una demo funcional en 6 semanas. Se enfoca en entregables iterativos, evita añadir características no necesarias y prioriza la estabilidad de la solución mínima viable.

## Semana 1 - Base operacional

Objetivo:
- Tener la infraestructura física y de desarrollo lista para comenzar.

Entregables:
- Raspberry Pi configurada y accesible.
- Conexión SSH establecida.
- VS Code conectado en remoto al dispositivo.
- Audio de salida probado en la Raspberry.
- Estructura inicial del proyecto creada en el repositorio.

Prioridades:
1. Configurar la Raspberry Pi con sistema operativo estable.
2. Validar acceso remoto seguro (SSH + VS Code Remote).
3. Confirmar que la salida de audio funciona con el hardware disponible.
4. Organizar carpetas y archivos base (`backend/`, `client/`, `shared/`, `docs/`, `tests/`).

Riesgos:
- Problemas de red o permisos SSH que retrasen el acceso remoto.
- Hardware de audio incompatible o sin drivers.
- Estructura del proyecto demasiado amplia antes de definir el MVP.

## Semana 2 - Primer flujo mínimo de audio y control

Objetivo:
- Establecer el primer flujo de audio y la comunicación básica entre módulos.

Entregables:
- Módulo de reproducción de audio local funcional.
- Cliente que pueda activar el audio desde el backend.
- Documentación breve del flujo de datos audio/comando.

Prioridades:
1. Implementar reproducción de audio simple en la Raspberry.
2. Validar el canal de comunicación entre `client/` y `backend/`.
3. Mantener el flujo lo más directo posible sin añadir procesamiento complejo.

Riesgos:
- Retrasos en integración entre Python y Go si se requiere comunicación entre servicios.
- Dependencias de audio que fallen en el entorno objetivo.
- Dificultad para reproducir audio continuamente y sin interrupciones.

## Semana 3 - Interfaz de control y parámetro básico

Objetivo:
- Crear una interfaz operativa para iniciar la demo y controlar el sistema.

Entregables:
- Control remoto simple en VS Code o terminal para iniciar la reproducción.
- Ejemplo de uso documentado.
- Validación de que el sistema completo inicia y responde.

Prioridades:
1. Generar un comando o script de inicio que orqueste los componentes.
2. Definir un caso de uso mínimo: reproduzca un audio al recibir una orden.
3. Asegurar que el estado de la Raspberry y el proceso sean visibles y fáciles de reiniciar.

Riesgos:
- Falta de un método claro para iniciar la demo durante la presentación.
- Comportamiento no determinista al reiniciar procesos.
- Configuración manual excesiva para ejecutar el MVP.

## Semana 4 - Iteración sobre la lógica de interacción

Objetivo:
- Refinar la interacción mínima, mejorar la estabilidad y preparar la demo.

Entregables:
- Flujo de interacción consolidado.
- Manejo de errores básico y recuperación al fallo de audio.
- Checklist de pasos para ejecutar la demo.

Prioridades:
1. Añadir validaciones simples para detectores de error.
2. Garantizar que la demo se pueda repetir sin reinstalar.
3. Ajustar la documentación operativa con comandos reales.

Riesgos:
- Errores que no se detectan hasta la ejecución en vivo.
- Dependencias externas faltantes en el entorno target.
- Documentación incompleta que genere confusión.

## Semana 5 - Prueba de demo y ajuste final

Objetivo:
- Ejecutar la demo completa varias veces y corregir los problemas más importantes.

Entregables:
- Demo funcional reproducida con éxito al menos 3 veces.
- Registro de problemas y correcciones aplicadas.
- Versión estable de la aplicación lista para mostrar.

Prioridades:
1. Probar la demo en condiciones reales de hardware.
2. Corregir fallos críticos y mejorar el comportamiento repetible.
3. Mantener el alcance: no añadir nuevas funciones, solo estabilizar lo existente.

Riesgos:
- Problemas de última hora con la Raspberry o el sistema de audio.
- Comportamiento distinto en la demo frente al entorno de desarrollo.
- Ajustes de tiempo insuficientes para pruebas adicionales.

## Semana 6 - Documentación, entrega y retroalimentación

Objetivo:
- Entregar el MVP, documentar el estado actual y preparar los siguientes pasos.

Entregables:
- Documentación operativa clara para ejecutar la demo.
- Resumen de lo que funciona, lo que está limitado y qué debe mejorar.
- Plan corto para evolución posterior en función de la retroalimentación.

Prioridades:
1. Redactar instrucciones de puesta en marcha paso a paso.
2. Registrar los limites del MVP y las áreas de riesgo conocidas.
3. Preparar una presentación ligera del estado actual.

Riesgos:
- Falta de claridad en la documentación de uso.
- Inconvenientes para compartir la demo si el hardware queda inaccesible.
- No definir claramente qué se deja fuera del MVP y por qué.

## Prioridades generales

- Priorizar siempre una demo funcional por encima de características adicionales.
- Construir el MVP en iteraciones pequeñas y verificables.
- Mantener el alcance limitado a lo necesario para mostrar un flujo operativo.
- Documentar hallazgos y decisiones técnicas semana a semana.

## Riesgos clave a vigilar

- Dependencia del hardware de audio en la Raspberry.
- Acceso remoto y estabilidad de la plataforma.
- Scope creep: resistir añadir funciones que no contribuyan a la demo mínima.
- Falta de pruebas en el entorno final antes de la presentación.

