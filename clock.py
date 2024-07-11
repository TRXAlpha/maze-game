# clock.py

import pygame
import time

class Clock:
    def __init__(self, screen_width, screen_height):
        self.start_time = time.time()
        self.font = pygame.font.SysFont("impact", 30)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.elapsed_time = time.time() - self.start_time

    def draw(self, screen):
        # Create a transparent white rectangle at the top of the screen
        transparent_rect = pygame.Surface((self.screen_width, 50), pygame.SRCALPHA)
        transparent_rect.fill((255, 255, 255, 128))
        screen.blit(transparent_rect, (0, 0))

        minutes, seconds = divmod(int(self.elapsed_time), 60)
        time_display = f"{minutes:02}:{seconds:02}"
        time_surface = self.font.render(time_display, True, (0, 0, 0))
        time_rect = time_surface.get_rect(center=(self.screen_width // 2, 25))
        screen.blit(time_surface, time_rect)
