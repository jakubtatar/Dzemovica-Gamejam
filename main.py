import pygame
import sys
import os
from player import Player
from camera import Camera
from gui import GUI
from fade import Fade
from grave import Grave

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

# Load images form folder functiuon
def load_images_from_folder(folder_path, tile_size):
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            key = filename.split("_")[-1].split(".")[0]  
            # Gravestone_1.png = "1"

            image = pygame.image.load(
                os.path.join(folder_path, filename)
            ).convert_alpha()

            image = pygame.transform.scale(image, (tile_size, tile_size))
            images[key] = image

    return images


# Initialize Pygame
pygame.init()

# Font initialization (required for GUI)
pygame.font.init()
font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 30)

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The pit you dig")
pygame.display.set_icon(pygame.image.load(r".\Resources\Logo_Small.png"))

# Set up clock for controlling FPS
clock = pygame.time.Clock()

# Fade effect
fade = Fade(screen, speed=8)

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

# Load gravestone images
gravestone_images = load_images_from_folder(
    "Resources/Gravestones",
    TILE_SIZE
)

# # Create graves (20 graves next to each other)
# graves = []

# start_x = 200
# start_y = 500
# spacing = TILE_SIZE

# for i in range(20):
#     x = start_x + i * spacing
#     y = start_y
#     graves.append(Grave(x, y, TILE_SIZE, gravestone_images))

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

        # We get selected item on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                selected_item = gui.get_selected_item()
                print(f"Used item: {selected_item}")
                fade.fade_in()

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

    # # Draw graves
    # for grave in graves:
    #     grave.draw(screen, camera)

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
