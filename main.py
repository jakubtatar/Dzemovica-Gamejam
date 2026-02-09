import pygame
import sys
import os

# Importy tvojich tried (musia byt v rovnakom priečinku)
from player import Player
from camera import Camera
from gui import GUI

<<<<<<< Updated upstream
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
=======
# --- TOTO JE TO OBALENIE DO FUNKCIE ---
def spustit_hru(screen):
    # Load images form folder functiuon
    def load_images_from_folder(folder_path, tile_size):
        images = {}
        if not os.path.exists(folder_path): return images
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                key = filename.split("_")[-1].split(".")[0]
                try:
                    image = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                    current_height = tile_size * 2 if key == "6" else tile_size
                    image = pygame.transform.scale(image, (tile_size, current_height))
                    images[key] = image
                except: pass
        return images

    # Initialize things inside the function
    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()
    
    # Font setup
    try:
        font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 30)
    except:
        font = pygame.font.SysFont("Arial", 30)

    maps_manager = MapsManager()
    fade = Fade(screen, speed=8)

    # Create game objects
    player = Player(x=100, y=100, width=50, height=50, color=(0, 128, 255))
    camera = Camera(screen_width, screen_height)
    gui = GUI(screen, player)

    # Map settings
    current_map = "cmitermap"
    TILE_SIZE = 50
    
    # Dátové štruktúry
    game_data = {
        "walls": [],
        "collidable_walls": [],
        "map_objects": [],
        "change_map_squares": [],
        "graves": [],
        "grave_pits": [],
        "map_switch_cooldown": 0
    }
