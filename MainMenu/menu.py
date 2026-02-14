import pygame
import sys
import os
import math
import random

# --- 1. CESTY A IMPORTY ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Cesta k fontu
FONT_PATH = os.path.join(parent_dir, "Resources", "Fonts", "upheavtt.ttf")
# Cesta k logu
LOGO_PATH = os.path.join(parent_dir, "Resources", "Logo_Big.png")

try:
    import main 
except ImportError:
    pass

# --- 2. INICIALIZÁCIA ---
pygame.init()
pygame.mixer.init()

# LOGICKÉ ROZLÍŠENIE (Hra beží interne v tomto rozlíšení)
WIDTH, HEIGHT = 1280, 720

# Stav zobrazenia
is_fullscreen = True

def set_display_mode(fullscreen):
    """Prepína medzi Fullscreen a Windowed režimom"""
    if fullscreen:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode((WIDTH, HEIGHT))

# Inicializácia obrazovky (defaultne Fullscreen)
real_screen = set_display_mode(is_fullscreen)
pygame.display.set_caption("Kto druhému jamu kope...")

# Virtuálny povrch (Canvas), na ktorý kreslíme hru
canvas = pygame.Surface((WIDTH, HEIGHT))

# --- 3. FARBY ---
COL_SKY_TOP = (10, 10, 25)
COL_SKY_BOT = (40, 30, 60)
COL_MOON = (255, 255, 220)
COL_HILL_FAR = (20, 15, 30)
COL_HILL_MID = (10, 5, 15)
COL_GROUND = (5, 5, 5)
ACCENT = (255, 190, 50)
TEXT_COL = (220, 220, 220)

# --- 4. TRIEDY ---

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, int(HEIGHT * 0.6))
        self.size = random.choice([1, 1, 2])
        self.base_alpha = random.randint(100, 255)
        self.twinkle_speed = random.uniform(0.05, 0.15)
        self.offset = random.random() * 100
    
    def update(self, time):
        self.alpha = self.base_alpha + math.sin(time * 0.005 * self.twinkle_speed + self.offset) * 50
        self.alpha = max(0, min(255, self.alpha))

    def draw(self, surface):
        col = (self.alpha, self.alpha, self.alpha)
        pygame.draw.circle(surface, col, (self.x, self.y), self.size)

class Bat:
    def __init__(self):
        self.reset()
        self.x = random.randint(0, WIDTH)

    def reset(self):
        self.x = -50
        self.y = random.randint(50, 300)
        self.speed = random.uniform(2, 4)
        self.wing_speed = random.uniform(0.2, 0.5)
        self.size = random.randint(3, 6)

    def update(self):
        self.x += self.speed
        self.y += math.sin(self.x * 0.02) * 1.5 
        if self.x > WIDTH + 50:
            self.reset()

    def draw(self, screen):
        flap = math.sin(pygame.time.get_ticks() * 0.02 * self.wing_speed) * 5
        center = (self.x, self.y)
        left_wing = (self.x - self.size * 2, self.y - self.size + flap)
        right_wing = (self.x + self.size * 2, self.y - self.size + flap)
        pygame.draw.lines(screen, (10, 5, 10), False, [left_wing, center, right_wing], 2)

class SpookyTree:
    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.surface = pygame.Surface((400, 500), pygame.SRCALPHA)
        self._draw_branch(self.surface, 200, 500, -90, 100 * scale, 10 * scale)

    def _draw_branch(self, surf, x, y, angle, length, width):
        if length < 5: return
        x2 = x + math.cos(math.radians(angle)) * length
        y2 = y + math.sin(math.radians(angle)) * length
        pygame.draw.line(surf, COL_GROUND, (x, y), (x2, y2), int(width))
        new_len = length * 0.75
        new_width = width * 0.7
        if new_len > 10:
            self._draw_branch(surf, x2, y2, angle - random.randint(15, 35), new_len, new_width)
            self._draw_branch(surf, x2, y2, angle + random.randint(15, 35), new_len, new_width)

    def draw(self, screen):
        screen.blit(self.surface, (self.x - 200, self.y - 500))

