import pygame
import sys
import os
import math
import random

# --- 1. CESTY K SÚBOROM ---
# Získame cestu k priečinku, kde je menu.py
current_dir = os.path.dirname(os.path.abspath(__file__))
# Získame rodičovský priečinok (hlavný priečinok hry)
parent_dir = os.path.dirname(current_dir)
# Pridáme ho do systému ciest, aby sme mohli importovať main.py
sys.path.append(parent_dir)

try:
    import main 
except ImportError as e:
    print(f"CHYBA IMPORTU: {e}")
    print(f"Hľadám main.py v: {parent_dir}")
    sys.exit()

# --- 2. INICIALIZÁCIA ---
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kto druhému jamu kope... - FINAL MENU")

# --- 3. FARBY A KONFIGURÁCIA ---
COL_SKY_TOP = (5, 5, 15)        # Hlboká noc
COL_SKY_BOT = (25, 20, 40)      # Fialový opar
COL_MOON = (255, 255, 230)      # Mesiac
COL_SILHOUETTE = (5, 2, 5)      # Čierna zem
ACCENT = (255, 190, 0)          # Zlatá pre text
TEXT_COL = (220, 220, 220)      # Biela pre text

# Cesta k tvojmu fontu
FONT_PATH = os.path.join(parent_dir, "Resources", "Fonts", "upheavtt.ttf")

# --- 4. TRIEDY PRE VIZUÁL ---

class Star:
    """Trblietajúca sa hviezda"""
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        # OPRAVA CHYBY: Pretypujeme na int()
        limit_y = int(HEIGHT / 1.5)
        self.y = random.randint(0, limit_y)
        self.size = random.choice([1, 1, 2])
        self.brightness = random.randint(100, 255)
        self.twinkle_speed = random.uniform(0.05, 0.2)
        self.offset = random.random() * 100
    
    def update(self):
        # Jemné blikanie
        self.brightness = 150 + math.sin(pygame.time.get_ticks() * 0.01 * self.twinkle_speed + self.offset) * 100
    
    def draw(self, screen):
        val = int(max(0, min(255, self.brightness)))
        col = (val, val, val)
        pygame.draw.circle(screen, col, (self.x, self.y), self.size)

class AdvancedFog:
    """Vylepšená, 'nadýchaná' hmla - UPRAVENÁ"""
    def __init__(self, y_base, speed, opacity):
        self.x = random.randint(-200, WIDTH)
        self.y_base = y_base
        # ZMENA: Výrazne širšia hmla pre "ťahavý" efekt
        self.w = random.randint(800, 1400)
        self.h = random.randint(100, 200)
        self.speed = speed
        self.opacity = opacity
        self.wobble_offset = random.random() * 100
        
        # Vytvoríme "textúru" oblaku z viacerých kruhov
        self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.generate_cloud_shape()

    def generate_cloud_shape(self):
        # ZMENA: Viac "bublín" pre jemnejší vzhľad
        num_blobs = 20
        for _ in range(num_blobs):
            bx = random.randint(0, self.w - 200)
            by = random.randint(10, self.h - 60)
            # ZMENA: Širšie elipsy
            bw = random.randint(200, 400)
            bh = random.randint(40, 90)
            # ZMENA: Jemnejšia farba
            col = (160, 150, 190, max(0, self.opacity - 5)) 
            pygame.draw.ellipse(self.surface, col, (bx, by, bw, bh))

    def update(self):
        self.x += self.speed
        if self.x > WIDTH:
            self.x = -self.w
        
        # ZMENA: Veľmi pomalé vlnenie (0.0003 namiesto 0.001)
        self.y_current = self.y_base + math.sin(pygame.time.get_ticks() * 0.0003 + self.wobble_offset) * 15

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y_current))

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
        
        screen.blit(shadow_sc, (rect.x+4, rect.y+4))
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
        pygame.draw.rect(screen, (40, 40, 50), self.rect, border_radius=5)
        fill = pygame.Rect(self.rect.x, self.rect.y, self.rect.width * self.val, self.rect.height)
        pygame.draw.rect(screen, ACCENT, fill, border_radius=5)
        hx = self.rect.x + (self.rect.width * self.val)
        pygame.draw.circle(screen, (255,255,255), (int(hx), self.rect.centery), 10)

