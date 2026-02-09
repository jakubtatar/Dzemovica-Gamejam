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
from item import Item


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
            images[key] = image  # Kluc je uz string a je hashevatelny

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
current_map = "cmitermap"  # Starting map
TILE_SIZE = 50
walls, collidable_walls = [], []

# --- MAP OBJECTS & CHANGE ZONES (FUTURE PROOF) ---
map_objects = []          # {rect, image, collidable}
change_map_squares = []   # {rect, target, spawn}

# 🔑 MAP SWITCH COOLDOWN (FIX)
map_switch_cooldown = 0

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
floor_planks_img = pygame.image.load(r"Resources/Floors/Floor_Planks.png").convert_alpha()
wall_img = pygame.image.load(r"Resources/Walls/Wall.png").convert_alpha()
wall_front_img = pygame.image.load(r"Resources/Walls/Wall_Front.png").convert_alpha()
wall_top_img = pygame.image.load(r"Resources/Walls/Wall_Top.png").convert_alpha()
wall_left_img = pygame.image.load(r"Resources/Walls/Wall_Left.png").convert_alpha()
wall_right_img = pygame.image.load(r"Resources/Walls/Wall_Right.png").convert_alpha()
wall_RT_img = pygame.image.load(r"Resources/Walls/Wall_RT.png").convert_alpha()
wall_LT_img = pygame.image.load(r"Resources/Walls/Wall_LT.png").convert_alpha()
wall_RD_img = pygame.image.load(r"Resources/Walls/Wall_RD.png").convert_alpha()
wall_LD_img = pygame.image.load(r"Resources/Walls/Wall_LD.png").convert_alpha()

wheat_wall_img = pygame.image.load(r"Resources/Walls/Wall_Wheat.png").convert_alpha()
wheat_wall_top_img = pygame.image.load(r"Resources/Walls/Wall_Wheat_Top.png").convert_alpha()

# Load gravestone images
grave_closed_img = pygame.image.load(r"Resources/Grave_Closed.png").convert_alpha()
grave_opened_img = pygame.image.load(r"Resources/Grave_Opened.png").convert_alpha()

# Scale images
tile1_img = pygame.transform.scale(tile1_img, (TILE_SIZE, TILE_SIZE))
tile2_img = pygame.transform.scale(tile2_img, (TILE_SIZE, TILE_SIZE))

hedgefront_img = pygame.transform.scale(hedgefront_img, (TILE_SIZE, TILE_SIZE))
hedgetopfront_img = pygame.transform.scale(hedgetopfront_img, (TILE_SIZE, TILE_SIZE))
hedgeRD_img = pygame.transform.scale(hedgeRD_img, (TILE_SIZE, TILE_SIZE))
hedgeLD_img = pygame.transform.scale(hedgeLD_img, (TILE_SIZE, TILE_SIZE))
hedgeRT_img = pygame.transform.scale(hedgeRT_img, (TILE_SIZE, TILE_SIZE))
hedgeLT_img = pygame.transform.scale(hedgeLT_img, (TILE_SIZE, TILE_SIZE))
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

gravestone_images = load_images_from_folder("Resources/Gravestones", TILE_SIZE)

# Jamy
grave_closed_img = pygame.transform.scale(grave_closed_img, (TILE_SIZE, TILE_SIZE * 2))
grave_opened_img = pygame.transform.scale(grave_opened_img, (TILE_SIZE, TILE_SIZE * 2))

# Load Well Object
object_well_img = pygame.image.load(r"Resources/Objects/Object_Well.png").convert_alpha()
object_well_img = pygame.transform.scale(object_well_img, (TILE_SIZE * 4, TILE_SIZE * 4))

# Load House Object
object_house_img = pygame.image.load(r"Resources/Objects/Object_House_01.png").convert_alpha()
object_house_img = pygame.transform.scale(object_house_img, (TILE_SIZE * 7, TILE_SIZE * 7))

# Load Church Object
object_church_img = pygame.image.load(r"Resources/Objects/Object_Church.png").convert_alpha()
object_church_img = pygame.transform.scale(object_church_img, (TILE_SIZE * 14, TILE_SIZE * 14))

# Load shop object
object_shop_img = pygame.image.load(r"Resources/Objects/Object_Zabkas.png").convert_alpha()
object_shop_img = pygame.transform.scale(object_shop_img, (TILE_SIZE * 7, TILE_SIZE * 7))

# Load tree object
object_tree_img = pygame.image.load(r"Resources/Objects/Object_Tree.png").convert_alpha()
object_tree_img = pygame.transform.scale(object_tree_img, (TILE_SIZE * 7, TILE_SIZE * 7))

# Create graves
graves = []
grave_pits = []


