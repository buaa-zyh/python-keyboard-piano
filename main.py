from utilize import *
from audio_ctrl import *
from gui import *
import sounddevice as sd
import sys

def main():
    if not os.path.exists("songs"):
        os.makedirs("songs")

    stream = sd.OutputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        blocksize=BLOCKSIZE
    )
    stream.start()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                instruments = draw_instrument_buttons()
                for i, inst in enumerate(instruments):
                    rect = pygame.Rect(50 + i * 150, HEIGHT - 60, 100, 30)
                    if rect.collidepoint(mx, my):
                        with shared.lock:
                            shared.instrument = inst
                modes = draw_mode_buttons()
                for i, mode in enumerate(modes):
                    rect = pygame.Rect(WIDTH - 200, 50 + i * 50, 100, 40)
                    if rect.collidepoint(mx, my):
                        with shared.lock:
                            shared.mode = mode.lower()
                if shared.mode == "auto" and not shared.auto_playing:
                    songs = draw_song_buttons()
                    for i, song in enumerate(songs):
                        rect = pygame.Rect(WIDTH - 200, 150 + i * 50, 150, 40)
                        if rect.collidepoint(mx, my):
                            threading.Thread(target=auto_play, args=(song,), daemon=True).start()

        draw_spectrum()
        draw_instrument_buttons()
        draw_mode_buttons()
        if shared.mode == "auto":
            draw_song_buttons()
        pygame.display.flip()
        clock.tick(30)

    listener.stop()
    stream.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    print("Virtual Piano Started! ESC to quit.")
    main()