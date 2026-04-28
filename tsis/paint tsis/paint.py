import pygame
import math
from datetime import datetime
from pathlib import Path

from tools import (
    make_rect,
    distance,
    draw_square,
    draw_right_triangle,
    draw_equilateral_triangle,
    draw_rhombus,
    flood_fill,
)

# ------------------------------------------------------------
# Initialization
# ------------------------------------------------------------
pygame.init()

WIDTH, HEIGHT = 640, 480
TOOLBAR_HEIGHT = 40
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Application - TSIS2")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 18)
small_font = pygame.font.SysFont("Arial", 15)
text_font = pygame.font.SysFont("Arial", 28)

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
DARK_GRAY = (90, 90, 90)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

colors = {
    "red": RED,
    "green": GREEN,
    "blue": BLUE,
    "yellow": YELLOW,
    "black": BLACK,
}

# ------------------------------------------------------------
# Current drawing settings
# ------------------------------------------------------------
current_color = colors["blue"]

# The default tool is pencil because the new task requires freehand drawing.
tool = "pencil"

# Three required brush sizes: small, medium, large.
brush_sizes = {
    "small": 2,
    "medium": 5,
    "large": 10,
}
brush_size_name = "medium"
brush_size = brush_sizes[brush_size_name]

# ------------------------------------------------------------
# Canvas
# ------------------------------------------------------------
# The canvas is a separate surface. We draw permanently on it,
# then blit it onto the screen every frame.
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# The toolbar is drawn on top, so we keep it clean on the canvas too.
pygame.draw.rect(canvas, WHITE, (0, 0, WIDTH, TOOLBAR_HEIGHT))

# ------------------------------------------------------------
# Mouse and drawing state
# ------------------------------------------------------------
drawing = False
start_pos = None
last_pos = None
current_pos = None

# ------------------------------------------------------------
# Text tool state
# ------------------------------------------------------------
text_active = False
text_pos = None
text_value = ""

# ------------------------------------------------------------
# Save folder
# ------------------------------------------------------------
SAVE_DIR = Path(__file__).resolve().parent / "saves"
SAVE_DIR.mkdir(exist_ok=True)


def save_canvas():
    """Save the canvas as a PNG file with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = SAVE_DIR / f"paint_{timestamp}.png"

    # We save the canvas surface, not the whole screen.
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")


def set_tool(new_tool):
    """Change the active drawing tool."""
    global tool, text_active, text_value
    tool = new_tool

    # When switching tools, cancel unfinished text input.
    if new_tool != "text":
        text_active = False
        text_value = ""


def set_brush_size(name):
    """Switch brush size between small, medium and large."""
    global brush_size_name, brush_size
    brush_size_name = name
    brush_size = brush_sizes[name]


def draw_ui():
    """Draw the toolbar with current tool, color and shortcuts."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    color_name = "unknown"
    for name, value in colors.items():
        if value == current_color:
            color_name = name
            break

    text = (
        f"Tool: {tool.upper()} | Color: {color_name} | Size: {brush_size_name}({brush_size}px) | "
        "P Pencil L Line R Rect C Circle E Eraser F Fill T Text"
    )
    img = small_font.render(text, True, BLACK)
    screen.blit(img, (8, 5))

    text2 = "Practice11: S Square | G RightTri | Q EqTri | D Rhombus | 1/2/3 Size | 4-8 Colors | Ctrl+S Save | Space Clear"
    img2 = small_font.render(text2, True, BLACK)
    screen.blit(img2, (8, 22))

    # Show selected color as a small square.
    pygame.draw.rect(screen, current_color, (WIDTH - 32, 8, 22, 22))
    pygame.draw.rect(screen, BLACK, (WIDTH - 32, 8, 22, 22), 1)


def draw_shape(surface, shape_tool, start, end):
    """Draw the selected shape permanently or as a live preview."""
    if shape_tool == "line":
        pygame.draw.line(surface, current_color, start, end, brush_size)

    elif shape_tool == "rectangle":
        rect = make_rect(start, end)
        pygame.draw.rect(surface, current_color, rect, brush_size)

    elif shape_tool == "circle":
        circle_radius = distance(start, end)
        pygame.draw.circle(surface, current_color, start, circle_radius, brush_size)

    elif shape_tool == "square":
        draw_square(surface, current_color, start, end, brush_size)

    elif shape_tool == "right_triangle":
        draw_right_triangle(surface, current_color, start, end, brush_size)

    elif shape_tool == "equilateral_triangle":
        draw_equilateral_triangle(surface, current_color, start, end, brush_size)

    elif shape_tool == "rhombus":
        draw_rhombus(surface, current_color, start, end, brush_size)


