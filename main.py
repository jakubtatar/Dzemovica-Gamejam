import pygame
import sys
import os
from player import Player
from camera import Camera
from gui import GUI
from fade import Fade
from grave import Grave
from dialogue import Dialogue
from mapsmanager import MapsManager
from quest import Quest
from objectZone import ObjectZone


# Load images form folder functiuon
def load_images_from_folder(folder_path, tile_size):
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            # Oprava: Ziskame kluc ako string ("1", "6", atd.)
            key = filename.split("_")[-1].split(".")[0]  

            image = pygame.image.load(
                os.path.join(folder_path, filename)
            ).convert_alpha()

            # Ak je kluc "6", vyska bude 2-nasobna (100px)
            current_height = tile_size * 2 if key == "6" else tile_size
            image = pygame.transform.scale(image, (tile_size, current_height))
            images[key] = image # Kluc je uz string a je hashevatelny

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

maps_manager = MapsManager()
# Fade effect
fade = Fade(screen, speed=8)

# Create game objects
player = Player(x=100, y=100, width=50, height=50, color=(0, 128, 255))
camera = Camera(screen_width, screen_height)
gui = GUI(screen, player)


# Map settings
TILE_SIZE = 50
walls, collidable_walls = maps_manager.load_map("./Resources/Bitmaps/cmitermap.txt", TILE_SIZE)

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

# Load walls and floors
floor_planks_img = pygame.image.load(r"Resources/Floors/Floor_Planks.png").convert_alpha()  #p
wall_img = pygame.image.load(r"Resources/Walls/Wall.png").convert_alpha()                   #s
wall_front_img = pygame.image.load(r"Resources/Walls/Wall_Front.png").convert_alpha()       #f
wall_top_img = pygame.image.load(r"Resources/Walls/Wall_Top.png").convert_alpha()           #w
wall_left_img = pygame.image.load(r"Resources/Walls/Wall_Left.png").convert_alpha()         #a
wall_right_img = pygame.image.load(r"Resources/Walls/Wall_Right.png").convert_alpha()       #d
wall_RT_img = pygame.image.load(r"Resources/Walls/Wall_RT.png").convert_alpha()             #e
wall_LT_img = pygame.image.load(r"Resources/Walls/Wall_LT.png").convert_alpha()             #q
wall_RD_img = pygame.image.load(r"Resources/Walls/Wall_RD.png").convert_alpha()             #c
wall_LD_img = pygame.image.load(r"Resources/Walls/Wall_LD.png").convert_alpha()             #z

wheat_wall_img = pygame.image.load(r"Resources/Walls/Wall_Wheat.png").convert_alpha()       #n
wheat_wall_top_img = pygame.image.load(r"Resources/Walls/Wall_Wheat_Top.png").convert_alpha()#m


# Load gravestone images
grave_closed_img = pygame.image.load(r"Resources/Grave_Closed.png").convert_alpha()
grave_opened_img = pygame.image.load(r"Resources/Grave_Opened.png").convert_alpha()

gravestone_images = load_images_from_folder(
    "Resources/Gravestones",
    TILE_SIZE
)

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

floor_planks_img = pygame.transform.scale(floor_planks_img, (TILE_SIZE, TILE_SIZE))
wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
wall_front_img = pygame.transform.scale(wall_front_img, (TILE_SIZE, TILE_SIZE))
wall_top_img = pygame.transform.scale(wall_top_img, (TILE_SIZE, TILE_SIZE))
wall_left_img = pygame.transform.scale(wall_left_img, (TILE_SIZE, TILE_SIZE))
wall_right_img = pygame.transform.scale(wall_right_img, (TILE_SIZE, TILE_SIZE))
wall_RT_img = pygame.transform.scale(wall_RT_img, (TILE_SIZE, TILE_SIZE))
wall_LT_img = pygame.transform.scale(wall_LT_img, (TILE_SIZE, TILE_SIZE))
wall_RD_img = pygame.transform.scale(wall_RD_img, (TILE_SIZE, TILE_SIZE))
wall_LD_img = pygame.transform.scale(wall_LD_img, (TILE_SIZE, TILE_SIZE))

