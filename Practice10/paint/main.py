import pygame
import math

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 18)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)

colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "black": (0, 0, 0)
}

current_color = colors["blue"]
tool = "brush"
radius = 8

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

drawing = False
start_pos = None
last_pos = None
current_pos = None


def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 40))

    text = f"Tool: {tool.upper()} | Size: {radius} | P Brush | R Rect | C Circle | E Eraser | 1-5 Colors | SPACE Clear"
    img = font.render(text, True, BLACK)
    screen.blit(img, (10, 10))


running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rectangle"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"

            elif event.key == pygame.K_1:
                current_color = colors["red"]
            elif event.key == pygame.K_2:
                current_color = colors["green"]
            elif event.key == pygame.K_3:
                current_color = colors["blue"]
            elif event.key == pygame.K_4:
                current_color = colors["yellow"]
            elif event.key == pygame.K_5:
                current_color = colors["black"]

            elif event.key == pygame.K_SPACE:
                canvas.fill(WHITE)

            elif event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos
                current_pos = event.pos

            elif event.button == 3:
                radius = max(1, radius - 1)

            elif event.button == 4:
                radius += 1

            elif event.button == 5:
                radius = max(1, radius - 1)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                end_pos = event.pos

                if tool == "rectangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    rect = pygame.Rect(
                        min(x1, x2),
                        min(y1, y2),
                        abs(x2 - x1),
                        abs(y2 - y1)
                    )

                    pygame.draw.rect(canvas, current_color, rect, radius)

                elif tool == "circle":  
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    circle_radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                    pygame.draw.circle(canvas, current_color, start_pos, circle_radius, radius)

        if event.type == pygame.MOUSEMOTION:
            current_pos = event.pos

            if drawing:
                if tool == "brush":
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, radius)
                    last_pos = event.pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, event.pos, radius * 2)
                    last_pos = event.pos

    screen.blit(canvas, (0, 0))

    # Preview rectangle and circle before placing
    if drawing and tool == "rectangle":
        x1, y1 = start_pos
        x2, y2 = current_pos

        preview_rect = pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            abs(x2 - x1),
            abs(y2 - y1)
        )

        pygame.draw.rect(screen, current_color, preview_rect, radius)

    elif drawing and tool == "circle":
        x1, y1 = start_pos
        x2, y2 = current_pos

        preview_radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        pygame.draw.circle(screen, current_color, start_pos, preview_radius, radius)

    draw_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()