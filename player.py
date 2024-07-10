import pygame
import random
class Player:
    def __init__(self, width, height, is_bot=False, difficulty='easy'):
        self.rect = pygame.Rect(0, 0, width, height)
        self.color = (0, 0, 255) if not is_bot else (255, 0, 0)
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 2
        self.is_bot = is_bot
        self.difficulty = difficulty

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, tile, grid_cells, thickness):
        if self.left_pressed:
            self.rect.x -= self.speed
        if self.right_pressed:
            self.rect.x += self.speed
        if self.up_pressed:
            self.rect.y -= self.speed
        if self.down_pressed:
            self.rect.y += self.speed

        self.rect.x = max(thickness, min(self.rect.x, tile * len(grid_cells[0]) - thickness - self.rect.width))
        self.rect.y = max(thickness, min(self.rect.y, tile * len(grid_cells) - thickness - self.rect.height))

    def check_move(self, tile, grid_cells, thickness):
        # Implement collision detection and response here
        pass

    def bot_move(self, goal_cell, grid_cells, tile):
        if self.difficulty == 'easy':
            self.random_move()
        elif self.difficulty == 'medium':
            self.pathfinding_move(goal_cell, grid_cells, tile)
        elif self.difficulty == 'hard':
            self.advanced_pathfinding_move(goal_cell, grid_cells, tile)

    def random_move(self):
        # Randomly choose a direction to move in
        self.rect.x += random.choice([-self.speed, self.speed])
        self.rect.y += random.choice([-self.speed, self.speed])

    def pathfinding_move(self, goal_cell, grid_cells, tile):
        # Basic pathfinding logic to move towards the goal
        if self.rect.x < goal_cell.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > goal_cell.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < goal_cell.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > goal_cell.rect.y:
            self.rect.y -= self.speed

    def advanced_pathfinding_move(self, goal_cell, grid_cells, tile):
        # More advanced pathfinding (like A* or Dijkstra)
        pass