>>>>>>> Stashed changes

    # Load images (kód skrátený pre prehľadnosť, ale funkčný)
    # Tu predpokladáme, že cesty k súborom sú správne
    try:
        tile1_img = pygame.transform.scale(pygame.image.load(r"Resources/Images/Image_Plot1.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        tile2_img = pygame.transform.scale(pygame.image.load(r"Resources/Images/Image_Plot2.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        
        hedgefront_img = pygame.transform.scale(pygame.image.load(r"Resources/Images/Image_HedgeFront.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        hedgetopfront_img = pygame.transform.scale(pygame.image.load(r"Resources/Images/Image_HedgeTopFront.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        hedgeRD_img = pygame.transform.scale(pygame.image.load(r"Resources/Images/Image_HedgeCornerRD.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        hedgeLD_img = pygame.transform.scale(pygame.image.load(r"Resources/Images/Image_HedgeCornerLD.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        hedgeRT_img = pygame.transform.scale(pygame.image.load(r"Resources/Images/Image_HedgeCornerRT.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        hedgeLT_img = pygame.transform.scale(pygame.image.load(r"Resources/Images/Image_HedgeCornerLT.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        hedgetopwall_img = pygame.transform.scale(pygame.image.load(r"Resources/Images/Image_HedgeTopWall.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))

        floor_planks_img = pygame.transform.scale(pygame.image.load(r"Resources/Floors/Floor_Planks.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        wall_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        wall_front_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall_Front.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        wall_top_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall_Top.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        wall_left_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall_Left.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        wall_right_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall_Right.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        wall_RT_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall_RT.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        wall_LT_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall_LT.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        wall_RD_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall_RD.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        wall_LD_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall_LD.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))

        wheat_wall_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall_Wheat.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
        wheat_wall_top_img = pygame.transform.scale(pygame.image.load(r"Resources/Walls/Wall_Wheat_Top.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))

<<<<<<< Updated upstream
# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kto druhemu jamu kope...")
=======
        grave_closed_img = pygame.transform.scale(pygame.image.load(r"Resources/Grave_Closed.png").convert_alpha(), (TILE_SIZE, TILE_SIZE * 2))
        grave_opened_img = pygame.transform.scale(pygame.image.load(r"Resources/Grave_Opened.png").convert_alpha(), (TILE_SIZE, TILE_SIZE * 2))
>>>>>>> Stashed changes

        object_well_img = pygame.transform.scale(pygame.image.load(r"Resources/Objects/Object_Well.png").convert_alpha(), (TILE_SIZE * 4, TILE_SIZE * 4))
        object_house_img = pygame.transform.scale(pygame.image.load(r"Resources/Objects/Object_House_01.png").convert_alpha(), (TILE_SIZE * 7, TILE_SIZE * 7))
        object_church_img = pygame.transform.scale(pygame.image.load(r"Resources/Objects/Object_Church.png").convert_alpha(), (TILE_SIZE * 14, TILE_SIZE * 14))
        object_shop_img = pygame.transform.scale(pygame.image.load(r"Resources/Objects/Object_Zabkas.png").convert_alpha(), (TILE_SIZE * 7, TILE_SIZE * 7))
        object_tree_img = pygame.transform.scale(pygame.image.load(r"Resources/Objects/Object_Tree.png").convert_alpha(), (TILE_SIZE * 7, TILE_SIZE * 7))
        
        gravestone_images = load_images_from_folder("Resources/Gravestones", TILE_SIZE)
    except Exception as e:
        print(f"Chyba pri načítaní obrázkov v main.py: {e}")
        return # Vráti do menu

<<<<<<< Updated upstream
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
=======
    # --- MAP SETUP FUNCTION ---
    def setup_map(map_name):
        nonlocal current_map # Aby sme menili premennú z vonkajšej funkcie
        current_map = map_name
        game_data["map_objects"] = []
        game_data["change_map_squares"] = []
        game_data["collidable_walls"] = []

        if map_name == "cmitermap":
            game_data["walls"], c = maps_manager.load_map(r"Resources/Bitmaps/cmitermap.txt", TILE_SIZE)
            game_data["collidable_walls"] = c
            player.rect.topleft = (2700, 150)

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(2800, 100, TILE_SIZE, TILE_SIZE*3),
                "target": "crossroad",
                "spawn": (100, 500)
            })

            game_data["map_objects"].append({
                "rect": pygame.Rect(400, 800, TILE_SIZE * 4, TILE_SIZE * 4),
                "image": object_well_img,
                "collidable": True
            })

            tree_positions = [(800, 200), (1200, 400), (1600, 300), (2000, 600), (2400, 200), (2200, 800)]
            for pos in tree_positions:
                game_data["map_objects"].append({
                    "rect": pygame.Rect(pos[0], pos[1], TILE_SIZE * 7, TILE_SIZE * 7),
                    "image": object_tree_img,
                    "collidable": True
                })


        elif map_name == "crossroad":
            game_data["walls"], c = maps_manager.load_map(r"Resources/Bitmaps/crossroad.txt", TILE_SIZE)
            game_data["collidable_walls"] = c
            player.rect.topleft = (100, 500)

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(450, 0, TILE_SIZE * 3, TILE_SIZE),
                "target": "houseplace",
                "spawn": (350, 650)
            })
            game_data["change_map_squares"].append({
                "rect": pygame.Rect(0, 450, TILE_SIZE, TILE_SIZE * 3),
                "target": "cmitermap",
                "spawn": (2700, 150)
            })
            game_data["change_map_squares"].append({
                "rect": pygame.Rect(1000, 450, TILE_SIZE, TILE_SIZE * 3),
                "target": "village",
                "spawn": (200, 350)
            })

        elif map_name == "houseplace":
            game_data["walls"], c = maps_manager.load_map(r"Resources/Bitmaps/houseplace.txt", TILE_SIZE)
            game_data["collidable_walls"] = c
            player.rect.topleft = (150, 450)

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(300, 750, TILE_SIZE * 3, TILE_SIZE),
                "target": "crossroad",
                "spawn": (500, 100)
            })

            game_data["map_objects"].append({
                "rect": pygame.Rect(200, 100, TILE_SIZE * 7, TILE_SIZE * 7),
                "image": object_house_img,
                "collidable": True
            })
        
        elif map_name == "village":
            game_data["walls"], c = maps_manager.load_map(r"Resources/Bitmaps/village.txt", TILE_SIZE)
            game_data["collidable_walls"] = c
            player.rect.topleft = (100, 500)

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(0, 300, TILE_SIZE, TILE_SIZE * 3),
                "target": "crossroad",
                "spawn": (900, 500)
            })

            game_data["map_objects"].append({
                "rect": pygame.Rect(600, -400, TILE_SIZE * 14, TILE_SIZE * 14),
                "image": object_church_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(1400, 0, TILE_SIZE * 7, TILE_SIZE * 7),
                "image": object_shop_img,
                "collidable": True
            })

        for obj in game_data["map_objects"]:
            if obj["collidable"]:
                game_data["collidable_walls"].append(obj["rect"])


    # INITIAL MAP
    setup_map("cmitermap")
    fade.fade_in()

    # Main loop
    is_running = True
    while is_running:
        selected_item = gui.get_selected_item()

        if game_data["map_switch_cooldown"] > 0:
            game_data["map_switch_cooldown"] -= 1

        if game_data["map_switch_cooldown"] == 0:
            for zone in game_data["change_map_squares"]:
                if player.rect.colliderect(zone["rect"]):
                    setup_map(zone["target"])
                    player.rect.topleft = zone["spawn"]
                    game_data["graves"] = []
                    game_data["grave_pits"] = []
                    game_data["map_switch_cooldown"] = 30
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Tu nezavrieme cele okno, len ukoncime funkciu
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return # VRÁTI NÁS DO MENU

            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: 
                    if selected_item == "[2] Shovel" and current_map == "cmitermap": 
                        gx = (player.rect.centerx // TILE_SIZE) * TILE_SIZE 
                        gy = (player.rect.bottom // TILE_SIZE) * TILE_SIZE 
                        game_data["graves"].append(Grave(gx, gy, TILE_SIZE, gravestone_images)) 
                        game_data["grave_pits"].append({ 'rect': pygame.Rect(gx, gy + 50, TILE_SIZE, TILE_SIZE * 2), 'state': 'closed' }) 
                elif event.button == 3: 
                    for pit in game_data["grave_pits"]: pit['state'] = 'opened' 

            gui.handle_input(event)

        player.handle_keys_with_collision(4000, 4000, game_data["collidable_walls"])
        camera.update(player)
        fade.update()

        screen.fill((8, 50, 20))

        for rect, tile_type in game_data["walls"]:
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

        # for zone in game_data["change_map_squares"]:
        #     pygame.draw.rect(screen, (255, 0, 0), camera.apply(zone["rect"]))
>>>>>>> Stashed changes

        for pit in game_data["grave_pits"]:
            image_to_draw = grave_closed_img if pit['state'] == 'closed' else grave_opened_img
            screen.blit(image_to_draw, camera.apply(pit['rect']))

<<<<<<< Updated upstream
# Quit Pygame
pygame.quit()
=======
        for grave in game_data["graves"]:
            grave.draw(screen, camera)

        for obj in game_data["map_objects"]:
            screen.blit(
                obj["image"],
                camera.apply(obj["rect"]).move(
                    0, obj["rect"].height - obj["image"].get_height()
                )
            )

        pygame.draw.rect(screen, player.color, camera.apply(player.rect))

        gui.draw_inventory()
        # gui.draw()
        fade.draw()
        pygame.display.flip()
        clock.tick(60)

# Pre prípad, že chceš spustiť iba main.py na testovanie
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    spustit_hru(screen)
>>>>>>> Stashed changes