# --- 5. POMOCNÉ FUNKCIE ---

def draw_moon(screen):
    # Vonkajšia žiara
    s = pygame.Surface((400, 400), pygame.SRCALPHA)
    pygame.draw.circle(s, (200, 200, 255, 10), (200, 200), 180)
    pygame.draw.circle(s, (200, 200, 255, 20), (200, 200), 140)
    screen.blit(s, (WIDTH - 250, 0))
    # Mesiac
    pygame.draw.circle(screen, COL_MOON, (WIDTH - 150, 150), 60)

def draw_silhouette(screen):
    # Zem
    pygame.draw.polygon(screen, COL_SILHOUETTE, [(0, HEIGHT), (0, HEIGHT-100), (WIDTH, HEIGHT-80), (WIDTH, HEIGHT)])
    # Kríže
    crosses = [(100, HEIGHT-130, 10, 40), (WIDTH-300, HEIGHT-120, 12, 50), (WIDTH-100, HEIGHT-110, 8, 30)]
    for cx, cy, cw, ch in crosses:
        pygame.draw.rect(screen, COL_SILHOUETTE, (cx, cy, cw, ch))
        pygame.draw.rect(screen, COL_SILHOUETTE, (cx - cw, cy + ch//3, cw*3, ch//4))

# --- 6. HLAVNÝ KÓD ---

def run_menu():
    clock = pygame.time.Clock()
    
    # 1. Pozadie (Gradient)
    bg = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        r = COL_SKY_TOP[0] + (COL_SKY_BOT[0] - COL_SKY_TOP[0]) * y / HEIGHT
        g = COL_SKY_TOP[1] + (COL_SKY_BOT[1] - COL_SKY_TOP[1]) * y / HEIGHT
        b = COL_SKY_TOP[2] + (COL_SKY_BOT[2] - COL_SKY_TOP[2]) * y / HEIGHT
        pygame.draw.line(bg, (r,g,b), (0, y), (WIDTH, y))

    # 2. Objekty
    stars = [Star() for _ in range(60)]
    
    # ZMENA: Výrazne nižšia rýchlosť (0.05 - 0.2) pre pomalú hmlu
    fogs_back = [AdvancedFog(random.randint(HEIGHT-300, HEIGHT-100), random.uniform(0.05, 0.1), 30) for _ in range(8)]
    fogs_front = [AdvancedFog(random.randint(HEIGHT-150, HEIGHT), random.uniform(0.1, 0.2), 50) for _ in range(10)]

    # 3. Načítanie Fontov a Zvukov
    try:
        if not os.path.exists(FONT_PATH):
            print(f"POZOR: Font sa nenašiel na ceste: {FONT_PATH}")
        
        font_title = pygame.font.Font(FONT_PATH, 80)
        font_menu = pygame.font.Font(FONT_PATH, 30)
        font_small = pygame.font.Font(FONT_PATH, 20)
        
        s_hover_path = os.path.join(parent_dir, "Resources", "Audio", "hover.wav")
        s_click_path = os.path.join(parent_dir, "Resources", "Audio", "click.wav")
        
        if os.path.exists(s_hover_path):
            s_hover = pygame.mixer.Sound(s_hover_path)
            s_hover.set_volume(0.2)
        else:
            s_hover = None

        if os.path.exists(s_click_path):
            s_click = pygame.mixer.Sound(s_click_path)
        else:
            s_click = None
            
    except Exception as e:
        print(f"Používam záložné fonty. Dôvod: {e}")
        font_title = pygame.font.SysFont("Arial", 80, bold=True)
        font_menu = pygame.font.SysFont("Arial", 30)
        font_small = pygame.font.SysFont("Arial", 20)
        s_hover, s_click = None, None

    # 4. Tlačidlá
    btns = [
        Button("PLAY", 350, font_menu, "play"),
        Button("SETTINGS", 430, font_menu, "settings"),
        Button("CREDITS", 510, font_menu, "credits"),
        Button("QUIT", 590, font_menu, "quit")
    ]
    btn_back = Button("BACK", 620, font_menu, "back")
    slider = Slider(WIDTH//2 - 150, 350, 300, 20, 0.5)

    view = "menu"

    while True:
        # --- KRESLENIE SCÉNY ---
        screen.blit(bg, (0,0))
        
        for s in stars: s.update(); s.draw(screen) 
        draw_moon(screen)                          
        for f in fogs_back: f.update(); f.draw(screen) 
        draw_silhouette(screen)                    
        for f in fogs_front: f.update(); f.draw(screen) 

        # Vinetácia
        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(vignette, (0,0,0,0), (WIDTH//2, HEIGHT//2), 600)
        pygame.draw.circle(vignette, (0,0,0,180), (WIDTH//2, HEIGHT//2), 900, 300)
        screen.blit(vignette, (0,0))

        # --- LOGIKA ---
        mx, my = pygame.mouse.get_pos()
        m_down = pygame.mouse.get_pressed()[0]
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if view != "menu": view = "menu"; 
                if s_click: s_click.play()

        # --- MENU ---
        if view == "menu":
            offset = math.sin(pygame.time.get_ticks() * 0.002) * 10
            scale = 1.0 + math.sin(pygame.time.get_ticks() * 0.003) * 0.03
            
            t_surf = font_title.render("KTO DRUHEMU JAMU KOPE...", True, ACCENT)
            w, h = int(t_surf.get_width() * scale), int(t_surf.get_height() * scale)
            t_surf = pygame.transform.smoothscale(t_surf, (w, h))
            
            s_surf = font_title.render("KTO DRUHEMU JAMU KOPE...", True, (0,0,0)) 
            s_surf = pygame.transform.smoothscale(s_surf, (w, h))
            
            r = t_surf.get_rect(center=(WIDTH//2, 140 + offset))
            screen.blit(s_surf, (r.x+5, r.y+5))
            screen.blit(t_surf, r)

            for btn in btns:
                act = btn.update(mx, my, click, s_hover)
                btn.draw(screen)
                if act:
                    if s_click: s_click.play()
                    if act == "play": main.spustit_hru(screen)
                    elif act == "settings": view = "settings"
                    elif act == "credits": view = "credits"
                    elif act == "quit": pygame.quit(); sys.exit()

        # --- SETTINGS ---
        elif view == "settings":
            head = font_title.render("SETTINGS", True, ACCENT)
            screen.blit(head, head.get_rect(center=(WIDTH//2, 100)))

            vol = slider.update(mx, my, m_down)
            if s_hover: s_hover.set_volume(vol)
            if s_click: s_click.set_volume(vol)
            
            slider.draw(screen)
            txt = font_menu.render(f"Volume: {int(vol*100)}%", True, TEXT_COL)
            screen.blit(txt, txt.get_rect(center=(WIDTH//2, 310)))

            if btn_back.update(mx, my, click, s_hover) == "back":
                if s_click: s_click.play()
                view = "menu"
            btn_back.draw(screen)

        # --- CREDITS ---
        elif view == "credits":
            head = font_title.render("CREDITS", True, ACCENT)
            screen.blit(head, head.get_rect(center=(WIDTH//2, 100)))
            
            data = [("CODE", "Ty"), ("ART", "Assets"), ("AUDIO", "Spooky SFX")]
            y = 230
            for r, n in data:
                lbl = font_small.render(r, True, (150,150,150))
                val = font_menu.render(n, True, (255,255,255))
                screen.blit(lbl, lbl.get_rect(center=(WIDTH//2, y)))
                screen.blit(val, val.get_rect(center=(WIDTH//2, y+30)))
                y += 90

            if btn_back.update(mx, my, click, s_hover) == "back":
                if s_click: s_click.play()
                view = "menu"
            btn_back.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_menu()