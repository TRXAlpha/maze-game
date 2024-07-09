# bot.py

import pygame

class Bot:
    def __init__(self, x, y, goal_x, goal_y):
        self.x = x
        self.y = y
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.speed = 2  # Adjust bot speed as needed

    def move_towards_goal(self):
        if self.x < self.goal_x:
            self.x += self.speed
        elif self.x > self.goal_x:
            self.x -= self.speed

        if self.y < self.goal_y:
            self.y += self.speed
        elif self.y > self.goal_y:
            self.y -= self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 10)  # Adjust circle size as needed
