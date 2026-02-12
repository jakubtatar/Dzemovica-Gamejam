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
from npc import NPC

# --- DÔLEŽITÉ: IMPORT ESC MENU ---
from EscMenu import EscMenu

try:
    from graveDigMinigame import GraveDigMinigame
except ImportError:
    print("POZOR: graveDigMinigame.py nenájdený. Kopanie nebude fungovať.")
    class GraveDigMinigame:
        def __init__(self, screen): pass
        def run(self): return 10

# --- ZÁCHRANNÉ TRIEDY ---
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
def rotate_surface(surface, angle, pivot, offset):
    rotated_image = pygame.transform.rotate(surface, angle)
    rotated_rect = rotated_image.get_rect(center=pivot + offset)
    return rotated_image, rotated_rect

def spustit_hru(screen):
    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()
    
    # 1. NAČÍTANIE ZDROJOV
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
    player = Player(x=100, y=100, width=50, height=100, color=(0, 128, 255))
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

        path_img = pygame.image.load(r"Resources/Floors/Floor_Path.png").convert_alpha()

        wheat_wall_img = pygame.image.load(r"Resources/Walls/Wall_Wheat.png").convert_alpha()
        wheat_wall_top_img = pygame.image.load(r"Resources/Walls/Wall_Wheat_Top.png").convert_alpha()

        grave_closed_img = pygame.image.load(r"Resources/Grave_Closed.png").convert_alpha()
        grave_opened_img = pygame.image.load(r"Resources/Grave_Opened.png").convert_alpha()

        #Voda
        water_gif = pygame.image.load(r"Resources/Water.gif").convert_alpha()

        # Objekty
        object_well_img = pygame.image.load(r"Resources/Objects/Object_Well.png").convert_alpha()
        object_house_img = pygame.image.load(r"Resources/Objects/Object_House_01.png").convert_alpha()
        object_church_img = pygame.image.load(r"Resources/Objects/Object_Church.png").convert_alpha()
        object_shop_img = pygame.image.load(r"Resources/Objects/Object_Zabkas.png").convert_alpha()
        object_tree_img = pygame.image.load(r"Resources/Objects/Object_Tree.png").convert_alpha()
        object_taverna_img = pygame.image.load(r"Resources/Objects/Object_Taverna.png").convert_alpha()

        # --- NOVÝ OBRÁZOK DUCHA ---
        ghost_img = pygame.image.load(r"Resources/NPCs/Ghost_Front1.png").convert_alpha()
        ghost_img = pygame.transform.scale(ghost_img, (50, 70)) # Zmena mierky (šírka 50, výška 70)

    except Exception as e:
        print(f"CHYBA PRI NAČÍTANÍ OBRÁZKOV: {e}")
        return

    # Škálovanie ostatných
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

    water_gif = pygame.transform.scale(water_gif, (TILE_SIZE, TILE_SIZE))
    path_img = pygame.transform.scale(path_img, (TILE_SIZE, TILE_SIZE))
    
    grave_closed_img = pygame.transform.scale(grave_closed_img, (TILE_SIZE, TILE_SIZE * 2))
    grave_opened_img = pygame.transform.scale(grave_opened_img, (TILE_SIZE, TILE_SIZE * 2))
    
    object_well_img = pygame.transform.scale(object_well_img, (TILE_SIZE * 4, TILE_SIZE * 4))
    object_house_img = pygame.transform.scale(object_house_img, (TILE_SIZE * 7, TILE_SIZE * 7))
    object_church_img = pygame.transform.scale(object_church_img, (TILE_SIZE * 14, TILE_SIZE * 14))
    object_shop_img = pygame.transform.scale(object_shop_img, (TILE_SIZE * 7, TILE_SIZE * 7))
    object_tree_img = pygame.transform.scale(object_tree_img, (TILE_SIZE * 7, TILE_SIZE * 7))
    object_taverna_img = pygame.transform.scale(object_taverna_img, (TILE_SIZE * 7, TILE_SIZE * 7))

    gravestone_images = load_images_from_folder("Resources/Gravestones", TILE_SIZE)

    player_dialog_img = pygame.image.load("Resources/Hugo/Hugo_Front1.png").convert_alpha()
    player_dialog_img = pygame.transform.scale(player_dialog_img, (200, 350))

    priest__img = pygame.image.load("Resources/NPCs/Priest_Front1.png").convert_alpha()
    priest__img = pygame.transform.scale(priest__img, (50, 100))
    priest_dialog_img = pygame.image.load("Resources/NPCs/Priest_Front1.png").convert_alpha()
    priest_dialog_img = pygame.transform.scale(priest_dialog_img, (200, 350))


    # --- SETUP MAPY ---
    game_data = {
        "walls": [],
        "collidable_walls": [],
        "map_objects": [],
        "change_map_squares": [],
        "current_map": "",
        "graves": [],       
        "grave_pits": [],
        "enemies": [], # Zoznam pre duchov (ukladáme slovníky: {"rect": Rect, "image": Surface})
        "persistent_graves": { "cmitermap": [], "crossroad": [], "houseplace": [], "village": [] },
        "persistent_pits": { "cmitermap": [], "crossroad": [], "houseplace": [], "village": [] },
        "map_switch_cooldown": 0,
        "night_mode": False,
        "night_timer": 0,
        "night_text_timer": 0,
        "visible_mapchangers": True, #Developerske nastavenie
    }

    def setup_map(map_name):
        game_data["current_map"] = map_name
        game_data["map_objects"] = []
        game_data["change_map_squares"] = []
        game_data["collidable_walls"] = []
        game_data["enemies"] = []

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
                    "collidable": False
                })

        elif map_name == "crossroad":
            w, c = maps_manager.load_map(r"Resources/Bitmaps/crossroad.txt", TILE_SIZE)
            game_data["walls"] = w
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
                "spawn": (200, 700)
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

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(250, 430, TILE_SIZE, TILE_SIZE),
                "target": "house",
                "spawn": (150, 450)
            })

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
                "rect": pygame.Rect(0, 600, TILE_SIZE, TILE_SIZE * 3),
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
            game_data["map_objects"].append({
                "rect": pygame.Rect(1900, 0, TILE_SIZE * 7, TILE_SIZE * 7),
                "image": object_taverna_img,
                "collidable": True
            })

            priest_x, priest_y = 800, 400
            priest_width, priest_height = 60, 100

            priest_npc = NPC(
                priest_x, priest_y,
                priest_width, priest_height,
                "Resources/NPCs/Priest_Front1.png",
                [
                    "My son...",
                    "Darkness is spreading across the land.",
                    "You need to protect the village.",
                    "God be with you."
                ]
            )

            game_data["npc"] = priest_npc

            game_data["map_objects"].append({
                "rect": priest_npc.rect,
                "image": priest__img,
                "collidable": False,
                "npc_ref": priest_npc
            })

        elif map_name == "house":
            w, c = maps_manager.load_map(r"Resources/Bitmaps/house.txt", TILE_SIZE)
            game_data["walls"] = w
            game_data["collidable_walls"] = c
            player.rect.topleft = (100, 500)

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(150, 550, TILE_SIZE, TILE_SIZE),
                "target": "houseplace",
                "spawn": (250, 500)
            })


        # Objekty do kolízií (len kolidovateľné)
        for obj in game_data["map_objects"]:
            if obj["collidable"]:
                game_data["collidable_walls"].append(obj["rect"])

    setup_map("cmitermap")
    fade.fade_in()

    # Dialogy
    dialogue_active = False
    dialogue_index = 0
    font = pygame.font.Font("Resources/Fonts/upheavtt.ttf", 32)

    attack_active = False
    attack_start_time = 0
    attack_duration = 150  # čas swingu v ms
    sword_length = 70
    sword_width = 10
    sword_surf = pygame.Surface((sword_length, sword_width), pygame.SRCALPHA)
    pygame.draw.rect(sword_surf, (100, 50, 0), (0, 0, 10, sword_width)) 
    pygame.draw.rect(sword_surf, (200, 200, 200), (10, 0, sword_length - 10, sword_width)) 
    enemies_hit_this_swing = []


    # --- HERNÁ SLUČKA ---
    running = True
    game_over = False

    while running:
        selected_item = gui.get_selected_item()
        
        if game_data["map_switch_cooldown"] > 0:
            game_data["map_switch_cooldown"] -= 1

        if game_data["map_switch_cooldown"] == 0:
            for zone in game_data["change_map_squares"]:
                if player.rect.colliderect(zone["rect"]) and not game_data["night_mode"]:
                    fade.fade_in()
                    stara_mapa = game_data["current_map"]
                    game_data["persistent_graves"][stara_mapa] = game_data["graves"]
                    game_data["persistent_pits"][stara_mapa] = game_data["grave_pits"]

                    nova_mapa = zone["target"]
                    setup_map(nova_mapa)
                    player.rect.topleft = zone["spawn"]

                    game_data["graves"] = game_data["persistent_graves"].get(nova_mapa, [])
                    game_data["grave_pits"] = game_data["persistent_pits"].get(nova_mapa, [])

                    for pit in game_data["grave_pits"]:
                        game_data["collidable_walls"].append(pit['rect'])

                    game_data["map_switch_cooldown"] = 30
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # --- NOVÁ ESC LOGIKA ---
                if event.key == pygame.K_ESCAPE:
                    menu = EscMenu(screen)
                    vysledok = menu.run()
                    if vysledok == "quit":
                        return  # Vráti sa do menu.py
                
                if event.key == pygame.K_e:
                    if game_data["current_map"] == "village":
                        npc = game_data.get("npc")
                        if npc and player.rect.colliderect(npc.rect.inflate(40,40)):
                            dialogue_active = True
                            dialogue_index = 0


            if event.type == pygame.MOUSEBUTTONDOWN: 
                if dialogue_active and event.button == 1:
                    dialogue_index += 1
                    npc = game_data.get("npc")
                    if dialogue_index >= len(npc.dialogue_lines):
                        dialogue_active = False
                    continue

                if event.button == 1 and not game_over: 
                    if selected_item == "[1] Sword":  # uprav podľa názvu v GUI
                        attack_active = True
                        attack_start_time = pygame.time.get_ticks()

                        attack_size = 100

                        if player.direction == "right":
                            attack_rect = pygame.Rect(player.rect.right, player.rect.centery-20, attack_size, 40)
                        elif player.direction == "left":
                            attack_rect = pygame.Rect(player.rect.left-attack_size, player.rect.centery-20, attack_size, 40)
                        elif player.direction == "up":
                            attack_rect = pygame.Rect(player.rect.centerx-20, player.rect.top-attack_size, 40, attack_size)
                        elif player.direction == "down":
                            attack_rect = pygame.Rect(player.rect.centerx-20, player.rect.bottom, 40, attack_size)

                        # DAMAGE CHECK
                        for enemy in game_data["enemies"]:
                            enemy["rect"].x += enemy["knockback_x"]
                            enemy["rect"].y += enemy["knockback_y"]

                            enemy["knockback_x"] *= 0.85
                            enemy["knockback_y"] *= 0.85
                            if attack_rect.colliderect(enemy["rect"]):

                                enemy["health"] -= 15

                                # --- KNOCKBACK ---
                                dx = enemy["rect"].centerx - player.rect.centerx
                                dy = enemy["rect"].centery - player.rect.centery
                                length = math.hypot(dx, dy)

                                if length != 0:
                                    dx /= length
                                    dy /= length

                                knockback_strength = 15
                                enemy["knockback_x"] = dx * knockback_strength
                                enemy["knockback_y"] = dy * knockback_strength
                    if selected_item == "[2] Shovel":
                        if game_data["current_map"] == "cmitermap":
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
                            print("Pôda je tu príliš tvrdá na kopanie.")

                # PRAVÉ TLAČIDLO (Otváranie hrobov + Spawn nepriateľov)
                elif event.button == 3 and not game_over: 
                   if not game_data["night_mode"]:
                    game_data["night_mode"] = True
                    game_data["night_timer"] = 60 * 60  # 60 sekúnd pri 60 FPS
                    game_data["night_text_timer"] = 180
                    for pit in game_data["grave_pits"]: 
                        pit['state'] = 'opened' 
                    
                    if game_data["current_map"] == "cmitermap":
                        for _ in range(5):
                            dist_x = random.randint(300, 600) * random.choice([-1, 1])
                            dist_y = random.randint(300, 600) * random.choice([-1, 1])
                            new_enemy_rect = ghost_img.get_rect(topleft=(player.rect.x + dist_x, player.rect.y + dist_y))
                            game_data["enemies"].append({
                                "rect": new_enemy_rect,
                                "image": ghost_img,
                                "health": 30,
                                "max_health": 30,
                                "knockback_x": 0,
                                "knockback_y": 0
                            })


            gui.handle_input(event)

        # --- UPDATE NEPRIATEĽOV ---
        for enemy in game_data["enemies"]:
            e_rect = enemy["rect"]
            speed = 1
            if player.rect.x > e_rect.x: e_rect.x += speed
            if player.rect.x < e_rect.x: e_rect.x -= speed
            if player.rect.y > e_rect.y: e_rect.y += speed
            if player.rect.y < e_rect.y: e_rect.y -= speed
            
            if player.rect.colliderect(e_rect):
                current_time = pygame.time.get_ticks()

                # damage iba raz za 1 sekundu
                if current_time - player.last_damage_time >= 1000 and not game_over:
                    player.health -= 10
                    player.last_damage_time = current_time
                    print("HP:", player.health)

                    if player.health <= 0:
                        game_over = True
        game_data["enemies"] = [e for e in game_data["enemies"] if e["health"] > 0]



        if not dialogue_active and not game_over:
            player.handle_keys_with_collision(4000, 4000, game_data["collidable_walls"])

        camera.update(player)
        fade.update()

        # --- VYKRESĽOVANIE ---
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
                wheat_wall_img, wheat_wall_top_img, water_gif, path_img
            )

        if game_data["visible_mapchangers"]:
            for zone in game_data["change_map_squares"]:
                debug_surf = pygame.Surface((zone["rect"].width, zone["rect"].height), pygame.SRCALPHA)
                debug_surf.fill((255, 255, 0, 120)) # Žltá je lepšie vidieť na tráve
                screen.blit(debug_surf, camera.apply(zone["rect"]))

        for pit in game_data["grave_pits"]:
            image_to_draw = grave_closed_img if pit['state'] == 'closed' else grave_opened_img
            screen.blit(image_to_draw, camera.apply(pit['rect']))

        # Y-SORTING
        render_queue = []
        render_queue.append({"type": "player", "obj": player, "y": player.rect.bottom})
        for obj in game_data["map_objects"]:
            render_queue.append({"type": "object", "obj": obj, "y": obj["rect"].bottom})
        for grave in game_data["graves"]:
            render_queue.append({"type": "grave", "obj": grave, "y": grave.rect.bottom})
        for enemy in game_data["enemies"]:
            render_queue.append({"type": "enemy", "obj": enemy, "y": enemy["rect"].bottom})
    
        render_queue.sort(key=lambda x: x["y"])

        for item in render_queue:
            if item["type"] == "player":
                try: item["obj"].draw(screen, camera)
                except: pygame.draw.rect(screen, item["obj"].color, camera.apply(item["obj"].rect))
            
            elif item["type"] == "grave":
                item["obj"].draw(screen, camera)
            
            elif item["type"] == "object":
                obj = item["obj"]
                draw_pos = camera.apply(obj["rect"]).move(0, obj["rect"].height - obj["image"].get_height())
                screen.blit(obj["image"], draw_pos)
            
            elif item["type"] == "enemy":
                # VYKRESLENIE OBRÁZKA DUCHA
                screen.blit(item["obj"]["image"], camera.apply(item["obj"]["rect"]))
                enemy = item["obj"]
                rect_on_screen = camera.apply(enemy["rect"])

                bar_width = 40
                bar_height = 6
                health_ratio = enemy["health"] / enemy["max_health"]

                bar_x = rect_on_screen.centerx - bar_width // 2
                bar_y = rect_on_screen.y - 10

                pygame.draw.rect(screen, (150,0,0), (bar_x, bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, (0,200,0), (bar_x, bar_y, bar_width * health_ratio, bar_height))


        # --- NPC INTERACT TEXT ---
        npc = game_data.get("npc")
        if npc and player.rect.colliderect(npc.rect.inflate(80, 80)) and not dialogue_active:
            interact_font = pygame.font.Font("Resources/Fonts/upheavtt.ttf", 24)
            interact_text = interact_font.render("Press E", True, (255, 255, 0))
            text_rect = interact_text.get_rect(center=(npc.rect.centerx, npc.rect.top - 20))
            screen.blit(interact_text, camera.apply(text_rect))

        if dialogue_active:
            screen.blit(player_dialog_img, (50, screen_height - 450))
            screen.blit(priest_dialog_img, (screen_width - 250, screen_height - 450))
            dialogue_box = pygame.Rect(0, screen_height - 200, screen_width, 200)
            pygame.draw.rect(screen, (0,0,0), dialogue_box)
            npc = game_data.get("npc")
            text = npc.dialogue_lines[dialogue_index]
            rendered_text = font.render(text, True, (255,255,255))
            screen.blit(rendered_text, (50, screen_height - 120))

        if game_over:
            # Šedý overlay
            grey_overlay = pygame.Surface((screen_width, screen_height))
            grey_overlay.set_alpha(180)  # priehľadnosť (0-255)
            grey_overlay.fill((0, 0, 0))  # šedá farba
            screen.blit(grey_overlay, (0, 0))

            # Text YOU DIED
            death_font = pygame.font.Font("Resources/Fonts/upheavtt.ttf", 100)
            death_text = death_font.render("YOU DIED", True, (200, 0, 0))
            text_rect = death_text.get_rect(center=(screen_width//2, screen_height//2))
            screen.blit(death_text, text_rect)
        
        # attack vizuál
        if attack_active and not game_over:
            elapsed = pygame.time.get_ticks() - attack_start_time
            progress = elapsed / attack_duration 

            if progress >= 1:
                attack_active = False
            else:
                direction_angles = {"right": 0, "left": 180, "up": 270, "down": 90}
                base_angle = direction_angles.get(player.direction, 0)

                swing_range = 120 
                current_swing_angle = base_angle - (progress * swing_range - 60)

                rotated_image = pygame.transform.rotate(sword_surf, -current_swing_angle)
                
                pivot_offset_vec = pygame.math.Vector2(sword_length / 2, 0)
                rotated_pivot_offset = pivot_offset_vec.rotate(current_swing_angle)
                
                new_rect_center = pygame.math.Vector2(player.rect.center) + rotated_pivot_offset
                sword_rect = rotated_image.get_rect(center=new_rect_center)

                screen.blit(rotated_image, camera.apply(sword_rect))

                for enemy in game_data["enemies"]:
                    if sword_rect.colliderect(enemy["rect"]):
                        if enemy not in enemies_hit_this_swing:
                            enemy["health"] -= 15
                            enemies_hit_this_swing.append(enemy)
                            dx = enemy["rect"].centerx - player.rect.centerx
                            dy = enemy["rect"].centery - player.rect.centery
                            dist = math.hypot(dx, dy)
                            if dist != 0:
                                enemy["knockback_x"] = (dx / dist) * 20
                                enemy["knockback_y"] = (dy / dist) * 20
        
        # NIGHT MODE
        if game_data["night_mode"] and not game_over:
            # 1. Overlay a svetelný kruh sledujúci hráča
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 230))
            
            # Výpočet pozície hráča na obrazovke
            player_screen_pos = camera.apply(player.rect).center
            pygame.draw.circle(overlay, (0, 0, 0, 0), player_screen_pos, 180)
            screen.blit(overlay, (0, 0))

            # 2. Odpočítavanie noci
            game_data["night_timer"] -= 1
            
            # Zobrazenie textu "NASTALA NOC"
            if game_data["night_text_timer"] > 0:
                night_font = pygame.font.Font("Resources/Fonts/upheavtt.ttf", 70)
                night_text = night_font.render("THE NIGHT HAS COME", True, (255, 255, 255))
                screen.blit(night_text, night_text.get_rect(center=(screen_width // 2, 100)))
                game_data["night_text_timer"] -= 1

            # Zobrazenie zostávajúceho času noci
            timer_font = pygame.font.Font("Resources/Fonts/upheavtt.ttf", 40)
            seconds_left = max(0, game_data["night_timer"] // 60)
            timer_text = timer_font.render(f"The night will end in: {seconds_left}s", True, (255, 255, 255))
            screen.blit(timer_text, (screen_width // 2 - 120, 20))

            # 3. Koniec noci - upratovanie
            if game_data["night_timer"] <= 0:
                game_data["night_mode"] = False
                game_data["enemies"].clear()  # Zabije všetkých duchov
                for pit in game_data["grave_pits"]: 
                    pit['state'] = 'closed'  # Zatvorí jamy

        gui.draw()
        fade.draw()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    spustit_hru(screen)