def draw_text_preview():
    """Show typed text before it is permanently placed on the canvas."""
    if not text_active or text_pos is None:
        return

    # Blinking cursor effect.
    cursor_visible = (pygame.time.get_ticks() // 400) % 2 == 0
    shown_text = text_value + ("|" if cursor_visible else "")

    img = text_font.render(shown_text, True, current_color)
    screen.blit(img, text_pos)


def confirm_text():
    """Render typed text permanently onto the canvas."""
    global text_active, text_value, text_pos

    if text_active and text_pos is not None and text_value:
        img = text_font.render(text_value, True, current_color)
        canvas.blit(img, text_pos)

    text_active = False
    text_value = ""
    text_pos = None


def cancel_text():
    """Cancel current text input without drawing it."""
    global text_active, text_value, text_pos
    text_active = False
    text_value = ""
    text_pos = None


# ------------------------------------------------------------
# Main loop
# ------------------------------------------------------------
running = True

while running:
    for event in pygame.event.get():

        # ----------------------------------------------------
        # Quit event
        # ----------------------------------------------------
        if event.type == pygame.QUIT:
            running = False

        # ----------------------------------------------------
        # Keyboard controls
        # ----------------------------------------------------
        if event.type == pygame.KEYDOWN:

            # If text tool is active, keyboard writes text first.
            if text_active:
                if event.key == pygame.K_RETURN:
                    confirm_text()
                elif event.key == pygame.K_ESCAPE:
                    cancel_text()
                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]
                elif event.unicode and event.unicode.isprintable():
                    text_value += event.unicode
                continue

            # Ctrl + S saves the canvas as a PNG file.
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                save_canvas()

            # Tools from Practice 10 and the extended task.
            elif event.key == pygame.K_p:
                set_tool("pencil")
            elif event.key == pygame.K_l:
                set_tool("line")
            elif event.key == pygame.K_r:
                set_tool("rectangle")
            elif event.key == pygame.K_c:
                set_tool("circle")
            elif event.key == pygame.K_e:
                set_tool("eraser")
            elif event.key == pygame.K_f:
                set_tool("fill")
            elif event.key == pygame.K_t:
                set_tool("text")

            # Practice 11 shapes.
            elif event.key == pygame.K_s:
                set_tool("square")
            elif event.key == pygame.K_g:
                set_tool("right_triangle")
            elif event.key == pygame.K_q:
                set_tool("equilateral_triangle")
            elif event.key == pygame.K_d:
                set_tool("rhombus")

            # Brush size shortcuts: 1, 2, 3.
            elif event.key == pygame.K_1:
                set_brush_size("small")
            elif event.key == pygame.K_2:
                set_brush_size("medium")
            elif event.key == pygame.K_3:
                set_brush_size("large")

            # Color shortcuts: 4, 5, 6, 7, 8.
            elif event.key == pygame.K_4:
                current_color = colors["red"]
            elif event.key == pygame.K_5:
                current_color = colors["green"]
            elif event.key == pygame.K_6:
                current_color = colors["blue"]
            elif event.key == pygame.K_7:
                current_color = colors["yellow"]
            elif event.key == pygame.K_8:
                current_color = colors["black"]

            # Space clears the whole canvas.
            elif event.key == pygame.K_SPACE:
                canvas.fill(WHITE)

            # Escape exits the application.
            elif event.key == pygame.K_ESCAPE:
                running = False

        # ----------------------------------------------------
        # Mouse button down
        # ----------------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Left mouse button draws or starts a shape.
            if event.button == 1:
                mouse_pos = event.pos

                # Do not draw inside the toolbar.
                if mouse_pos[1] < TOOLBAR_HEIGHT:
                    continue

                # Fill tool fills a closed area immediately.
                if tool == "fill":
                    flood_fill(canvas, mouse_pos, current_color, TOOLBAR_HEIGHT)

                # Text tool starts text input at the clicked position.
                elif tool == "text":
                    text_active = True
                    text_pos = mouse_pos
                    text_value = ""

                # Pencil and eraser draw continuously while mouse is held.
                elif tool in ["pencil", "eraser"]:
                    drawing = True
                    start_pos = mouse_pos
                    last_pos = mouse_pos
                    current_pos = mouse_pos

                # Shape tools store the start position and draw on mouse release.
                else:
                    drawing = True
                    start_pos = mouse_pos
                    current_pos = mouse_pos

            # Mouse wheel can also change brush size.
            elif event.button == 4:
                if brush_size_name == "small":
                    set_brush_size("medium")
                elif brush_size_name == "medium":
                    set_brush_size("large")

            elif event.button == 5:
                if brush_size_name == "large":
                    set_brush_size("medium")
                elif brush_size_name == "medium":
                    set_brush_size("small")

        # ----------------------------------------------------
        # Mouse button up
        # ----------------------------------------------------
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                end_pos = event.pos

                # Final drawing for shape tools.
                if tool in [
                    "line",
                    "rectangle",
                    "circle",
                    "square",
                    "right_triangle",
                    "equilateral_triangle",
                    "rhombus",
                ]:
                    draw_shape(canvas, tool, start_pos, end_pos)

        # ----------------------------------------------------
        # Mouse motion
        # ----------------------------------------------------
        if event.type == pygame.MOUSEMOTION:
            current_pos = event.pos

            if drawing:
                # Pencil draws connected lines between previous and current position.
                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                    last_pos = event.pos

                # Eraser draws white lines.
                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, event.pos, brush_size * 2)
                    last_pos = event.pos

    # --------------------------------------------------------
    # Drawing frame
    # --------------------------------------------------------
    screen.blit(canvas, (0, 0))

    # Live preview for shape tools while dragging.
    if drawing and start_pos is not None and current_pos is not None:
        if tool in [
            "line",
            "rectangle",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus",
        ]:
            draw_shape(screen, tool, start_pos, current_pos)

    # Live preview for text tool.
    draw_text_preview()

    # Toolbar is drawn last so it stays visible.
    draw_ui()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
