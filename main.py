# Import necessary modules and classes
from maze import Maze
from player import Player
from game import Game
from clock import Clock
import pygame
import sys
import random

# Initialize pygame and fonts
pygame.init()
pygame.font.init()

# Define the Star class for the background effect
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

# Define the MainMenu class for the game menu
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
                        return "1v1 Local"
                    elif text == "vs Bot":
                        self.show_bot_difficulty = True
                    elif text == "Easy":
                        return "vs Bot Easy"
                    elif text == "Medium":
                        return "vs Bot Medium"
                    elif text == "Hard":
                        return "vs Bot Hard"
                    elif text == "Exit the Game":
                        pygame.quit()
                        sys.exit()
        return None

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                action = self.handle_event(event)
                if action:
                    return action
            self.draw()

# Define the Main class for the game logic
class Main:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 30)
        self.message_color = pygame.Color("cyan")
        self.running = True
        self.game_over = False
        self.FPS = pygame.time.Clock()

    def instructions(self, vs_bot=False):
        instructions1 = self.font.render('Player 1: Use WASD Keys to Move', True, self.message_color)
        self.screen.blit(instructions1, (810, 100))
        if not vs_bot:
            instructions2 = self.font.render('Player 2: Use IJKL Keys to Move', True, self.message_color)
            self.screen.blit(instructions2, (810, 150))

    def _draw(self, maze, tile, players, game, clock):
        maze_area = pygame.Rect(0, 0, 800, 800)
        pygame.draw.rect(self.screen, (0, 0, 0), maze_area)

        for row in maze.grid_cells:
            for cell in row:
                cell.draw(self.screen, tile)

        for player in players:
            player.draw(self.screen)

        game.add_goal_point(self.screen)

        if self.game_over:
            self.screen.fill((0, 0, 0))
            message = "Game Over! Press R to Restart"
            text = self.font.render(message, True, (255, 255, 255))
            self.screen.blit(text, (400 - text.get_width() // 2, 400 - text.get_height() // 2))
            pygame.display.flip()
            return

        self.instructions(vs_bot=players[1].is_bot)

        game.message(self.screen, (810, 300))
        clock.display_clock(self.screen)

        pygame.display.update()

    def main(self, dimension, tile, vs_bot=False, bot_difficulty='easy'):
        maze = Maze(dimension[0] // tile, dimension[1] // tile, tile)
        maze.generate_maze()
        start = maze.grid_cells[0][0]
        goal = maze.grid_cells[-1][-1]
        game = Game(goal, tile)
        players = [
            Player(tile, tile),
            Player(tile, tile, is_bot=vs_bot, difficulty=bot_difficulty) if vs_bot else Player(tile, tile)
        ]
        clock = Clock(pygame.time.get_ticks())

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    for player in players:
                        if event.key == pygame.K_w and not player.is_bot:
                            player.up_pressed = True
                        if event.key == pygame.K_a and not player.is_bot:
                            player.left_pressed = True
                        if event.key == pygame.K_s and not player.is_bot:
                            player.down_pressed = True
                        if event.key == pygame.K_d and not player.is_bot:
                            player.right_pressed = True
                        if event.key == pygame.K_i and not vs_bot:
                            player.up_pressed = True
                        if event.key == pygame.K_j and not vs_bot:
                            player.left_pressed = True
                        if event.key == pygame.K_k and not vs_bot:
                            player.down_pressed = True
                        if event.key == pygame.K_l and not vs_bot:
                            player.right_pressed = True
                if event.type == pygame.KEYUP:
                    for player in players:
                        if event.key == pygame.K_w and not player.is_bot:
                            player.up_pressed = False
                        if event.key == pygame.K_a and not player.is_bot:
                            player.left_pressed = False
                        if event.key == pygame.K_s and not player.is_bot:
                            player.down_pressed = False
                        if event.key == pygame.K_d and not player.is_bot:
                            player.right_pressed = False
                        if event.key == pygame.K_i and not vs_bot:
                            player.up_pressed = False
                        if event.key == pygame.K_j and not vs_bot:
                            player.left_pressed = False
                        if event.key == pygame.K_k and not vs_bot:
                            player.down_pressed = False
                        if event.key == pygame.K_l and not vs_bot:
                            player.right_pressed = False

            self._draw(maze, tile, players, game, clock)

            if game.is_game_over(players):
                self.game_over = True

            self.FPS.tick(30)

def show_instructions(screen, vs_bot=False):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("impact", 50)
    lines = [
        "Instructions:",
        "Player 1: Use WASD to move",
        "Player 2: Use IJKL to move" if not vs_bot else "The bot will play against you",
        "Reach the green goal point first to win!"
    ]

    y_offset = 100
    for line in lines:
        text = font.render(line, True, (255, 255, 255))
        rect = text.get_rect(center=(screen.get_width() // 2, y_offset))
        screen.blit(text, rect)
        y_offset += 60

    pygame.display.flip()
    pygame.time.wait(3000)

def countdown(screen):
    font = pygame.font.SysFont("impact", 100)
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        MainMenu(screen).draw_stars()
        text = font.render(str(i), True, (255, 255, 255))
        rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.wait(1000)

def main():
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Maze Duel")
    main_menu = MainMenu(screen)
    game = Main(screen)

    while True:
        action = main_menu.main_loop()
        if action == "1v1 Local":
            show_instructions(screen)
            countdown(screen)
            game.main((800, 800), 40)
        elif action == "vs Bot Easy":
            show_instructions(screen, vs_bot=True)
            countdown(screen)
            game.main((800, 800), 40, vs_bot=True, bot_difficulty='easy')
        elif action == "vs Bot Medium":
            show_instructions(screen, vs_bot=True)
            countdown(screen)
            game.main((800, 800), 40, vs_bot=True, bot_difficulty='medium')
        elif action == "vs Bot Hard":
            show_instructions(screen, vs_bot=True)
            countdown(screen)
            game.main((800, 800), 40, vs_bot=True, bot_difficulty='hard')

if __name__ == "__main__":
    main()