# --- MAP SETUP FUNCTION ---
def setup_map(map_name):
    global walls, collidable_walls, map_objects, change_map_squares, current_map

    current_map = map_name
    map_objects = []
    change_map_squares = []
    collidable_walls = []

    if map_name == "cmitermap":
        walls, collidable_walls = maps_manager.load_map(r"Resources/Bitmaps/cmitermap.txt", TILE_SIZE)
        player.rect.topleft = (2700, 150)

        change_map_squares.append({
            "rect": pygame.Rect(2800, 100, TILE_SIZE, TILE_SIZE*3),
            "target": "crossroad",
            "spawn": (100, 500)
        })

        # Well object
        well_rect = pygame.Rect(400, 800, TILE_SIZE * 4, TILE_SIZE * 4)
        map_objects.append({
            "rect": well_rect,
            "image": object_well_img,
            "collidable": True
        })

        # Load Tree Object
        object_tree_img = pygame.image.load(r"Resources/Objects/Object_Tree.png").convert_alpha()
        object_tree_img = pygame.transform.scale(object_tree_img, (TILE_SIZE * 7, TILE_SIZE * 7))

        # Trees manually placed across the map
        tree_positions = [
            (800, 200), (1200, 400), (1600, 300), (2000, 600), (2400, 200), (2200, 800)
        ]

        for pos in tree_positions:
            tree_rect = pygame.Rect(pos[0], pos[1], TILE_SIZE * 7, TILE_SIZE * 7)
            map_objects.append({
                "rect": tree_rect,
                "image": object_tree_img,
                "collidable": True
            })


    elif map_name == "crossroad":
        walls, collidable_walls = maps_manager.load_map(r"Resources/Bitmaps/crossroad.txt", TILE_SIZE)
        player.rect.topleft = (100, 500)

        # House exit
        change_map_squares.append({
            "rect": pygame.Rect(450, 0, TILE_SIZE * 3, TILE_SIZE),
            "target": "houseplace",
            "spawn": (350, 650)
        })

        # Cimiter exit
        change_map_squares.append({
            "rect": pygame.Rect(0, 450, TILE_SIZE, TILE_SIZE * 3),
            "target": "cmitermap",
            "spawn": (2700, 150)
        })

        # Village exit
        change_map_squares.append({
            "rect": pygame.Rect(1000, 450, TILE_SIZE, TILE_SIZE * 3),
            "target": "village",
            "spawn": (200, 350)
        })

    elif map_name == "houseplace":
        walls, collidable_walls = maps_manager.load_map(r"Resources/Bitmaps/houseplace.txt", TILE_SIZE)
        player.rect.topleft = (150, 450)

        change_map_squares.append({
            "rect": pygame.Rect(300, 750, TILE_SIZE * 3, TILE_SIZE),
            "target": "crossroad",
            "spawn": (500, 100)
        })

        # House object (CENTER)
        house_rect = pygame.Rect(200, 100, TILE_SIZE * 7, TILE_SIZE * 7)

        map_objects.append({
            "rect": house_rect,
            "image": object_house_img,
            "collidable": True
        })
    
    elif map_name == "village":
        walls, collidable_walls = maps_manager.load_map(r"Resources/Bitmaps/village.txt", TILE_SIZE)
        player.rect.topleft = (100, 500)

        change_map_squares.append({
            "rect": pygame.Rect(0, 300, TILE_SIZE, TILE_SIZE * 3),
            "target": "crossroad",
            "spawn": (900, 500)
        })

        # Load Church on village map
        church_rect = pygame.Rect(600, -400, TILE_SIZE * 14, TILE_SIZE * 14)
        map_objects.append({
            "rect": church_rect,
            "image": object_church_img,
            "collidable": True
        })

        shop_rect = pygame.Rect(1400, 0, TILE_SIZE * 7, TILE_SIZE * 7)
        map_objects.append({
            "rect": shop_rect,
            "image": object_shop_img,
            "collidable": True
        })

    # Add collidable objects
    for obj in map_objects:
        if obj["collidable"]:
            collidable_walls.append(obj["rect"])


# INITIAL MAP
setup_map("cmitermap")

# Main loop
is_running = True
while is_running:
    selected_item = gui.get_selected_item()

    if map_switch_cooldown > 0:
        map_switch_cooldown -= 1

    if map_switch_cooldown == 0:
        for zone in change_map_squares:
            if player.rect.colliderect(zone["rect"]):
                setup_map(zone["target"])
                player.rect.topleft = zone["spawn"]
                graves = []
                grave_pits = []
                map_switch_cooldown = 30
                break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1: 
                if selected_item == "[2] Shovel" and current_map == "cmitermap": 
                    gx = (player.rect.centerx // TILE_SIZE) * TILE_SIZE 
                    gy = (player.rect.bottom // TILE_SIZE) * TILE_SIZE 
                    graves.append(Grave(gx, gy, TILE_SIZE, gravestone_images)) 
                    grave_pits.append({ 'rect': pygame.Rect(gx, gy + 50, TILE_SIZE, TILE_SIZE * 2), 'state': 'closed' }) 
            elif event.button == 3: 
                for pit in grave_pits: pit['state'] = 'opened' 

        gui.handle_input(event)

    player.handle_keys_with_collision(4000, 4000, collidable_walls)
    camera.update(player)

    screen.fill((8, 50, 20))

    for rect, tile_type in walls:
        maps_manager.drawTilemap(
            screen, tile_type, rect, camera,
            tile1_img, tile2_img,
            hedgefront_img, hedgetopfront_img,
            hedgeRD_img, hedgeLD_img,
            hedgetopwall_img, hedgeLT_img, hedgeRT_img,
            floor_planks_img,
            wall_img, wall_front_img, wall_top_img,
            wall_left_img, wall_right_img,
            wall_RT_img, wall_LT_img, wall_RD_img, wall_LD_img,
            wheat_wall_img, wheat_wall_top_img
        )

    for zone in change_map_squares:
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(zone["rect"]))

    for pit in grave_pits:
        image_to_draw = grave_closed_img if pit['state'] == 'closed' else grave_opened_img
        screen.blit(image_to_draw, camera.apply(pit['rect']))

    for grave in graves:
        grave.draw(screen, camera)

    for obj in map_objects:
        screen.blit(
            obj["image"],
            camera.apply(obj["rect"]).move(
                0, obj["rect"].height - obj["image"].get_height()
            )
        )

    pygame.draw.rect(screen, player.color, camera.apply(player.rect))

    gui.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
