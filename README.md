# Basic Pitch Audio-to-MIDI Transcriber

**Basic Pitch Audio-to-MIDI Transcriber** (`basic-pitch-transcriber`) is an AI skill and CLI tool powered by Spotify's Basic Pitch neural network. It transcribes any audio recording (`.wav`, `.mp3`, `.flac`, `.m4a`, `.aiff`, `.ogg`) into expressive MIDI clips, with full support for standalone file export and deep integration with Ableton Live.

---

## ⚡ Core Capabilities

- **Polyphonic & Expressive Pitch Tracking**: Transcribes complex multi-note chords, melodic runs, and individual note velocities while capturing expressive microtonal pitch bends.
- **Dual Operation Modes**:
  - **Local File Mode**: Creates a standard Type 1 `.mid` file right in the same folder as the source audio.
  - **DAW / Ableton Mode**: Automatically stages clips into the Ableton User Library (`A:\User Library\Samples\Basic Pitch`) and broadcasts OSC clip notifications to Producer Pal / Live Actions.
- **Pitch Bend Refinement**:
  - `--smooth-bends`: Moving-average smoothing eliminates acoustic jitter and flutter while retaining intentional slides and vibrato.
  - `--scale-bends <float>`: Multiplies pitch bend depth to match the pitch wheel range of target software synthesizers (e.g. Serum, Vital, Phase Plant).
  - `--no-bends`: Strips pitch bends completely for rigid, grid-quantized MIDI notes.
- **Monophonic Filter**: `--monophonic` eliminates overlapping double-notes for clean solo melody or vocal lead extraction.
- **Transparent Runtime Delegation**: Automatically calls into the dedicated `basic-pitch` uv Python environment (`C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe`).
- **Zero-Duplicate Tri-Platform Availability**: Installed canonically in `.agents/skills/basic-pitch-transcriber` and linked via NTFS junctions to Claude, Grok, and Antigravity.

---

## 🎛️ Acoustic Thresholds Reference

| Parameter | Default | Range | Description |
| :--- | :--- | :--- | :--- |
| `--onset` | `0.5` | `0.0 - 1.0` | Minimum note onset likelihood. Increase (`0.65`) for staccato plucks / fewer ghosts; decrease (`0.35`) for quiet legato. |
| `--frame` | `0.3` | `0.0 - 1.0` | Sustain threshold. Higher values cut ring-out early; lower values extend notes. |
| `--min-len` | `120.0` | Milliseconds | Minimum note duration. Rejects tiny transient artifacts. |
| `--min-freq` / `--max-freq` | None | Hz | Restricts frequency range (e.g. `--max-freq 320` for bass). |

---

## 🚀 Usage

### In Chat (Prompts & Slash Commands)

- `/basic-pitch-transcriber "C:\Music\guitar_riff.wav"`
- *"Transcribe this audio file to MIDI: 'C:\Recordings\piano_chords.mp3' --no-bends"*
- *"Convert this vocal recording to MIDI for Ableton: 'C:\Audio\vocal_lead.wav' --monophonic --smooth-bends --mode daw"*
- *"Transcribe 'D:\Samples\bassline.wav' with max frequency 300Hz and monophonic filtering."*

### Command Line Interface (`scripts/transcribe.py`)

```powershell
# Standard polyphonic transcription:
python scripts/transcribe.py "C:\Music\guitar_riff.wav"

# Monophonic solo melody with smoothed pitch bends:
python scripts/transcribe.py "C:\Music\solo.wav" --monophonic --smooth-bends

# Rigid quantization (no pitch bends):
python scripts/transcribe.py "C:\Music\synth_loop.mp3" --no-bends

# DAW / Ableton Mode staging:
python scripts/transcribe.py "C:\Music\vocal_riff.wav" --mode daw --track-name "Vocal Lead MIDI"
```

---

## 📁 Repository Structure

```
basic-pitch-transcriber/
├── SKILL.md                  # Skill trigger and platform integration instructions
├── HOW_TO_USE.txt            # Quick-reference cheat sheet & prompt guide
├── IMPLEMENTATION_PLAN.md    # Multi-version roadmap and completed tasks
├── App Changes Tracker.html  # Permanent interactive HTML version changelog
├── README.md                 # This overview
└── scripts/
    └── transcribe.py         # Spotify Basic Pitch inference & MIDI formatting engine
```

---

## 📜 Documentation & Lifecycle

- **Version History & Releases**: Tracked permanently in [App Changes Tracker.html](App%20Changes%20Tracker.html).
- **Roadmap & Completed Features**: Documented in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).
