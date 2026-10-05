from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, SmoothLine, Ellipse, Rectangle, PushMatrix, PopMatrix, Translate, Scale
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, StringProperty
from kivy.animation import Animation
from kivy.clock import Clock
import random

class FaceState:
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    ERROR = "error"

class TontoFace(Widget):
    # Colors
    bg_color = ListProperty([0.05, 0.75, 0.85, 1])  # Cyan
    line_color = ListProperty([1, 1, 1, 1])         # White

    # Eyes (Pill shaped = RoundedRectangle)
    eye_width = NumericProperty(40)
    eye_height = NumericProperty(140)
    eye_spacing = NumericProperty(120)
    eye_offset_x = NumericProperty(0)
    eye_offset_y = NumericProperty(0)
    
    left_eye_scale_y = NumericProperty(1.0)
    right_eye_scale_y = NumericProperty(1.0)
    left_eye_scale_x = NumericProperty(1.0)
    right_eye_scale_x = NumericProperty(1.0)
    
    # Eyebrow offsets
    left_eyebrow_offset_y = NumericProperty(0)
    right_eyebrow_offset_y = NumericProperty(0)
    eyebrow_angle = NumericProperty(0) # >0 means inner part goes down, <0 means outer part goes down
    
    # Mouth
    mouth_width = NumericProperty(200)
    mouth_height = NumericProperty(40) # Used for curve depth
    mouth_offset_y = NumericProperty(-100)
    mouth_oval_opacity = NumericProperty(0) # 1 when speaking
    mouth_line_opacity = NumericProperty(1) # 1 when not speaking
    
    face_scale = NumericProperty(1.0)
    face_offset_y = NumericProperty(0)
    
    current_state = StringProperty(FaceState.IDLE)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
        # Bind all animatable properties to update_canvas
        props_to_bind = [
            'bg_color', 'line_color', 'eye_width', 'eye_height', 'eye_spacing',
            'eye_offset_x', 'eye_offset_y', 'left_eye_scale_y', 'right_eye_scale_y',
            'left_eye_scale_x', 'right_eye_scale_x', 'left_eyebrow_offset_y', 'right_eyebrow_offset_y',
            'eyebrow_angle', 'mouth_width', 'mouth_height', 'mouth_offset_y', 
            'mouth_oval_opacity', 'mouth_line_opacity', 'face_scale', 'face_offset_y'
        ]
        for prop in props_to_bind:
            self.bind(**{prop: self.update_canvas})
            
        self._blink_event = None
        self._speak_event = None
        self._think_event = None
        
        # Initial draw
        self.update_canvas()
        self.set_state(FaceState.IDLE)

    def update_canvas(self, *args):
        self.canvas.clear()
        cx = self.center_x
        cy = self.center_y + self.face_offset_y
        
        with self.canvas:
            # Background
            Color(*self.bg_color)
            Rectangle(pos=self.pos, size=self.size)
            
            PushMatrix()
            Translate(cx, cy)
            Scale(self.face_scale, self.face_scale, 1)
            Translate(-cx, -cy)
            
            # Eyes
            Color(*self.line_color)
            
            # Left Eye
            lex = cx - self.eye_spacing/2 - self.eye_width/2 + self.eye_offset_x
            ley = cy - self.eye_height/2 + self.eye_offset_y
            lew = self.eye_width * self.left_eye_scale_x
            leh = self.eye_height * self.left_eye_scale_y
            RoundedRectangle(pos=(lex, ley), size=(lew, leh), radius=[lew/2])
            
            # Right Eye
            rex = cx + self.eye_spacing/2 - self.eye_width/2 + self.eye_offset_x
            rey = cy - self.eye_height/2 + self.eye_offset_y
            rew = self.eye_width * self.right_eye_scale_x
            reh = self.eye_height * self.right_eye_scale_y
            RoundedRectangle(pos=(rex, rey), size=(rew, reh), radius=[rew/2])
            
            # Eyebrows
            eb_base_y = cy + self.eye_height/2 + 40
            eb_w = 60
            
            # Left eyebrow
            l_y = eb_base_y + self.left_eyebrow_offset_y
            l_inner_y = l_y - self.eyebrow_angle
            l_outer_y = l_y + self.eyebrow_angle
            SmoothLine(bezier=[
                cx - self.eye_spacing/2 - eb_w/2, l_outer_y,
                cx - self.eye_spacing/2, l_outer_y + 20, 
                cx - self.eye_spacing/2 + eb_w/2, l_inner_y
            ], width=8, cap='round')
            
            # Right eyebrow
            r_y = eb_base_y + self.right_eyebrow_offset_y
            r_inner_y = r_y - self.eyebrow_angle
            r_outer_y = r_y + self.eyebrow_angle
            SmoothLine(bezier=[
                cx + self.eye_spacing/2 - eb_w/2, r_inner_y,
                cx + self.eye_spacing/2, r_outer_y + 20,
                cx + self.eye_spacing/2 + eb_w/2, r_outer_y
            ], width=8, cap='round')
            
            # Mouth (Line)
            Color(self.line_color[0], self.line_color[1], self.line_color[2], self.mouth_line_opacity)
            my = cy + self.mouth_offset_y
            SmoothLine(bezier=[
                cx - self.mouth_width/2, my + 20,
                cx - self.mouth_width/4, my - self.mouth_height,
                cx + self.mouth_width/4, my - self.mouth_height,
                cx + self.mouth_width/2, my + 20
            ], width=10, cap='round')
            
            # Mouth (Oval for speaking)
            if self.mouth_oval_opacity > 0:
                Color(self.line_color[0], self.line_color[1], self.line_color[2], self.mouth_oval_opacity)
                oval_w = self.mouth_width * 0.6
                oval_h = max(20.0, self.mouth_height * 2)
                Ellipse(pos=(cx - oval_w/2, my - oval_h/2), size=(oval_w, oval_h))
                
            PopMatrix()

    def _cancel_events(self):
        if self._blink_event:
            self._blink_event.cancel()
            self._blink_event = None
        if self._speak_event:
            self._speak_event.cancel()
            self._speak_event = None
        if self._think_event:
            self._think_event.cancel()
            self._think_event = None
        Animation.cancel_all(self)

    def set_state(self, state):
        if self.current_state == state and state != FaceState.IDLE:
            return
        
        self.current_state = state
        self._cancel_events()
        
        # Base reset for all states (default is IDLE)
        anim = Animation(
            eye_width=40, eye_height=140, eye_spacing=120,
            eye_offset_x=0, eye_offset_y=0,
            left_eye_scale_y=1, right_eye_scale_y=1,
            left_eye_scale_x=1, right_eye_scale_x=1,
            left_eyebrow_offset_y=0, right_eyebrow_offset_y=0, eyebrow_angle=0,
            mouth_width=200, mouth_height=40, mouth_offset_y=-100,
            mouth_line_opacity=1, mouth_oval_opacity=0,
            # We keep the unified cyan background everywhere as requested
            bg_color=[0.05, 0.75, 0.85, 1],
            d=0.3, t='out_quad'
        )
        
        if state == FaceState.IDLE:
            self._schedule_blink()
            
        elif state == FaceState.LISTENING:
            anim &= Animation(
                eye_width=45, eye_height=145,
                left_eyebrow_offset_y=15, right_eyebrow_offset_y=15, 
                mouth_height=20,
                d=0.3
            )
            
        elif state == FaceState.THINKING:
            anim &= Animation(
                mouth_height=0, mouth_width=100,
                right_eyebrow_offset_y=25,
                left_eyebrow_offset_y=5,
                d=0.3
            )
            anim.bind(on_complete=self._start_think_loop)
            
        elif state == FaceState.SPEAKING:
            anim &= Animation(
                mouth_line_opacity=0, mouth_oval_opacity=1,
                mouth_width=120, mouth_height=40,
                left_eyebrow_offset_y=10, right_eyebrow_offset_y=10,
                d=0.2
            )
            self._schedule_speak_pulse()
            
        elif state == FaceState.ERROR:
            # We use the X logic visually by making eyes very small and angled
            # But since it's hard to rotate rounded rectangles easily without PushMatrix, 
            # we make them smaller and slant the eyebrows sharply downwards
            anim &= Animation(
                eye_height=40, eye_width=20,
                eyebrow_angle=40,  # Sharp down in center
                left_eyebrow_offset_y=-20, right_eyebrow_offset_y=-20,
                mouth_height=-50,  # Frown
                mouth_width=150,
                d=0.3
            )

        anim.start(self)

    def _schedule_blink(self):
        delay = random.uniform(2.5, 6.0)
        self._blink_event = Clock.schedule_once(self._do_blink, delay)
        
    def _do_blink(self, dt):
        if self.current_state not in (FaceState.IDLE, FaceState.LISTENING):
            return
        anim = Animation(left_eye_scale_y=0.1, right_eye_scale_y=0.1, d=0.1) + \
               Animation(left_eye_scale_y=1.0, right_eye_scale_y=1.0, d=0.1)
        anim.bind(on_complete=lambda *args: self._schedule_blink())
        anim.start(self)
        
    def _start_think_loop(self, *args):
        if self.current_state != FaceState.THINKING:
            return
        anim = Animation(eye_offset_x=25, d=0.5, t='in_out_quad') + \
               Animation(eye_offset_x=-25, d=1.0, t='in_out_quad') + \
               Animation(eye_offset_x=0, d=0.5, t='in_out_quad')
        self._think_event = Clock.schedule_once(self._start_think_loop, 2.0)
        anim.start(self)
        
    def _schedule_speak_pulse(self):
        self._speak_event = Clock.schedule_interval(self._do_speak_pulse, 0.15)
        
    def _do_speak_pulse(self, dt):
        if self.current_state != FaceState.SPEAKING:
            return False
        target_h = random.uniform(15, 60)
        Animation(mouth_height=target_h, d=0.1).start(self)
