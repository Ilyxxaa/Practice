# main.py
# Entry point of the TSIS4 Snake project.
# Contains all Pygame screens:
# - Main Menu
# - Username input
# - Game Over
# - Leaderboard
# - Settings

import sys
import pygame

from config import WIDTH, HEIGHT
from db import init_db, get_leaderboard
from game import SnakeGame
from settings_manager import load_settings, save_settings

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("Arial", 24)
SMALL = pygame.font.SysFont("Arial", 17)
BIG = pygame.font.SysFont("Arial", 44)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK = (25, 25, 25)
GREEN = (0, 180, 0)
RED = (180, 40, 40)
BLUE = (50, 120, 255)
YELLOW = (230, 200, 50)
PURPLE = (160, 60, 220)

settings = load_settings()
username = "Player"
last_result = {"score": 0, "level": 1, "best": 0}


class Button:
    """
    Simple Pygame button.
    No external UI libraries are used.
    """

    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        color = (210, 210, 210) if self.rect.collidepoint(mouse) else GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)
        img = FONT.render(self.text, True, BLACK)
        surface.blit(img, img.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_text(text, font, color, center=None, topleft=None):
    """
    Helper function for drawing text.
    """
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = center
    if topleft:
        rect.topleft = topleft
    screen.blit(img, rect)


def quit_game():
    """
    Safely exits Pygame and Python.
    """
    pygame.quit()
    sys.exit()


def username_screen():
    """
    Lets player type username using keyboard.
    The username is used for PostgreSQL leaderboard.
    """
    global username
    text = ""

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and text.strip():
                    username = text.strip()[:50]
                    return
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif len(text) < 50 and event.unicode.isprintable():
                    text += event.unicode

        screen.fill(DARK)
        draw_text("Enter username", BIG, WHITE, center=(WIDTH // 2, 110))
        pygame.draw.rect(screen, WHITE, (120, 185, WIDTH - 240, 48), border_radius=8)
        pygame.draw.rect(screen, BLACK, (120, 185, WIDTH - 240, 48), 2, border_radius=8)
        draw_text(text or "Player", FONT, BLACK, center=(WIDTH // 2, 209))
        draw_text("Press Enter to start", SMALL, WHITE, center=(WIDTH // 2, 270))
        pygame.display.flip()


def main_menu():
    """
    Main menu screen with required buttons:
    Play, Leaderboard, Settings, Quit.
    """
    global last_result

    buttons = [
        Button((WIDTH // 2 - 110, 150, 220, 44), "Play"),
        Button((WIDTH // 2 - 110, 210, 220, 44), "Leaderboard"),
        Button((WIDTH // 2 - 110, 270, 220, 44), "Settings"),
        Button((WIDTH // 2 - 110, 330, 220, 44), "Quit"),
    ]

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if buttons[0].clicked(event):
                username_screen()
                result = SnakeGame(screen, username, settings).run()
                if result.get("action") == "quit":
                    quit_game()
                if result.get("action") == "game_over":
                    last_result = result
                    game_over_screen()

            if buttons[1].clicked(event):
                leaderboard_screen()
            if buttons[2].clicked(event):
                settings_screen()
            if buttons[3].clicked(event):
                quit_game()

        screen.fill(DARK)
        draw_text("Snake Game", BIG, WHITE, center=(WIDTH // 2, 75))
        draw_text("TSIS4 Database + Advanced Gameplay", SMALL, WHITE, center=(WIDTH // 2, 112))
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()


def game_over_screen():
    """
    Game Over screen.
    Shows final score, level reached and personal best.
    """
    retry = Button((WIDTH // 2 - 110, 290, 220, 44), "Retry")
    menu = Button((WIDTH // 2 - 110, 350, 220, 44), "Main Menu")

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if retry.clicked(event):
                result = SnakeGame(screen, username, settings).run()
                if result.get("action") == "quit":
                    quit_game()
                if result.get("action") == "game_over":
                    global last_result
                    last_result = result
                    return game_over_screen()
            if menu.clicked(event):
                return

        screen.fill((90, 0, 0))
        draw_text("GAME OVER", BIG, WHITE, center=(WIDTH // 2, 90))
        draw_text(f"Player: {username}", FONT, WHITE, center=(WIDTH // 2, 155))
        draw_text(f"Score: {last_result.get('score', 0)}", FONT, WHITE, center=(WIDTH // 2, 190))
        draw_text(f"Level reached: {last_result.get('level', 1)}", FONT, WHITE, center=(WIDTH // 2, 225))
        draw_text(f"Personal best: {last_result.get('best', 0)}", FONT, WHITE, center=(WIDTH // 2, 260))
        retry.draw(screen)
        menu.draw(screen)
        pygame.display.flip()


def leaderboard_screen():
    """
    Leaderboard screen.
    Loads Top 10 scores from PostgreSQL.
    """
    back = Button((WIDTH // 2 - 90, HEIGHT - 58, 180, 42), "Back")

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if back.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

        board = get_leaderboard(10)

        screen.fill(DARK)
        draw_text("Leaderboard", BIG, WHITE, center=(WIDTH // 2, 45))
        draw_text("#   Username          Score   Level   Date", SMALL, WHITE, topleft=(35, 95))

        if not board:
            draw_text("No database results yet", FONT, WHITE, center=(WIDTH // 2, HEIGHT // 2))
        else:
            for i, row in enumerate(board, start=1):
                name, score, level, played_at = row
                date_text = played_at.strftime("%Y-%m-%d") if played_at else "-"
                line = f"{i:<2}  {name[:14]:<14}  {score:<6}  {level:<5}  {date_text}"
                draw_text(line, SMALL, WHITE, topleft=(35, 110 + i * 28))

        back.draw(screen)
        pygame.display.flip()


def settings_screen():
    """
    Settings screen.
    Saves preferences to settings.json:
    - snake color
    - grid overlay
    - sound on/off
    """
    global settings

    colors = [
        [0, 180, 0],
        [50, 120, 255],
        [230, 200, 50],
        [160, 60, 220],
        [220, 50, 50],
    ]

    grid_btn = Button((WIDTH // 2 - 130, 135, 260, 42), "")
    sound_btn = Button((WIDTH // 2 - 130, 195, 260, 42), "")
    color_btn = Button((WIDTH // 2 - 130, 255, 260, 42), "")
    save_btn = Button((WIDTH // 2 - 130, 330, 260, 42), "Save & Back")

    while True:
        clock.tick(60)
        grid_btn.text = f"Grid: {'On' if settings.get('grid', True) else 'Off'}"
        sound_btn.text = f"Sound: {'On' if settings.get('sound', True) else 'Off'}"
        color_btn.text = "Snake Color"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if grid_btn.clicked(event):
                settings["grid"] = not settings.get("grid", True)
            if sound_btn.clicked(event):
                settings["sound"] = not settings.get("sound", True)
            if color_btn.clicked(event):
                current = settings.get("snake_color", [0, 180, 0])
                idx = colors.index(current) if current in colors else 0
                settings["snake_color"] = colors[(idx + 1) % len(colors)]
            if save_btn.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                save_settings(settings)
                return

        screen.fill(DARK)
        draw_text("Settings", BIG, WHITE, center=(WIDTH // 2, 70))
        grid_btn.draw(screen)
        sound_btn.draw(screen)
        color_btn.draw(screen)
        save_btn.draw(screen)

        # Shows selected snake color as a preview block.
        pygame.draw.rect(screen, tuple(settings.get("snake_color", [0, 180, 0])), (WIDTH // 2 + 150, 260, 30, 30))
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 + 150, 260, 30, 30), 2)

        pygame.display.flip()


if __name__ == "__main__":
    # Try to initialize PostgreSQL tables when game starts.
    # If database is not configured yet, the game still opens,
    # but leaderboard saving/loading will print errors in terminal.
    init_db()
    main_menu()
