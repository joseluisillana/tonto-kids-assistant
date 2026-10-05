"""Construct real widgets; isolate audio, HTTP and worker threads only."""
from unittest.mock import Mock

import pytest
from kivy.animation import Animation
from kivy.clock import Clock

from client import touch_ui
from client.tonto_face import FaceState


@pytest.fixture
def ui(monkeypatch):
    monkeypatch.delenv("TONTO_BACKEND_URL", raising=False)
    widget = touch_ui.TontoTouchUI()
    yield widget
    Clock.tick()
    widget.face._cancel_events()
    Animation.cancel_all(widget.btn_talk)


@pytest.fixture
def worker(monkeypatch):
    thread = Mock()
    monkeypatch.setattr(touch_ui.threading, "Thread", thread)
    return thread


def test_progress_button_constructs():
    button = touch_ui.ProgressButton()
    assert button.progress == 0
    assert button.background_color == [0, 0, 0, 0]


def test_touch_ui_constructs_with_default_backend_url(ui):
    assert ui.backend_url == "http://127.0.0.1:8000"
    assert ui.face in ui.children
    assert ui.btn_talk in ui.children
    assert ui.text_input in ui.text_panel.children
    assert ui.face.current_state == FaceState.IDLE


def test_touch_ui_reads_backend_url_from_env(ui, monkeypatch):
    monkeypatch.setenv("TONTO_BACKEND_URL", "http://test-backend:9000")
    other = touch_ui.TontoTouchUI()
    try:
        assert other.backend_url == "http://test-backend:9000"
    finally:
        other.face._cancel_events()


def test_toggle_text_mode_restores_talk_button(ui):
    ui.toggle_text_mode(None)
    assert ui.text_mode_active
    assert ui.text_panel.opacity == 1
    assert ui.btn_talk.opacity == 0
    ui.toggle_text_mode(None)
    assert not ui.text_mode_active
    assert ui.text_panel.opacity == 0
    assert ui.btn_talk.opacity == 1


def test_talk_button_starts_listening_and_worker(ui, worker):
    ui.btn_talk.dispatch("on_release")
    assert ui.face.current_state == FaceState.LISTENING
    assert ui.btn_talk.text == "ESCUCHANDO..."
    worker.assert_called_once_with(target=ui.voice_pipeline_thread, daemon=True)
    worker.return_value.start.assert_called_once()


def test_talk_press_ignored_while_busy(ui, worker):
    ui.face.set_state(FaceState.THINKING)
    ui.on_talk_press(None)
    worker.assert_not_called()


@pytest.mark.parametrize("text,state", [("   ", FaceState.IDLE), ("Hola", FaceState.SPEAKING)])
def test_text_submit_ignores_empty_or_busy(ui, worker, text, state):
    ui.text_input.text = text
    ui.face.set_state(state)
    ui.on_text_submit(None)
    worker.assert_not_called()


def test_text_submit_strips_input_and_starts_worker(ui, worker):
    ui.text_input.text = "  Hola TONTO  "
    ui.text_input.dispatch("on_text_validate")
    assert ui.text_input.text == ""
    assert ui.face.current_state == FaceState.THINKING
    assert ui.transcript_label.text == "Tú: Hola TONTO"
    worker.assert_called_once_with(target=ui.text_pipeline_thread, args=("Hola TONTO",), daemon=True)


def test_pipeline_success_speaks_and_returns_to_idle(ui, worker, monkeypatch):
    speak = Mock()
    monkeypatch.setattr(touch_ui, "speak", speak)
    ui.on_pipeline_success("Hola", "¡Hola!")
    Clock.tick()
    assert ui.face.current_state == FaceState.SPEAKING
    assert ui.response_label.text == "¡Hola!"
    worker.assert_called_once_with(target=ui.speak_thread, args=("¡Hola!",), daemon=True)
    ui.speak_thread("¡Hola!")
    Clock.tick()
    speak.assert_called_once_with("¡Hola!")
    assert ui.face.current_state == FaceState.IDLE
    assert ui.btn_talk.text == "TOCA PARA HABLAR"


def test_pipeline_error_displays_message_and_schedules_reset(ui, worker):
    ui.on_pipeline_error("Backend no disponible")
    Clock.tick()
    assert ui.face.current_state == FaceState.ERROR
    assert ui.response_label.text == "Backend no disponible"
    assert ui.btn_talk.progress == 0
    worker.assert_called_once_with(target=ui.delayed_reset, args=(4,), daemon=True)


def test_voice_pipeline_uses_audio_contract(ui, monkeypatch):
    capture = Mock(return_value=b"wav-fixture")
    send = Mock(return_value={"transcript": "Hola", "response": "¡Hola!"})
    success = Mock()
    monkeypatch.setattr(touch_ui, "capture_audio", capture)
    monkeypatch.setattr(touch_ui, "send_audio", send)
    monkeypatch.setattr(ui, "on_pipeline_success", success)
    ui.voice_pipeline_thread()
    capture.assert_called_once_with(ui.audio_device, ui.record_seconds, ui.wav_path, show_progress=False)
    send.assert_called_once_with(
        f"{ui.backend_url}/chat/audio", ui.session_id, ui.device_id,
        b"wav-fixture", ui.record_seconds * 1000,
    )
    success.assert_called_once_with("Hola", "¡Hola!")


def test_text_pipeline_reports_backend_failure(ui, monkeypatch):
    send = Mock(return_value=None)
    error = Mock()
    monkeypatch.setattr(touch_ui, "send_message", send)
    monkeypatch.setattr(ui, "on_pipeline_error", error)
    ui.text_pipeline_thread("Hola")
    send.assert_called_once_with(f"{ui.backend_url}/chat", ui.session_id, "Hola")
    error.assert_called_once_with("Error de backend")
