# ☯ Reiki Studio — Complete Healing Arts Application

A comprehensive Streamlit app for Reiki practitioners, students, and enthusiasts.

## Features

| Page | Description |
|------|-------------|
| ⏱️ Session Timer | Hand position guide with JavaScript countdown timers and bell tones |
| 📔 Chakra Journal | SVG body map, log energy levels per chakra, trend charts |
| 🎯 Attunement Tracker | Level progression, practice hours log, symbol checklist |
| 📚 Chakra Encyclopedia | Full reference for all 7 chakras (crystals, affirmations, yoga, etc.) |
| ✍️ Symbol Trainer | Interactive drawing canvas for the 4 Reiki symbols |
| 🧘 Meditation Builder | Generate personalized meditation scripts with the Five Precepts |
| 📊 Energy Diary | Daily check-ins with Reiki vs non-Reiki correlation charts |
| 👥 Client Management | Client intake, session notes, history tracking |
| 🎵 Soundscape Generator | Generate & play Solfeggio frequencies as WAV audio |
| 🌐 Distance Healing | Sacred geometry board with intention setting & timer |

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Data Storage

All data (clients, journal entries, sessions, etc.) is saved to a `reiki_data/` 
directory as JSON files. Data persists between sessions automatically.

## Requirements

- Python 3.9+
- See requirements.txt
