# player.py

import pygame
import random
class Player:
    def __init__(self, width, height, is_bot=False, difficulty='easy'):
        self.rect = pygame.Rect(0, 0, width, height)
        self.speed = 2
        self.is_bot = is_bot
        self.difficulty = difficulty

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255) if not self.is_bot else (255, 0, 0), self.rect)

    def move(self, dx, dy, grid, tile_size):
        if not self.is_collision(dx, dy, grid, tile_size):
            self.rect.x += dx
            self.rect.y += dy

    def is_collision(self, dx, dy, grid, tile_size):
        new_rect = self.rect.move(dx, dy)
        x, y = new_rect.topleft
        col, row = x // tile_size, y // tile_size
        if col < 0 or row < 0 or col >= len(grid) or row >= len(grid[0]):
            return True
        cell = grid[col][row]
        if dx > 0 and cell.walls['right']:
            return True
        if dx < 0 and cell.walls['left']:
            return True
        if dy > 0 and cell.walls['bottom']:
            return True
        if dy < 0 and cell.walls['top']:
            return True
        return False

    def bot_move(self, goal_cell, grid, tile_size):
        if self.difficulty == 'easy':
            self.easy_bot_move(goal_cell, grid, tile_size)
        elif self.difficulty == 'medium':
            self.medium_bot_move(goal_cell, grid, tile_size)
        elif self.difficulty == 'hard':
            self.hard_bot_move(goal_cell, grid, tile_size)

    def easy_bot_move(self, goal, grid, tile_size):
        # Simple random movement for easy bot
        move_options = [
            (0, -self.speed),  # move up
            (0, self.speed),   # move down
            (-self.speed, 0),  # move left
            (self.speed, 0)    # move right
        ]
        move = random.choice(move_options)
        self.rect.move_ip(*move)

    def medium_bot_move(self, goal, grid, tile_size):
        # Implement basic pathfinding to move towards the goal
        if self.rect.x < goal.x:
            self.rect.x += self.speed
        elif self.rect.x > goal.x:
            self.rect.x -= self.speed
        if self.rect.y < goal.y:
            self.rect.y += self.speed
        elif self.rect.y > goal.y:
            self.rect.y -= self.speed

 
    def hard_bot_move(self, goal_cell, grid_cells, tile):
        start = (self.rect.x // tile, self.rect.y // tile)
        end = (goal_cell.rect.x // tile, goal_cell.rect.y // tile)
        frontier = [(start, 0)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = frontier.pop(0)[0]
            if current == end:
                break

            for next in self.get_neighbors(current, grid_cells):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(end, next)
                    frontier.append((next, priority))
                    frontier.sort(key=lambda x: x[1])
                    came_from[next] = current

        if end in came_from:
            path = []
            while end:
                path.append(end)
                end = came_from[end]
            path.reverse()

            if path:
                next_step = path[1]  # the next step after the start
                self.rect.x = next_step[0] * tile
                self.rect.y = next_step[1] * tile

    def get_neighbors(self, cell, grid_cells):
        neighbors = []
        x, y = cell
        if x > 0 and not grid_cells[y][x].walls['left']:
            neighbors.append((x-1, y))
        if x < len(grid_cells[0]) - 1 and not grid_cells[y][x].walls['right']:
            neighbors.append((x+1, y))
        if y > 0 and not grid_cells[y][x].walls['top']:
            neighbors.append((x, y-1))
        if y < len(grid_cells) - 1 and not grid_cells[y][x].walls['bottom']:
            neighbors.append((x, y+1))
        return neighbors

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def can_move(self, new_x, new_y, grid_cells, tile):
        grid_x, grid_y = new_x // tile, new_y // tile
        if grid_x < 0 or grid_x >= len(grid_cells[0]) or grid_y < 0 or grid_y >= len(grid_cells):
            return False

        cell = grid_cells[grid_y][grid_x]
        if new_x > self.rect.x and cell.walls['left']:
            return False
        if new_x < self.rect.x and cell.walls['right']:
            return False
        if new_y > self.rect.y and cell.walls['top']:
            return False
        if new_y < self.rect.y and cell.walls['bottom']:
            return False

        return True

    def get_neighbors(self, x, y, grid_cells):
        neighbors = []
        if x < len(grid_cells) - 1 and not grid_cells[x + 1][y].walls['left']:
            neighbors.append(grid_cells[x + 1][y])
        if x > 0 and not grid_cells[x - 1][y].walls['right']:
            neighbors.append(grid_cells[x - 1][y])
        if y < len(grid_cells[0]) - 1 and not grid_cells[x][y + 1].walls['top']:
            neighbors.append(grid_cells[x][y + 1])
        if y > 0 and not grid_cells[x][y - 1].walls['bottom']:
            neighbors.append(grid_cells[x][y - 1])
        return neighbors