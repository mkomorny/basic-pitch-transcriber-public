---
name: basic-pitch-transcriber
description: Polyphonic and monophonic audio-to-MIDI transcription using Spotify's Basic Pitch neural model. Supports Local File Mode (saving standalone .mid files on disk) and DAW Mode (integrating with Ableton Live via User Library, Producer Pal, or OSC). Includes pitch bend smoothing, scaling, and monophonic voice cleaning.
---

# Basic Pitch Audio-to-MIDI Transcriber (Local & DAW)

Audio-to-MIDI transcription skill using Spotify's **Basic Pitch** neural network. Works on any local audio file (`.wav`, `.mp3`, `.flac`, `.m4a`, `.aiff`, `.ogg`) and provides seamless integration with Ableton Live.

## Capabilities & Guarantees

1. **Polyphonic & Expressive Pitch Tracking**: Transcribes chords, melodic runs, and individual note velocities while capturing expressive microtonal pitch bends.
2. **Dual Operation Modes**:
   - **Local File Mode**: Creates a standard `.mid` file right in the same folder as the source audio.
   - **DAW / Ableton Mode**: Prepares the transcribed MIDI file for Ableton Live, automatically copies it to the Ableton User Library (`User Library/Samples/Basic Pitch`), and sends clip notifications to the Live Actions / Producer Pal bridge.
3. **Pitch Bend Refinement**:
   - `--smooth-bends`: Cleans jittery flutter from raw recordings while keeping musical glissandos and slides.
   - `--scale-bends <float>`: Scales pitch bend sensitivity to match your virtual instrument's pitch wheel settings.
   - `--no-bends`: Strips bends for rigid, grid-quantized MIDI notes.
4. **Monophonic Filter**: `--monophonic` eliminates overlapping double-notes for clean solo melody extraction.

---

## Command Line Usage

### Local File Mode
```bash
# Standard polyphonic transcription:
python "C:\Users\<you>\.agents\skills\basic-pitch-transcriber\scripts\transcribe.py" "C:\Music\guitar_riff.wav"

# Monophonic solo melody with smoothed pitch bends:
python "C:\Users\<you>\.agents\skills\basic-pitch-transcriber\scripts\transcribe.py" "C:\Music\solo.wav" --monophonic --smooth-bends

# Rigid quantization (no pitch bends):
python "C:\Users\<you>\.agents\skills\basic-pitch-transcriber\scripts\transcribe.py" "C:\Music\synth_loop.mp3" --no-bends
```

### DAW / Ableton Mode
```bash
# Transcribe and stage for Ableton Live:
python "C:\Users\<you>\.agents\skills\basic-pitch-transcriber\scripts\transcribe.py" "C:\Music\vocal_riff.wav" --mode daw --track-name "Vocal Lead MIDI"
```

---

## Thresholds & Parameter Reference

- `--onset <0.0-1.0>` (Default: `0.5`): Minimum likelihood for a note to begin. Increase (e.g. `0.65`) for cleaner note separation and fewer ghost notes; decrease (e.g. `0.4`) for soft or quiet passages.
- `--frame <0.0-1.0>` (Default: `0.3`): Sustain threshold. Controls how long notes ring out.
- `--min-len <ms>` (Default: `120.0`): Minimum allowed note duration in milliseconds. Filters out tiny acoustic blips.
- `--min-freq <Hz>` / `--max-freq <Hz>`: Sets pitch floor and ceiling (e.g. `--max-freq 350` for bass).
