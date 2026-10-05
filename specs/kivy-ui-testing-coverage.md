# Kivy UI Testing Coverage

**Status:** Implemented
**Date:** 2026-10-05
**Branch:** `feature/kivy-ui-testing-coverage`
**Tracking:** #105, part of #81

## Contexto y objetivo

La UI táctil post-MVP ya implementa `client/tonto_face.py` y
`client/touch_ui.py`, pero CI no ejercitaba esos módulos. Añadir pruebas de
widgets reales, estados y callbacks sin pantalla física, micrófono, llamadas
HTTP ni reproducción de voz. Mantener intacto el código de producto.

## Alcance

- `tests/test_tonto_face.py`: constantes, constructor y canvas reales, los cinco
  estados, repetición de IDLE, destino de animaciones ERROR/SPEAKING y cancelación
  de eventos al salir de SPEAKING.
- `tests/test_touch_ui.py`: construcción real de ProgressButton/TontoTouchUI,
  configuración de backend, modo texto, eventos enlazados a botones/input,
  protección frente a entradas vacías o estado ocupado, éxito/error/reset,
  reproducción delegada y contratos de llamadas de texto/audio.
- `tonto.sh test ui`, integración en `test all`, ayuda y evidencia documental.
- No comparar píxeles ni validar hardware, kiosk o proveedores reales. La Fase 7
  sigue siendo un trabajo separado (#88).

## Entorno reproducible

Ejecutar Kivy 2.3.0 real en `ui-emulator` mediante SDL2 y Xvfb. La instalación
actual no incluye un proveedor de ventana `headless`; esa premisa del borrador
se descarta. El Dockerfile existente ya instala Xvfb y sus dependencias.

`./tonto.sh test ui` debe:

1. Ejecutar pytest con `.venv/bin/python` del volumen Docker existente.
2. Usar `xvfb-run -a` y un volumen temporal `/tmp/.X11-unix`, sustituyendo el
   socket del host solo para esta ejecución. No requiere DISPLAY del host.
3. Establecer KIVY_WINDOW=sdl2, SDL_VIDEODRIVER=x11,
   LIBGL_ALWAYS_SOFTWARE=1 y SDL_AUDIODRIVER=dummy.
4. Usar KIVY_NO_ARGS=1 para que Kivy no interprete argumentos de pytest,
   KIVY_HOME=/tmp/.kivy-test, KIVY_CLIPBOARD=dummy y XDG_CACHE_HOME=/tmp/.cache.
5. Desactivar bytecode y caché de pytest. No configurar Kivy globalmente en
   `tests/conftest.py` ni simular módulos Kivy mediante sys.modules.

El Dockerfile prepara `/tmp/.X11-unix` con permisos 1777 para el volumen
temporal. El target reconstruye la imagen cuando cambia el Dockerfile y usa un
wrapper Bash como padre de xvfb-run, conservando el código de salida de pytest.
Ejecutar xvfb-run directamente como PID 1 bloqueó su señal de arranque durante
la validación; no debe eliminarse ese wrapper sin verificar este recorrido.

Los constructores deben ejecutarse normalmente: no sustituirlos por `__new__`
ni reproducir la lógica del producto dentro del test. Se simulan operaciones
externas en `client.touch_ui`, donde se resuelven sus imports, y los workers
para que no ejecuten audio/red. Los callbacks `mainthread` se procesan con
`Clock.tick()`. Las animaciones reales avanzan con el reloj hasta sus valores
destino, con plazo acotado de dos segundos; no asumir que el destino es visible
inmediatamente tras `set_state`. Limpiar eventos y animaciones entre tests.

## Integración y aceptación

- `test python` conserva sus comprobaciones de sintaxis y suite existente,
  excluyendo únicamente los dos módulos gráficos.
- `test all` ejecuta python → ui → web. CI ya utiliza este comando.
- `test ui` devuelve 0 con todos los tests reales pasando sin pantalla física.
- `test all` devuelve 0 y backend/web siguen pasando.
- La ayuda y documentación describen el entorno y sus límites.
- No añadir dependencias, modificar arquitectura ni tocar código de producto.

## Riesgos

La validación con Mesa por software no sustituye la prueba de OpenGL ES/touch en
Raspberry. El volumen de dependencias requiere `./tonto.sh setup` en un checkout
limpio. Xvfb debe aislarse de los sockets del host para evitar colisiones.