class Grave:
    def __init__(self, x, y, type_id):
        self.x = x
        self.y = y
        self.type = type_id 
        self.tilt = random.randint(-5, 5)

    def draw(self, screen):
        surf = pygame.Surface((60, 80), pygame.SRCALPHA)
        c = COL_GROUND
        if self.type == 0:
            pygame.draw.rect(surf, c, (25, 10, 10, 70))
            pygame.draw.rect(surf, c, (10, 25, 40, 10))
        elif self.type == 1:
            pygame.draw.rect(surf, c, (10, 20, 40, 60), border_top_left_radius=20, border_top_right_radius=20)
        elif self.type == 2:
            pygame.draw.polygon(surf, c, [(10, 80), (10, 30), (30, 40), (50, 20), (50, 80)])
        rot_surf = pygame.transform.rotate(surf, self.tilt)
        rect = rot_surf.get_rect(midbottom=(self.x, self.y))
        screen.blit(rot_surf, rect)

class Button:
    def __init__(self, text, y, font, action_id):
        self.text = text; self.base_y = y; self.font = font; self.action_id = action_id
        self.scale = 1.0; self.target_scale = 1.0; self.color = TEXT_COL
        self.rect = None; self.hovered = False

    def update(self, mx, my, click, sound_hover):
        triggered = None
        if self.rect and self.rect.collidepoint((mx, my)):
            self.target_scale = 1.2
            self.color = (255, 60, 60)
            if not self.hovered and sound_hover: sound_hover.play()
            self.hovered = True
            if click: triggered = self.action_id
        else:
            self.target_scale = 1.0; self.color = TEXT_COL; self.hovered = False
        self.scale += (self.target_scale - self.scale) * 0.2
        return triggered

    def draw(self, screen):
        shadow = self.font.render(self.text, True, (0,0,0))
        w, h = int(shadow.get_width() * self.scale), int(shadow.get_height() * self.scale)
        shadow_sc = pygame.transform.smoothscale(shadow, (w, h))
        
        surf = self.font.render(self.text, True, self.color)
        surf_sc = pygame.transform.smoothscale(surf, (w, h))
        
        rect = surf_sc.get_rect(center=(WIDTH//2, self.base_y))
        self.rect = rect
        
        screen.blit(shadow_sc, (rect.x+3, rect.y+3))
        screen.blit(surf_sc, rect)

class Slider:
    def __init__(self, x, y, w, h, initial_val=0.5):
        self.rect = pygame.Rect(x, y, w, h)
        self.val = initial_val; self.dragging = False

    def update(self, mx, my, mouse_down):
        if mouse_down:
            if self.rect.collidepoint((mx, my)) or self.dragging:
                self.dragging = True
                self.val = max(0.0, min(1.0, (mx - self.rect.x) / self.rect.width))
        else: self.dragging = False
        return self.val

    def draw(self, screen):
        pygame.draw.rect(screen, (30, 30, 30), self.rect, border_radius=4)
        fill_w = self.rect.width * self.val
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_w, self.rect.height)
        pygame.draw.rect(screen, ACCENT, fill_rect, border_radius=4)
        hx = self.rect.x + (self.rect.width * self.val)
        pygame.draw.circle(screen, (255, 255, 255), (int(hx), self.rect.centery), 8)

# --- 5. POMOCNÉ FUNKCIE ---

def draw_gradient_sky(surface):
    surf = pygame.Surface((1, HEIGHT))
    for y in range(HEIGHT):
        r = COL_SKY_TOP[0] + (COL_SKY_BOT[0] - COL_SKY_TOP[0]) * y / HEIGHT
        g = COL_SKY_TOP[1] + (COL_SKY_BOT[1] - COL_SKY_TOP[1]) * y / HEIGHT
        b = COL_SKY_TOP[2] + (COL_SKY_BOT[2] - COL_SKY_TOP[2]) * y / HEIGHT
        surf.set_at((0, y), (int(r), int(g), int(b)))
    scaled = pygame.transform.scale(surf, (WIDTH, HEIGHT))
    surface.blit(scaled, (0, 0))

def draw_moon(surface):
    glow = pygame.Surface((300, 300), pygame.SRCALPHA)
    pygame.draw.circle(glow, (200, 200, 255, 10), (150, 150), 140)
    pygame.draw.circle(glow, (200, 200, 255, 20), (150, 150), 100)
    surface.blit(glow, (WIDTH - 250, 50))
    pygame.draw.circle(surface, COL_MOON, (WIDTH - 100, 200), 50)

def draw_hills(surface):
    points_far = [(0, HEIGHT), (0, HEIGHT-150), (WIDTH*0.3, HEIGHT-220), 
                  (WIDTH*0.6, HEIGHT-180), (WIDTH, HEIGHT-250), (WIDTH, HEIGHT)]
    pygame.draw.polygon(surface, COL_HILL_FAR, points_far)
    points_mid = [(0, HEIGHT), (0, HEIGHT-80), (WIDTH*0.2, HEIGHT-120), 
                  (WIDTH*0.5, HEIGHT-90), (WIDTH*0.8, HEIGHT-140), (WIDTH, HEIGHT-60), (WIDTH, HEIGHT)]
    pygame.draw.polygon(surface, COL_HILL_MID, points_mid)

# --- 6. HLAVNÝ LOOP ---

def run_menu():
    global real_screen, is_fullscreen
    clock = pygame.time.Clock()
    
    # Objekty scény
    stars = [Star() for _ in range(80)]
    bats = [Bat() for _ in range(5)]
    graves = []
    
    for i in range(15):
        gx = random.randint(50, WIDTH - 50)
        if WIDTH//2 - 200 < gx < WIDTH//2 + 200: continue
        gy = random.randint(HEIGHT - 80, HEIGHT - 20)
        graves.append(Grave(gx, gy, random.choice([0, 0, 1, 1, 2])))
    graves.sort(key=lambda g: g.y)

    tree_left = SpookyTree(150, HEIGHT, scale=1.2)
    tree_right = SpookyTree(WIDTH - 100, HEIGHT - 20, scale=0.8)

    # Fonty
    try:
        font_title = pygame.font.Font(FONT_PATH, 75)
        font_menu = pygame.font.Font(FONT_PATH, 30)
        font_small = pygame.font.Font(FONT_PATH, 20)
    except Exception as e:
        print(f"Font nenájdený: {FONT_PATH}")
        font_title = pygame.font.SysFont("Georgia", 75, bold=True)
        font_menu = pygame.font.SysFont("Arial", 30)
        font_small = pygame.font.SysFont("Arial", 20)

    # Logo
    logo_surf = None
    if os.path.exists(LOGO_PATH):
        try:
            logo_surf = pygame.image.load(LOGO_PATH).convert_alpha()
        except: pass

    # Zvuky
    s_hover_path = os.path.join(parent_dir, "Resources", "Audio", "hover.wav")
    s_click_path = os.path.join(parent_dir, "Resources", "Audio", "click.wav")
    s_hover = pygame.mixer.Sound(s_hover_path) if os.path.exists(s_hover_path) else None
    s_click = pygame.mixer.Sound(s_click_path) if os.path.exists(s_click_path) else None
    if s_hover: s_hover.set_volume(0.3)

    # UI Elementy
    btns_main = [
        Button("PLAY", 320, font_menu, "play"),
        Button("SETTINGS", 400, font_menu, "settings"),
        Button("CREDITS", 480, font_menu, "credits"),
        Button("QUIT", 560, font_menu, "quit")
    ]
    
    # Settings elementy
    btn_screen_mode = Button("MODE: FULLSCREEN", 360, font_menu, "toggle_screen")
    btn_back = Button("BACK", 600, font_menu, "back")
    slider = Slider(WIDTH//2 - 150, 260, 300, 20, 0.5)
    
    view = "menu"

    # --- NAČÍTANIE A SPUSTENIE HUDBY ---
    menu_music_path = os.path.join(parent_dir, "Resources", "Music", "Night.mp3")
    try:
        if os.path.exists(menu_music_path):
            pygame.mixer.music.load(menu_music_path)
            pygame.mixer.music.set_volume(0.5) # Podľa začiatočnej hodnoty slidera
            pygame.mixer.music.play(-1)
        else:
            print(f"Hudba nenájdená: {menu_music_path}")
    except Exception as e:
        print(f"Chyba pri načítaní hudby: {e}")

    while True:
        time = pygame.time.get_ticks()
        
        # 1. Získanie aktuálnej veľkosti okna (či už fullscreen alebo okno)
        real_w, real_h = real_screen.get_size()
        
        # 2. Výpočet scale faktora pre Letterboxing
        scale_w = real_w / WIDTH
        scale_h = real_h / HEIGHT
        scale = min(scale_w, scale_h)
        
        new_w = int(WIDTH * scale)
        new_h = int(HEIGHT * scale)
        offset_x = (real_w - new_w) // 2
        offset_y = (real_h - new_h) // 2

        # 3. Prepočet myši
        raw_mx, raw_my = pygame.mouse.get_pos()
        mx = (raw_mx - offset_x) / scale
        my = (raw_my - offset_y) / scale
        m_down = pygame.mouse.get_pressed()[0]
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                if view != "menu": 
                    if s_click: s_click.play()
                    view = "menu"
                else:
                    pygame.quit(); sys.exit()

        # 4. Kreslenie na Canvas
        draw_gradient_sky(canvas)
        for s in stars: s.update(time); s.draw(canvas)
        draw_moon(canvas)
        for b in bats: b.update(); b.draw(canvas)
        draw_hills(canvas)
        tree_right.draw(canvas)
        tree_left.draw(canvas)
        for g in graves: g.draw(canvas)
        pygame.draw.rect(canvas, COL_GROUND, (0, HEIGHT-30, WIDTH, 30))

        # 5. Logika Menu
        if view == "menu":
            offset_y = math.sin(time * 0.002) * 5
            if logo_surf:
                lr = logo_surf.get_rect(center=(WIDTH//2, 150 + offset_y))
                canvas.blit(logo_surf, lr)
            else:
                t_surf = font_title.render("KTO DRUHEMU JAMU KOPE...", True, ACCENT)
                tr = t_surf.get_rect(center=(WIDTH//2, 150 + offset_y))
                canvas.blit(t_surf, tr)

            for btn in btns_main:
                act = btn.update(mx, my, click, s_hover)
                btn.draw(canvas)
                if act:
                    if s_click: s_click.play()
                    if act == "play": 
                        if "main" in sys.modules: main.spustit_hru(real_screen) 
                    elif act == "settings": view = "settings"
                    elif act == "credits": view = "credits"
                    elif act == "quit": pygame.quit(); sys.exit()

        elif view == "settings":
            head = font_title.render("SETTINGS", True, ACCENT)
            canvas.blit(head, head.get_rect(center=(WIDTH//2, 120)))

            # Slider
            vol = slider.update(mx, my, m_down)
            if s_hover: s_hover.set_volume(vol)
            if s_click: s_click.set_volume(vol)
            pygame.mixer.music.set_volume(vol) # <-- Nastavuje hlasitosť hudby
            slider.draw(canvas)
            txt = font_menu.render(f"Volume: {int(vol*100)}%", True, TEXT_COL)
            canvas.blit(txt, txt.get_rect(center=(WIDTH//2, 230)))

            # Tlačidlo pre zmenu režimu obrazovky
            btn_screen_mode.text = "MODE: FULLSCREEN" if is_fullscreen else "MODE: WINDOWED"
            if btn_screen_mode.update(mx, my, click, s_hover) == "toggle_screen":
                if s_click: s_click.play()
                # Prepnutie režimu
                is_fullscreen = not is_fullscreen
                real_screen = set_display_mode(is_fullscreen)
            
            btn_screen_mode.draw(canvas)

            # Späť
            if btn_back.update(mx, my, click, s_hover) == "back":
                if s_click: s_click.play()
                view = "menu"
            btn_back.draw(canvas)


        elif view == "credits":
            head = font_title.render("CREDITS", True, ACCENT)
            canvas.blit(head, head.get_rect(center=(WIDTH//2, 120)))
            
            credits_data = [
                ("CODE BY", "Matúš Beke, Jakub Tatár, Ján Kristián Preisler"),
                ("ART BY", "Jakub Tatár"),
                ("AUDIO BY", "Ján Kristián Preisler"),
                ("SPECIAL THANKS TO", "Vladimír Koššuth")
            ]
            y_pos = 230
            for role, name in credits_data:
                lbl = font_small.render(role, True, (150, 150, 150))
                val = font_menu.render(name, True, (255, 255, 255))
                canvas.blit(lbl, lbl.get_rect(center=(WIDTH//2, y_pos)))
                canvas.blit(val, val.get_rect(center=(WIDTH//2, y_pos + 30)))
                y_pos += 80

            if btn_back.update(mx, my, click, s_hover) == "back":
                if s_click: s_click.play()
                view = "menu"
            btn_back.draw(canvas)

        # 6. Finálne vykreslenie
        real_screen.fill((0, 0, 0))
        scaled_surf = pygame.transform.smoothscale(canvas, (new_w, new_h))
        real_screen.blit(scaled_surf, (offset_x, offset_y))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_menu()