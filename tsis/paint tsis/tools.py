import pygame
import math
from collections import deque


def make_rect(start_pos, end_pos):
    """Create a pygame.Rect from two mouse positions."""
    x1, y1 = start_pos
    x2, y2 = end_pos
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))


def distance(p1, p2):
    """Return distance between two points."""
    x1, y1 = p1
    x2, y2 = p2
    return int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


def draw_square(surface, color, start_pos, end_pos, width):
    """Draw a square. The side length is based on the bigger mouse movement."""
    x1, y1 = start_pos
    x2, y2 = end_pos
    side = max(abs(x2 - x1), abs(y2 - y1))
    if x2 < x1:
        side = -side
    rect = pygame.Rect(x1, y1, side, side)
    rect.normalize()
    pygame.draw.rect(surface, color, rect, width)


def draw_right_triangle(surface, color, start_pos, end_pos, width):
    """Draw a right triangle inside the rectangle made by drag start/end."""
    x1, y1 = start_pos
    x2, y2 = end_pos
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, start_pos, end_pos, width):
    """Draw an equilateral-like triangle using drag width as triangle size."""
    x1, y1 = start_pos
    x2, y2 = end_pos
    side = max(abs(x2 - x1), abs(y2 - y1))
    direction = 1 if y2 >= y1 else -1
    half = side // 2
    height = int(side * math.sqrt(3) / 2)
    points = [(x1, y1), (x1 - half, y1 + direction * height), (x1 + half, y1 + direction * height)]
    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, start_pos, end_pos, width):
    """Draw a rhombus/diamond shape using the drag rectangle."""
    x1, y1 = start_pos
    x2, y2 = end_pos
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    points = [(center_x, y1), (x2, center_y), (center_x, y2), (x1, center_y)]
    pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start_pos, fill_color, protected_height=40):
    """Flood-fill tool implemented with get_at() and set_at().

    It fills all connected pixels with the same exact color as the clicked pixel.
    The protected_height parameter prevents filling the toolbar area.
    """
    width, height = surface.get_size()
    x, y = start_pos

    if x < 0 or x >= width or y < protected_height or y >= height:
        return

    target_color = surface.get_at((x, y))
    fill_color = pygame.Color(*fill_color)

    if target_color == fill_color:
        return

    queue = deque([(x, y)])
    visited = set()

    while queue:
        px, py = queue.popleft()

        if (px, py) in visited:
            continue
        visited.add((px, py))

        if px < 0 or px >= width or py < protected_height or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))
