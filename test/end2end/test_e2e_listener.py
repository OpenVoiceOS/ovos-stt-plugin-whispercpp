"""
E2E listener tests for ovos-stt-plugin-whispercpp.

The tiny whisper.cpp model (~74 MB) is downloaded once on first run and cached
at ~/.local/share/pywhispercpp/models/. Subsequent runs are fully offline.

Fixture: test/fixtures/command.wav — 16 kHz mono, speech "what time is it in london".
"""
import os
from pathlib import Path

import pytest

import pywhispercpp
from ovos_plugin_manager.utils.audio import AudioFile
from ovos_stt_plugin_whispercpp import WhispercppSTT
from ovoscope.listener import get_mini_listener

FIXTURE = Path(__file__).parent / "fixtures" / "command.wav"
# These tokens must appear in the transcript produced by the tiny model for
# "what time is it in london".
EXPECTED_TOKENS = {"time", "london"}


@pytest.fixture(scope="module")
def stt():
    """Real WhisperCPP STT using the tiny model (smallest available)."""
    return WhispercppSTT(config={"model": "tiny"})


# ---------------------------------------------------------------------------
# 1. Direct transcription
# ---------------------------------------------------------------------------

def test_direct_transcription(stt):
    """STT.execute() returns a non-empty transcript containing expected words."""
    with AudioFile(str(FIXTURE)) as source:
        audio = source.read()

    transcript = stt.execute(audio, language="en")

    assert isinstance(transcript, str), "execute() must return a str"
    assert transcript.strip(), "transcript must be non-empty"

    lower = transcript.lower()
    matched = [t for t in EXPECTED_TOKENS if t in lower]
    assert matched, (
        f"expected at least one of {EXPECTED_TOKENS} in transcript, got: {transcript!r}"
    )


# ---------------------------------------------------------------------------
# 2. Through the listener
# ---------------------------------------------------------------------------

def test_listener_utterance(stt):
    """MiniListener.listen() emits recognizer_loop:utterance with non-empty text."""
    listener = get_mini_listener(stt_instance=stt)
    messages = listener.listen(str(FIXTURE), language="en-us")

    utterance_msgs = [
        m for m in messages if m.msg_type == "recognizer_loop:utterance"
    ]
    assert utterance_msgs, (
        f"no recognizer_loop:utterance emitted; all messages: {[m.msg_type for m in messages]}"
    )

    utterances = utterance_msgs[0].data.get("utterances", [])
    assert utterances, "utterances list must be non-empty"
    assert utterances[0].strip(), "first utterance must not be blank"
