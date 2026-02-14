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
from GhostEnemy import GhostEnemy, SkeletonArcher, GhoulTank

from gamedays import Monday
from gamedays import Tuesday

pygame.mixer.init()
current_track = None

# --- DÔLEŽITÉ: IMPORT ESC MENU ---
from EscMenu import EscMenu

try:
    from graveDigMinigame import GraveDigMinigame
    from graveDigMinigame import TimingDigMinigame
    from graveDigMinigame import SequenceDigMinigame
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
            self.health = 100
            self.last_damage_time = 0
            self.direction = "down"
        def handle_keys_with_collision(self, w, h, walls):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: self.rect.y -= 5; self.direction = "up"
            if keys[pygame.K_s]: self.rect.y += 5; self.direction = "down"
            if keys[pygame.K_a]: self.rect.x -= 5; self.direction = "left"
            if keys[pygame.K_d]: self.rect.x += 5; self.direction = "right"
        def draw(self, screen, camera):
            screen.blit(self.image, camera.apply(self.rect))

try:
    from quest import Quest
except ImportError:
    class Quest: pass 
# ==========================================
# HLAVNÁ FUNKCIA HRY
# ==========================================
def rotate_surface(surface, angle, pivot, offset):
    rotated_image = pygame.transform.rotate(surface, angle)
    rotated_rect = rotated_image.get_rect(center=pivot + offset)
    return rotated_image, rotated_rect
# ==========================================
             #Sound management
