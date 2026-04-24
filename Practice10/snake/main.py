import pygame
import random
import sys

pygame.init()

# ---------------------------
# Settings
# ---------------------------
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS_START = 8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
BLUE = (50, 120, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 42)

# Wall cells inside the playing field
WALLS = {
    (10, 8), (11, 8), (12, 8), (13, 8),
    (16, 12), (17, 12), (18, 12), (19, 12),
    (7, 15), (7, 16), (7, 17)
}


def draw_grid():
    """Draw the playing field and thin grid lines."""
    screen.fill(BLACK)

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))


def draw_walls():
    """Draw all wall blocks."""
    for wx, wy in WALLS:
        rect = pygame.Rect(wx * CELL_SIZE, wy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GRAY, rect)


def draw_snake(snake):
    """Draw snake segments."""
    for i, (x, y) in enumerate(snake):
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if i == 0:
            pygame.draw.rect(screen, BLUE, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)


def draw_food(food):
    """Draw food."""
    rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)


def random_food_position(snake):
    """Generate food in a free cell that is not on walls and not on the snake."""
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake and pos not in WALLS:
            return pos


def draw_info(score, level, speed):
    """Draw score and level text."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    speed_text = font.render(f"Speed: {speed}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (120, 10))
    screen.blit(speed_text, (230, 10))


def game_over_screen(score, level):
    """Show final result."""
    screen.fill((120, 0, 0))
    t1 = big_font.render("GAME OVER", True, WHITE)
    t2 = font.render(f"Final score: {score}", True, WHITE)
    t3 = font.render(f"Level reached: {level}", True, WHITE)
    t4 = font.render("Press R to restart or Q to quit", True, WHITE)

    screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
    screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    screen.blit(t3, t3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35)))
    screen.blit(t4, t4.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90)))
    pygame.display.flip()


def run_game():
    """Main Snake game loop."""
    while True:
        snake = [(5, 5), (4, 5), (3, 5)]
        direction = (1, 0)
        next_direction = (1, 0)
        food = random_food_position(snake)
        score = 0
        level = 1
        speed = FPS_START
        foods_eaten = 0
        running = True

        while running:
            clock.tick(speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, 1):
                        next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        next_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        next_direction = (1, 0)

            direction = next_direction

            # Calculate new head position
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # 1) Border collision check
            if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                running = False

            # 2) Wall collision check
            elif new_head in WALLS:
                running = False

            # 3) Snake self-collision check
            elif new_head in snake:
                running = False
            else:
                snake.insert(0, new_head)

                # Eat food
                if new_head == food:
                    score += 10
                    foods_eaten += 1
                    food = random_food_position(snake)

                    # Level up every 4 foods
                    if foods_eaten % 4 == 0:
                        level += 1
                        speed += 2  # increase speed
                else:
                    snake.pop()

            # Draw everything
            draw_grid()
            draw_walls()
            draw_snake(snake)
            draw_food(food)
            draw_info(score, level, speed)
            pygame.display.flip()

        # Game over waiting screen
        game_over_screen(score, level)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    run_game()