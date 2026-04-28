# ui.py
# This file contains simple UI helper code.
# It does not use external UI libraries.
# It creates buttons and draws text for menus, settings, leaderboard, and game over screens.

import pygame

# Common colors used by UI screens.
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (70, 70, 70)
LIGHT = (215, 215, 215)
BLUE = (40, 110, 220)


class Button:
    """
    Simple button class for Pygame.

    Each button has:
    - rectangle area
    - text
    - font
    - background color
    - text color
    """

    def __init__(self, rect, text, font, bg=LIGHT, fg=BLACK):
        # Convert tuple/list into pygame.Rect.
        # rect example: (x, y, width, height)
        self.rect = pygame.Rect(rect)

        # Text displayed inside button.
        self.text = text

        # Font used to render text.
        self.font = font

        # Button background color.
        self.bg = bg

        # Button text color.
        self.fg = fg

    def draw(self, surf):
        """
        Draws the button on a given surface.
        Also changes color when mouse is over the button.
        """
        # Get current mouse position.
        mouse = pygame.mouse.get_pos()

        # If mouse is over button, use BLUE color.
        # Otherwise use normal background color.
        color = self.bg if not self.rect.collidepoint(mouse) else BLUE

        # Draw button body.
        pygame.draw.rect(surf, color, self.rect, border_radius=10)

        # Draw button border.
        pygame.draw.rect(surf, BLACK, self.rect, 2, border_radius=10)

        # Render button text.
        # If button is blue on hover, text becomes white.
        label = self.font.render(self.text, True, self.fg if color != BLUE else WHITE)

        # Put text exactly in the center of the button.
        surf.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        """
        Returns True if player clicked this button with left mouse button.
        """
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def draw_text(surf, text, font, color, center=None, topleft=None):
    """
    Helper function to draw text.

    center  -> draw text by center position
    topleft -> draw text by top-left position
    """
    # Convert text to string and render it.
    img = font.render(str(text), True, color)

    # Get rectangle of rendered text.
    rect = img.get_rect()

    # Place text by center if center argument is passed.
    if center:
        rect.center = center

    # Place text by top-left corner if topleft argument is passed.
    if topleft:
        rect.topleft = topleft

    # Draw text on the screen.
    surf.blit(img, rect)

    # Return rect in case we need it later.
    return rect
