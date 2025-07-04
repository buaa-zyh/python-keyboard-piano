# python-keyboard-piano
A simple virtual piano built with Python, supporting real-time playing, multiple instrument synthesis, automatic song playback, and spectrum visualization using Pygame and Sounddevice.

## ✨ Features

✅ Play notes in real-time using your computer keyboard  
✅ Switch between multiple instrument sounds  
✅ Automatic playback mode: play songs written in simple `.txt` notation  
✅ Supports flexible note durations, including rests  
✅ Spectrum analysis visualization with Pygame  
✅ Pure Python, no heavy external libraries

---

## 📖 How It Works

- Uses `sounddevice` to output real-time generated waveforms  
- Synthesizes different instruments using sine waves, harmonics, envelope shaping (ADSR), reverb, and simple filters  
- Uses `pynput` to capture keyboard input for live playing  
- Uses `pygame` to display spectrum and UI buttons

---

## 📁 Folder Structure

project/
│
├── main.py # Main script
├── audio_ctrl.py # Control audio playback in two modes
├── wave_gen.py # Generate waveforms for different instruments
├── gui.py # Pygame GUI
├── utilize.py # Define constants and shared variables
├── songs/ # Folder with song files (e.g. Twinkle.txt)
│ ├── Twinkle.txt
│ └── ...
├── requirements.txt
└── README.md

---

## 🎵 Song File Format

- Store your songs in the `songs/` folder.
- Each `.txt` file should contain lines with notes and their durations:  
  Example (`Twinkle.txt`):
    
    C4(1) C4(1) G4(0.5) G4(0.5) A4(2) G4(1)
    F4(1) E4(1) D4(1) C4(1)

  `-(0.5)` means a 0.5-beat rest.

---

## ⌨️ Keyboard Controls

- Keys like `a,s,d,f` correspond to C4, D4, E4, F4, etc.  
- You can customize the key-to-note mapping in the script.
- Use on-screen buttons to switch instrument or mode (Play / Auto).

---

## 🚀 How to Run

1. Install Python 3.8+  
2. Install dependencies:  
 ```bash
 pip install -r requirements.txt
 ```
3. Run:
 ```bash
 python main.py
 ```
