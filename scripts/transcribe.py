#!/usr/bin/env python3
"""
Basic Pitch Audio-to-MIDI Transcriber (Local & DAW Modes)
Powered by Spotify's Basic Pitch and pretty_midi.

Features:
- Local Mode: High-precision polyphonic or monophonic MIDI export.
- DAW Mode: Prepares and injects MIDI clips for Ableton Live.
- Expressive pitch bend controls (scaling, smoothing, removal).
"""

import os
import sys
import warnings
import logging
import json
import socket
import argparse
import importlib.util
import subprocess
from pathlib import Path

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

BASIC_PITCH_PYTHON = r"C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe"

# Auto re-exec in dedicated uv environment if needed
if not importlib.util.find_spec("basic_pitch"):
    if os.path.exists(BASIC_PITCH_PYTHON) and sys.executable.lower() != BASIC_PITCH_PYTHON.lower():
        result = subprocess.run([BASIC_PITCH_PYTHON] + sys.argv)
        sys.exit(result.returncode)

import numpy as np
import pretty_midi
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH


def clean_monophonic(instrument: pretty_midi.Instrument) -> None:
    if not instrument.notes:
        return
    notes = sorted(instrument.notes, key=lambda n: (n.start, n.pitch))
    cleaned = []
    for i in range(len(notes)):
        curr_note = notes[i]
        if i + 1 < len(notes):
            next_note = notes[i + 1]
            if curr_note.end > next_note.start:
                curr_note.end = max(curr_note.start + 0.05, next_note.start - 0.005)
        if curr_note.end > curr_note.start + 0.02:
            cleaned.append(curr_note)
    instrument.notes = cleaned


def smooth_bends(instrument: pretty_midi.Instrument, window_size: int = 5) -> None:
    if len(instrument.pitch_bends) < window_size:
        return
    bends = sorted(instrument.pitch_bends, key=lambda pb: pb.time)
    values = [pb.pitch for pb in bends]
    half = window_size // 2
    smoothed = []
    for i in range(len(values)):
        start_idx = max(0, i - half)
        end_idx = min(len(values), i + half + 1)
        smoothed.append(int(sum(values[start_idx:end_idx]) / (end_idx - start_idx)))
    for i, pb in enumerate(bends):
        pb.pitch = smoothed[i]
    instrument.pitch_bends = bends


def scale_bends(instrument: pretty_midi.Instrument, scale: float = 1.0, clamp_zero: bool = False) -> None:
    if clamp_zero:
        instrument.pitch_bends = []
        return
    if scale == 1.0:
        return
    for pb in instrument.pitch_bends:
        new_val = int(pb.pitch * scale)
        pb.pitch = max(-8192, min(8191, new_val))


