import pygame
import random
class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x * size, y * size, size, size)
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.visited = False

    def draw(self, screen, tile):
        if self.walls[0]:
            pygame.draw.line(screen, (255, 255, 255), (self.x * tile, self.y * tile), ((self.x + 1) * tile, self.y * tile), 2)
        if self.walls[1]:
            pygame.draw.line(screen, (255, 255, 255), ((self.x + 1) * tile, self.y * tile), ((self.x + 1) * tile, (self.y + 1) * tile), 2)
        if self.walls[2]:
            pygame.draw.line(screen, (255, 255, 255), ((self.x + 1) * tile, (self.y + 1) * tile), (self.x * tile, (self.y + 1) * tile), 2)
        if self.walls[3]:
            pygame.draw.line(screen, (255, 255, 255), (self.x * tile, (self.y + 1) * tile), (self.x * tile, self.y * tile), 2)

class Maze:
    def __init__(self, cols, rows, tile):
        self.cols = cols
        self.rows = rows
        self.tile = tile
        self.grid_cells = [[Cell(x, y, tile) for y in range(rows)] for x in range(cols)]

    def generate_maze(self):
        current_cell = self.grid_cells[0][0]
        stack = [current_cell]
        current_cell.visited = True

        while stack:
            neighbors = self.get_unvisited_neighbors(current_cell)
            if neighbors:
                next_cell = random.choice(neighbors)
                self.remove_walls(current_cell, next_cell)
                stack.append(current_cell)
                current_cell = next_cell
                current_cell.visited = True
            else:
                current_cell = stack.pop()

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        directions = [
            (0, -1),  # top
            (1, 0),  # right
            (0, 1),  # bottom
            (-1, 0)  # left
        ]
        for direction in directions:
            nx, ny = cell.x + direction[0], cell.y + direction[1]
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                neighbor = self.grid_cells[nx][ny]
                if not neighbor.visited:
                    neighbors.append(neighbor)
        return neighbors

    def remove_walls(self, current, next):
        dx = current.x - next.x
        dy = current.y - next.y
        if dx == 1:  # next is to the left of current
            current.walls[3] = False
            next.walls[1] = False
        elif dx == -1:  # next is to the right of current
            current.walls[1] = False
            next.walls[3] = False
        if dy == 1:  # next is above current
            current.walls[0] = False
            next.walls[2] = False
        elif dy == -1:  # next is below current
            current.walls[2] = False
            next.walls[0] = False
