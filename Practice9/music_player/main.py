import pygame

pygame.init()
pygame.mixer.init()

playlist = [
    {"music": "music/Neu roses.mp3", "image": "images/Daniel Caesar.png"},
    {"music": "music/Cheap Thrills.mp3", "image": "images/Sia.png"},
    {"music": "music/Roommates.mp3", "image": "images/Malcolm Todd.png"}
]
current = 0

def play():
    pygame.mixer.music.load(playlist[current]["music"])
    pygame.mixer.music.play()

screen = pygame.display.set_mode((800,600))
running = True

font = pygame.font.SysFont(None, 36)

image = pygame.image.load(playlist[current]["image"])
image = pygame.transform.scale(image, (300, 300))

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        screen.fill((40,40,60))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play()
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
            elif event.key == pygame.K_n:
                current = (current + 1) % len(playlist)
                play()
                image = pygame.image.load(playlist[current]["image"])
                image = pygame.transform.scale(image, (300, 300))
            elif event.key == pygame.K_b:
                current = (current - 1) % len(playlist)
                play()
                image = pygame.image.load(playlist[current]["image"])
                image = pygame.transform.scale(image, (300, 300))
            elif event.key == pygame.K_q:
                running = False
            
        screen.blit(image, (250, 50))

        controls = [
        "P - Play",
        "S - Stop",
        "N - Next",
        "B - Back",
        "Q - Quit"
        ]

        for i, text in enumerate(controls):
            control_text = font.render(text, True, (200, 200, 200, 100))
            screen.blit(control_text, (30, 30 + i * 40))

        track_text = font.render(f"Now playing: {playlist[current]["music"].split("/")[-1]}", True, (255, 255, 255))
        screen.blit(track_text, (210, 390))

        pos = pygame.mixer.music.get_pos() // 1000
        time_text = font.render(f"Time: {pos} sec", True, (255, 255, 0))
        screen.blit(time_text, (325, 440))

        clock.tick(60)
        pygame.display.flip()
        

pygame.quit()