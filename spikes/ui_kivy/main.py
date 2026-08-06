import os
# Aseguramos que corra en modo ventana (Windowed) para desarrollo en PC
os.environ['KIVY_WINDOW'] = 'sdl2'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Tamaño típico de la pantalla de 5" (800x480)
Window.size = (800, 480)

class TontoSpikeApp(App):
    def build(self):
        # Fondo oscuro para contraste
        Window.clearcolor = get_color_from_hex('#1e1e2e')
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Etiqueta que hará las veces de "Cara" / Estado
        self.status_label = Label(
            text="TONTO UI Spike - Inactivo",
            font_size='32sp',
            size_hint=(1, 0.7),
            color=get_color_from_hex('#cdd6f4')
        )
        layout.add_widget(self.status_label)
        
        # Botón gigante para hablar
        self.btn = Button(
            text="PULSA PARA HABLAR",
            font_size='36sp',
            size_hint=(1, 0.3),
            background_normal='',
            background_color=get_color_from_hex('#a6e3a1') # Verde
        )
        
        # Bind events
        self.btn.bind(on_press=self.on_button_press)
        self.btn.bind(on_release=self.on_button_release)
        
        layout.add_widget(self.btn)
        
        return layout

    def on_button_press(self, instance):
        self.status_label.text = "Escuchando... (Detectado toque)"
        self.status_label.color = get_color_from_hex('#f38ba8') # Rojo pastel
        instance.background_color = get_color_from_hex('#f38ba8') # Botón rojo
        instance.text = "GRABANDO..."

    def on_button_release(self, instance):
        self.status_label.text = "Procesando respuesta..."
        self.status_label.color = get_color_from_hex('#89b4fa') # Azul
        instance.background_color = get_color_from_hex('#a6e3a1') # Botón verde
        instance.text = "PULSA PARA HABLAR"

if __name__ == '__main__':
    TontoSpikeApp().run()
