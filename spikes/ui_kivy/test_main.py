import os
import sys

# Desactivar argumentos de consola de Kivy y forzar proveedor mock (sin ventana real)
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_WINDOW'] = 'mock'
os.environ['KIVY_LOG_LEVEL'] = 'warning' # Para no ensuciar la salida

from main import TontoSpikeApp

def test_app():
    print("Iniciando prueba automatizada del Agente IA...")
    app = TontoSpikeApp()
    
    # Construimos el árbol de widgets sin levantar la aplicación
    layout = app.build()
    
    # El layout añade los widgets: primero label, luego button.
    # En kivy los hijos se insertan al principio de la lista por defecto,
    # así que el botón está en el índice 0 y el label en el 1.
    btn = layout.children[0]
    label = layout.children[1]
    
    print("\n--- Estado Inicial ---")
    print(f"Texto del Label: '{label.text}'")
    print(f"Texto del Botón: '{btn.text}'")
    
    # Validamos estado inicial
    assert "Inactivo" in label.text
    assert btn.text == "PULSA PARA HABLAR"
    
    print("\n--- Simulando Touch (FINGERDOWN / MOUSEBUTTONDOWN) ---")
    btn.dispatch('on_press')
    
    print(f"Texto del Label: '{label.text}'")
    print(f"Texto del Botón: '{btn.text}'")
    
    # Validamos el cambio
    assert "Escuchando" in label.text
    assert btn.text == "GRABANDO..."
    
    print("\n--- Simulando Release (FINGERUP / MOUSEBUTTONUP) ---")
    btn.dispatch('on_release')
    
    print(f"Texto del Label: '{label.text}'")
    print(f"Texto del Botón: '{btn.text}'")
    
    # Validamos el estado final
    assert "Procesando" in label.text
    
    print("\n✅ PRUEBA EXITOSA: La lógica de la UI reacciona perfectamente a los eventos de estado.")

if __name__ == '__main__':
    test_app()
