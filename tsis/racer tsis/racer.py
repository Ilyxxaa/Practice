# racer.py
# This file contains the main gameplay of the Arcade Racer game.
# It includes:
# - player car
# - traffic cars
# - weighted coins from Practice 11
# - obstacles
# - power-ups
# - dynamic road events
# - score, distance, difficulty scaling
# - saving result to leaderboard

import pygame
import random
import math
from pathlib import Path
from persistence import DIFFICULTY, add_score

# Game window size.
WIDTH, HEIGHT = 400, 600

# Frames per second.
FPS = 60

# X positions of road lanes.
# Objects spawn in these lanes.
LANES = [80, 160, 240, 320]

# Finish distance in meters.
FINISH_DISTANCE = 5000

# Colors used for drawing simple objects and HUD.
BLACK = (20, 20, 20)
WHITE = (245, 245, 245)
ROAD = (55, 55, 55)
YELLOW = (255, 220, 0)
RED = (220, 50, 50)
GREEN = (40, 180, 80)
BLUE = (45, 105, 230)
ORANGE = (255, 150, 30)
PURPLE = (150, 70, 220)
CYAN = (40, 220, 230)
GRAY = (120, 120, 120)

# Path to folder with old assets.
# You need to put your old files here:
# racer/AnimatedStreet.png
# racer/Player.png
# racer/Enemy.png
# racer/crash.wav
ASSET_DIR = Path(__file__).resolve().parent / "racer"

# Available car colors in Settings screen.
# They are used as a light tint over Player.png.
CAR_COLORS = {
    "blue": BLUE,
    "red": RED,
    "green": GREEN,
    "yellow": YELLOW,
    "purple": PURPLE,
}


class Player(pygame.sprite.Sprite):
    """
    Player car class.

    Responsibilities:
    - load player image
    - apply color from settings
    - move left/right
    - stay inside road boundaries
    """

    def __init__(self, color_name):
        super().__init__()

        # Load original player image from old Practice 10 assets.
        self.original_image = pygame.image.load(ASSET_DIR / "Player.png").convert_alpha()

        # Copy original image before tinting it.
        self.image = self.original_image.copy()

        # Apply selected car color from settings.
        self.apply_color(color_name)

        # Put player near the bottom of the screen.
        self.rect = self.image.get_rect(center=(LANES[1], HEIGHT - 75))

        # Horizontal movement speed.
        self.speed = 6

        # Crash counter is used by repair power-up logic.
        self.crashes = 0

    def apply_color(self, color_name):
        """
        Applies selected color to Player.png.
        This does not replace the image, it only adds a light tint.
        """
        # Get RGB color from dictionary. If wrong color, use blue.
        color = CAR_COLORS.get(color_name, BLUE)

        # Create transparent surface the same size as player image.
        tint = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)

        # Fill it with selected color and low alpha value.
        # Alpha 45 means the tint is light, so original PNG is still visible.
        tint.fill((*color, 45))

        # Reset image to original before applying tint.
        self.image = self.original_image.copy()

        # Add tint to image.
        self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    def update(self, keys):
        """
        Updates player movement every frame.
        Player can move with arrows or A/D keys.
        """
        # Move left.
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        # Move right.
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Keep player inside road/screen boundaries.
        self.rect.clamp_ip(pygame.Rect(35, 0, WIDTH - 70, HEIGHT))


class FallingSprite(pygame.sprite.Sprite):
    """
    Base class for all objects that move from top to bottom.

    Used by:
    - traffic cars
    - coins
    - obstacles
    - power-ups
    - dynamic road events
    """

    def __init__(self, lane, y, speed):
        super().__init__()

        # Extra speed of this object.
        self.base_speed = speed

        # Default rectangle. Child classes usually replace it with image rect.
        self.rect = pygame.Rect(0, 0, 30, 30)

        # Place object in selected lane and y position.
        self.rect.center = (lane, y)

    def update(self, game_speed):
        """
        Moves object down according to current game speed.
        Removes object if it leaves the screen.
        """
        self.rect.y += game_speed + self.base_speed

        # Delete sprite when it goes below the screen.
        if self.rect.top > HEIGHT + 60:
            self.kill()