# ==========================================
def handle_music(is_night):
    global current_track
        
    if is_night:
            target_track = os.path.join("Resources", "Music", "Night.mp3")
    else:
            target_track = os.path.join("Resources", "Music", "Day.mp3")
            
    if current_track != target_track:
            try:
                if target_track:
                    if os.path.exists(target_track):
                        pygame.mixer.music.fadeout(1000)
                        pygame.mixer.music.load(target_track)
                        pygame.mixer.music.play(-1)
                        if target_track == os.path.join("Resources", "Music", "Day.mp3"):
                            pygame.mixer.music.set_volume(0.01)
                        else:
                            pygame.mixer.music.set_volume(0.8)
                        current_track = target_track
                        print(f"Hrá hudba: {target_track}")
                    else:
                        print(f"CHYBA: Súbor nenájdený na ceste: {os.path.abspath(target_track)}")
                        current_track = target_track 
                else:
                    pygame.mixer.music.fadeout(1000)
                    current_track = None
            except Exception as e:
                print(f"Chyba pri načítaní hudby: {e}")

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
        floor_tiles_img = pygame.image.load(r"Resources/Floors/Floor_Tiles.png").convert_alpha()

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
        object_bridge_img = pygame.image.load(r"Resources/Objects/Object_Bridge.png").convert_alpha()
        object_register_img = pygame.image.load(r"Resources/Objects/Object_Register.png").convert_alpha() 
        object_fruit_img = pygame.image.load(r"Resources/Objects/Object_Fruit.png").convert_alpha()
        object_shelf_img = pygame.image.load(r"Resources/Objects/Object_Shelf.png").convert_alpha()  

        object_bottleshelf_img = pygame.image.load(r"Resources/Objects/Object_BottleShelf.png").convert_alpha()
        object_barchair_img = pygame.image.load(r"Resources/Objects/Object_BarChair.png").convert_alpha()
        object_counter_img = pygame.image.load(r"Resources/Objects/Object_Counter.png").convert_alpha()
        object_bartable_img = pygame.image.load(r"Resources/Objects/Object_Bartable.png").convert_alpha()

        object_bed_img = pygame.image.load(r"Resources/Objects/Object_Bed.png").convert_alpha()
        object_wardrobe_img = pygame.image.load(r"Resources/Objects/Object_Wardrobe.png").convert_alpha()   
        object_desk_img = pygame.image.load(r"Resources/Objects/Object_Desk.png").convert_alpha()               

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
    floor_tiles_img = pygame.transform.scale(floor_tiles_img, (TILE_SIZE, TILE_SIZE))
    
    grave_closed_img = pygame.transform.scale(grave_closed_img, (TILE_SIZE, TILE_SIZE * 2))
    grave_opened_img = pygame.transform.scale(grave_opened_img, (TILE_SIZE, TILE_SIZE * 2))
    
    object_well_img = pygame.transform.scale(object_well_img, (TILE_SIZE * 4, TILE_SIZE * 4))
    object_house_img = pygame.transform.scale(object_house_img, (TILE_SIZE * 7, TILE_SIZE * 7))
    object_church_img = pygame.transform.scale(object_church_img, (TILE_SIZE * 14, TILE_SIZE * 14))
    object_shop_img = pygame.transform.scale(object_shop_img, (TILE_SIZE * 7, TILE_SIZE * 7))
    object_tree_img = pygame.transform.scale(object_tree_img, (TILE_SIZE * 7, TILE_SIZE * 7))
    object_taverna_img = pygame.transform.scale(object_taverna_img, (TILE_SIZE * 7, TILE_SIZE * 7))
    object_bridge_img = pygame.transform.scale(object_bridge_img, (TILE_SIZE * 3, TILE_SIZE * 3))
    object_register_img  = pygame.transform.scale(object_register_img, (TILE_SIZE * 4, TILE_SIZE * 2))
    object_fruit_img  = pygame.transform.scale(object_fruit_img, (TILE_SIZE * 4, TILE_SIZE * 4))
    object_shelf_img  = pygame.transform.scale(object_shelf_img, (TILE_SIZE * 3, TILE_SIZE * 4))

    #nabytok
    object_bottleshelf_img = pygame.transform.scale(object_bottleshelf_img, (TILE_SIZE *4, TILE_SIZE *4))
    object_barchair_img = pygame.transform.scale(object_barchair_img, (TILE_SIZE *1.5, TILE_SIZE *1.5))
    object_counter_img = pygame.transform.scale(object_counter_img, (TILE_SIZE *1.5, TILE_SIZE *1.5))
    object_bartable_img = pygame.transform.scale(object_bartable_img, (TILE_SIZE *3, TILE_SIZE *3))
    object_bed_img = pygame.transform.scale(object_bed_img, (TILE_SIZE *2, TILE_SIZE *2.5))
    object_wardrobe_img = pygame.transform.scale(object_wardrobe_img, (TILE_SIZE *2, TILE_SIZE *3))
    object_desk_img = pygame.transform.scale(object_desk_img, (TILE_SIZE *2, TILE_SIZE *3))

    gravestone_images = load_images_from_folder("Resources/Gravestones", TILE_SIZE)

    player_dialog_img = pygame.image.load("Resources/Hugo/Hugo_Front1.png").convert_alpha()
    player_dialog_img = pygame.transform.scale(player_dialog_img, (200, 350))

    priest__img = pygame.image.load("Resources/NPCs/Priest_Front1.png").convert_alpha()
    priest__img = pygame.transform.scale(priest__img, (50, 100))

    barman__img = pygame.image.load("Resources/NPCs/Barman_Front1.png").convert_alpha()
    barman__img = pygame.transform.scale(barman__img, (50, 100))

    barman_dialog_img = pygame.image.load("Resources/NPCs/Barman_Front1.png").convert_alpha()
    barman_dialog_img = pygame.transform.scale(barman_dialog_img, (200, 350))

    priest_dialog_img = pygame.image.load("Resources/NPCs/Priest_Front1.png").convert_alpha()
    priest_dialog_img = pygame.transform.scale(priest_dialog_img, (200, 350))

    shopkeeper__img = pygame.image.load("Resources/NPCs/Shopkeeper_Front1.png").convert_alpha()
    shopkeeper__img = pygame.transform.scale(shopkeeper__img, (50, 100))

    shopkeeper_dialog_img = pygame.image.load("Resources/NPCs/Shopkeeper_Front1.png").convert_alpha()
    shopkeeper_dialog_img = pygame.transform.scale(shopkeeper__img, (200, 350))

    # --- SETUP MAPY ---
    game_data = {
        "walls": [],
        "collidable_walls": [],
        "map_objects": [],
        "change_map_squares": [],
        "current_map": "",
        "graves": [],       
        "grave_pits": [],
        "enemies": [], 
        "arrows": [],
        "persistent_graves": { "cmitermap": [], "crossroad": [], "houseplace": [], "village": [] },
        "persistent_pits": { "cmitermap": [], "crossroad": [], "houseplace": [], "village": [] },
        "map_switch_cooldown": 0,
        "night_mode": False,
        "night_timer": 0,
        "night_text_timer": 0,
        "visible_mapchangers": True, #Developerske nastavenie
        "last_dig_time": 0,
        "dig_cooldown": 2000, # 2 sekundy pauza medzi kopaním (v milisekundách)
        "gameday": 1,
        "night_finished": False, 
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
            game_data["change_map_squares"].append({
                "rect": pygame.Rect(1750, 320, TILE_SIZE*3, TILE_SIZE * 3),
                "target": "taverna",
                "spawn": (400, 500)
            })
            game_data["change_map_squares"].append({
                "rect": pygame.Rect(1620, 770, TILE_SIZE*2, TILE_SIZE * 3),
                "target": "store",
                "spawn": (300, 350)
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(900, -400, TILE_SIZE * 14, TILE_SIZE * 14),
                "image": object_church_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(1600, 550, TILE_SIZE * 7, TILE_SIZE * 7),
                "image": object_shop_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(1650, 100, TILE_SIZE * 7, TILE_SIZE * 7),
                "image": object_taverna_img,
                "collidable": True
            })
            tree_positions = [(350, 250),(650, 200), (850, 500), (1250, 400), (1300, 800), (700, -150), (1550, -150), (1850, 200)]
            for pos in tree_positions:
                game_data["map_objects"].append({
                    "rect": pygame.Rect(pos[0], pos[1], TILE_SIZE * 7, TILE_SIZE * 7),
                    "image": object_tree_img,
                    "collidable": False
                })

            priest_x, priest_y = 1400, 230
            priest_width, priest_height = 60, 100

            priest_npc = NPC(priest_x, priest_y, priest_width, priest_height, 
                 "Resources/NPCs/Priest_Front1.png", 
                 ["My son...", "Darkness is spreading.", "God be with you."],
                 priest_dialog_img)

            game_data["npc"] = priest_npc

            game_data["map_objects"].append({
                "rect": priest_npc.rect,
                "image": priest__img,
                "collidable": False,
                "npc_ref": priest_npc
            })
            priest_npc.name = "Priest"


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
            
            game_data["map_objects"].append({
                "rect": pygame.Rect(200, 75, TILE_SIZE * 2, TILE_SIZE * 2.5),
                "image": object_bed_img,
                "collidable": True
            })

            game_data["map_objects"].append({
                "rect": pygame.Rect(50, 50, TILE_SIZE * 2, TILE_SIZE * 3),
                "image": object_wardrobe_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(200, 300, TILE_SIZE * 2, TILE_SIZE * 3),
                "image": object_desk_img,
                "collidable": True
            })

        elif map_name == "taverna":
            w, c = maps_manager.load_map(r"Resources/Bitmaps/taverna.txt", TILE_SIZE)
            game_data["walls"] = w
            game_data["collidable_walls"] = c
            player.rect.topleft = (100, 500)

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(300, 550, TILE_SIZE*3, TILE_SIZE),
                "target": "village",
                "spawn": (1800, 500)
            })

            game_data["map_objects"].append({
                "rect": pygame.Rect(500, 0, TILE_SIZE * 4, TILE_SIZE * 4),
                "image": object_bottleshelf_img,
                "collidable": True
            })

            game_data["map_objects"].append({
                "rect": pygame.Rect(300, 0, TILE_SIZE * 4, TILE_SIZE * 4),
                "image": object_bottleshelf_img,
                "collidable": True
            })

            game_data["map_objects"].append({
                "rect": pygame.Rect(400, 225, TILE_SIZE * 1.5, TILE_SIZE * 1.5),
                "image": object_counter_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(475, 225, TILE_SIZE * 1.5, TILE_SIZE * 1.5),
                "image": object_counter_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(550, 225, TILE_SIZE * 1.5, TILE_SIZE * 1.5),
                "image": object_counter_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(625, 225, TILE_SIZE * 1.5, TILE_SIZE * 1.5),
                "image": object_counter_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(625, 275, TILE_SIZE * 1.5, TILE_SIZE * 1.5),
                "image": object_barchair_img,
                "collidable": False
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(550, 275, TILE_SIZE * 1.5, TILE_SIZE * 1.5),
                "image": object_barchair_img,
                "collidable": False
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(475, 275, TILE_SIZE * 1.5, TILE_SIZE * 1.5),
                "image": object_barchair_img,
                "collidable": False
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(400, 275, TILE_SIZE * 1.5, TILE_SIZE * 1.5),
                "image": object_barchair_img,
                "collidable": False
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(100, 300, TILE_SIZE * 3, TILE_SIZE * 3),
                "image": object_bartable_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(100, 100, TILE_SIZE * 3, TILE_SIZE * 3),
                "image": object_bartable_img,
                "collidable": True
            })

            barman_x, barman_y = 400, 150
            barman_width, barman_height = 60, 100

            barman_npc = NPC(barman_x, barman_y, barman_width, barman_height, 
                            "Resources/NPCs/Barman_Front1.png", 
                            ["Wanna something healthy to drink?"],
                            barman_dialog_img)
            barman_npc.name = "Barman"
            game_data["npc"] = barman_npc

            game_data["map_objects"].append({
                "rect": barman_npc.rect,
                "image": barman__img,
                "collidable": False,
                "npc_ref": barman_npc
            })

        elif map_name == "store":
            w, c = maps_manager.load_map(r"Resources/Bitmaps/store.txt", TILE_SIZE)
            game_data["walls"] = w
            game_data["collidable_walls"] = c
            player.rect.topleft = (100, 500)

            game_data["change_map_squares"].append({
                "rect": pygame.Rect(200, 500, TILE_SIZE*3, TILE_SIZE),
                "target": "village",
                "spawn": (1700, 1000)
            })
            

            shopkeeper_x, shopkeeper_y = 200, 0
            shopkeeper_width, shopkeeper_height = 60, 100

            shopkeeper_npc = NPC(shopkeeper_x, shopkeeper_y, shopkeeper_width, shopkeeper_height, 
                            "Resources/NPCs/Shopkeeper_Front1.png", 
                            ["Hello! Welcome to Zabkas!"],
                            shopkeeper_dialog_img)
            shopkeeper_npc.name = "Shopkeeper"
            game_data["npc"] = shopkeeper_npc

            game_data["map_objects"].append({
                "rect": shopkeeper_npc.rect,
                "image": shopkeeper__img,
                "collidable": False,
                "npc_ref": shopkeeper__img
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(50, 100, TILE_SIZE * 4, TILE_SIZE * 2),
                "image": object_register_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(50, 250, TILE_SIZE * 4, TILE_SIZE * 4),
                "image": object_fruit_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(350, 0, TILE_SIZE * 3, TILE_SIZE * 4),
                "image": object_shelf_img,
                "collidable": True
            })
            game_data["map_objects"].append({
                "rect": pygame.Rect(350, 220, TILE_SIZE * 3, TILE_SIZE * 4),
                "image": object_shelf_img,
                "collidable": True
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
    attack_duration = 150
    sword_length = 70
    sword_width = 10
    sword_surf = pygame.Surface((sword_length, sword_width), pygame.SRCALPHA)
    pygame.draw.rect(sword_surf, (100, 50, 0), (0, 0, 10, sword_width)) 
    pygame.draw.rect(sword_surf, (200, 200, 200), (10, 0, sword_length - 10, sword_width)) 
    enemies_hit_this_swing = []

    monday_manager = Monday(screen, player, gui, game_data)
    tuesday_manager = Tuesday(screen, player, gui, game_data)

    current_day_manager = monday_manager
    player.day = "Monday"

    game_data["night_mode"] = False
    game_data["night_finished"] = False
    game_data["gameday"] = 1 

    current_day_manager.start(setup_map)


    # --- HERNÁ SLUČKA ---
    running = True
    game_over = False

    while running:
        is_busy = gui.shop_open or dialogue_active or game_data.get("dialogue_active", False)

        is_night = game_data.get("night_mode", False)
        handle_music(is_night)
        selected_item = gui.get_selected_item()

        if game_data["night_mode"]:
            game_data["night_timer"] -= 1
            if game_data["night_timer"] <= 0:
                game_data["night_mode"] = False
                game_data["night_finished"] = True
                current_day_manager.day_finished = True

        current_day_manager.update_quests()

        if current_day_manager.day_finished:
            if player.day == "Monday" and game_data.get("night_finished"):
                player.day = "Tuesday"
                current_day_manager = tuesday_manager
                current_day_manager.start(setup_map)
                game_data["night_mode"] = False
                game_data["night_finished"] = False
        
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
                
                # 1. ESCAPE: Zatváranie obchodu alebo otvorenie hlavného menu
                if event.key == pygame.K_ESCAPE:
                    if gui.shop_open:
                        gui.shop_open = False
                    else:
                        menu = EscMenu(screen)
                        vysledok = menu.run()
                        if vysledok == "quit": return

                # 2. KLÁVESA E: Interakcia (NPC, Obchod, Dialóg)
                elif event.key == pygame.K_e:
                    if gui.shop_open:
                        # Logika nákupu v obchode
                        item = gui.shop_items[gui.shop_selected_index]
                        
                        if player.money >= item["price"]:
                            if item["type"] == "consumable":
                                # Okamžitý efekt (napr. potion)
                                player.money -= item["price"]
                                player.health = min(100, player.health + 20)
                                print(f"Použité: {item['name']}")
                            else:
                                # Trvalé predmety (meče, lopaty) idú do inventára
                                if item["name"] not in gui.inventory:
                                    if len(gui.inventory) < gui.max_slots:
                                        player.money -= item["price"]
                                        gui.inventory.append(item["name"])
                                        print(f"Kúpené: {item['name']}")
                                    else:
                                        print("Inventár je plný!")
                                else:
                                    print("Tento predmet už máš!")
                        else:
                            print("Nedostatok peňazí!")
                    
                    else:
                        # Ak nie je otvorený obchod, skúsime interakciu s NPC
                        npc = game_data.get("npc")
                        if npc and player.rect.colliderect(npc.rect.inflate(60, 60)):
                            # Ak je to Shopkeeper, otvoríme GUI obchodu
                            if getattr(npc, 'name', '') == "Shopkeeper":
                                gui.shop_open = True
                            else:
                                # Inak spustíme klasický dialóg
                                dialogue_active = True
                                dialogue_index = 0
                                game_data["dialogue_active"] = True

                # 3. POHYB V OBCHODE (W/S alebo šípky)
                elif gui.shop_open:
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        gui.shop_selected_index = (gui.shop_selected_index - 1) % len(gui.shop_items)
                    elif event.key in [pygame.K_s, pygame.K_DOWN]:
                        gui.shop_selected_index = (gui.shop_selected_index + 1) % len(gui.shop_items)

                # 4. VÝBER SLOTU (1-9): Delegujeme na GUI
                # Táto funkcia v gui.py zmení selected_index (bezpečne)
                gui.handle_input(event)


            if event.type == pygame.MOUSEBUTTONDOWN: 
                if dialogue_active and event.button == 1:
                    dialogue_index += 1
                    npc = game_data.get("npc")
                    if dialogue_index >= len(npc.dialogue_lines):
                        dialogue_active = False
                        game_data["dialogue_active"] = False
                    continue

                if event.button == 1 and not game_over: 
                    if selected_item == "Sword":
                        attack_active = True
                        attack_start_time = pygame.time.get_ticks()
                        enemies_hit_this_swing = []

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
                            if attack_rect.colliderect(enemy.rect):
                                knockback_vec = pygame.math.Vector2(enemy.rect.center) - pygame.math.Vector2(player.rect.center)
                                if knockback_vec.length() > 0:
                                    knockback_vec = knockback_vec.normalize() * 15
                                else:
                                    knockback_vec = pygame.math.Vector2(0, 0)
                                
                                enemy.take_damage(15, knockback_vec)

                    if selected_item == "Shovel" and not game_data["night_mode"]:
                        current_time = pygame.time.get_ticks()
                        
                        if current_time - game_data["last_dig_time"] < game_data["dig_cooldown"]:
                            print("Ešte si unavený...")
                        elif game_data["current_map"] == "cmitermap":
                            chosen_minigame = random.choice([GraveDigMinigame, TimingDigMinigame, SequenceDigMinigame])
                            minigame = chosen_minigame(screen)
                            reward = minigame.run() 

                            pygame.event.clear() 
                            game_data["last_dig_time"] = pygame.time.get_ticks()

                            if reward > 0:
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
                                print("Minihra zatvorená - neúspech.")
                        else:
                            print("Tu sa kopať nedá.")

                # PRAVÉ TLAČIDLO (Otváranie hrobov + Spawn nepriateľov)
                elif (event.button == 3 and not game_over) and game_data["current_map"] == "cmitermap": 
                    if not game_data["night_mode"]:
                        game_data["night_mode"] = True
                        game_data["night_timer"] = 60 * 60
                        game_data["night_text_timer"] = 180
                        for pit in game_data["grave_pits"]: 
                            pit['state'] = 'opened' 
                        
                        GhostEnemy.spawn_horde(player, game_data, ghost_img, count=5)


            gui.handle_input(event)

        # --- UPDATE NEPRIATEĽOV ---
        for enemy in game_data["enemies"]:
            enemy.update(player, game_data) 
            
            # Útok ducha na hráča
            if player.rect.colliderect(enemy.rect) and enemy.state == "CHASING":
                current_time = pygame.time.get_ticks()
                if not hasattr(player, 'last_damage_time'): player.last_damage_time = 0
                
                if current_time - player.last_damage_time >= 1000 and not game_over:
                    player.health -= enemy.damage
                    player.last_damage_time = current_time
                    print("HP:", player.health)
                    if player.health <= 0:
                        game_over = True

        
        # Zmaž zo zoznamu len tých duchov, ktorí dokončili svoju "DYING" animáciu
        game_data["enemies"] = [e for e in game_data["enemies"] if not e.is_dead]

       # --- UPDATE ŠÍPOV ---
        for arrow in game_data.get("arrows", [])[:]:
            arrow.update()
            
            # Ak trafí hráča
            if arrow.rect.colliderect(player.rect):
                current_time = pygame.time.get_ticks()
                if not hasattr(player, 'last_damage_time'): player.last_damage_time = 0
                if current_time - player.last_damage_time >= 500:
                    player.health -= arrow.damage
                    player.last_damage_time = current_time
                    if player.health <= 0: game_over = True
                game_data["arrows"].remove(arrow)
            
            # Ak vyprší čas a netrafí
            elif arrow.lifetime <= 0:
                game_data["arrows"].remove(arrow)

        if (not dialogue_active and not game_over) and not is_busy:
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
                wheat_wall_img, wheat_wall_top_img, water_gif, path_img, floor_tiles_img
            )

        if game_data["visible_mapchangers"]:
            for zone in game_data["change_map_squares"]:
                debug_surf = pygame.Surface((zone["rect"].width, zone["rect"].height), pygame.SRCALPHA)
                debug_surf.fill((255, 255, 0, 120))
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
            render_queue.append({"type": "enemy", "obj": enemy, "y": enemy.rect.bottom})
    
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
                item["obj"].draw(screen, camera)

            for arrow in game_data.get("arrows", []):
                arrow.draw(screen, camera)


        # --- NPC INTERACT TEXT ---
        npc = game_data.get("npc")
        if npc and player.rect.colliderect(npc.rect.inflate(80, 80)) and not dialogue_active:
            interact_font = pygame.font.Font("Resources/Fonts/upheavtt.ttf", 24)
            interact_text = interact_font.render("Press E", True, (255, 255, 0))
            text_rect = interact_text.get_rect(center=(npc.rect.centerx, npc.rect.top - 20))
            screen.blit(interact_text, camera.apply(text_rect))

        if dialogue_active:
            npc = game_data.get("npc")
            if npc:
                screen.blit(player_dialog_img, (50, screen_height - 450))
                screen.blit(npc.portrait, (screen_width - 250, screen_height - 450))
                
                dialogue_box = pygame.Rect(0, screen_height - 200, screen_width, 200)
                pygame.draw.rect(screen, (0, 0, 0, 200), dialogue_box)
                pygame.draw.rect(screen, (255, 255, 255), dialogue_box, 2)
                
                text = npc.dialogue_lines[dialogue_index]
                rendered_text = font.render(text, True, (255, 255, 255))
                screen.blit(rendered_text, (50, screen_height - 120))

        if game_over:
            grey_overlay = pygame.Surface((screen_width, screen_height))
            grey_overlay.set_alpha(180)
            grey_overlay.fill((0, 0, 0))
            screen.blit(grey_overlay, (0, 0))

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
                base_angle = direction_angles.get(getattr(player, 'direction', 'down'), 0)

                swing_range = 120 
                current_swing_angle = base_angle - (progress * swing_range - 60)

                rotated_image = pygame.transform.rotate(sword_surf, -current_swing_angle)
                
                pivot_offset_vec = pygame.math.Vector2(sword_length / 2, 0)
                rotated_pivot_offset = pivot_offset_vec.rotate(current_swing_angle)
                
                new_rect_center = pygame.math.Vector2(player.rect.center) + rotated_pivot_offset
                sword_rect = rotated_image.get_rect(center=new_rect_center)

                screen.blit(rotated_image, camera.apply(sword_rect))

                for enemy in game_data["enemies"]:
                    if sword_rect.colliderect(enemy.rect):
                        if enemy not in enemies_hit_this_swing:
                            knockback_vec = pygame.math.Vector2(enemy.rect.center) - pygame.math.Vector2(player.rect.center)
                            if knockback_vec.length() > 0:
                                knockback_vec = knockback_vec.normalize() * 20
                            else:
                                knockback_vec = pygame.math.Vector2(0, 0)
                                
                            enemy.take_damage(15, knockback_vec)
                            enemies_hit_this_swing.append(enemy)
        
        # NIGHT MODE
        if game_data["night_mode"] and not game_over:
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 230))
            
            player_screen_pos = camera.apply(player.rect).center
            pygame.draw.circle(overlay, (0, 0, 0, 0), player_screen_pos, 180)
            screen.blit(overlay, (0, 0))

            game_data["night_timer"] -= 1

            # --- NIGHT MODE SPAWN KAŽDÉ 2 SEKUNDY ---
            if game_data["night_timer"] % 120 == 0:
                dist_x = random.randint(400, 800) * random.choice([-1, 1])
                dist_y = random.randint(400, 800) * random.choice([-1, 1])
                
                spawn_x = player.rect.x + dist_x
                spawn_y = player.rect.y + dist_y

                # Vyberieme náhodný typ - Ghost padá častejšie
                enemy_type = random.choice(["ghost", "ghost", "archer", "ghoul"])
                
                if enemy_type == "ghost":
                    game_data["enemies"].append(GhostEnemy(spawn_x, spawn_y, ghost_img))
                elif enemy_type == "archer":
                    game_data["enemies"].append(SkeletonArcher(spawn_x, spawn_y, ghost_img)) # Neskôr nahraď archer obrázkom
                elif enemy_type == "ghoul":
                    game_data["enemies"].append(GhoulTank(spawn_x, spawn_y, ghost_img)) # Neskôr nahraď ghoul obrázkom

            if game_data["night_text_timer"] > 0:
                night_font = pygame.font.Font("Resources/Fonts/upheavtt.ttf", 70)
                night_text = night_font.render("THE NIGHT HAS COME", True, (255, 255, 255))
                screen.blit(night_text, night_text.get_rect(center=(screen_width // 2, 100)))
                game_data["night_text_timer"] -= 1

            timer_font = pygame.font.Font("Resources/Fonts/upheavtt.ttf", 40)
            seconds_left = max(0, game_data["night_timer"] // 60)
            timer_text = timer_font.render(f"The night will end in: {seconds_left}s", True, (255, 255, 255))
            screen.blit(timer_text, (screen_width // 2 -250, screen_height // 2 +200))

            if game_data["night_timer"] <= 0:
                game_data["night_mode"] = False
                game_data["enemies"].clear()
                for pit in game_data["grave_pits"]: 
                    pit['state'] = 'closed'

        gui.draw()
        fade.draw()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    spustit_hru(screen)