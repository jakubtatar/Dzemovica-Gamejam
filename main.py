import pygame
from player import Player

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kto druhemu jamu kope...")

clock = pygame.time.Clock()

player = Player(x=50, y=50, width=50, height=50, color=(0, 128, 255))

# Main loop
is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    keys = pygame.key.get_pressed()
    player.handle_keys(screen_width, screen_height)

    # Update the display
    screen.fill((135, 206, 235))  # Sky blue background
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60) # Limit to 60 FPS

# Quit Pygame
pygame.quit()

