import pygame
import sys
import os
import math
import random

# --- IMPORTY TVOJICH EXISTUJÚCICH SÚBOROV ---
from camera import Camera
from gui import GUI
from fade import Fade
from grave import Grave
from dialogue import Dialogue
from mapsmanager import MapsManager
from item import Item
# Ak máš minihru v samostatnom súbore, nechaj tento import.
# Ak nie, uisti sa, že trieda GraveDigMinigame je dostupná.
try:
    from graveDigMinigame import GraveDigMinigame
except ImportError:
    print("POZOR: graveDigMinigame.py nenájdený. Kopanie nebude fungovať.")
    class GraveDigMinigame:
        def __init__(self, screen): pass
        def run(self): return 10 # Dummy reward

# --- ZÁCHRANNÉ TRIEDY (AK CHÝBA PLAYER ALEBO QUEST) ---
try:
    from player import Player
except ImportError:
    print("POZOR: Chýba player.py, používam náhradný (Dummy) Player.")
    class Player:
        def __init__(self, x, y, size=50, width=50, height=50, color=(0,0,255)):
            self.rect = pygame.Rect(x, y, width, height)
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
            self.money = 0
            self.day = "Monday"
            self.color = color
        def handle_keys_with_collision(self, w, h, walls):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: self.rect.y -= 5
            if keys[pygame.K_s]: self.rect.y += 5
            if keys[pygame.K_a]: self.rect.x -= 5
            if keys[pygame.K_d]: self.rect.x += 5
        def draw(self, screen, camera):
            screen.blit(self.image, camera.apply(self.rect))

try:
    from quest import Quest
except ImportError:
    class Quest: pass 
try:
    from objectZone import ObjectZone
except ImportError:
    class ObjectZone: pass


# ==========================================
# HLAVNÁ FUNKCIA HRY
# ==========================================

