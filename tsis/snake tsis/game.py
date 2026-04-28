# game.py
# Main Snake gameplay logic.
# Includes Practice 10, Practice 11, and TSIS4 extensions:
# - weighted food
# - food timeout
# - poison food
# - power-ups
# - obstacles from level 3
# - personal best display

import random
import pygame

from config import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, WIDTH, HEIGHT, FPS_START, LEVEL_UP_EVERY
from db import get_personal_best, save_game_result

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)
RED = (220, 50, 50)
DARK_RED = (120, 0, 0)
BLUE = (50, 120, 255)
YELLOW = (245, 210, 50)
PURPLE = (160, 60, 220)
CYAN = (40, 220, 230)
ORANGE = (255, 150, 30)


class SnakeGame:
    """
    One game session.
    main.py creates this class when player presses Play or Retry.
    """

    def __init__(self, screen, username, settings):
        self.screen = screen
        self.username = username or "Player"
        self.settings = settings
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)
        self.small = pygame.font.SysFont("Arial", 16)

        # Load best score from PostgreSQL and show it in gameplay HUD.
        self.personal_best = get_personal_best(self.username)

        self.reset()

    def reset(self):
        """
        Creates a fresh snake game state.
        """
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.score = 0
        self.level = 1
        self.speed = FPS_START
        self.foods_eaten = 0

        self.obstacles = set()

        # Practice 11 food: value and timer.
        self.food = None
        self.food_value = 1
        self.food_spawn_time = 0
        self.food_timeout = 7000

        # Poison food.
        self.poison = None
        self.poison_spawn_time = 0
        self.poison_timeout = 7000

        # Power-up system.
        self.powerup = None
        self.powerup_kind = None
        self.powerup_spawn_time = 0
        self.powerup_timeout = 8000
        self.active_power = None
        self.power_end_time = 0
        self.shield = False

        self.game_over = False
        self.saved = False

        self.spawn_food()
        self.spawn_poison()

    def all_blocked_cells(self):
        """
        Returns cells where new objects cannot spawn.
        Food and power-ups must avoid snake body and obstacles.
        """
        blocked = set(self.snake) | set(self.obstacles)
        if self.food:
            blocked.add(self.food)
        if self.poison:
            blocked.add(self.poison)
        if self.powerup:
            blocked.add(self.powerup)
        return blocked

    def random_free_cell(self):
        """
        Finds a random empty cell.
        This replaces simple random food placement from Practice 10.
        """
        blocked = self.all_blocked_cells()
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in blocked:
                return pos

    def spawn_food(self):
        """
        Practice 11: normal food has different point weights.
        Food disappears after a timer and then respawns.
        """
        self.food = self.random_free_cell()
        self.food_value = random.choices([1, 2, 3], weights=[70, 22, 8])[0]
        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_poison(self):
        """
        Poison appears randomly and shortens snake by 2 segments.
        """
        self.poison = self.random_free_cell()
        self.poison_spawn_time = pygame.time.get_ticks()

    def maybe_spawn_powerup(self):
        """
        Only one power-up can be active on the field at a time.
        It disappears after 8 seconds if not collected.
        """
        if self.powerup is not None:
            return
        if random.random() < 0.025:
            self.powerup = self.random_free_cell()
            self.powerup_kind = random.choice(["speed", "slow", "shield"])
            self.powerup_spawn_time = pygame.time.get_ticks()

    def generate_obstacles(self):
        """
        Starting from level 3, static wall blocks appear inside arena.
        They are placed randomly and never on the snake.
        A safety zone around snake head prevents immediate trapping.
        """
        if self.level < 3:
            self.obstacles = set()
            return

        head_x, head_y = self.snake[0]
        safe_zone = {
            (head_x, head_y),
            (head_x + 1, head_y),
            (head_x - 1, head_y),
            (head_x, head_y + 1),
            (head_x, head_y - 1),
        }

        count = min(6 + self.level * 2, 35)
        new_obstacles = set()
        attempts = 0

        while len(new_obstacles) < count and attempts < 500:
            attempts += 1
            pos = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
            if pos in self.snake or pos in safe_zone:
                continue
            new_obstacles.add(pos)

        self.obstacles = new_obstacles

        # If food/power-up accidentally became invalid after new obstacles, respawn it.
        if self.food in self.obstacles:
            self.spawn_food()
        if self.poison in self.obstacles:
            self.spawn_poison()
        if self.powerup in self.obstacles:
            self.powerup = None
            self.powerup_kind = None

    def handle_input(self, event):
        """
        Reads keyboard arrows and prevents reversing into itself.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, 1):
                self.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                self.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                self.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.next_direction = (1, 0)

    def active_speed(self):
        """
        Calculates current game speed.
        Power-ups temporarily change speed for 5 seconds.
        """
        if self.active_power == "speed":
            return self.speed + 5
        if self.active_power == "slow":
            return max(4, self.speed - 4)
        return self.speed

    def activate_powerup(self, kind):
        """
        Activates collected power-up.
        speed and slow last 5 seconds.
        shield stays until the next collision.
        """
        now = pygame.time.get_ticks()
        if kind == "speed":
            self.active_power = "speed"
            self.power_end_time = now + 5000
            self.shield = False
        elif kind == "slow":
            self.active_power = "slow"
            self.power_end_time = now + 5000
            self.shield = False
        elif kind == "shield":
            self.active_power = "shield"
            self.power_end_time = 0
            self.shield = True

    def use_shield(self):
        """
        Shield ignores next wall, self, or obstacle collision once.
        It moves snake head back to previous safe position.
        """
        if self.shield:
            self.shield = False
            self.active_power = None
            self.power_end_time = 0
            return True
        return False

    def update_timers(self):
        """
        Handles timers for food, poison and power-ups.
        Uses pygame.time.get_ticks(), as required in the task.
        """
        now = pygame.time.get_ticks()

        # Food disappears and respawns after timeout.
        if now - self.food_spawn_time > self.food_timeout:
            self.spawn_food()

        # Poison also moves after timeout.
        if self.poison and now - self.poison_spawn_time > self.poison_timeout:
            self.spawn_poison()

        # Power-up disappears after 8 seconds if not collected.
        if self.powerup and now - self.powerup_spawn_time > self.powerup_timeout:
            self.powerup = None
            self.powerup_kind = None

        # Timed power-up effects expire after 5 seconds.
        if self.active_power in ("speed", "slow") and now > self.power_end_time:
            self.active_power = None
            self.power_end_time = 0

    def move(self):
        """
        Moves the snake one cell and handles collisions/eating.
        """
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall/border collision.
        hit_border = not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT)
        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles

        if hit_border or hit_self or hit_obstacle:
            if self.use_shield():
                return
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Eat weighted food.
        if new_head == self.food:
            self.score += self.food_value * 10
            self.foods_eaten += 1
            self.spawn_food()

            # Level up every N food items.
            if self.foods_eaten % LEVEL_UP_EVERY == 0:
                self.level += 1
                self.speed += 2
                self.generate_obstacles()
        else:
            self.snake.pop()

        # Eat poison food: shorten by 2 segments.
        if new_head == self.poison:
            self.score = max(0, self.score - 5)
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()
            self.spawn_poison()
            if len(self.snake) <= 1:
                self.game_over = True
                return

        # Eat power-up.
        if self.powerup and new_head == self.powerup:
            self.activate_powerup(self.powerup_kind)
            self.powerup = None
            self.powerup_kind = None

    def draw_cell(self, pos, color):
        """
        Draws one grid cell.
        """
        x, y = pos
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def draw_grid(self):
        """
        Optional grid overlay from settings.json.
        """
        if not self.settings.get("grid", True):
            return
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WIDTH, y))

    def draw(self):
        """
        Draws the full game screen.
        """
        self.screen.fill(BLACK)
        self.draw_grid()

        for obs in self.obstacles:
            self.draw_cell(obs, GRAY)

        if self.food:
            color = RED if self.food_value == 1 else YELLOW if self.food_value == 2 else ORANGE
            self.draw_cell(self.food, color)
            value_text = self.small.render(str(self.food_value), True, BLACK)
            self.screen.blit(value_text, (self.food[0] * CELL_SIZE + 5, self.food[1] * CELL_SIZE + 2))

        if self.poison:
            self.draw_cell(self.poison, DARK_RED)

        if self.powerup:
            power_colors = {"speed": CYAN, "slow": PURPLE, "shield": BLUE}
            self.draw_cell(self.powerup, power_colors[self.powerup_kind])
            label = {"speed": "B", "slow": "S", "shield": "H"}[self.powerup_kind]
            txt = self.small.render(label, True, WHITE)
            self.screen.blit(txt, (self.powerup[0] * CELL_SIZE + 5, self.powerup[1] * CELL_SIZE + 2))

        snake_color = tuple(self.settings.get("snake_color", [0, 180, 0]))
        for i, segment in enumerate(self.snake):
            self.draw_cell(segment, BLUE if i == 0 else snake_color)

        self.draw_hud()
        pygame.display.flip()

    def draw_hud(self):
        """
        Draws score, level, speed, personal best and active power-up.
        """
        hud_items = [
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Best: {self.personal_best}",
            f"Speed: {self.active_speed()}",
        ]
        for i, item in enumerate(hud_items):
            img = self.small.render(item, True, WHITE)
            self.screen.blit(img, (8 + i * 105, 5))

        if self.active_power:
            if self.active_power in ("speed", "slow"):
                remaining = max(0, (self.power_end_time - pygame.time.get_ticks()) / 1000)
                text = f"Power: {self.active_power} {remaining:.1f}s"
            else:
                text = "Power: Shield 1 hit"
            img = self.small.render(text, True, WHITE)
            self.screen.blit(img, (8, HEIGHT - 24))

    def save_result_once(self):
        """
        Saves the game result only once after Game Over.
        """
        if not self.saved:
            save_game_result(self.username, self.score, self.level)
            self.saved = True

    def run(self):
        """
        Main game loop.
        Returns final stats to main.py for Game Over screen.
        """
        while not self.game_over:
            self.clock.tick(self.active_speed())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return {"action": "quit"}
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return {"action": "menu"}
                self.handle_input(event)

            self.update_timers()
            self.maybe_spawn_powerup()
            self.move()
            self.draw()

        self.save_result_once()
        return {
            "action": "game_over",
            "score": self.score,
            "level": self.level,
            "best": max(self.personal_best, self.score),
        }
