import pygame
import time

class TestPlay:
    # Function to play the track using pygame
    def play_track(self,preview_url):
        pygame.mixer.init()
        pygame.mixer.music.load(preview_url)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)  # Wait until the track finishes playing