def spustit_hru(screen):
    """
    Toto je tvoj herný kód. Keď sa funkcia ukončí (return), vráti sa do menu.
    """
    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()
    
    # 1. NAČÍTANIE ZDROJOV (Funkcie a premenné)
    def load_images_from_folder(folder_path, tile_size):
        images = {}
        if not os.path.exists(folder_path): return images
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                key = filename.split("_")[-1].split(".")[0]
                image = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                current_height = tile_size * 2 if key == "6" else tile_size
                image = pygame.transform.scale(image, (tile_size, current_height))
                images[key] = image
        return images

    TILE_SIZE = 50
    maps_manager = MapsManager()
    fade = Fade(screen, speed=8)
    
    # Hráč a GUI
    player = Player(x=100, y=100, width=50, height=50, color=(0, 128, 255))
    camera = Camera(screen_width, screen_height)
    gui = GUI(screen, player)

    # --- NAČÍTANIE OBRÁZKOV ---
    try:
        tile1_img = pygame.image.load(r"Resources/Images/Image_Plot1.png").convert_alpha()
        tile2_img = pygame.image.load(r"Resources/Images/Image_Plot2.png").convert_alpha()
        
        hedgefront_img = pygame.image.load(r"Resources/Images/Image_HedgeFront.png").convert_alpha()
        hedgetopfront_img = pygame.image.load(r"Resources/Images/Image_HedgeTopFront.png").convert_alpha()
        hedgeRD_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerRD.png").convert_alpha()
        hedgeLD_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerLD.png").convert_alpha()
        hedgeRT_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerRT.png").convert_alpha()
        hedgeLT_img = pygame.image.load(r"Resources/Images/Image_HedgeCornerLT.png").convert_alpha()
        hedgetopwall_img = pygame.image.load(r"Resources/Images/Image_HedgeTopWall.png").convert_alpha()

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

        grave_closed_img = pygame.image.load(r"Resources/Grave_Closed.png").convert_alpha()
        grave_opened_img = pygame.image.load(r"Resources/Grave_Opened.png").convert_alpha()

        # Objekty
        object_well_img = pygame.image.load(r"Resources/Objects/Object_Well.png").convert_alpha()
        object_house_img = pygame.image.load(r"Resources/Objects/Object_House_01.png").convert_alpha()
        object_church_img = pygame.image.load(r"Resources/Objects/Object_Church.png").convert_alpha()
        object_shop_img = pygame.image.load(r"Resources/Objects/Object_Zabkas.png").convert_alpha()
        object_tree_img = pygame.image.load(r"Resources/Objects/Object_Tree.png").convert_alpha()

    except Exception as e:
        print(f"CHYBA PRI NAČÍTANÍ OBRÁZKOV: {e}")
        print("Uistite sa, že priečinok Resources je na správnom mieste.")
        return # Vráti do menu pri chybe

    # Škálovanie
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
    
    grave_closed_img = pygame.transform.scale(grave_closed_img, (TILE_SIZE, TILE_SIZE * 2))
    grave_opened_img = pygame.transform.scale(grave_opened_img, (TILE_SIZE, TILE_SIZE * 2))
    
    object_well_img = pygame.transform.scale(object_well_img, (TILE_SIZE * 4, TILE_SIZE * 4))
    object_house_img = pygame.transform.scale(object_house_img, (TILE_SIZE * 7, TILE_SIZE * 7))
    object_church_img = pygame.transform.scale(object_church_img, (TILE_SIZE * 14, TILE_SIZE * 14))
    object_shop_img = pygame.transform.scale(object_shop_img, (TILE_SIZE * 7, TILE_SIZE * 7))
    object_tree_img = pygame.transform.scale(object_tree_img, (TILE_SIZE * 7, TILE_SIZE * 7))

    gravestone_images = load_images_from_folder("Resources/Gravestones", TILE_SIZE)

    # --- SETUP MAPY ---
    game_data = {
        "walls": [],
        "collidable_walls": [],
        "map_objects": [],
        "change_map_squares": [],
        "current_map": "",
        "graves": [],       
        "grave_pits": [],   
        
        "persistent_graves": { "cmitermap": [], "crossroad": [], "houseplace": [], "village": [] },
        "persistent_pits": { "cmitermap": [], "crossroad": [], "houseplace": [], "village": [] },
        
        "map_switch_cooldown": 0
    }

    def setup_map(map_name):
        game_data["current_map"] = map_name
        game_data["map_objects"] = []
        game_data["change_map_squares"] = []
        game_data["collidable_walls"] = []

        if map_name == "cmitermap":
            w, c = maps_manager.load_map(r"Resources/Bitmaps/cmitermap.txt", TILE_SIZE)
            game_data["walls"] = w
            game_data["collidable_walls"] = c
            player.rect.topleft = (2700, 150)

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(2800, 100, TILE_SIZE, TILE_SIZE*3),
                "target": "crossroad",
                "spawn": (100, 500)
            })

            # Well object
            game_data["map_objects"].append({
                "rect": pygame.Rect(400, 800, TILE_SIZE * 4, TILE_SIZE * 4),
                "image": object_well_img,
                "collidable": True
            })

            # Trees
            tree_positions = [(800, 200), (1200, 400), (1600, 300), (2000, 600), (2400, 200), (2200, 800)]
            for pos in tree_positions:
                game_data["map_objects"].append({
                    "rect": pygame.Rect(pos[0], pos[1], TILE_SIZE * 7, TILE_SIZE * 7),
                    "image": object_tree_img,
                    "collidable": False
                })

        elif map_name == "crossroad":
            w, c = maps_manager.load_map(r"Resources/Bitmaps/crossroad.txt", TILE_SIZE)
            game_data["walls"] = w
            game_data["collidable_walls"] = c
            player.rect.topleft = (100, 500)

            # Exits
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
            w, c = maps_manager.load_map(r"Resources/Bitmaps/houseplace.txt", TILE_SIZE)
            game_data["walls"] = w
            game_data["collidable_walls"] = c
            player.rect.topleft = (150, 450)

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(300, 750, TILE_SIZE * 3, TILE_SIZE),
                "target": "crossroad",
                "spawn": (500, 100)
            })

            # House
            game_data["map_objects"].append({
                "rect": pygame.Rect(200, 100, TILE_SIZE * 7, TILE_SIZE * 7),
                "image": object_house_img,
                "collidable": True
            })
        
        elif map_name == "village":
            w, c = maps_manager.load_map(r"Resources/Bitmaps/village.txt", TILE_SIZE)
            game_data["walls"] = w
            game_data["collidable_walls"] = c
            player.rect.topleft = (100, 500)

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(0, 300, TILE_SIZE, TILE_SIZE * 3),
                "target": "crossroad",
                "spawn": (900, 500)
            })

            # Church & Shop
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

        # Pridať objekty do kolízií
        for obj in game_data["map_objects"]:
            if obj["collidable"]:
                game_data["collidable_walls"].append(obj["rect"])

    # Spustenie prvej mapy
    setup_map("cmitermap")
    fade.fade_in()

    # --- HERNÁ SLUČKA ---
    running = True
    while running:
        selected_item = gui.get_selected_item()
        
        # --- LOGIKA ZMENY MAPY ---
        if game_data["map_switch_cooldown"] > 0:
            game_data["map_switch_cooldown"] -= 1

        if game_data["map_switch_cooldown"] == 0:
            for zone in game_data["change_map_squares"]:
                if player.rect.colliderect(zone["rect"]):
                    # A. ULOŽÍME hroby STAREJ mapy
                    stara_mapa = game_data["current_map"]
                    game_data["persistent_graves"][stara_mapa] = game_data["graves"]
                    game_data["persistent_pits"][stara_mapa] = game_data["grave_pits"]

                    # B. ZMENÍME MAPU
                    nova_mapa = zone["target"]
                    setup_map(nova_mapa)
                    player.rect.topleft = zone["spawn"]

                    # C. NAČÍTAME hroby NOVEJ mapy
                    game_data["graves"] = game_data["persistent_graves"].get(nova_mapa, [])
                    game_data["grave_pits"] = game_data["persistent_pits"].get(nova_mapa, [])

                    # D. OBNOVA KOLÍZIÍ
                    for pit in game_data["grave_pits"]:
                        game_data["collidable_walls"].append(pit['rect'])

                    game_data["map_switch_cooldown"] = 30
                    break

        # Eventy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return # Vráti sa do Menu!

            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    if selected_item == "[2] Shovel":
                        # KOPANIE LEN NA CMITERMAP
                        if game_data["current_map"] == "cmitermap":
                            # Spustenie minihry
                            minigame = GraveDigMinigame(screen)
                            reward = minigame.run()
                            
                            if not hasattr(player, 'money'): player.money = 0
                            player.money += reward

                            gx = (player.rect.centerx // TILE_SIZE) * TILE_SIZE 
                            gy = (player.rect.bottom // TILE_SIZE) * TILE_SIZE 
                            
                            new_grave = Grave(gx, gy, TILE_SIZE, gravestone_images)
                            new_pit = { 'rect': pygame.Rect(gx, gy + 50, TILE_SIZE, TILE_SIZE * 2), 'state': 'closed' }
                            
                            game_data["graves"].append(new_grave) 
                            game_data["grave_pits"].append(new_pit)
                            game_data["collidable_walls"].append(new_pit['rect'])
                        else:
                            print("Pôda je tu príliš tvrdá na kopanie. Skús to na cintoríne!")

                elif event.button == 3: 
                    for pit in game_data["grave_pits"]: pit['state'] = 'opened' 

            gui.handle_input(event)

        # Update
        player.handle_keys_with_collision(4000, 4000, game_data["collidable_walls"])
        camera.update(player)
        fade.update()

        # Draw
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

        for pit in game_data["grave_pits"]:
            image_to_draw = grave_closed_img if pit['state'] == 'closed' else grave_opened_img
            screen.blit(image_to_draw, camera.apply(pit['rect']))

        for grave in game_data["graves"]:
            grave.draw(screen, camera)

        for obj in game_data["map_objects"]:
            screen.blit(
                obj["image"],
                camera.apply(obj["rect"]).move(
                    0, obj["rect"].height - obj["image"].get_height()
                )
            )

        try: player.draw(screen, camera)
        except: pygame.draw.rect(screen, player.color, camera.apply(player.rect))

        gui.draw_inventory()
        fade.draw()
        
        pygame.display.flip()
        clock.tick(60)

# ==========================================
# SPÚŠŤAČ (LEN PRE TESTOVANIE MAIN.PY)
# ==========================================
if __name__ == "__main__":
    # Tento blok sa spustí len ak zapneš priamo main.py
    # Ak ho zapne menu.py, tento kód sa ignoruje (čo je správne)
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    spustit_hru(screen)