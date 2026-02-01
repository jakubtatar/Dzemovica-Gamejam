import pygame
import sys
import os
from player import Player
from camera import Camera
from gui import GUI

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
                    tiles.append((rect, "1"))  
                elif char == "2":
                    tiles.append((rect, "2"))
                    collidable_tiles.append(rect) 
                elif char == "0":
                    tiles.append((rect, "0"))  
                elif char == "3":
                    tiles.append((rect, "3"))
                    collidable_tiles.append(rect)
                elif char == "4":
                    tiles.append((rect, "4"))
                    collidable_tiles.append(rect)
                elif char == "5":
                    tiles.append((rect, "5"))
                    collidable_tiles.append(rect)
                elif char == "6":
                    tiles.append((rect, "6"))
                    collidable_tiles.append(rect)
                elif char == "7":
                    tiles.append((rect, "7"))
                    collidable_tiles.append(rect)
                elif char == "8":
                    tiles.append((rect, "8"))
                    collidable_tiles.append(rect)
                elif char == "9":
                    tiles.append((rect, "9"))
                    collidable_tiles.append(rect)
    return tiles, collidable_tiles


# Initialize Pygame
pygame.init()

# Font initialization (required for GUI)
pygame.font.init()
font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 30)

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kto druhemu jamu kope...")

# Set up clock for controlling FPS
clock = pygame.time.Clock()

# Create game objects
player = Player(x=100, y=100, width=50, height=50, color=(0, 128, 255))
camera = Camera(screen_width, screen_height)
gui = GUI(screen, player)

# Map settings
TILE_SIZE = 50
walls, collidable_walls = load_map(r".\Resources\Bitmaps\cmitermap.txt", TILE_SIZE)

# Load tile images
tile1_img = pygame.image.load(r"Resources/Images/Image_Plot1.png").convert_alpha()
tile2_img = pygame.image.load(r"Resources/Images/Image_Plot2.png").convert_alpha()

# Load hedge images
hedgefront_img = pygame.image.load(r"Resources/Images/Image_HedgeFront.png").convert_alpha()
hedgetopfront_img = pygame.image.load(r"Resources/Images/Image_HedgeTopFront.png").convert_alpha()
hedgeRD_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerRD.png").convert_alpha()
hedgeLD_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerLD.png").convert_alpha()
hedgeRT_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerRT.png").convert_alpha()
hedgeLT_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerLT.png").convert_alpha()
hedgetopwall_img = pygame.image.load(r"Resources/Images/Image_HedgeTopWall.png").convert_alpha()

# Optionally scale to TILE_SIZE
tile1_img = pygame.transform.scale(tile1_img, (TILE_SIZE, TILE_SIZE))
tile2_img = pygame.transform.scale(tile2_img, (TILE_SIZE, TILE_SIZE))
hedgefront_img = pygame.transform.scale(hedgefront_img, (TILE_SIZE, TILE_SIZE))
hedgeRD_img = pygame.transform.scale(hedgeRD_img, (TILE_SIZE, TILE_SIZE))
hedgeLD_img = pygame.transform.scale(hedgeLD_img, (TILE_SIZE, TILE_SIZE))
hedgeRT_img = pygame.transform.scale(hedgeRT_img, (TILE_SIZE, TILE_SIZE))
hedgeLT_img = pygame.transform.scale(hedgeLT_img, (TILE_SIZE, TILE_SIZE))
hedgetopfront_img = pygame.transform.scale(hedgetopfront_img, (TILE_SIZE, TILE_SIZE))
hedgetopwall_img = pygame.transform.scale(hedgetopwall_img, (TILE_SIZE, TILE_SIZE))

# Main loop
is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        gui.handle_input(event)

    # Update player and camera
    player.handle_keys_with_collision(4000, 4000, collidable_walls)
    camera.update(player)

    # CLEAR SCREEN FIRST
    screen.fill((8, 50, 20))

    # Draw tiles from the bitmapmap
    for rect, tile_type in walls:
        if tile_type == "1":
            screen.blit(tile1_img, camera.apply(rect))
        elif tile_type == "0":
            screen.blit(tile2_img, camera.apply(rect))
        elif tile_type == "3":
            screen.blit(hedgefront_img, camera.apply(rect))
        elif tile_type == "4":
            screen.blit(hedgetopfront_img, camera.apply(rect))
        elif tile_type == "5":
            screen.blit(hedgeRD_img, camera.apply(rect))
        elif tile_type == "6":
            screen.blit(hedgeLD_img, camera.apply(rect))
        elif tile_type == "7":
            screen.blit(hedgetopwall_img, camera.apply(rect))
        elif tile_type == "8":
            screen.blit(hedgeLT_img, camera.apply(rect))
        elif tile_type == "9":
            screen.blit(hedgeRT_img, camera.apply(rect))

    # Draw player
    pygame.draw.rect(
        screen,
        player.color,
        camera.apply(player.rect)
    )

    gui.draw()

    pygame.display.flip()
    clock.tick(60)


# Quit Pygame
pygame.quit()
