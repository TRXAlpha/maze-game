from maze import Maze
from player import Player
from game import Game
from clock import Clock
import pygame
import sys
import random

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
            {"text": "Multiplayer", "pos": (0, 400)},
            {"text": "Exit the Game", "pos": (0, 500)}
        ]
        self.running = True
        self.stars = [Star(screen.get_width(), screen.get_height()) for _ in range(100)]

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
        
        for button in self.buttons:
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
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    text = button["text"]
                    if text == "1v1 Local":
                        return "1v1 Local"
                    elif text == "Multiplayer":
                        return "Multiplayer"
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

class Main:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 30)
        self.message_color = pygame.Color("cyan")
        self.running = True
        self.game_over = False
        self.FPS = pygame.time.Clock()

    def instructions(self):
        instructions1 = self.font.render('Player 1: Use WASD Keys to Move', True, self.message_color)
        instructions2 = self.font.render('Player 2: Use IJKL Keys to Move', True, self.message_color)
        self.screen.blit(instructions1, (810, 100))
        self.screen.blit(instructions2, (810, 150))

    def _draw(self, maze, tile, players, game, clock):
        maze_area = pygame.Rect(0, 0, 800, 800)
        info_area = pygame.Rect(800, 0, 200, 800)
        
        # Draw maze
        self.screen.fill("black", maze_area)
        [cell.draw(self.screen, tile) for cell in maze.grid_cells]

        # Draw info area background
        self.screen.fill(pygame.Color("darkslategray"), info_area)

        # Add a goal point to reach
        game.add_goal_point(self.screen)

        # Draw every player movement
        for player in players:
            player.draw(self.screen)
            player.update(tile, maze.grid_cells, maze.thickness)

        # Instructions, clock, winning message
        self.instructions()
        if self.game_over:
            clock.stop_timer()
            self.screen.blit(game.message(), (810, 220))
        else:
            clock.update_timer()
        self.screen.blit(clock.display_timer(), (825, 50))
        
        pygame.display.flip()

    def main(self, frame_size, tile):
        cols, rows = frame_size[0] // tile, frame_size[-1] // tile
        maze = Maze(cols, rows)
        maze.generate_maze()
        game = Game(maze.grid_cells[-1], tile)
        player1 = Player(tile // 3, tile // 3)
        player2 = Player(tile // 3, tile // 3)
        player1.controls = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s}
        player2.controls = {'left': pygame.K_j, 'right': pygame.K_l, 'up': pygame.K_i, 'down': pygame.K_k}
        players = [player1, player2]
        clock = Clock()

        clock.start_timer()
        while self.running:
            self.screen.fill("black")
            self.screen.fill(pygame.Color("darkslategray"), (803, 0, 197, 797))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for player in players:
                    if event.type == pygame.KEYDOWN:
                        if not self.game_over:
                            if event.key == player.controls['left']:
                                player.left_pressed = True
                            if event.key == player.controls['right']:
                                player.right_pressed = True
                            if event.key == player.controls['up']:
                                player.up_pressed = True
                            if event.key == player.controls['down']:
                                player.down_pressed = True
                            player.check_move(tile, maze.grid_cells, maze.thickness)
        
                    if event.type == pygame.KEYUP:
                        if not self.game_over:
                            if event.key == player.controls['left']:
                                player.left_pressed = False
                            if event.key == player.controls['right']:
                                player.right_pressed = False
                            if event.key == player.controls['up']:
                                player.up_pressed = False
                            if event.key == player.controls['down']:
                                player.down_pressed = False
                            player.check_move(tile, maze.grid_cells, maze.thickness)

            if game.is_game_over(players):
                self.game_over = True
                for player in players:
                    player.left_pressed = False
                    player.right_pressed = False
                    player.up_pressed = False
                    player.down_pressed = False

            self._draw(maze, tile, players, game, clock)
            self.FPS.tick(60)

def show_instructions(screen):
    font = pygame.font.SysFont("impact", 50)
    screen.fill((0, 0, 0))
    MainMenu(screen).draw_stars()
    
    instructions = [
        "Player 1 (Blue): Use WASD for movement.",
        "Player 2 (Red): Use IJKL for movement.",
        "First one to reach the exit wins!"
    ]
    
    y_offset = 200
    for line in instructions:
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
    screen.fill((0, 0, 0))
    MainMenu(screen).draw_stars()
    text = font.render("GO!", True, (255, 255, 255))
    rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(1000)

if __name__ == "__main__":
    window_size = (800, 800)
    screen_size = (1000, 800)  # Wider screen to accommodate the information section
    tile_size = 30
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Maze")

    menu = MainMenu(screen)
    action = menu.main_loop()

    if action == "1v1 Local":
        # Show options for vs Person or vs Bot
        font = pygame.font.SysFont("impact", 50)
        options = ["vs Person", "vs Bot"]
        running = True
        while running:
            screen.fill((0, 0, 0))
            MainMenu(screen).draw_stars()
            y_offset = 300
            for option in options:
                text = font.render(option, True, (255, 255, 255))
                rect = text.get_rect(center=(screen.get_width() // 2, y_offset))
                screen.blit(text, rect)
                pygame.display.flip()
                y_offset += 100

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 250 < mouse_pos[1] < 350:
                        show_instructions(screen)
                        countdown(screen)
                        game = Main(screen)
                        game.main(window_size, tile_size)
                    elif 350 < mouse_pos[1] < 450:
                        print("Bot option selected (not implemented).")

    elif action == "Multiplayer":
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("impact", 50)
        text = font.render("To be continued", True, (255, 255, 255))
        screen.blit(text, (450, 300))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()
    elif action == "Exit the Game":
        pygame.quit()
        sys.exit()