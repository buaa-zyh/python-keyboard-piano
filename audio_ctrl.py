from utilize import *
from wave_gen import generate_wave
import numpy as np
import time
from pynput import keyboard

def audio_callback(outdata, frames, time, status):
    outdata.fill(0)
    with shared.lock:
        instrument = shared.instrument
        mode = shared.mode
        notes_to_play = shared.current_notes.copy()
        auto_note = shared.auto_note

    if mode == "auto" and auto_note:
        freq = NOTE_FREQS[auto_note]
        wave = generate_wave(freq, frames / SAMPLE_RATE, instrument)
        outdata[:, 0] += wave[:frames]
        combined_wave = wave[:frames]
    elif notes_to_play:
        combined_wave = np.zeros(frames)
        for note in notes_to_play:
            freq = NOTE_FREQS[note]
            wave = generate_wave(freq, frames / SAMPLE_RATE, instrument)
            combined_wave += wave[:frames]
            outdata[:, 0] += wave[:frames]
    else:
        combined_wave = np.zeros(frames)

    fft = np.abs(np.fft.rfft(combined_wave))
    freqs = np.fft.rfftfreq(frames, 1 / SAMPLE_RATE)
    with shared.lock:
        if np.max(fft) > 0:
            shared.spectrum = (freqs, fft / np.max(fft))
        else:
            shared.spectrum = (freqs, fft)

def auto_play(song_name):
    with open(f"songs/{song_name}.txt") as f:
        lines = f.readlines()

    beat_base = 60.0 / BPM  # The number of seconds per shot
    note_on_ratio = 0.8     # The proportion of each note's sound to the beat

    shared.auto_playing = True

    for line in lines:
        entries = line.strip().split()
        for entry in entries:
            # === Analyze notes (beats) ===
            if "(" in entry and ")" in entry:
                note_part, beat_part = entry.split("(")
                beat_count = float(beat_part.strip(")"))
                note = note_part.strip()
            else:
                # If the number of shots is not specified, default is 1
                note = entry.strip()
                beat_count = 1.0

            duration = beat_base * beat_count
            note_on_time = duration * note_on_ratio
            rest_time = duration * (1 - note_on_ratio)

            # === Set the current note ===
            with shared.lock:
                if note == "-":
                    shared.auto_note = None
                else:
                    shared.auto_note = note

            time.sleep(note_on_time)

            # === Add gap ===
            with shared.lock:
                shared.auto_note = None

            if rest_time > 0:
                time.sleep(rest_time)

    # Clean up
    with shared.lock:
        shared.auto_note = None

    shared.auto_playing = False

def on_press(key):
    if shared.mode != "play":
        return
    try:
        key_char = key.char.lower()
        if key_char in KEY_TO_NOTE:
            with shared.lock:
                shared.current_notes.add(KEY_TO_NOTE[key_char])
    except AttributeError:
        pass

def on_release(key):
    if shared.mode != "play":
        return
    if key == keyboard.Key.esc:
        return False
    try:
        key_char = key.char.lower()
        if key_char in KEY_TO_NOTE:
            with shared.lock:
                shared.current_notes.discard(KEY_TO_NOTE[key_char])
    except AttributeError:
        pass