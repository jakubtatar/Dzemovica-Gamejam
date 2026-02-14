import pygame
import random
import sys
import os

# --- POMOCNÉ FUNKCIE ---
def draw_minigame_background(screen, sw, sh):
    """Spoločné pozadie pre všetky minihry"""
    overlay = pygame.Surface((sw, sh))
    overlay.set_alpha(200)
    overlay.fill((10, 5, 0))
    screen.blit(overlay, (0, 0))

    # Hnedá jama (rámček) - šírka 500px
    pit_rect = pygame.Rect(sw//2 - 250, sh//2 - 200, 500, 450)
    pygame.draw.rect(screen, (50, 30, 20), pit_rect)
    pygame.draw.rect(screen, (100, 70, 50), pit_rect, 6)

def show_final_message(screen, font, text, color, sw, sh):
    """Zobrazí veľký nápis na konci minihry"""
    # Malý tmavý pás pod textom pre lepšiu čitateľnosť
    bg_rect = pygame.Rect(0, sh//2 - 60, sw, 120)
    pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect)
    
    txt_surf = font.render(text, True, color)
    screen.blit(txt_surf, (sw//2 - txt_surf.get_width()//2, sh//2 - txt_surf.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(1000) # Počká 1 sekundu, aby si hráč prečítal výsledok

# --- MINIHRY ---

class GraveDigMinigame:
    def __init__(self, screen):
        self.screen = screen
        self.sw, self.sh = screen.get_size()
        self.clock = pygame.time.Clock()
        self.clicks_needed = 10
        self.clicks_done = 0
        self.base_size = 80
        self.active_cube = pygame.Rect(0, 0, self.base_size, self.base_size)
        self.time_limit = 3000 
        self.timer_start = pygame.time.get_ticks()
        self.particles = []
        self.spawn_cube()
        
        try:
            path = os.path.join("Resources", "Fonts", "upheavtt.ttf")
            self.font = pygame.font.Font(path, 40)
            self.big_font = pygame.font.Font(path, 80)
        except:
            self.font = pygame.font.SysFont("Arial", 32, bold=True)
            self.big_font = pygame.font.SysFont("Arial", 64, bold=True)

    def spawn_cube(self):
        self.active_cube.width = self.base_size
        self.active_cube.height = self.base_size
        self.active_cube.center = (
            random.randint(self.sw//2 - 150, self.sw//2 + 150),
            random.randint(self.sh//2 - 100, self.sh//2 + 150)
        )
        self.timer_start = pygame.time.get_ticks()

    def create_particles(self, x, y):
        for _ in range(15):
            self.particles.append({
                "pos": [x, y],
                "vel": [random.uniform(-4, 4), random.uniform(-7, 2)],
                "timer": random.randint(20, 50),
                "color": random.choice([(100, 70, 40), (139, 69, 19), (80, 50, 20)])
            })

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.timer_start
            
            if elapsed > self.time_limit:
                show_final_message(self.screen, self.big_font, "GRAVE FAILED", (255, 50, 50), self.sw, self.sh)
                return 0 

            time_left_ratio = max(0, (self.time_limit - elapsed) / self.time_limit)
            new_size = max(10, int(self.base_size * time_left_ratio))
            old_center = self.active_cube.center
            self.active_cube.width = new_size
            self.active_cube.height = new_size
            self.active_cube.center = old_center

            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return 0
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.active_cube.collidepoint((mx, my)):
                        self.create_particles(mx, my)
                        self.clicks_done += 1
                        if self.clicks_done >= self.clicks_needed:
                            show_final_message(self.screen, self.big_font, "GRAVE COMPLETED", (50, 255, 50), self.sw, self.sh)
                            return random.randint(10, 50)
                        self.spawn_cube()

            # Update častíc
            for p in self.particles[:]:
                p["pos"][0] += p["vel"][0]
                p["pos"][1] += p["vel"][1]
                p["vel"][1] += 0.2 
                p["timer"] -= 1
                if p["timer"] <= 0: self.particles.remove(p)

            self.draw(elapsed)
            pygame.display.flip()
            self.clock.tick(60)

    def draw(self, elapsed):
        draw_minigame_background(self.screen, self.sw, self.sh)
        timer_width = 400
        time_percent = max(0, (self.time_limit - elapsed) / self.time_limit)
        pygame.draw.rect(self.screen, (30, 30, 30), (self.sw//2 - 200, self.sh//2 + 280, timer_width, 20))
        pygame.draw.rect(self.screen, (255, 215, 0), (self.sw//2 - 200, self.sh//2 + 280, int(timer_width * time_percent), 20))
        pygame.draw.rect(self.screen, (139, 69, 19), self.active_cube)
        pygame.draw.rect(self.screen, (255, 255, 255), self.active_cube, 2)
        for p in self.particles:
            pygame.draw.rect(self.screen, p["color"], (p["pos"][0], p["pos"][1], 6, 6))
        txt = self.font.render(f"DIG FAST! {self.clicks_done}/{self.clicks_needed}", True, (210, 180, 140))
        self.screen.blit(txt, (self.sw//2 - txt.get_width()//2, self.sh//2 - 260))

class TimingDigMinigame:
    def __init__(self, screen):
        self.screen = screen
        self.sw, self.sh = screen.get_size()
        self.clock = pygame.time.Clock()
        self.bar_rect = pygame.Rect(self.sw//2 - 150, self.sh//2 + 50, 300, 40)
        self.marker_x = self.bar_rect.left
        self.direction = 1
        self.speed = 12
        self.target_zone = pygame.Rect(self.sw//2 - 30, self.sh//2 + 45, 60, 50)
        self.successes = 0
        self.needed = 3
        self.particles = []
        try:
            path = os.path.join("Resources", "Fonts", "upheavtt.ttf")
            self.font = pygame.font.Font(path, 40)
            self.big_font = pygame.font.Font(path, 80)
        except:
            self.font = pygame.font.SysFont("Arial", 32, bold=True)
            self.big_font = pygame.font.SysFont("Arial", 64, bold=True)

    def create_particles(self, x, y):
        for _ in range(15):
            self.particles.append({
                "pos": [x, y], "vel": [random.uniform(-4, 4), random.uniform(-7, 2)],
                "timer": random.randint(20, 50), "color": (139, 69, 19)
            })

    def run(self):
        while True:
            self.marker_x += self.speed * self.direction
            if self.marker_x <= self.bar_rect.left or self.marker_x >= self.bar_rect.right:
                self.direction *= -1

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.target_zone.left <= self.marker_x <= self.target_zone.right:
                        self.successes += 1
                        self.create_particles(self.marker_x, self.sh//2 + 70)
                        self.speed += 4
                        if self.successes >= self.needed:
                            show_final_message(self.screen, self.big_font, "GRAVE COMPLETED", (50, 255, 50), self.sw, self.sh)
                            return 60
                    else:
                        show_final_message(self.screen, self.big_font, "GRAVE FAILED", (255, 50, 50), self.sw, self.sh)
                        return 0

            for p in self.particles[:]:
                p["pos"][0] += p["vel"][0]; p["pos"][1] += p["vel"][1]
                p["vel"][1] += 0.2; p["timer"] -= 1
                if p["timer"] <= 0: self.particles.remove(p)

            self.draw()
            pygame.display.flip(); self.clock.tick(60)

    def draw(self):
        draw_minigame_background(self.screen, self.sw, self.sh)
        txt = self.font.render(f"TIMING! {self.successes}/{self.needed}", True, (210, 180, 140))
        self.screen.blit(txt, (self.sw//2 - txt.get_width()//2, self.sh//2 - 260))
        pygame.draw.rect(self.screen, (30, 30, 30), self.bar_rect)
        pygame.draw.rect(self.screen, (0, 200, 0), self.target_zone, 4)
        pygame.draw.line(self.screen, (255, 255, 255), (self.marker_x, self.bar_rect.top - 10), (self.marker_x, self.bar_rect.bottom + 10), 6)
        for p in self.particles:
            pygame.draw.rect(self.screen, p["color"], (p["pos"][0], p["pos"][1], 6, 6))

class SequenceDigMinigame:
    def __init__(self, screen):
        self.screen = screen
        self.sw, self.sh = screen.get_size()
        self.clock = pygame.time.Clock()
        self.keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        self.key_names = {pygame.K_UP: "UP", pygame.K_DOWN: "DN", pygame.K_LEFT: "LT", pygame.K_RIGHT: "RT"}
        
        # Sekvencia 5 kľúčov
        self.sequence = [random.choice(self.keys) for _ in range(5)]
        self.current_step = 0
        self.time_limit = 4000
        self.start_time = pygame.time.get_ticks()
        self.particles = []

        try:
            path = os.path.join("Resources", "Fonts", "upheavtt.ttf")
            self.font = pygame.font.Font(path, 35) # Mierne menší font pre kľúče
            self.big_font = pygame.font.Font(path, 80)
        except:
            self.font = pygame.font.SysFont("Arial", 28, bold=True)
            self.big_font = pygame.font.SysFont("Arial", 64, bold=True)

    def create_particles(self):
        for _ in range(20):
            self.particles.append({
                "pos": [self.sw//2, self.sh//2 + 50],
                "vel": [random.uniform(-5, 5), random.uniform(-8, 3)],
                "timer": random.randint(20, 50),
                "color": (100, 100, 100)
            })

    def run(self):
        while True:
            elapsed = pygame.time.get_ticks() - self.start_time
            if elapsed > self.time_limit:
                show_final_message(self.screen, self.big_font, "GRAVE FAILED", (255, 50, 50), self.sw, self.sh)
                return 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: return 0
                    if event.key == self.sequence[self.current_step]:
                        self.current_step += 1
                        self.create_particles()
                        if self.current_step >= len(self.sequence):
                            show_final_message(self.screen, self.big_font, "GRAVE COMPLETED", (50, 255, 50), self.sw, self.sh)
                            return 80
                    else:
                        show_final_message(self.screen, self.big_font, "GRAVE FAILED", (255, 50, 50), self.sw, self.sh)
                        return 0

            for p in self.particles[:]:
                p["pos"][0] += p["vel"][0]; p["pos"][1] += p["vel"][1]
                p["vel"][1] += 0.2; p["timer"] -= 1
                if p["timer"] <= 0: self.particles.remove(p)

            self.draw(elapsed)
            pygame.display.flip(); self.clock.tick(60)

    def draw(self, elapsed):
        draw_minigame_background(self.screen, self.sw, self.sh)
        txt = self.font.render("BREAK THE ROCK!", True, (210, 180, 140))
        self.screen.blit(txt, (self.sw//2 - txt.get_width()//2, self.sh//2 - 260))

        # --- OPRAVENÉ CENTROVANIE KĽÚČOV ---
        spacing = 90
        total_w = (len(self.sequence) - 1) * spacing
        start_x = self.sw // 2 - total_w // 2

        for i, key in enumerate(self.sequence):
            color = (50, 255, 50) if i < self.current_step else (150, 150, 150)
            key_txt = self.font.render(self.key_names[key], True, color)
            # Každý kľúč má pod sebou malý obdĺžnik (rámček)
            key_rect = pygame.Rect(start_x + (i * spacing) - 40, self.sh//2 - 30, 80, 60)
            pygame.draw.rect(self.screen, (30, 30, 30), key_rect)
            pygame.draw.rect(self.screen, color, key_rect, 2)
            
            self.screen.blit(key_txt, (key_rect.centerx - key_txt.get_width()//2, key_rect.centery - key_txt.get_height()//2))

        # Timer bar
        timer_w = 400 * (1 - elapsed / self.time_limit)
        pygame.draw.rect(self.screen, (200, 0, 0), (self.sw//2 - 200, self.sh//2 + 120, timer_w, 10))
        for p in self.particles:
            pygame.draw.rect(self.screen, p["color"], (p["pos"][0], p["pos"][1], 8, 8))