# Implementation Plan: Basic Pitch Audio-to-MIDI Transcriber

This document tracks planned, in-progress, and completed work for the **Basic Pitch Audio-to-MIDI Transcriber** skill. It persists across all version passes.

---

## Completed Work

### v1.0.0 — Initial Release (2026-09-24)
- [x] **Spotify Basic Pitch Core Pipeline (`scripts/transcribe.py`)**: Integrated `basic-pitch` neural model (`ICASSP_2022_MODEL_PATH`) and `pretty_midi` for high-precision polyphonic/monophonic audio-to-MIDI transcription. (✅ done in v1.0.0)
- [x] **Local File Mode**: Direct standard Type 1 `.mid` generation saved next to source audio or in custom output directories. (✅ done in v1.0.0)
- [x] **Ableton Live DAW Mode**: Automatic staging into Ableton Live User Library (`A:\User Library\Samples\Basic Pitch`) with optional OSC notification broadcast to Live Actions / Producer Pal bridges. (✅ done in v1.0.0)
- [x] **Pitch Bend Processing**:
  - [x] Moving-average smoothing (`--smooth-bends`) to tame acoustic pitch jitter while retaining intentional slides. (✅ done in v1.0.0)
  - [x] Pitch bend sensitivity multiplier (`--scale-bends <float>`). (✅ done in v1.0.0)
  - [x] Rigid quantization mode (`--no-bends`) to strip pitch bends entirely. (✅ done in v1.0.0)
- [x] **Monophonic Overlap Cleaning**: `--monophonic` algorithm that eliminates overlapping double-notes for clean solo melody and vocal transcription. (✅ done in v1.0.0)
- [x] **Configurable Acoustic Thresholds**: Exposes onset detection (`--onset`), frame sustain (`--frame`), minimum duration (`--min-len`), and frequency limits (`--min-freq` / `--max-freq`). (✅ done in v1.0.0)
- [x] **Transparent Runtime Delegation**: Auto-reexecutes inside the dedicated `basic-pitch` uv environment (`C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe`). (✅ done in v1.0.0)
- [x] **Tri-Platform Deployment**: Established canonical skill in `.agents/skills/basic-pitch-transcriber` with NTFS directory junctions to `.claude/skills`, `.grok/skills`, and `.gemini/config/skills`. (✅ done in v1.0.0)
- [x] **Documentation & Versioning**: Authored `SKILL.md`, standardized `HOW_TO_USE.txt`, `README.md`, and permanent `App Changes Tracker.html`. (✅ done in v1.0.0)

---

## Planned Future Work

- [ ] **Direct Max for Live Clip Insertion**: Directly place transcribed MIDI notes into the currently selected clip slot on the selected Ableton track via Producer Pal / Live API.
- [ ] **Drum / Percussion Transcribe Profile**: Optimized model parameters and pitch-to-pad mappings for acoustic and electronic drum kit transcription.
- [ ] **MPE (MIDI Polyphonic Expression) Export**: Export polyphonic pitch bends as per-note MPE pitch wheel messages.
