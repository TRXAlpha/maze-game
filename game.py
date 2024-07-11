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

   
    def add_goal_point(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.goal_cell.rect)

    def is_game_over(self, players):
        for player in players:
            if self.goal_cell.rect.colliderect(player.rect):
                return True
        return False

    def message(self, screen, position, text):
        font = pygame.font.SysFont("impact", 30)
        message_surface = font.render(text, True, pygame.Color("cyan"))
        screen.blit(message_surface, position)

