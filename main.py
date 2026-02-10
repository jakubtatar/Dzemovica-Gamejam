import pygame
import sys
import os
import math
import random

# --- IMPORTY TVOJICH SÚBOROV ---
# (Tieto súbory musia byť v rovnakom priečinku ako main.py)
from camera import Camera
from gui import GUI
from fade import Fade
from grave import Grave
from dialogue import Dialogue
from mapsmanager import MapsManager
from item import Item

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
# ČASŤ 1: TRIEDY PRE MENU
# ==========================================

class Particle:
    """Efekt lietajúcich častíc v menu"""
    def __init__(self, w, h):
        self.x = random.randint(0, w)
        self.y = random.randint(0, h)
        self.size = random.randint(2, 5)
        self.speed_y = random.uniform(-0.5, -0.1)
        self.alpha = random.randint(50, 150)
        self.w, self.h = w, h

    def update(self):
        self.y += self.speed_y
        self.alpha -= 0.2
        if self.y < 0 or self.alpha <= 0:
            self.y = self.h
            self.x = random.randint(0, self.w)
            self.alpha = random.randint(50, 150)

    def draw(self, screen):
        s = pygame.Surface((self.size, self.size))
        s.set_alpha(self.alpha)
        s.fill((100, 100, 120))
        screen.blit(s, (self.x, self.y))

class Button:
    """Animované tlačidlo"""
    def __init__(self, text, y, font, action_id):
        self.text = text
        self.base_y = y
        self.font = font
        self.action_id = action_id
        self.scale = 1.0
        self.target_scale = 1.0
        self.color = (200, 200, 200)
        self.rect = None

    def update(self, mx, my, click):
        if self.rect and self.rect.collidepoint((mx, my)):
            self.target_scale = 1.2
            self.color = (255, 50, 50)
            if click:
                return self.action_id
        else:
            self.target_scale = 1.0
            self.color = (200, 200, 200)

        self.scale += (self.target_scale - self.scale) * 0.2
        return None

<<<<<<< HEAD
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
game_paused = False
pause_start_time = 0
total_paused_time = 0
pause_view = "menu"
mouse_click = False

