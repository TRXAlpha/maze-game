# main.py

import pygame
import sys
import random
from maze import Maze
from player import Player
from game import Game
from clock import Clock

# Initialize pygame and fonts
pygame.init()
pygame.font.init()

class Star:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.speed = random.uniform(0.1, 0.5)
        self.size = random.randint(1, 2)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        self.y += self.speed
        if self.y > self.screen_height:
            self.y = 0
            self.x = random.randint(0, self.screen_width)

    def draw(self, screen):
        faded_color = (255, 255, 255, random.randint(50, 150))
        star_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(star_surface, faded_color, (self.size // 2, self.size // 2), self.size)
        screen.blit(star_surface, (self.x, self.y))

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 50)
        self.title_font = pygame.font.SysFont("impact", 100)
        self.buttons = [
            {"text": "1v1 Local", "pos": (0, 300)},
            {"text": "vs Bot", "pos": (0, 400)},
            {"text": "Exit the Game", "pos": (0, 500)}
        ]
        self.bot_buttons = [
            {"text": "Easy", "pos": (0, 300)},
            {"text": "Medium", "pos": (0, 400)},
            {"text": "Hard", "pos": (0, 500)}
        ]
        self.running = True
        self.stars = [Star(screen.get_width(), screen.get_height()) for _ in range(100)]
        self.show_bot_difficulty = False

    def draw_stars(self):
        for star in self.stars:
            star.move()
            star.draw(self.screen)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_stars()
        title = self.title_font.render("MAZE DUEL", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)

        if self.show_bot_difficulty:
            buttons = self.bot_buttons
        else:
            buttons = self.buttons
        
        for button in buttons:
            text = button["text"]
            pos = button["pos"]
            btn = self.font.render(text, True, (255, 255, 255))
            btn_rect = btn.get_rect(center=(self.screen.get_width() // 2, pos[1]))
            self.screen.blit(btn, btn_rect)
            button["rect"] = btn_rect  # Save the rect for collision detection
        
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            buttons = self.bot_buttons if self.show_bot_difficulty else self.buttons
            for button in buttons:
                if button["rect"].collidepoint(mouse_pos):
                    text = button["text"]
                    if text == "1v1 Local":
                        self.running = False
                        return "1v1"
                    elif text == "vs Bot":
                        self.show_bot_difficulty = True
                        return None
                    elif text == "Exit the Game":
                        pygame.quit()
                        sys.exit()
                    elif text in ["Easy", "Medium", "Hard"]:
                        self.running = False
                        return text.lower()
        return None

class MainGame:
    def __init__(self):
        self.goal_image = pygame.image.load('gate.jpeg')

    def run_game(self, size, tile, vs_bot=False, bot_difficulty='easy'):
        pygame.init()
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Maze Game")
        clock = pygame.time.Clock()

        maze = Maze(size[0] // tile, size[1] // tile, tile)
        maze.generate_maze()
        
        goal = maze.get_random_goal_cell()
        game = Game(goal, tile, goal_image=self.goal_image)

        if vs_bot:
            players = [Player(tile, tile), Player(tile, tile, is_bot=True, difficulty=bot_difficulty)]
        else:
            players = [Player(tile, tile), Player(tile, tile)]

        players[0].rect.topleft = maze.get_start_position()
        players[1].rect.topleft = maze.get_start_position()

        font = pygame.font.SysFont("impact", 30)
        back_button = font.render("Back", True, (255, 255, 255))
        back_rect = back_button.get_rect(topleft=(10, size[1] - 40))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_rect.collidepoint(event.pos):
                        return  # Return to main menu

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                players[0].rect.y -= players[0].speed
            if keys[pygame.K_s]:
                players[0].rect.y += players[0].speed
            if keys[pygame.K_a]:
                players[0].rect.x -= players[0].speed
            if keys[pygame.K_d]:
                players[0].rect.x += players[0].speed

            if not vs_bot:
                if keys[pygame.K_UP]:
                    players[1].rect.y -= players[1].speed
                if keys[pygame.K_DOWN]:
                    players[1].rect.y += players[1].speed
                if keys[pygame.K_LEFT]:
                    players[1].rect.x -= players[1].speed
                if keys[pygame.K_RIGHT]:
                    players[1].rect.x += players[1].speed

            screen.fill((0, 0, 0))
            maze.draw(screen)
            game.draw(screen)
            for player in players:
                player.draw(screen)

            if vs_bot:
                players[1].bot_move(goal, maze.grid_cells, tile)

            if players[0].rect.colliderect(goal.rect):
                print("Player 1 wins!")
                running = False
            if players[1].rect.colliderect(goal.rect):
                print("Player 2 wins!")
                running = False

            screen.blit(back_button, back_rect)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

def main():
    screen = pygame.display.set_mode((800, 800))
    menu = MainMenu(screen)
    while menu.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                result = menu.handle_event(event)
                if result:
                    main_game = MainGame()
                    if result == "1v1":
                        main_game.run_game((800, 800), 40, vs_bot=False)
                    else:
                        main_game.run_game((800, 800), 40, vs_bot=True, bot_difficulty=result)
                    menu.running = True

        menu.draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()