wheat_wall_img = pygame.transform.scale(wheat_wall_img, (TILE_SIZE, TILE_SIZE))
wheat_wall_top_img = pygame.transform.scale(wheat_wall_top_img, (TILE_SIZE, TILE_SIZE))

# Jamy (closed/opened img) budu mat vysku 2-nasobok TILE_SIZE (100px)
grave_closed_img = pygame.transform.scale(grave_closed_img, (TILE_SIZE, TILE_SIZE * 2))
grave_opened_img = pygame.transform.scale(grave_opened_img, (TILE_SIZE, TILE_SIZE * 2))

# Load Well Object
object_well_img = pygame.image.load(r"Resources/Objects/Object_Well.png").convert_alpha()
object_well_img = pygame.transform.scale(object_well_img, (TILE_SIZE * 4, TILE_SIZE * 4)) 

# # Create graves (20 graves next to each other)
graves = []
grave_pits = [] 

start_x = 200
start_y = 500
spacing = TILE_SIZE

for i in range(20):
    x = start_x + i * spacing
    y = start_y
    graves.append(Grave(x, y, TILE_SIZE, gravestone_images))
    grave_pits.append({'rect': pygame.Rect(x, y + 50, TILE_SIZE, TILE_SIZE * 2), 'state': 'closed'})

# Define the well's position and size in world coordinates (x400, y800)
# Rect pre studnu, velkost 4x4 tiles (200x200px)
well_rect = pygame.Rect(400, 800, TILE_SIZE * 4, TILE_SIZE * 4) 
collidable_walls.append(well_rect) # Pridame studnu do kolizii


# Main loop
is_running = True

while is_running:
    selected_item = gui.get_selected_item()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click (kopanie)
                if selected_item == "[2] Shovel":
                    gx = (player.rect.centerx // TILE_SIZE) * TILE_SIZE
                    gy = (player.rect.bottom // TILE_SIZE) * TILE_SIZE
                    graves.append(Grave(gx, gy, TILE_SIZE, gravestone_images))
                    grave_pits.append({'rect': pygame.Rect(gx, gy + 50, TILE_SIZE, TILE_SIZE * 2), 'state': 'closed'})
                    print(f"Hrob vytvorený na {gx}, {gy}")
            
            elif event.button == 3: # Right click (otvaranie)
                for pit in grave_pits:
                    pit['state'] = 'opened'
                print("Vsetky jamy otvorene!")


        gui.handle_input(event)


    # Update player and camera
    player.handle_keys_with_collision(4000, 4000, collidable_walls)
    camera.update(player)

    # CLEAR SCREEN FIRST
    screen.fill((8, 50, 20))

    # Draw tiles from the bitmapmap
    for rect, tile_type in walls:
        maps_manager.drawTilemap(screen, tile_type, rect, camera, tile1_img, tile2_img, hedgefront_img, hedgetopfront_img, hedgeRD_img, hedgeLD_img, hedgetopwall_img, hedgeLT_img, hedgeRT_img, floor_planks_img, wall_img, wall_front_img, wall_top_img, wall_left_img, wall_right_img, wall_RT_img, wall_LT_img, wall_RD_img, wall_LD_img, wheat_wall_img, wheat_wall_top_img)

    # Draw closed grave pits (Vykreslujeme prve, aby boli pod hrobmi)
    for pit in grave_pits:
        image_to_draw = grave_closed_img if pit['state'] == 'closed' else grave_opened_img
        screen.blit(image_to_draw, camera.apply(pit['rect']))

     # Draw graves
    for grave in graves:
        grave.draw(screen, camera)
        
    # Draw the well object (Posunieme Y suradnicu blitovania o vysku objektu, aby sedel na 800y)
    screen.blit(object_well_img, camera.apply(well_rect).move(0, well_rect.height - object_well_img.get_height()))

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