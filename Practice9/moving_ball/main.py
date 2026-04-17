import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Moving Ball")

x,y = 400, 300
radius = 25
speed = 20

running = True
while running:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x - speed - radius >= 0:
        x -= speed
    if keys[pygame.K_RIGHT] and x + speed + radius <= 800:
        x += speed
    if keys[pygame.K_UP] and y - speed - radius >= 0:
        y -= speed
    if keys[pygame.K_DOWN] and y + speed + radius <= 600:
        y += speed
    
    pygame.draw.circle(screen, (255, 0, 0), (x,y), radius)

    clock = pygame.time.Clock()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()