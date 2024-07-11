# game.py

import pygame

class Game:
    def __init__(self, goal, tile, goal_image):
        self.goal = goal
        self.tile = tile
        self.goal_image = pygame.transform.scale(goal_image, (tile, tile))
        self.goal.rect = pygame.Rect(goal.x * tile, goal.y * tile, tile, tile)

    def draw(self, screen):
        screen.blit(self.goal_image, self.goal.rect.topleft)
