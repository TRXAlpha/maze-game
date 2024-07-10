import pygame

class Game:
    def __init__(self, goal_cell, tile):
        self.goal_cell = goal_cell
        self.tile = tile

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

# Note: Ensure that the pygame.display.flip() or pygame.display.update() is called after drawing everything on the screen, including the game over message, to actually update the display.