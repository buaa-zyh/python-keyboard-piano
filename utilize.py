import threading
import pygame

# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Piano Spectrum")
font = pygame.font.SysFont('Arial', 20)

# === Colors ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

# === Shared Data ===
class SharedData:
    def __init__(self):
        self.spectrum = None
        self.current_notes = set()
        self.lock = threading.Lock()
        self.mode = "play"
        self.instrument = "piano"
        self.auto_playing = False
        self.auto_note = None

shared = SharedData()

# === Audio Setup ===
SAMPLE_RATE = 44100
BLOCKSIZE = 2048
NOTE_FREQS = {
    'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
    'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
    'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
    'REST': 0.0
}

KEY_TO_NOTE = {
    'z': 'C3', 'x': 'D3', 'c': 'E3', 'v': 'F3', 'm': 'G3', ',': 'A3', '.': 'B3',
    'a': 'C4', 's': 'D4', 'd': 'E4', 'f': 'F4', 'j': 'G4', 'k': 'A4', 'l': 'B4',
    'q': 'C5', 'w': 'D5', 'e': 'E5', 'r': 'F5', 'u': 'G5', 'i': 'A5', 'o': 'B5'
}

BPM = 120  # Adjust here to control the speed (beats per minute)