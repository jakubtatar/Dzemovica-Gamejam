import pygame
import random
import sys
import os

# ==========================================
# NOVÁ TRIEDA PRE MINIHRU (Vložiť nad spustit_hru)
# ==========================================
class GraveDigMinigame:
    def __init__(self, screen):
        self.screen = screen
        self.sw, self.sh = screen.get_size()
        self.clicks_needed = 10
        self.clicks_done = 0
        self.active_cube = pygame.Rect(0, 0, 80, 80)
        self.spawn_cube()
        # Skúsime načítať tvoj font, ak nie, použijeme systémový
        try:
            path = os.path.join("Resources", "Fonts", "upheavtt.ttf")
            self.font = pygame.font.Font(path, 40)
        except:
            self.font = pygame.font.SysFont("Arial", 32, bold=True)

    def spawn_cube(self):
        """Vygeneruje hnedú kocku na náhodnom mieste v 'jame'"""
        self.active_cube.center = (
            random.randint(self.sw//2 - 150, self.sw//2 + 150),
            random.randint(self.sh//2 - 100, self.sh//2 + 150)
        )

    def run(self):
        """Hlavná slučka minihry"""
        running_mini = True
        while running_mini:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.active_cube.collidepoint((mx, my)):
                        self.clicks_done += 1
                        if self.clicks_done >= self.clicks_needed:
                            return random.randint(10, 50) # VRÁTI REWARD (Peniaze)
                        self.spawn_cube()
                
                # Umožníme odísť z minihry cez ESC
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 0

            self.draw()
            pygame.display.flip()

    def draw(self):
        # Stmavenie pozadia hry
        overlay = pygame.Surface((self.sw, self.sh))
        overlay.set_alpha(200)
        overlay.fill((10, 5, 0))
        self.screen.blit(overlay, (0, 0))

        # Kreslenie "jamy"
        pit_rect = pygame.Rect(self.sw//2 - 250, self.sh//2 - 200, 500, 450)
        pygame.draw.rect(self.screen, (50, 30, 20), pit_rect) # Podklad jamy
        pygame.draw.rect(self.screen, (100, 70, 50), pit_rect, 6) # Okraj

        # Aktuálna kocka hliny (klikateľný cieľ)
        pygame.draw.rect(self.screen, (139, 69, 19), self.active_cube)
        pygame.draw.rect(self.screen, (255, 255, 255), self.active_cube, 2) # Biely okraj kocky

        # Texty s inštrukciami
        txt = self.font.render(f"DIGGING... {self.clicks_done}/{self.clicks_needed}", True, (210, 180, 140))
        self.screen.blit(txt, (self.sw//2 - txt.get_width()//2, self.sh//2 - 260))