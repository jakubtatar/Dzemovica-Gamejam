import pygame
import random
import sys
import os

class GraveDigMinigame:
    def __init__(self, screen):
        self.screen = screen
        self.sw, self.sh = screen.get_size()
        self.clock = pygame.time.Clock()
        
        self.clicks_needed = 10
        self.clicks_done = 0
        self.base_size = 80  # Pôvodná veľkosť
        self.active_cube = pygame.Rect(0, 0, self.base_size, self.base_size)
        
        self.time_limit = 3000 
        self.timer_start = pygame.time.get_ticks()
        
        self.particles = []
        self.spawn_cube()
        
        try:
            path = os.path.join("Resources", "Fonts", "upheavtt.ttf")
            self.font = pygame.font.Font(path, 40)
        except:
            self.font = pygame.font.SysFont("Arial", 32, bold=True)

    def spawn_cube(self):
        """Vygeneruje cieľ na novom mieste a resetuje jeho veľkosť"""
        # Resetujeme veľkosť na základnú pri každom spawne
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
        running_mini = True
        while running_mini:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.timer_start
            
            if elapsed > self.time_limit:
                return 0 

            # --- LOGIKA ZMENŠOVANIA ---
            # Vypočítame percento zostávajúceho času (1.0 až 0.0)
            time_left_ratio = max(0, (self.time_limit - elapsed) / self.time_limit)
            
            # Nová veľkosť: lineárne klesá z 80 na 10
            new_size = max(10, int(self.base_size * time_left_ratio))
            
            # Uložíme si stred, zmeníme veľkosť a vrátime stred späť
            old_center = self.active_cube.center
            self.active_cube.width = new_size
            self.active_cube.height = new_size
            self.active_cube.center = old_center

            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.active_cube.collidepoint((mx, my)):
                        self.create_particles(mx, my)
                        self.clicks_done += 1
                        if self.clicks_done >= self.clicks_needed:
                            return random.randint(10, 50)
                        self.spawn_cube()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 0

            # Update častíc
            for p in self.particles[:]:
                p["pos"][0] += p["vel"][0]
                p["pos"][1] += p["vel"][1]
                p["vel"][1] += 0.2 
                p["timer"] -= 1
                if p["timer"] <= 0:
                    self.particles.remove(p)

            self.draw(elapsed)
            pygame.display.flip()
            self.clock.tick(60)

    def draw(self, elapsed):
        overlay = pygame.Surface((self.sw, self.sh))
        overlay.set_alpha(200)
        overlay.fill((10, 5, 0))
        self.screen.blit(overlay, (0, 0))

        pit_rect = pygame.Rect(self.sw//2 - 250, self.sh//2 - 200, 500, 450)
        pygame.draw.rect(self.screen, (50, 30, 20), pit_rect)
        pygame.draw.rect(self.screen, (100, 70, 50), pit_rect, 6)

        # Timer Bar
        timer_width = 400
        time_percent = max(0, (self.time_limit - elapsed) / self.time_limit)
        bar_color = (255, 50, 50) if time_percent < 0.3 else (255, 215, 0)
        pygame.draw.rect(self.screen, (30, 30, 30), (self.sw//2 - 200, self.sh//2 + 280, timer_width, 20))
        pygame.draw.rect(self.screen, bar_color, (self.sw//2 - 200, self.sh//2 + 280, int(timer_width * time_percent), 20))

        # Kocka (teraz sa zmenšuje)
        pygame.draw.rect(self.screen, (139, 69, 19), self.active_cube)
        pygame.draw.rect(self.screen, (255, 255, 255), self.active_cube, 2)

        for p in self.particles:
            pygame.draw.rect(self.screen, p["color"], (p["pos"][0], p["pos"][1], 6, 6))

        txt = self.font.render(f"DIG FAST! {self.clicks_done}/{self.clicks_needed}", True, (210, 180, 140))
        self.screen.blit(txt, (self.sw//2 - txt.get_width()//2, self.sh//2 - 260))