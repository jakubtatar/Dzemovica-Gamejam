import pygame
from player import Player
from camera import Camera

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kto druhemu jamu kope...")

# Set up clock for controlling FPS
clock = pygame.time.Clock()

# Create game objects
player = Player(x=50, y=50, width=50, height=50, color=(0, 128, 255))
camera = Camera(screen_width, screen_height)

# World objects (rectangles in the world)
world_objects = [
    pygame.Rect(0, 0, 2000, 50),        # top wall
    pygame.Rect(0, 1950, 2000, 50),     # bottom wall
    pygame.Rect(0, 0, 50, 2000),        # left wall
    pygame.Rect(1950, 0, 50, 2000),     # right wall

    pygame.Rect(300, 300, 100, 100),
    pygame.Rect(700, 500, 150, 80),
    pygame.Rect(1200, 800, 200, 120),
    pygame.Rect(1600, 300, 80, 200),
]

# Main loop
is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    player.handle_keys(2000, 2000)
    camera.update(player)

    # Update the display
    screen.fill((135, 206, 235))

    # Draw world objects using camera
    for obj in world_objects:
        pygame.draw.rect(
            screen,
            (60, 60, 60),
            camera.apply(obj)
        )

    # Draw player
    pygame.draw.rect(
        screen,
        player.color,
        camera.apply(player.rect)
    )

    pygame.display.flip()
    clock.tick(60) # Limit to 60 FPS

# Quit Pygame
pygame.quit()
