# game.py
import pygame

class Game:
    def __init__(self, goal_cell, tile_size):
        self.goal_cell = goal_cell
        self.tile_size = tile_size

    def add_goal_point(self, screen):
        img = pygame.image.load('gate.jpeg')
        img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
        screen.blit(img, (self.goal_cell.x * self.tile_size, self.goal_cell.y * self.tile_size))

    def is_game_over(self, players):
        goal_cell_abs_x = self.goal_cell.x * self.tile_size
        goal_cell_abs_y = self.goal_cell.y * self.tile_size
        for player in players:
            if player.x >= goal_cell_abs_x and player.y >= goal_cell_abs_y:
                return True
        return False

    def message(self):
        font = pygame.font.SysFont("impact", 50)
        return font.render("You Win!", True, pygame.Color("cyan"))
