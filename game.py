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

    def message(self, screen):
        font = pygame.font.SysFont("impact", 50)
        text_surface = font.render("Game Over!", True, (255, 0, 0))
        # Assuming you want to display the message at the center of the screen
        screen_rect = screen.get_rect()
        text_rect = text_surface.get_rect(center=screen_rect.center)
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

# Note: Ensure that the pygame.display.flip() or pygame.display.update() is called after drawing everything on the screen, including the game over message, to actually update the display.