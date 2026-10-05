import os
import threading
import tempfile
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle

from client.tonto_face import TontoFace, FaceState
from client.main import capture_audio, send_audio, speak, send_message

Window.size = (800, 480)
# En Raspberry Pi Lite (headless), forzamos el provider sdl2 y aceleración
if 'KIVY_WINDOW' not in os.environ:
    os.environ['KIVY_WINDOW'] = 'sdl2'
if 'KIVY_GL_BACKEND' not in os.environ:
    os.environ['KIVY_GL_BACKEND'] = 'gl'

class ProgressButton(Button):
    progress = NumericProperty(0)
    bg_color = ListProperty([1, 1, 1, 1])
    bar_color = ListProperty([0, 0, 0, 0.2])
    
    def __init__(self, **kwargs):
        if 'bg_color' in kwargs:
            self.bg_color = kwargs.pop('bg_color')
        if 'bar_color' in kwargs:
            self.bar_color = kwargs.pop('bar_color')
            
        kwargs['background_color'] = [0, 0, 0, 0] # Make default background transparent
        kwargs['background_normal'] = ''
        super().__init__(**kwargs)
        
        self.bind(pos=self.update_canvas, size=self.update_canvas, progress=self.update_canvas, bg_color=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
            if self.progress > 0:
                Color(*self.bar_color)
                w = self.width * self.progress
                RoundedRectangle(pos=self.pos, size=(w, self.height), radius=[15])

class TontoTouchUI(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.backend_url = os.environ.get("TONTO_BACKEND_URL", "http://127.0.0.1:8000")
        self.session_id = "touch-session-1"
        self.device_id = os.environ.get("TONTO_DEVICE_ID", "tonto-pi-touch")
        self.audio_device = os.environ.get("TONTO_AUDIO_DEVICE")
        self.wav_path = os.environ.get("TONTO_AUDIO_PATH", os.path.join(tempfile.gettempdir(), "tonto-touch.wav"))
        try:
            self.record_seconds = int(os.environ.get("TONTO_RECORD_SECONDS", "6"))
        except ValueError:
            self.record_seconds = 6

        # 1. Face Widget taking full screen but drawing face higher up
        self.face = TontoFace(size_hint=(1, 1))
        self.face.face_offset_y = 60 # Shift up slightly to make room for bottom button
        self.add_widget(self.face)

        # 2. Main Talk Button (floating at bottom)
        self.btn_talk = ProgressButton(
            text="TOCA PARA HABLAR",
            font_size='28sp',
            size_hint=(0.8, 0.15),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            bg_color=get_color_from_hex('#a6e3a1'),
            color=get_color_from_hex('#1e1e2e'),
            bold=True
        )
        self.btn_talk.bind(on_release=self.on_talk_press)
        self.add_widget(self.btn_talk)

        # 3. Toggle Text Mode Button (top right)
        self.btn_toggle_text = Button(
            text="MODO TEXTO",
            size_hint=(0.25, 0.08),
            pos_hint={'right': 0.95, 'top': 0.95},
            background_normal='',
            background_color=get_color_from_hex('#585b70')
        )
        self.btn_toggle_text.bind(on_release=self.toggle_text_mode)
        self.add_widget(self.btn_toggle_text)

        # 4. Text Mode Panel (bottom half, offscreen initially)
        self.text_panel = BoxLayout(
            orientation='vertical', padding=10, spacing=10,
            size_hint=(0.9, 0.45), pos_hint={'center_x': 2.0, 'y': 0.05} # offscreen to prevent touch block
        )
        self.text_panel.opacity = 0
        
        self.transcript_label = Label(text="", font_size='18sp', color=[1,1,1,1], text_size=(700, None), halign='center', valign='bottom')
        self.response_label = Label(text="", font_size='20sp', color=[1,1,1,1], text_size=(700, None), halign='center', valign='top', bold=True)
        
        self.text_input = TextInput(size_hint=(1, 0.4), multiline=False, font_size='22sp', hint_text="Escribe aquí y presiona Enter...")
        self.text_input.bind(on_text_validate=self.on_text_submit)
        
        self.text_panel.add_widget(self.transcript_label)
        self.text_panel.add_widget(self.response_label)
        self.text_panel.add_widget(self.text_input)
        
        self.add_widget(self.text_panel)
        
        self.text_mode_active = False

    def toggle_text_mode(self, instance):
        self.text_mode_active = not self.text_mode_active
        if self.text_mode_active:
            self.text_panel.opacity = 1
            self.text_panel.pos_hint = {'center_x': 0.5, 'y': 0.05} # bring onscreen
            
            self.btn_talk.opacity = 0
            self.btn_talk.pos_hint = {'center_x': 2.0, 'y': 0.05} # push offscreen
            
            self.btn_toggle_text.text = "OCULTAR TEXTO"
            
            # Shrink and move face up to make room for text
            Animation(face_offset_y=120, face_scale=0.65, d=0.3, t='out_quad').start(self.face)
        else:
            self.text_panel.opacity = 0
            self.text_panel.pos_hint = {'center_x': 2.0, 'y': 0.05} # push offscreen
            
            self.btn_talk.opacity = 1
            self.btn_talk.pos_hint = {'center_x': 0.5, 'y': 0.05} # bring onscreen
            
            self.btn_toggle_text.text = "MODO TEXTO"
            
            # Restore face
            Animation(face_offset_y=60, face_scale=1.0, d=0.3, t='out_quad').start(self.face)

    def on_talk_press(self, instance):
        if self.face.current_state != FaceState.IDLE:
            return 
            
        self.face.set_state(FaceState.LISTENING)
        self.btn_talk.text = "ESCUCHANDO..."
        self.btn_talk.bg_color = get_color_from_hex('#f38ba8') 
        self.transcript_label.text = "Grabando..."
        self.response_label.text = ""
        
        # Start progress bar animation for the recording duration
        self.btn_talk.progress = 0
        Animation(progress=1.0, d=self.record_seconds).start(self.btn_talk)
        
        threading.Thread(target=self.voice_pipeline_thread, daemon=True).start()

    def on_text_submit(self, instance):
        text = self.text_input.text.strip()
        if not text or self.face.current_state != FaceState.IDLE:
            return
            
        self.text_input.text = ""
        self.face.set_state(FaceState.THINKING)
        self.transcript_label.text = f"Tú: {text}"
        self.response_label.text = "Pensando..."
        
        threading.Thread(target=self.text_pipeline_thread, args=(text,), daemon=True).start()

    def voice_pipeline_thread(self):
        wav_bytes = capture_audio(self.audio_device, self.record_seconds, self.wav_path, show_progress=False)
        
        if not wav_bytes:
            # Simulate thinking and error for visual testing if mic fails on Windows
            self.set_thinking_state()
            import time
            time.sleep(1.5)
            self.on_pipeline_error("Micrófono no detectado.\n(Usa el modo texto para ver todas las animaciones)")
            return
            
        self.set_thinking_state()
        audio_url = f"{self.backend_url.rstrip('/')}/chat/audio"
        audio_response = send_audio(audio_url, self.session_id, self.device_id, wav_bytes, self.record_seconds * 1000)
        
        if not audio_response:
            self.on_pipeline_error("Error de conexión con el backend")
            return
            
        self.on_pipeline_success(audio_response["transcript"], audio_response["response"])

    def text_pipeline_thread(self, text):
        chat_url = f"{self.backend_url.rstrip('/')}/chat"
        response_text = send_message(chat_url, self.session_id, text)
        
        if not response_text:
            self.on_pipeline_error("Error de backend")
            return
            
        self.on_pipeline_success(text, response_text)

    @mainthread
    def set_thinking_state(self):
        Animation.cancel_all(self.btn_talk, 'progress')
        self.btn_talk.progress = 0
        self.face.set_state(FaceState.THINKING)
        self.btn_talk.text = "PENSANDO..."
        self.btn_talk.bg_color = get_color_from_hex('#89b4fa')
        self.transcript_label.text = "Procesando..."

    @mainthread
    def on_pipeline_error(self, error_msg):
        Animation.cancel_all(self.btn_talk, 'progress')
        self.btn_talk.progress = 0
        self.face.set_state(FaceState.ERROR)
        self.btn_talk.text = "ERROR. TOCA PARA REINTENTAR"
        self.btn_talk.bg_color = get_color_from_hex('#f38ba8')
        self.response_label.text = error_msg
        
        threading.Thread(target=self.delayed_reset, args=(4,), daemon=True).start()

    @mainthread
    def on_pipeline_success(self, transcript, response):
        Animation.cancel_all(self.btn_talk, 'progress')
        self.btn_talk.progress = 0
        self.transcript_label.text = f"Tú: {transcript}"
        self.response_label.text = response
        
        self.face.set_state(FaceState.SPEAKING)
        self.btn_talk.text = "HABLANDO..."
        self.btn_talk.bg_color = get_color_from_hex('#f9e2af')
        
        threading.Thread(target=self.speak_thread, args=(response,), daemon=True).start()

    def speak_thread(self, text):
        speak(text)
        self.on_speak_finished()

    @mainthread
    def on_speak_finished(self):
        Animation.cancel_all(self.btn_talk, 'progress')
        self.btn_talk.progress = 0
        self.face.set_state(FaceState.IDLE)
        self.btn_talk.text = "TOCA PARA HABLAR"
        self.btn_talk.bg_color = get_color_from_hex('#a6e3a1')

    def delayed_reset(self, delay):
        import time
        time.sleep(delay)
        self.on_speak_finished()

class TontoTouchApp(App):
    def build(self):
        return TontoTouchUI()

if __name__ == '__main__':
    TontoTouchApp().run()
