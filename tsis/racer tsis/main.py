# main.py
# This is the entry point of the game.
# It creates the Pygame window and controls all screens:
# - username input
# - main menu
# - leaderboard
# - settings
# - game over
# - starting RacerGame from racer.py

import pygame
import sys
from persistence import load_settings, save_settings, load_leaderboard
from racer import RacerGame, WIDTH, HEIGHT, CAR_COLORS
from ui import Button, draw_text, WHITE, BLACK

# Initialize all Pygame modules.
pygame.init()

# Create game window using width and height from racer.py.
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Window title.
pygame.display.set_caption("Arcade Racer")

# Clock controls menu FPS.
CLOCK = pygame.time.Clock()

# Fonts used in screens.
FONT = pygame.font.SysFont("Verdana", 20)
SMALL = pygame.font.SysFont("Verdana", 16)
BIG = pygame.font.SysFont("Verdana", 42)

# Load settings from settings.json at startup.
settings = load_settings()

# Default username before player enters a name.
username = "Player"

# This variable is kept for possible future stats usage.
last_stats = None


def quit_game():
    """
    Fully closes the game.
    """
    pygame.quit()
    sys.exit()


def ask_username():
    """
    Username input screen.
    Player types a name before starting the run.
    The name is later used in leaderboard.
    """
    global username

    # Text typed by player.
    text = ""

    while True:
        # Limit FPS to 60.
        CLOCK.tick(60)

        # Process events.
        for event in pygame.event.get():
            # Close window.
            if event.type == pygame.QUIT:
                quit_game()

            # Keyboard input.
            if event.type == pygame.KEYDOWN:
                # Enter starts game if name is not empty.
                if event.key == pygame.K_RETURN and text.strip():
                    username = text.strip()[:12]
                    return

                # Backspace deletes one character.
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                # Add printable characters, maximum 12 symbols.
                elif len(text) < 12 and event.unicode.isprintable():
                    text += event.unicode

        # Draw background.
        SCREEN.fill(WHITE)

        # Draw title.
        draw_text(SCREEN, "Enter username", BIG, BLACK, center=(WIDTH // 2, 180))

        # Draw input box.
        pygame.draw.rect(SCREEN, (230, 230, 230), (70, 270, 260, 46), border_radius=8)
        pygame.draw.rect(SCREEN, BLACK, (70, 270, 260, 46), 2, border_radius=8)

        # Draw typed name or default placeholder.
        draw_text(SCREEN, text or "Player", FONT, BLACK, center=(WIDTH // 2, 293))

        # Draw hint.
        draw_text(SCREEN, "Press Enter to start", SMALL, BLACK, center=(WIDTH // 2, 350))

        # Update screen.
        pygame.display.flip()


def main_menu():
    """
    Main Menu screen.
    Buttons:
    - Play
    - Leaderboard
    - Settings
    - Quit
    """
    # Create menu buttons.
    buttons = [
        Button((100, 210, 200, 45), "Play", FONT),
        Button((100, 270, 200, 45), "Leaderboard", FONT),
        Button((100, 330, 200, 45), "Settings", FONT),
        Button((100, 390, 200, 45), "Quit", FONT),
    ]

    while True:
        # Limit menu FPS.
        CLOCK.tick(60)

        # Process events.
        for event in pygame.event.get():
            # Close window.
            if event.type == pygame.QUIT:
                quit_game()

            # Play button.
            if buttons[0].clicked(event):
                # Ask username first.
                ask_username()

                # Start the gameplay.
                result = RacerGame(SCREEN, settings, username).run()

                # If gameplay says quit, close the game.
                if result == "quit":
                    quit_game()

                # After run ends, show Game Over screen.
                game_over_screen()

            # Leaderboard button.
            if buttons[1].clicked(event):
                leaderboard_screen()

            # Settings button.
            if buttons[2].clicked(event):
                settings_screen()

            # Quit button.
            if buttons[3].clicked(event):
                quit_game()

        # Draw menu background.
        SCREEN.fill(WHITE)

        # Draw game title.
        draw_text(SCREEN, "Arcade Racer", BIG, BLACK, center=(WIDTH // 2, 130))

        # Draw all buttons.
        for b in buttons:
            b.draw(SCREEN)

        # Update display.
        pygame.display.flip()


def leaderboard_screen():
    """
    Leaderboard screen.
    Shows top 10 saved scores from leaderboard.json.
    """
    # Back button.
    back = Button((120, 525, 160, 42), "Back", FONT)

    while True:
        CLOCK.tick(60)

        # Process events.
        for event in pygame.event.get():
            # Close window.
            if event.type == pygame.QUIT:
                quit_game()

            # Back button or ESC returns to previous screen.
            if back.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

        # Draw background.
        SCREEN.fill(WHITE)

        # Draw title.
        draw_text(SCREEN, "Top 10", BIG, BLACK, center=(WIDTH // 2, 55))

        # Load leaderboard from JSON.
        board = load_leaderboard()

        # Draw table header.
        headers = "#  Name        Score   Dist"
        draw_text(SCREEN, headers, SMALL, BLACK, topleft=(30, 105))

        # Draw each leaderboard row.
        for i, row in enumerate(board[:10], 1):
            line = f"{i:<2} {row['name']:<10} {row['score']:<7} {row['distance']}m"
            draw_text(SCREEN, line, SMALL, BLACK, topleft=(30, 130 + i * 34))

        # Message if leaderboard is empty.
        if not board:
            draw_text(SCREEN, "No scores yet", FONT, BLACK, center=(WIDTH // 2, 250))

        # Draw back button.
        back.draw(SCREEN)

        # Update display.
        pygame.display.flip()


def settings_screen():
    """
    Settings screen.
    Player can change:
    - sound on/off
    - car color
    - difficulty

    Every change is saved immediately to settings.json.
    """
    global settings

    # Available car colors from racer.py.
    colors = list(CAR_COLORS.keys())

    # Available difficulty levels.
    diffs = ["easy", "normal", "hard"]

    # Create buttons.
    buttons = {
        "sound": Button((85, 180, 230, 42), "", FONT),
        "color": Button((85, 245, 230, 42), "", FONT),
        "difficulty": Button((85, 310, 230, 42), "", FONT),
        "back": Button((120, 500, 160, 42), "Back", FONT),
    }

    while True:
        CLOCK.tick(60)

        # Update button text every frame because settings can change.
        buttons["sound"].text = f"Sound: {'On' if settings['sound'] else 'Off'}"
        buttons["color"].text = f"Car: {settings['car_color']}"
        buttons["difficulty"].text = f"Difficulty: {settings['difficulty']}"

        # Process events.
        for event in pygame.event.get():
            # Close window.
            if event.type == pygame.QUIT:
                quit_game()

            # Toggle sound and save settings.
            if buttons["sound"].clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            # Switch car color and save settings.
            if buttons["color"].clicked(event):
                idx = (colors.index(settings["car_color"]) + 1) % len(colors)
                settings["car_color"] = colors[idx]
                save_settings(settings)

            # Switch difficulty and save settings.
            if buttons["difficulty"].clicked(event):
                idx = (diffs.index(settings["difficulty"]) + 1) % len(diffs)
                settings["difficulty"] = diffs[idx]
                save_settings(settings)

            # Back button or ESC returns to menu.
            if buttons["back"].clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

        # Draw background.
        SCREEN.fill(WHITE)

        # Draw title.
        draw_text(SCREEN, "Settings", BIG, BLACK, center=(WIDTH // 2, 95))

        # Draw all buttons.
        for b in buttons.values():
            b.draw(SCREEN)

        # Update display.
        pygame.display.flip()


def game_over_screen():
    """
    Game Over screen.
    Shows latest result and gives two buttons:
    - Retry
    - Main Menu
    """
    # Create buttons.
    retry = Button((95, 365, 210, 45), "Retry", FONT)
    menu = Button((95, 430, 210, 45), "Main Menu", FONT)

    # Load leaderboard.
    board = load_leaderboard()

    # Current result is taken from top board entry.
    # This works because add_score sorts leaderboard by score.
    current = board[0] if board else {"score": 0, "distance": 0, "coins": 0}

    while True:
        CLOCK.tick(60)

        # Process events.
        for event in pygame.event.get():
            # Close window.
            if event.type == pygame.QUIT:
                quit_game()

            # Retry starts a new run with same username/settings.
            if retry.clicked(event):
                result = RacerGame(SCREEN, settings, username).run()
                if result == "quit":
                    quit_game()
                return game_over_screen()

            # Main Menu button returns to main menu.
            if menu.clicked(event):
                return

        # Draw red background for game over.
        SCREEN.fill((235, 80, 80))

        # Draw title and stats.
        draw_text(SCREEN, "Game Over", BIG, BLACK, center=(WIDTH // 2, 120))
        draw_text(SCREEN, f"Name: {username}", FONT, BLACK, center=(WIDTH // 2, 205))
        draw_text(SCREEN, f"Score: {current.get('score', 0)}", FONT, BLACK, center=(WIDTH // 2, 240))
        draw_text(SCREEN, f"Distance: {current.get('distance', 0)}m", FONT, BLACK, center=(WIDTH // 2, 275))
        draw_text(SCREEN, f"Coins: {current.get('coins', 0)}", FONT, BLACK, center=(WIDTH // 2, 310))

        # Draw buttons.
        retry.draw(SCREEN)
        menu.draw(SCREEN)

        # Update display.
        pygame.display.flip()


# This condition means main_menu() starts only when we run main.py directly.
# It does not run automatically if this file is imported somewhere else.
if __name__ == "__main__":
    main_menu()
