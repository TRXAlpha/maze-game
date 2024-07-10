import pygame
import sys
import random

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

class Main:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 30)
        self.message_color = pygame.Color("cyan")
        self.running = True
        self.game_over = False
        self.FPS = pygame.time.Clock()
        self.clock = Clock()
        self.goal_image = pygame.image.load('gate.jpe')

    def instructions(self, vs_bot=False):
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

        game.message(self.screen, (810, 300), "Game Message")
        clock.update_timer()
        self.screen.blit(clock.display_timer(), (810, 200))

        pygame.display.update()

    def main(self, dimension, tile, vs_bot=False, bot_difficulty='easy'):
        maze = Maze(dimension[0] // tile, dimension[1] // tile, tile)
        maze.generate_maze()
        start = maze.grid_cells[0][0]
        goal = maze.grid_cells[-1][-1]
        game = Game(goal, tile, goal_image=self.goal_image)
        players = [
            Player(tile // 2, tile // 2),
            Player(tile // 2, tile // 2, is_bot=vs_bot, difficulty=bot_difficulty) if vs_bot else Player(tile // 2, tile // 2)
        ]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_over = False
                        self.main(dimension, tile, vs_bot, bot_difficulty)
                    if not vs_bot:
                        if event.key == pygame.K_w:
                            players[0].move(0, -1, maze)
                        elif event.key == pygame.K_s:
                            players[0].move(0, 1, maze)
                        elif event.key == pygame.K_a:
                            players[0].move(-1, 0, maze)
                        elif event.key == pygame.K_d:
                            players[0].move(1, 0, maze)
                        elif event.key == pygame.K_i:
                            players[1].move(0, -1, maze)
                        elif event.key == pygame.K_k:
                            players[1].move(0, 1, maze)
                        elif event.key == pygame.K_j:
                            players[1].move(-1, 0, maze)
                        elif event.key == pygame.K_l:
                            players[1].move(1, 0, maze)

            self._draw(maze, tile, players, game, self.clock)
            self.FPS.tick(60)

class Maze:
    def __init__(self, cols, rows, tile_size):
        self.cols = cols
        self.rows = rows
        self.tile_size = tile_size
        self.grid_cells = [[Cell(x, y, tile_size) for y in range(rows)] for x in range(cols)]
        self.stack = []

    def generate_maze(self):
        current_cell = self.grid_cells[0][0]
        self.stack.append(current_cell)
        current_cell.visited = True

        while self.stack:
            next_cell = current_cell.check_neighbors(self.grid_cells, self.cols, self.rows)
            if next_cell:
                next_cell.visited = True
                self.stack.append(current_cell)
                current_cell.remove_walls(next_cell)
                current_cell = next_cell
            elif self.stack:
                current_cell = self.stack.pop()

class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.walls = [True, True, True, True]
        self.visited = False

    def draw(self, screen, tile_size):
        x = self.x * tile_size
        y = self.y * tile_size
        if self.walls[0]:
            pygame.draw.line(screen, (255, 255, 255), (x, y), (x + tile_size, y))
        if self.walls[1]:
            pygame.draw.line(screen, (255, 255, 255), (x + tile_size, y), (x + tile_size, y + tile_size))
        if self.walls[2]:
            pygame.draw.line(screen, (255, 255, 255), (x + tile_size, y + tile_size), (x, y + tile_size))
        if self.walls[3]:
            pygame.draw.line(screen, (255, 255, 255), (x, y + tile_size), (x, y))
        if self.visited:
            pygame.draw.rect(screen, (0, 0, 0), (x, y, tile_size, tile_size))

    def check_neighbors(self, grid_cells, cols, rows):
        neighbors = []
        top = grid_cells[self.x][self.y - 1] if self.y > 0 else None
        right = grid_cells[self.x + 1][self.y] if self.x < cols - 1 else None
        bottom = grid_cells[self.x][self.y + 1] if self.y < rows - 1 else None
        left = grid_cells[self.x - 1][self.y] if self.x > 0 else None

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        if neighbors:
            return random.choice(neighbors)
        return None

    def remove_walls(self, next_cell):
        x = self.x - next_cell.x
        y = self.y - next_cell.y
        if x == 1:
            self.walls[3] = False
            next_cell.walls[1] = False
        elif x == -1:
            self.walls[1] = False
            next_cell.walls[3] = False
        if y == 1:
            self.walls[0] = False
            next_cell.walls[2] = False
        elif y == -1:
            self.walls[2] = False
            next_cell.walls[0] = False

class Player:
    def __init__(self, width, height, is_bot=False, difficulty='easy'):
        self.width = width
        self.height = height
        self.is_bot = is_bot
        self.difficulty = difficulty
        self.rect = pygame.Rect(0, 0, width, height)
        self.color = (255, 0, 0) if not is_bot else (0, 255, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, dx, dy, maze):
        x = self.rect.x // maze.tile_size + dx
        y = self.rect.y // maze.tile_size + dy
        if 0 <= x < maze.cols and 0 <= y < maze.rows:
            self.rect.x += dx * maze.tile_size
            self.rect.y += dy * maze.tile_size

class Game:
    def __init__(self, goal, tile, goal_image):
        self.goal = goal
        self.tile = tile
        self.goal_image = pygame.transform.scale(goal_image, (tile, tile))

    def add_goal_point(self, screen):
        x = self.goal.x * self.tile
        y = self.goal.y * self.tile
        screen.blit(self.goal_image, (x, y))

    def message(self, screen, position, text):
        font = pygame.font.SysFont("impact", 30)
        message_surface = font.render(text, True, pygame.Color("cyan"))
        screen.blit(message_surface, position)

class Clock:
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()
        self.font = pygame.font.SysFont("impact", 30)

    def update_timer(self):
        self.elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000

    def display_timer(self):
        minutes = int(self.elapsed_seconds // 60)
        seconds = int(self.elapsed_seconds % 60)
        time_string = f"{minutes:02}:{seconds:02}"
        return self.font.render(time_string, True, pygame.Color("cyan"))

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Maze Duel")

    menu = MainMenu(screen)
    game_mode = menu.main_loop()

    main_game = Main(screen)

    if game_mode == "1v1 Local":
        main_game.main((800, 800), 40, vs_bot=False)
    elif game_mode == "vs Bot Easy":
        main_game.main((800, 800), 40, vs_bot=True, bot_difficulty='easy')
    elif game_mode == "vs Bot Medium":
        main_game.main((800, 800), 40, vs_bot=True, bot_difficulty='medium')
    elif game_mode == "vs Bot Hard":
        main_game.main((800, 800), 40, vs_bot=True, bot_difficulty='hard')

if __name__ == "__main__":
    main()
