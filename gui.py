from utilize import *
import numpy as np
import os

def draw_spectrum():
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (50, HEIGHT - 100), (WIDTH - 50, HEIGHT - 100), 2)
    pygame.draw.line(screen, WHITE, (50, 50), (50, HEIGHT - 100), 2)

    with shared.lock:
        if shared.spectrum:
            freqs, fft = shared.spectrum
            bin_width = (WIDTH - 100) / 32
            for i in range(32):
                start_freq = i * (2000 / 32)
                end_freq = (i + 1) * (2000 / 32)
                mask = (freqs >= start_freq) & (freqs < end_freq)
                avg_amp = np.mean(fft[mask]) if np.any(mask) else 0
                x = 50 + i * bin_width
                bar_height = avg_amp * (HEIGHT - 150)
                pygame.draw.rect(screen, (0, 255 - int(avg_amp * 200), 255),
                                 (x, HEIGHT - 100 - bar_height, bin_width - 2, bar_height))
    with shared.lock:
        if shared.mode == "auto":
            notes_text = f"Current Auto Note: {shared.auto_note}" if shared.auto_note else "Current Auto Note: None"
        else:
            notes_text = "Current Notes: " + " ".join(shared.current_notes) if shared.current_notes else "Current Auto Note: None"
    text = font.render(notes_text, True, RED)
    screen.blit(text, (50, 20))

    for i in range(0, 2001, 500):
        x = 50 + (i / 2000) * (WIDTH - 100)
        freq_text = font.render(f"{i}Hz", True, WHITE)
        screen.blit(freq_text, (x - 20, HEIGHT - 90))

def draw_instrument_buttons():
    instruments = ["piano", "synth", "guitar", "marimba", "flute"]
    for i, inst in enumerate(instruments):
        rect = pygame.Rect(50 + i * 150, HEIGHT - 60, 100, 30)
        color = CYAN if shared.instrument == inst else WHITE
        pygame.draw.rect(screen, color, rect)
        text = font.render(inst.capitalize(), True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 5))
    return instruments

def draw_mode_buttons():
    modes = ["Play", "Auto"]
    for i, mode in enumerate(modes):
        rect = pygame.Rect(WIDTH - 200, 50 + i * 50, 100, 40)
        color = CYAN if shared.mode == mode.lower() else WHITE
        pygame.draw.rect(screen, color, rect)
        text = font.render(mode, True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 10))
    return modes

def draw_song_buttons():
    songs = [f[:-4] for f in os.listdir("songs") if f.endswith(".txt")]
    for i, song in enumerate(songs):
        rect = pygame.Rect(WIDTH - 200, 150 + i * 50, 150, 40)
        pygame.draw.rect(screen, WHITE, rect)
        text = font.render(song, True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 10))
    return songs