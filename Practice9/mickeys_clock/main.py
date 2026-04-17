import pygame
import time

pygame.init()

screen = pygame.display.set_mode((700, 700))
bg = pygame.image.load("mickey.jpg")
bg = pygame.transform.scale(bg, (700, 700))
clock = pygame.time.Clock()

left_hand = pygame.image.load("1.png").convert_alpha()
right_hand = pygame.image.load("2.png").convert_alpha()

center = (350,350)

running = True
while running:
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = time.localtime()

    seconds = t.tm_sec
    minutes = t.tm_min

    sec_angle = -seconds * 6
    min_angle = -minutes * 6

    sec_hand = pygame.transform.rotate(left_hand, sec_angle)
    min_hand = pygame.transform.rotate(right_hand, min_angle)  

    screen.blit(sec_hand, sec_hand.get_rect(center=center))
    screen.blit(min_hand, min_hand.get_rect(center=center)) 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()