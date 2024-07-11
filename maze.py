# maze.py

import pygame
import random

class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw(self, screen):
        x = self.x * self.size
        y = self.y * self.size
        if self.walls['top']:
            pygame.draw.line(screen, (255, 255, 255), (x, y), (x + self.size, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, (255, 255, 255), (x + self.size, y), (x + self.size, y + self.size), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, (255, 255, 255), (x + self.size, y + self.size), (x, y + self.size), 2)
        if self.walls['left']:
            pygame.draw.line(screen, (255, 255, 255), (x, y + self.size), (x, y), 2)

    def remove_wall(self, next_cell):
        dx = self.x - next_cell.x
        dy = self.y - next_cell.y
        if dx == 1:
            self.walls['left'] = False
            next_cell.walls['right'] = False
        elif dx == -1:
            self.walls['right'] = False
            next_cell.walls['left'] = False
        if dy == 1:
            self.walls['top'] = False
            next_cell.walls['bottom'] = False
        elif dy == -1:
            self.walls['bottom'] = False
            next_cell.walls['top'] = False

class Maze:
    def __init__(self, cols, rows, size):
        self.cols = cols
        self.rows = rows
        self.size = size
        self.grid = [[Cell(col, row, size) for row in range(rows)] for col in range(cols)]
        self.stack = []
        self.current = self.grid[0][0]

    def draw(self, screen):
        for col in range(self.cols):
            for row in range(self.rows):
                self.grid[col][row].draw(screen)

    def generate_maze(self):
        self.current.visited = True
        while True:
            next_cell = self.get_next_cell(self.current)
            if next_cell:
                next_cell.visited = True
                self.stack.append(self.current)
                self.current.remove_wall(next_cell)
                self.current = next_cell
            elif self.stack:
                self.current = self.stack.pop()
            else:
                break

    def get_next_cell(self, cell):
        neighbors = []
        col, row = cell.x, cell.y
        if col > 0 and not self.grid[col - 1][row].visited:
            neighbors.append(self.grid[col - 1][row])
        if col < self.cols - 1 and not self.grid[col + 1][row].visited:
            neighbors.append(self.grid[col + 1][row])
        if row > 0 and not self.grid[col][row - 1].visited:
            neighbors.append(self.grid[col][row - 1])
        if row < self.rows - 1 and not self.grid[col][row + 1].visited:
            neighbors.append(self.grid[col][row + 1])

        if neighbors:
            return random.choice(neighbors)
        else:
            return None

    def get_random_goal_cell(self):
        while True:
            col = random.randint(0, self.cols - 1)
            row = random.randint(0, self.rows - 1)
            if col != 0 or row != 0:  # ensure goal is not at the start position
                return self.grid[col][row]

    def get_start_position(self):
        return self.grid[0][0].x * self.size, self.grid[0][0].y * self.size
