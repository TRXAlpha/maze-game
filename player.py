import pygame
import random

class Player:
    def __init__(self, width, height, is_bot=False, difficulty='easy'):
        self.rect = pygame.Rect(0, 0, width, height)
        self.color = (0, 0, 255) if not is_bot else (255, 0, 0)
        self.speed = 2
        self.is_bot = is_bot
        self.difficulty = difficulty

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def bot_move(self, goal_cell, grid_cells, tile):
        if self.difficulty == 'easy':
            self.easy_bot_move(grid_cells, tile)
        elif self.difficulty == 'medium':
            self.medium_bot_move(goal_cell, grid_cells, tile)
        elif self.difficulty == 'hard':
            self.hard_bot_move(goal_cell, grid_cells, tile)

    def easy_bot_move(self, grid_cells, tile):
        # Randomly choose a direction to move in
        self.rect.x += random.choice([-self.speed, 0, self.speed])
        self.rect.y += random.choice([-self.speed, 0, self.speed])

        # Keep the bot within the maze boundaries
        self.rect.x = max(0, min(self.rect.x, tile * len(grid_cells[0]) - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, tile * len(grid_cells) - self.rect.height))

    def medium_bot_move(self, goal_cell, grid_cells, tile):
        # Basic pathfinding logic to move towards the goal
        if self.rect.x < goal_cell.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > goal_cell.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < goal_cell.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > goal_cell.rect.y:
            self.rect.y -= self.speed

        # Keep the bot within the maze boundaries
        self.rect.x = max(0, min(self.rect.x, tile * len(grid_cells[0]) - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, tile * len(grid_cells) - self.rect.height))

    def hard_bot_move(self, goal_cell, grid_cells, tile):
        # Advanced pathfinding using A* algorithm
        start = (self.rect.x // tile, self.rect.y // tile)
        end = (goal_cell.x, goal_cell.y)
        frontier = [(start, 0)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = frontier.pop(0)
            if current[0] == end:
                break

            for next in self.get_neighbors(current[0], grid_cells):
                new_cost = cost_so_far[current[0]] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(end, next)
                    frontier.append((next, priority))
                    came_from[next] = current[0]

        if end in came_from:
            path = [end]
            while end != start:
                end = came_from[end]
                path.append(end)
            path.reverse()

            if path:
                next_step = path[0]
                self.rect.x = next_step[0] * tile + tile // 2 - self.rect.width // 2
                self.rect.y = next_step[1] * tile + tile // 2 - self.rect.height // 2

    def get_neighbors(self, cell, grid_cells):
        neighbors = []
        x, y = cell
        if x > 0 and not grid_cells[x-1][y].walls['right']:
            neighbors.append((x-1, y))
        if x < len(grid_cells) - 1 and not grid_cells[x+1][y].walls['left']:
            neighbors.append((x+1, y))
        if y > 0 and not grid_cells[x][y-1].walls['bottom']:
            neighbors.append((x, y-1))
        if y < len(grid_cells[0]) - 1 and not grid_cells[x][y+1].walls['top']:
            neighbors.append((x, y+1))
        return neighbors

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)