while is_running:
    selected_item = gui.get_selected_item()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                game_paused = not game_paused
                print("Pauza:", game_paused)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = True

        if game_paused and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Ľavý klik
                for rect, action in gui.pause_buttons:
                    if rect.collidepoint(event.pos):
                        if action == "RESUME":
                            game_paused = False
                        elif action == "QUIT":
                            is_running = False

        if not game_paused:
         if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click (kopanie)
                if selected_item == "Shovel":
                    gx = (player.rect.centerx // TILE_SIZE) * TILE_SIZE
                    gy = (player.rect.bottom // TILE_SIZE) * TILE_SIZE
                    graves.append(Grave(gx, gy, TILE_SIZE, gravestone_images))
                    grave_pits.append({'rect': pygame.Rect(gx, gy + 50, TILE_SIZE, TILE_SIZE * 2), 'state': 'closed'})
                    print(f"Hrob vytvorený na {gx}, {gy}")
            
            elif event.button == 3: # Right click (otvaranie)
                for pit in grave_pits:
                    pit['state'] = 'opened'
                print("Vsetky jamy otvorene!")


        gui.handle_input(event, game_paused)

      
    # Update player and camera
    if not game_paused:
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
        elif tile_type == "p":
            screen.blit(floor_planks_img, camera.apply(rect))
        elif tile_type == "s":
            screen.blit(wall_img, camera.apply(rect))
        elif tile_type == "f":
            screen.blit(wall_front_img, camera.apply(rect))
        elif tile_type == "w":
            screen.blit(wall_top_img, camera.apply(rect))
        elif tile_type == "a":
            screen.blit(wall_left_img, camera.apply(rect))
        elif tile_type == "d":
            screen.blit(wall_right_img, camera.apply(rect))
        elif tile_type == "e":
            screen.blit(wall_RT_img, camera.apply(rect))
        elif tile_type == "q":
            screen.blit(wall_LT_img, camera.apply(rect))
        elif tile_type == "c":
            screen.blit(wall_RD_img, camera.apply(rect))
        elif tile_type == "z":
            screen.blit(wall_LD_img, camera.apply(rect))
        elif tile_type == "n":
            screen.blit(wheat_wall_img, camera.apply(rect))
        elif tile_type == "m":
            screen.blit(wheat_wall_top_img, camera.apply(rect))

    # Draw closed grave pits (Vykreslujeme prve, aby boli pod hrobmi)
    for pit in grave_pits:
        image_to_draw = grave_closed_img if pit['state'] == 'closed' else grave_opened_img
        screen.blit(image_to_draw, camera.apply(pit['rect']))

     # Draw graves
    for grave in graves:
        grave.draw(screen, camera)

   
=======
    def draw(self, screen, width):
        surf = self.font.render(self.text, True, self.color)
        new_w = int(surf.get_width() * self.scale)
        new_h = int(surf.get_height() * self.scale)
        scaled_surf = pygame.transform.smoothscale(surf, (new_w, new_h))
>>>>>>> main
        
        shadow_surf = self.font.render(self.text, True, (0, 0, 0))
        scaled_shadow = pygame.transform.smoothscale(shadow_surf, (new_w, new_h))

        rect = scaled_surf.get_rect(center=(width // 2, self.base_y))
        self.rect = rect 

        screen.blit(scaled_shadow, (rect.x + 3, rect.y + 3))
        screen.blit(scaled_surf, rect)

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()
        
        path = os.path.join("Resources", "Fonts", "upheavtt.ttf")
        try:
            self.title_font = pygame.font.Font(path, 70)
            self.font = pygame.font.Font(path, 40)
            self.small_font = pygame.font.Font(path, 25)
        except:
            self.title_font = pygame.font.SysFont("Arial", 70, bold=True)
            self.font = pygame.font.SysFont("Arial", 40)
            self.small_font = pygame.font.SysFont("Arial", 25)

        self.particles = [Particle(self.width, self.height) for _ in range(50)]
        self.menu_buttons = [
            Button("PLAY", 300, self.font, "play"),
            Button("SETTINGS", 380, self.font, "settings"),
            Button("CREDITS", 460, self.font, "credits"),
            Button("QUIT", 540, self.font, "quit")
        ]
        self.volume = 0.5
        self.dragging_slider = False

    def draw_background(self):
        self.screen.fill((15, 10, 20))
        for p in self.particles:
            p.update()
            p.draw(self.screen)

    def draw_slider(self, text, y, value):
        label = self.font.render(f"{text}: {int(value * 100)}%", True, (255, 255, 255))
        self.screen.blit(label, (self.width//2 - 200, y))
        line_rect = pygame.Rect(self.width//2 - 200, y + 40, 400, 4)
        pygame.draw.rect(self.screen, (100, 100, 100), line_rect)
        handle_x = line_rect.x + (line_rect.width * value)
        handle_rect = pygame.Rect(handle_x - 10, y + 30, 20, 24)
        pygame.draw.rect(self.screen, (255, 215, 0), handle_rect)
        return handle_rect, line_rect

    def run(self):
        view = "menu"
        while True:
            mx, my = pygame.mouse.get_pos()
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: click = True
                if event.type == pygame.MOUSEBUTTONUP: self.dragging_slider = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if view != "menu": view = "menu"

            self.draw_background()

            if view == "menu":
                offset_y = math.sin(pygame.time.get_ticks() * 0.003) * 10
                t_surf = self.title_font.render("KTO DRUHEMU JAMU KOPE...", True, (255, 215, 0))
                t_rect = t_surf.get_rect(center=(self.width // 2, 120 + offset_y))
                self.screen.blit(t_surf, t_rect)

                for btn in self.menu_buttons:
                    action = btn.update(mx, my, click)
                    btn.draw(self.screen, self.width)
                    if action:
                        if action == "play": return "play"
                        elif action == "settings": view = "settings"
                        elif action == "credits": view = "credits"
                        elif action == "quit": pygame.quit(); sys.exit()

            elif view == "settings":
                handle, line = self.draw_slider("Volume", 300, self.volume)
                if pygame.mouse.get_pressed()[0]:
                    if handle.collidepoint((mx, my)) or self.dragging_slider:
                        self.dragging_slider = True
                        self.volume = max(0.0, min(1.0, (mx - line.x) / line.width))
                
                back_btn = Button("BACK", 600, self.font, "back")
                if back_btn.update(mx, my, click): view = "menu"
                back_btn.draw(self.screen, self.width)

            elif view == "credits":
                c_lines = [("CODE", "Ty"), ("ART", "Ty & Assets")]
                for i, (r, n) in enumerate(c_lines):
                    self.screen.blit(self.small_font.render(r, True, (150,150,150)), (self.width//2-50, 200+i*60))
                    self.screen.blit(self.font.render(n, True, (255,255,255)), (self.width//2-50, 230+i*60))
                
                back_btn = Button("BACK", 600, self.font, "back")
                if back_btn.update(mx, my, click): view = "menu"
                back_btn.draw(self.screen, self.width)

            pygame.display.flip()
            self.clock.tick(60)


# ==========================================
# ČASŤ 2: LOGIKA HRY (Tvoja hra zabalená vo funkcii)
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

<<<<<<< HEAD
    gui.draw()

    # Draw pause menu if game is paused

  

# 2. V časti, kde kreslíš pauzu (okolo riadku 280)
    if game_paused:
        # Voláme GUI a ukladáme vrátenú hodnotu
        result = gui.draw_pause_menu(screen, pause_view, mouse_click)

        if mouse_click:
            mouse_click = False
        
        if result == "resume":
            game_paused = False
            pause_view = "menu"
        elif result == "quit":
            is_running = False
        elif result is not None:
            # Ak result je napr. "settings", pause_view sa prepne a menu sa zmení
            pause_view = result
    pygame.display.flip()
    clock.tick(60)



# Quit Pygame
pygame.quit()
=======
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
    # Používame slovník 'game_data', aby sme mohli meniť premenné vo vnútornej funkcii
    game_data = {
        "walls": [],
        "collidable_walls": [],
        "map_objects": [],
        "change_map_squares": [],
        "current_map": "",
        "graves": [],
        "grave_pits": [],
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
                    "collidable": True
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
        
        # Cooldown na zmenu mapy
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

        # Eventy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return # Vráti sa do Menu!

            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: 
                    if selected_item == "[2] Shovel" and game_data["current_map"] == "cmitermap": 
                        gx = (player.rect.centerx // TILE_SIZE) * TILE_SIZE 
                        gy = (player.rect.bottom // TILE_SIZE) * TILE_SIZE 
                        game_data["graves"].append(Grave(gx, gy, TILE_SIZE, gravestone_images)) 
                        game_data["grave_pits"].append({ 'rect': pygame.Rect(gx, gy + 50, TILE_SIZE, TILE_SIZE * 2), 'state': 'closed' }) 
                elif event.button == 3: 
                    for pit in game_data["grave_pits"]: pit['state'] = 'opened' 

            gui.handle_input(event)

        # Update
        player.handle_keys_with_collision(4000, 4000, game_data["collidable_walls"])
        camera.update(player)
        fade.update()

        # Draw
        screen.fill((8, 50, 20))

        # Map tiles
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

        # Zones (debug red squares)
        # for zone in game_data["change_map_squares"]:
        #    pygame.draw.rect(screen, (255, 0, 0), camera.apply(zone["rect"]))

        # Jamy
        for pit in game_data["grave_pits"]:
            image_to_draw = grave_closed_img if pit['state'] == 'closed' else grave_opened_img
            screen.blit(image_to_draw, camera.apply(pit['rect']))

        # Hroby
        for grave in game_data["graves"]:
            grave.draw(screen, camera)

        # Objekty
        for obj in game_data["map_objects"]:
            screen.blit(
                obj["image"],
                camera.apply(obj["rect"]).move(
                    0, obj["rect"].height - obj["image"].get_height()
                )
            )

        # Hráč
        try: player.draw(screen, camera)
        except: pygame.draw.rect(screen, player.color, camera.apply(player.rect))

        gui.draw_inventory()
        # gui.draw() # Ak máš metódu draw v GUI, použi ju
        fade.draw()
        
        pygame.display.flip()
        clock.tick(60)


# ==========================================
# ČASŤ 3: HLAVNÝ START
# ==========================================

if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kto druhému jamu kope...")
    
    # 1. Spustíme Menu
    menu = MainMenu(screen)
    
    while True:
        # Čakáme na výber v menu
        action = menu.run()
        
        if action == "play":
            # 2. Ak vybral PLAY, spustíme hru
            spustit_hru(screen)
            # Keď hra skončí (ESC), cyklus pokračuje a znova zobrazí menu
            
        elif action == "quit":
            pygame.quit()
            sys.exit()
>>>>>>> main
