# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initialize pygame
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)

# Screen and game variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Loading background image
background = pygame.image.load("racer/AnimatedStreet.png")

# Creating screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer Game")


class Enemy(pygame.sprite.Sprite):
    """Enemy car that moves down the road."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer/Enemy.png")
        self.rect = self.image.get_rect()

        # Enemy starts at a random x position at the top of the screen
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """Move enemy down. If it leaves the screen, reset it."""
        global SCORE

        self.rect.move_ip(0, SPEED)

        # If enemy reaches bottom, increase score and move it back to top
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    """Player car controlled by left and right arrow keys."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer/Player.png")
        self.rect = self.image.get_rect()

        # Starting position of player
        self.rect.center = (160, 520)

    def move(self):
        """Move player left and right."""
        pressed_keys = pygame.key.get_pressed()

        # Move left only if player is inside screen
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        # Move right only if player is inside screen
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    """Coin that appears randomly on the road and moves down."""

    def __init__(self):
        super().__init__()

        # Create coin image using a yellow circle
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (12, 12), 12)
        pygame.draw.circle(self.image, WHITE, (12, 12), 6, 2)

        self.rect = self.image.get_rect()

        # Coin appears at random x position on the road
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """Move coin down and delete it if it leaves the screen."""
        self.rect.move_ip(0, SPEED) #move in place

        # Remove coin if it goes below the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Creating player and enemy
P1 = Player()
E1 = Enemy()

# Creating sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Custom event for increasing speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Custom event for creating coins
ADD_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_COIN, 1500)


# Main game loop
while True:

    # Event handling
    for event in pygame.event.get():

        # Increase speed every second
        if event.type == INC_SPEED:
            SPEED += 0.5

        # Create a new coin every 1.5 seconds
        if event.type == ADD_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

        # Quit game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Show score in top left corner
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Show collected coins in top right corner
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    coin_rect = coin_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    DISPLAYSURF.blit(coin_text, coin_rect)

    # Move and draw all sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Check collision between player and coins
    collected = pygame.sprite.spritecollide(P1, coins, True)

    # If player collected coins, increase coin counter
    if collected:
        COINS += len(collected)

    # Check collision between player and enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("racer/crash.wav").play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()

        # Remove all sprites from groups
        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Update display
    pygame.display.update()

    # Limit FPS
    FramePerSec.tick(FPS)