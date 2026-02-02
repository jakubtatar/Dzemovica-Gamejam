import pygame
import sys
import os
from player import Player
from camera import Camera

# Function to load a simple map from a text file
def load_map(filename, tile_size):
    tiles = []
    collidable_tiles = []
    with open(filename, "r") as file:
        for row_index, line in enumerate(file):
            for col_index, char in enumerate(line.strip()):
                x = col_index * tile_size
                y = row_index * tile_size
                rect = pygame.Rect(x, y, tile_size, tile_size)
                
                if char == "1":
                    tiles.append((rect, "1"))  # iba vizuálne, bez kolízie
                elif char == "2":
                    tiles.append((rect, "2"))
                    collidable_tiles.append(rect)  # iba 2-ky budú kolidovať
                elif char == "0":
                    tiles.append((rect, "0"))  # vizuálne, bez kolízie
    return tiles, collidable_tiles


# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The pit you dig")
pygame.display.set_icon(pygame.image.load(r".\Resources\Logo_Small.png").convert_alpha())

# Set up clock for controlling FPS
clock = pygame.time.Clock()

# Create game objects
player = Player(x=50, y=50, width=50, height=50, color=(0, 128, 255))
camera = Camera(screen_width, screen_height)

# Map settings
TILE_SIZE = 50
walls, collidable_walls = load_map(r".\Resources\Bitmaps\cmitermap.txt", TILE_SIZE)

# Load tile images
tile1_img = pygame.image.load(r"Resources/Images/Image_Plot1.png").convert_alpha()
tile2_img = pygame.image.load(r"Resources/Images/Image_Plot2.png").convert_alpha()

<<<<<<< Updated upstream
=======
# Load hedge images
hedgefront_img = pygame.image.load(r"Resources/Images/Image_HedgeFront.png").convert_alpha()
hedgetopfront_img = pygame.image.load(r"Resources/Images/Image_HedgeTopFront.png").convert_alpha()
hedgeRD_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerRD.png").convert_alpha()
hedgeLD_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerLD.png").convert_alpha()
hedgeRT_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerRT.png").convert_alpha()
hedgeLT_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerLT.png").convert_alpha()
hedgetopwall_img = pygame.image.load(r"Resources/Images/Image_HedgeTopWall.png").convert_alpha()

# Load human images
human_img = pygame.image.load(r"Resources/Humans/Human_1.png").convert_alpha()
human_img = pygame.transform.scale(human_img, (TILE_SIZE, TILE_SIZE *2))

>>>>>>> Stashed changes
# Optionally scale to TILE_SIZE
tile1_img = pygame.transform.scale(tile1_img, (TILE_SIZE, TILE_SIZE))
tile2_img = pygame.transform.scale(tile2_img, (TILE_SIZE, TILE_SIZE))




# Main loop
is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # Update player and camera
    player.handle_keys_with_collision(4000, 4000, collidable_walls)
    camera.update(player)

    # CLEAR SCREEN FIRST
    screen.fill((135, 206, 235))

    # Draw tiles from the bitmapmap
    for rect, tile_type in walls:
        if tile_type == "1":
            screen.blit(tile1_img, camera.apply(rect))
        elif tile_type == "0":
            screen.blit(tile2_img, camera.apply(rect))

    # Draw player
    pygame.draw.rect(
        screen,
        player.color,
        camera.apply(player.rect)
    )
    
    # Draw a human for demonstration
    human_rect = pygame.Rect(300, 300, TILE_SIZE, TILE_SIZE * 2)
    screen.blit(human_img, camera.apply(human_rect))


    pygame.display.flip()
    clock.tick(60)


# Quit Pygame
pygame.quit()
