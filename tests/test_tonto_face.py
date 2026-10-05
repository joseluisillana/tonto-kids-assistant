"""Real Kivy widgets under the virtual display provided by tonto.sh test ui."""
import time

import pytest
from kivy.clock import Clock

from client.tonto_face import FaceState, TontoFace


@pytest.fixture
def face():
    widget = TontoFace()
    yield widget
    widget._cancel_events()


def test_face_state_constants():
    states = {key: value for key, value in vars(FaceState).items() if key.isupper()}
    assert states == {
        "IDLE": "idle", "LISTENING": "listening", "THINKING": "thinking",
        "SPEAKING": "speaking", "ERROR": "error",
    }


def test_initial_state_is_idle(face):
    assert face.current_state == FaceState.IDLE
    assert face._blink_event is not None
    assert len(face.canvas.children) > 0


@pytest.mark.parametrize("state", ["idle", "listening", "thinking", "speaking", "error"])
def test_set_state_changes_current_state(face, state):
    face.set_state(state)
    assert face.current_state == state


def test_set_state_idle_replaces_blink_event(face):
    previous = face._blink_event
    face.set_state(FaceState.IDLE)
    assert face.current_state == FaceState.IDLE
    assert not previous.is_triggered
    assert face._blink_event is not previous
    assert face._blink_event.is_triggered


@pytest.mark.parametrize("state,properties", [
    (FaceState.ERROR, {"eyebrow_angle": 40, "mouth_height": -50}),
    (FaceState.SPEAKING, {"mouth_oval_opacity": 1, "mouth_line_opacity": 0}),
])
def test_state_animation_reaches_target(face, state, properties):
    face.set_state(state)
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        Clock.tick()
        if all(getattr(face, key) == pytest.approx(value) for key, value in properties.items()):
            break
    for key, value in properties.items():
        assert getattr(face, key) == pytest.approx(value)


def test_leaving_speaking_cancels_pulse(face):
    face.set_state(FaceState.SPEAKING)
    previous = face._speak_event
    face.set_state(FaceState.LISTENING)
    assert face._speak_event is None
    assert not previous.is_triggered