class TrafficCar(FallingSprite):
    """
    Enemy traffic car.
    If player collides with it, the run ends unless shield is active.
    """

    def __init__(self, lane, speed):
        super().__init__(lane, -90, speed)

        # Load enemy car image from old assets.
        self.image = pygame.image.load(ASSET_DIR / "Enemy.png").convert_alpha()

        # Put enemy car above the screen so it drives into view.
        self.rect = self.image.get_rect(center=(lane, -60))


class Coin(FallingSprite):
    """
    Weighted coin class from Practice 11.

    Coin can have value 1, 2, or 5.
    Higher value gives more score.
    """

    def __init__(self, lane, value, speed):
        super().__init__(lane, -30, speed)

        # Coin value: 1, 2, or 5.
        self.value = value

        # Bigger value creates a bigger coin.
        radius = 10 + value * 2

        # Create coin image with transparent background.
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        # Draw yellow coin circle.
        pygame.draw.circle(self.image, YELLOW, (radius, radius), radius)

        # Draw white inner circle.
        pygame.draw.circle(self.image, WHITE, (radius, radius), radius // 2, 2)

        # Draw coin value number on the coin.
        txt = pygame.font.SysFont("Verdana", 12).render(str(value), True, BLACK)
        self.image.blit(txt, txt.get_rect(center=(radius, radius)))

        # Set coin rectangle.
        self.rect = self.image.get_rect(center=(lane, -25))


class Obstacle(FallingSprite):
    """
    Road obstacle class.

    kind can be:
    - oil      -> moves player sideways but does not end game
    - pothole  -> dangerous collision
    - barrier  -> dangerous collision
    """

    def __init__(self, lane, kind, speed):
        super().__init__(lane, -40, speed)

        # Save obstacle type.
        self.kind = kind

        # Create image for obstacle.
        self.image = pygame.Surface((58, 32), pygame.SRCALPHA)

        # Draw oil spill.
        if kind == "oil":
            pygame.draw.ellipse(self.image, BLACK, (4, 7, 50, 18))
            pygame.draw.ellipse(self.image, GRAY, (16, 10, 18, 7))

        # Draw pothole.
        elif kind == "pothole":
            pygame.draw.ellipse(self.image, (45, 30, 20), (5, 3, 48, 24))
            pygame.draw.ellipse(self.image, BLACK, (14, 8, 28, 12))

        # Draw barrier.
        else:
            pygame.draw.rect(self.image, RED, (2, 8, 54, 18), border_radius=4)
            pygame.draw.rect(self.image, WHITE, (8, 12, 42, 6))

        # Set rectangle for collision and drawing.
        self.rect = self.image.get_rect(center=(lane, -35))


class PowerUp(FallingSprite):
    """
    Collectible power-up class.

    Types:
    - nitro  -> temporary speed boost
    - shield -> protects from one collision
    - repair -> clears one obstacle / repairs crash
    """

    def __init__(self, lane, kind, speed):
        super().__init__(lane, -35, speed)

        # Save power-up type.
        self.kind = kind

        # Time when power-up was spawned.
        self.spawn_time = pygame.time.get_ticks()

        # Power-up disappears after 7 seconds if not collected.
        self.timeout = 7000

        # Create power-up image.
        self.image = pygame.Surface((34, 34), pygame.SRCALPHA)

        # Color depends on power-up type.
        colors = {"nitro": CYAN, "shield": BLUE, "repair": GREEN}
        pygame.draw.circle(self.image, colors[kind], (17, 17), 16)

        # Letter shown inside power-up.
        letter = {"nitro": "N", "shield": "S", "repair": "+"}[kind]
        txt = pygame.font.SysFont("Verdana", 18, True).render(letter, True, WHITE)
        self.image.blit(txt, txt.get_rect(center=(17, 17)))

        # Set rectangle.
        self.rect = self.image.get_rect(center=(lane, -30))

    def update(self, game_speed):
        """
        Moves power-up down and removes it after timeout.
        """
        # Use normal falling movement from parent class.
        super().update(game_speed)

        # Remove power-up if player does not collect it in time.
        if pygame.time.get_ticks() - self.spawn_time > self.timeout:
            self.kill()


class NitroStrip(FallingSprite):
    """
    Dynamic road event.
    Nitro strip is placed on the road and gives nitro when touched.
    """

    def __init__(self, lane, speed):
        super().__init__(lane, -40, speed)

        # Create image for nitro strip.
        self.image = pygame.Surface((62, 28), pygame.SRCALPHA)
        pygame.draw.rect(self.image, CYAN, (0, 0, 62, 28), border_radius=5)

        # Draw arrows on strip.
        pygame.draw.polygon(self.image, WHITE, [(10, 6), (28, 14), (10, 22)])
        pygame.draw.polygon(self.image, WHITE, [(32, 6), (50, 14), (32, 22)])

        # Set rectangle.
        self.rect = self.image.get_rect(center=(lane, -30))


class MovingBarrier(FallingSprite):
    """
    Dynamic moving barrier.
    It moves down and also slightly left-right using sine wave.
    """

    def __init__(self, lane, speed):
        super().__init__(lane, -40, speed)

        # Create barrier image.
        self.image = pygame.Surface((62, 24), pygame.SRCALPHA)
        pygame.draw.rect(self.image, ORANGE, (0, 0, 62, 24), border_radius=4)
        pygame.draw.rect(self.image, BLACK, (0, 10, 62, 4))

        # Set rectangle.
        self.rect = self.image.get_rect(center=(lane, -35))

        # Random phase makes each moving barrier move differently.
        self.phase = random.random() * math.pi

    def update(self, game_speed):
        """
        Moves barrier down and left-right.
        """
        # Move down using parent update.
        super().update(game_speed)

        # Add horizontal movement using sine function.
        self.rect.x += int(math.sin(pygame.time.get_ticks() / 250 + self.phase) * 3)

        # Keep barrier inside road boundaries.
        self.rect.clamp_ip(pygame.Rect(35, -100, WIDTH - 70, HEIGHT + 160))


class RacerGame:
    """
    Main gameplay class.

    It controls:
    - game loop
    - object spawning
    - movement
    - collisions
    - power-ups
    - score
    - distance
    - saving final result
    """

    def __init__(self, screen, settings, username):
        # Screen is created in main.py and passed here.
        self.screen = screen

        # Settings loaded from settings.json.
        self.settings = settings

        # Username entered before starting game.
        self.username = username

        # Clock controls FPS.
        self.clock = pygame.time.Clock()

        # Fonts for HUD and messages.
        self.font = pygame.font.SysFont("Verdana", 18)
        self.big = pygame.font.SysFont("Verdana", 42)

        # Load old road background image.
        self.background = pygame.image.load(ASSET_DIR / "AnimatedStreet.png").convert()

        # Scale background to window size.
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Load crash sound from old assets.
        self.crash_sound = pygame.mixer.Sound(ASSET_DIR / "crash.wav")

        # Create player with selected car color.
        self.player = Player(settings["car_color"])

        # Group with all sprites for drawing/updating.
        self.all = pygame.sprite.Group(self.player)

        # Separate groups are used for collision logic.
        self.traffic = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.events = pygame.sprite.Group()

        # Get difficulty parameters from persistence.py.
        params = DIFFICULTY[settings["difficulty"]]

        # Base game speed depends on selected difficulty.
        self.base_speed = params["speed"]
        self.speed = self.base_speed

        # Spawn rates depend on selected difficulty.
        self.traffic_rate = params["traffic"]
        self.obstacle_rate = params["obstacles"]

        # Game stats.
        self.distance = 0
        self.coins_count = 0
        self.coin_score = 0
        self.score = 0

        # Power-up state.
        self.active_power = None
        self.power_end = 0
        self.shield = False

        # Background scroll position.
        self.road_y = 0

        # Finish and save flags.
        self.finished = False
        self.saved = False

    def safe_lane(self):
        """
        Chooses a lane that is not directly on top of the player.
        This is safe spawn logic.
        """
        # Find lane closest to player.
        player_lane = min(LANES, key=lambda x: abs(x - self.player.rect.centerx))

        # Choose lanes that are not too close to player lane.
        lanes = [lane for lane in LANES if abs(lane - player_lane) > 45]

        # Return random safe lane.
        # If no safe lane exists, use any lane as fallback.
        return random.choice(lanes or LANES)

    def occupied(self, lane):
        """
        Checks if top part of selected lane already has an object.
        This prevents objects from spawning on top of each other.
        """
        # Check every object group.
        for group in [self.traffic, self.obstacles, self.events, self.powerups, self.coins]:
            for spr in group:
                # If object is in same lane and near top, lane is occupied.
                if abs(spr.rect.centerx - lane) < 35 and spr.rect.top < 95:
                    return True
        return False

    def spawn(self, cls, group, *args):
        """
        Universal spawn function.

        cls   -> class to create, for example Coin or TrafficCar
        group -> sprite group where object will be added
        args  -> extra arguments for object constructor
        """
        # Choose safe lane first.
        lane = self.safe_lane()

        # Do not spawn if that lane is already occupied.
        if self.occupied(lane):
            return

        # Create object.
        item = cls(lane, *args)

        # Add object to its own group.
        group.add(item)

        # Add object to all sprites group for drawing/updating.
        self.all.add(item)

    def scale(self):
        """
        Difficulty scaling.
        As distance increases, speed and spawn rates increase.
        """
        # Every 1000 meters increases difficulty.
        progress = self.distance / 1000

        # Increase speed by progress.
        self.speed = self.base_speed + progress * 0.45

        # Slowly increase traffic and obstacle frequency.
        self.traffic_rate += 0.000003
        self.obstacle_rate += 0.000002

    def draw_road(self):
        """
        Draws scrolling road background using original AnimatedStreet.png.
        """
        # Current scroll position.
        y = int(self.road_y)

        # Draw two copies of background to create infinite scrolling effect.
        self.screen.blit(self.background, (0, y - HEIGHT))
        self.screen.blit(self.background, (0, y))

        # Move road down.
        self.road_y = (self.road_y + self.speed) % HEIGHT

    def activate_power(self, kind):
        """
        Activates collected power-up.

        Rule: only one active power-up at a time.
        """
        # Store active power-up name.
        self.active_power = kind

        # Current time in milliseconds.
        now = pygame.time.get_ticks()

        # Nitro gives temporary speed boost for 4 seconds.
        if kind == "nitro":
            self.power_end = now + 4000
            self.shield = False

        # Shield protects from one collision.
        elif kind == "shield":
            self.power_end = 0
            self.shield = True

        # Repair is instant.
        # It reduces crash counter and clears nearest obstacle.
        elif kind == "repair":
            self.player.crashes = max(0, self.player.crashes - 1)

            # Find nearest obstacle to player.
            nearest = None
            for obs in list(self.obstacles):
                if nearest is None or obs.rect.y > nearest.rect.y:
                    nearest = obs

            # Remove nearest obstacle if it exists.
            if nearest:
                nearest.kill()

            # Repair does not stay active.
            self.active_power = None
            self.power_end = 0

    def collide_danger(self):
        """
        Handles collisions with dangerous objects.

        Returns True if game should end.
        Returns False if collision was handled safely.
        """
        # Check collision with traffic, obstacles, and dynamic events.
        hit = (
            pygame.sprite.spritecollideany(self.player, self.traffic)
            or pygame.sprite.spritecollideany(self.player, self.obstacles)
            or pygame.sprite.spritecollideany(self.player, self.events)
        )

        # No collision.
        if not hit:
            return False

        # Nitro strip is not dangerous, it activates nitro.
        if isinstance(hit, NitroStrip):
            self.activate_power("nitro")
            hit.kill()
            return False

        # If shield is active, it blocks one collision.
        if self.shield:
            self.shield = False
            self.active_power = None
            hit.kill()
            return False

        # Oil spill does not end game; it makes car slide sideways.
        if isinstance(hit, Obstacle) and hit.kind == "oil":
            self.player.rect.x += random.choice([-55, 55])
            self.player.rect.clamp_ip(pygame.Rect(35, 0, WIDTH - 70, HEIGHT))
            hit.kill()
            return False

        # Any other dangerous collision ends the run.
        return True

    def draw_hud(self):
        """
        Draws score, coins, distance, finish distance, and active power-up.
        """
        # Calculate remaining distance to finish.
        remaining = max(0, FINISH_DISTANCE - int(self.distance))

        # HUD text lines.
        lines = [
            f"Score: {int(self.score)}",
            f"Coins: {self.coins_count}",
            f"Distance: {int(self.distance)}m",
            f"Finish: {remaining}m",
        ]

        # Draw HUD lines in top-left corner.
        for i, line in enumerate(lines):
            self.screen.blit(self.font.render(line, True, BLACK), (8, 8 + i * 22))

        # Draw active power-up information.
        if self.active_power:
            if self.active_power == "nitro":
                # Remaining nitro time in seconds.
                rem = max(0, (self.power_end - pygame.time.get_ticks()) / 1000)
                text = f"Power: Nitro {rem:.1f}s"
            elif self.active_power == "shield":
                text = "Power: Shield 1 hit"
            else:
                text = f"Power: {self.active_power}"

            # Draw black background for power-up HUD.
            img = self.font.render(text, True, WHITE)
            pygame.draw.rect(self.screen, BLACK, (WIDTH - 190, 8, 182, 28), border_radius=7)
            self.screen.blit(img, (WIDTH - 184, 12))

    def save_result(self):
        """
        Saves player result to leaderboard only once.
        """
        if not self.saved:
            add_score(self.username, self.score, self.distance, self.coins_count)
            self.saved = True

    def run(self):
        """
        Main game loop.
        Runs until player loses, finishes, exits, or returns to menu.
        """
        running = True
        result = "game_over"

        while running:
            # Limit FPS and get delta time.
            dt = self.clock.tick(FPS)

            # Event handling.
            for event in pygame.event.get():
                # Close window.
                if event.type == pygame.QUIT:
                    return "quit"

                # Escape returns to main menu.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

            # Get keyboard state.
            keys = pygame.key.get_pressed()

            # Move player.
            self.player.update(keys)

            # Increase difficulty over time.
            self.scale()

            # Nitro adds extra speed while active.
            effective_speed = self.speed + (3.5 if self.active_power == "nitro" else 0)

            # Turn off nitro when time is over.
            if self.active_power == "nitro" and pygame.time.get_ticks() > self.power_end:
                self.active_power = None
                self.power_end = 0

            # Update distance.
            self.distance += effective_speed * dt / 45

            # Score formula: coin score + distance score + shield bonus.
            self.score = self.coin_score + self.distance * 0.3 + (25 if self.shield else 0)

            # Spawn weighted coins.
            if random.random() < 0.018:
                # Practice 11: weighted random coins.
                # 1 appears often, 2 less often, 5 is rare.
                value = random.choices([1, 2, 5], weights=[70, 23, 7])[0]
                self.spawn(Coin, self.coins, value, 0)

            # Spawn traffic cars.
            if random.random() < self.traffic_rate:
                self.spawn(TrafficCar, self.traffic, random.uniform(0.5, 2.0))

            # Spawn road obstacles.
            if random.random() < self.obstacle_rate:
                self.spawn(Obstacle, self.obstacles, random.choice(["barrier", "oil", "pothole"]), 0)

            # Spawn collectible power-ups.
            if random.random() < 0.003:
                self.spawn(PowerUp, self.powerups, random.choice(["nitro", "shield", "repair"]), 0)

            # Spawn dynamic road events.
            if random.random() < 0.0025:
                if random.random() < 0.5:
                    self.spawn(NitroStrip, self.events, 0)
                else:
                    self.spawn(MovingBarrier, self.events, 0)

            # Update all non-player sprites.
            for sprite in list(self.all):
                if sprite is not self.player:
                    sprite.update(effective_speed)

            # Check coin collection.
            for coin in pygame.sprite.spritecollide(self.player, self.coins, True):
                # Count collected coins.
                self.coins_count += 1

                # Add score based on coin value.
                self.coin_score += coin.value * 10

                # Practice 11 requirement:
                # speed increases after collecting coins.
                self.base_speed += 0.06 * coin.value

            # Check power-up collection.
            for p in pygame.sprite.spritecollide(self.player, self.powerups, True):
                # Only one power-up can be active at a time.
                if self.active_power is None:
                    self.activate_power(p.kind)

            # Check dangerous collisions.
            if self.collide_danger():
                # Play crash sound only if sound setting is enabled.
                if self.settings.get("sound", True):
                    self.crash_sound.play()

                # Stop game and go to Game Over screen.
                result = "game_over"
                running = False

            # Check finish line.
            if self.distance >= FINISH_DISTANCE:
                self.finished = True

                # Finish bonus.
                self.score += 500

                # Game ends after finish too.
                result = "game_over"
                running = False

            # Draw road background.
            self.draw_road()

            # Draw all sprites.
            for sprite in self.all:
                self.screen.blit(sprite.image, sprite.rect)

            # Draw HUD.
            self.draw_hud()

            # Update display.
            pygame.display.flip()

        # Save result after run ends.
        self.save_result()

        # Return result to main.py.
        return result