def send_osc_message(host: str, port: int, address: str, args: list) -> bool:
    """Send OSC packet over UDP if an OSC bridge is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)
        # Construct simple OSC packet
        def osc_pad(b):
            return b + b'\x00' * ((4 - (len(b) % 4)) % 4)
        
        msg = osc_pad(address.encode('utf-8'))
        tags = ',' + ''.join(['s' if isinstance(a, str) else 'i' if isinstance(a, int) else 'f' for a in args])
        msg += osc_pad(tags.encode('utf-8'))
        for a in args:
            if isinstance(a, str):
                msg += osc_pad(a.encode('utf-8'))
            elif isinstance(a, int):
                import struct
                msg += struct.pack('>i', a)
            elif isinstance(a, float):
                import struct
                msg += struct.pack('>f', a)
        sock.sendto(msg, (host, port))
        sock.close()
        return True
    except Exception:
        return False


def run_transcription(
    audio_path: str,
    output_midi_path: str = None,
    mode: str = "local",
    onset_threshold: float = 0.5,
    frame_threshold: float = 0.3,
    min_note_length: float = 120.0,
    min_frequency: float = None,
    max_frequency: float = None,
    monophonic: bool = False,
    multiple_pitch_bends: bool = False,
    smooth_pitch_bends: bool = False,
    scale_bends_factor: float = 1.0,
    no_bends: bool = False,
    daw_track_name: str = None
) -> dict:
    audio_file = Path(audio_path).resolve()
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    if output_midi_path is None:
        output_midi_path = audio_file.with_name(f"{audio_file.stem}_basic_pitch.mid")
    else:
        output_midi_path = Path(output_midi_path).resolve()

    output_midi_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n[*] Basic Pitch Transcribing: {audio_file.name}")
    print(f"    Mode: {mode.upper()}")
    print(f"    Thresholds: Onset={onset_threshold}, Frame={frame_threshold}, MinLen={min_note_length}ms")

    model_output, midi_data, note_events = predict(
        audio_path=str(audio_file),
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=min_note_length,
        minimum_frequency=min_frequency,
        maximum_frequency=max_frequency,
        multiple_pitch_bends=multiple_pitch_bends,
        melodia_trick=True
    )

    for inst in midi_data.instruments:
        if monophonic:
            clean_monophonic(inst)
        if no_bends:
            scale_bends(inst, clamp_zero=True)
        else:
            if smooth_pitch_bends:
                smooth_bends(inst, window_size=5)
            if scale_bends_factor != 1.0:
                scale_bends(inst, scale=scale_bends_factor)

    midi_data.write(str(output_midi_path))
    total_notes = sum(len(i.notes) for i in midi_data.instruments)
    print(f"[+] Exported MIDI to: {output_midi_path} ({total_notes} notes)")

    result = {
        "audio_path": str(audio_file),
        "midi_path": str(output_midi_path),
        "total_notes": total_notes,
        "mode": mode
    }

    if mode.lower() in ("daw", "ableton"):
        track_name = daw_track_name or f"BP - {audio_file.stem}"
        # Copy to Ableton Live Actions / User Library inbox if path exists
        user_lib_samples = Path("C:/Users/<you>/Documents/Ableton/User Library/Samples/Basic Pitch")
        try:
            user_lib_samples.mkdir(parents=True, exist_ok=True)
            copied_midi = user_lib_samples / output_midi_path.name
            import shutil
            shutil.copy2(output_midi_path, copied_midi)
            print(f"[DAW] Copied to Ableton User Library: {copied_midi}")
            result["user_library_midi"] = str(copied_midi)
        except Exception:
            pass

        # Attempt OSC notification to Ableton bridge (port 11925 / 11924)
        osc_sent = send_osc_message("127.0.0.1", 11925, "/live/clip/new", [str(output_midi_path), track_name])
        result["osc_notified"] = osc_sent
        print(f"[DAW] Ableton track target: '{track_name}' (Drag & drop or import {output_midi_path.name})")

    return result


def main():
    parser = argparse.ArgumentParser(description="Basic Pitch Audio-to-MIDI Transcriber (Local & DAW)")
    parser.add_argument("audio_path", help="Path to input audio file")
    parser.add_argument("--output", "-o", help="Path to output .mid file")
    parser.add_argument("--mode", choices=["local", "daw", "ableton"], default="local",
                        help="Operation mode: 'local' saves file; 'daw'/'ableton' prepares for Ableton Live")
    parser.add_argument("--onset", type=float, default=0.5, help="Onset likelihood threshold (0.0 - 1.0)")
    parser.add_argument("--frame", type=float, default=0.3, help="Frame sustain threshold (0.0 - 1.0)")
    parser.add_argument("--min-len", type=float, default=120.0, help="Minimum note length in milliseconds")
    parser.add_argument("--min-freq", type=float, default=None, help="Minimum note frequency in Hz")
    parser.add_argument("--max-freq", type=float, default=None, help="Maximum note frequency in Hz")
    parser.add_argument("--monophonic", action="store_true", help="Enforce monophonic single-voice melody")
    parser.add_argument("--multi-bends", action="store_true", help="Allow overlapping notes to have pitch bends")
    parser.add_argument("--smooth-bends", action="store_true", help="Smooth rapid pitch bend tremors/vibrato")
    parser.add_argument("--scale-bends", type=float, default=1.0, help="Scale pitch bend range factor")
    parser.add_argument("--no-bends", action="store_true", help="Strip pitch bend events completely")
    parser.add_argument("--track-name", help="Custom track name for DAW mode")

    args = parser.parse_args()

    res = run_transcription(
        audio_path=args.audio_path,
        output_midi_path=args.output,
        mode=args.mode,
        onset_threshold=args.onset,
        frame_threshold=args.frame,
        min_note_length=args.min_len,
        min_frequency=args.min_freq,
        max_frequency=args.max_freq,
        monophonic=args.monophonic,
        multiple_pitch_bends=args.multi_bends,
        smooth_pitch_bends=args.smooth_bends,
        scale_bends_factor=args.scale_bends,
        no_bends=args.no_bends,
        daw_track_name=args.track_name
    )
    print("\n[SUCCESS] Completed:")
    print(f"  Audio: {res['audio_path']}")
    print(f"  MIDI:  {res['midi_path']}")
    print(f"  Notes: {res['total_notes']}")


if __name__ == "__main__":
    main()
