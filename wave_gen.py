import numpy as np
from utilize import *
from scipy.signal import butter, lfilter

def generate_wave(freq, duration, instrument="piano"):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = np.zeros_like(t)

    if freq == 0:
        return wave  # REST

    if instrument == "piano":
        # === Piano: rich harmonics + ADSR + reverb ===
        harmonics = [1, 0.5, 0.3, 0.1]
        for i, amp in enumerate(harmonics, start=1):
            wave += amp * np.sin(2 * np.pi * freq * i * t)
        wave = apply_adsr(wave, attack=0.01, decay=0.2, sustain_level=0.6, release=0.3)
        wave = add_simple_reverb(wave, delay=0.03, decay=0.1)

    elif instrument == "guitar":
        # === Guitar: bright pluck + ADSR + light reverb ===
        harmonics = [1, 0.5, 0.3]
        for i, amp in enumerate(harmonics, start=1):
            wave += amp * np.sign(np.sin(2 * np.pi * freq * i * t))
        wave = apply_adsr(wave, attack=0.005, decay=0.3, sustain_level=0.4, release=0.3)
        wave = add_simple_reverb(wave, delay=0.02, decay=0.2)
        wave = lowpass_filter(wave, cutoff=4000)

    elif instrument == "synth":
        # === Synth: smooth saw + chorus-like reverb ===
        wave = 2 * np.arcsin(np.sin(2 * np.pi * freq * t)) / np.pi  # Triangle wave
        wave = apply_adsr(wave, attack=0.01, decay=0.2, sustain_level=0.8, release=0.4)
        wave = add_simple_reverb(wave, delay=0.04, decay=0.5)

    elif instrument == "marimba":
        freqs = [1, 2.76, 5.4, 8.9]
        amps = [1, 0.4, 0.2, 0.1]
        wave = np.zeros_like(t)
        for f_mul, amp in zip(freqs, amps):
            wave += amp * np.sin(2 * np.pi * freq * f_mul * t)

        # Ultra short transient
        wave = apply_adsr(wave, attack=0.001, decay=0.8, sustain_level=0.0, release=0.05)

        # Don't have long reverb! Just a very short room feel
        wave = add_simple_reverb(wave, delay=0.005, decay=0.1)

        wave = lowpass_filter(wave, cutoff=3000)  # Wood will not have too many high-frequency spikes

        max_amp = np.max(np.abs(wave))
        if max_amp > 0:
            wave /= max_amp

    elif instrument == "flute":
        wave = np.sin(2 * np.pi * freq * t)
        wave += 0.2 * np.sin(2 * np.pi * freq * 2.01 * t)  # Non strict 2nd harmonic
        wave += 0.1 * np.sin(2 * np.pi * freq * 3.99 * t)  # Near 4th harmonic

        # Breath noise
        noise = np.random.normal(0, 0.01, len(t))
        wave += noise

        # ADSR
        wave = apply_adsr(wave, attack=0.02, decay=0.2, sustain_level=0.7, release=0.3)

        # Slight reverb
        wave = add_simple_reverb(wave, delay=0.04, decay=0.4)

        # Optional: Slightly apply high pass filtering
        wave = highpass_filter(wave, cutoff=100)   # Cut off excess whirring low frequencies
        wave = lowpass_filter(wave, cutoff=6000)  # Keep the whistle high frequency

        max_amp = np.max(np.abs(wave))
        if max_amp > 0:
            wave /= max_amp

    else:
        # Fallback: simple sine
        wave = np.sin(2 * np.pi * freq * t)

    # Normalize
    max_amp = np.max(np.abs(wave))
    if max_amp > 0:
        wave /= max_amp
    
    # Fade in/out for anti-click
    wave = apply_fade(wave, fade_time=0.02)

    return wave

def apply_adsr(wave, attack=0.02, decay=0.1, sustain_level=0.7, release=0.2):
    length = len(wave)
    adsr = np.ones(length)

    attack_samples = int(attack * length)
    decay_samples = int(decay * length)
    release_samples = int(release * length)
    sustain_samples = length - (attack_samples + decay_samples + release_samples)
    sustain_samples = max(sustain_samples, 0)  # Prevent negative numbers

    # Attack
    adsr[:attack_samples] = np.linspace(0, 1, attack_samples, endpoint=False)
    # Decay
    adsr[attack_samples:attack_samples+decay_samples] = np.linspace(1, sustain_level, decay_samples, endpoint=False)
    # Sustain
    adsr[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] = sustain_level
    # Release
    adsr[-release_samples:] = np.linspace(sustain_level, 0, release_samples)

    return wave * adsr

def add_simple_reverb(wave, delay=0.02, decay=0.2):
    delay_samples = int(delay * SAMPLE_RATE)
    if delay_samples <= 0 or delay_samples >= len(wave):
        return wave

    reverb_wave = np.zeros_like(wave)
    reverb_wave[delay_samples:] = wave[:-delay_samples]
    return wave + decay * reverb_wave

def apply_fade(wave, fade_time=0.005):
    fade_samples = int(fade_time * SAMPLE_RATE)
    if fade_samples > 0 and fade_samples * 2 < len(wave):
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        wave[:fade_samples] *= fade_in
        wave[-fade_samples:] *= fade_out
    return wave

def lowpass_filter(data, cutoff=4000, fs=SAMPLE_RATE, order=6):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

def highpass_filter(data, cutoff=80, fs=SAMPLE_RATE, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return lfilter(b, a, data)