import pygame
import sys
import os

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()
        
        # 1. Načítanie fontu (bezpečný spôsob)
        try:
            path = os.path.join("Resources", "Fonts", "upheavtt.ttf")
            self.font = pygame.font.Font(path, 50)
            self.small_font = pygame.font.Font(path, 30)
        except:
            print("Font nenájdený, používam systémový.")
            self.font = pygame.font.SysFont("Arial", 50)
            self.small_font = pygame.font.SysFont("Arial", 30)

    def draw_text(self, text, y, size="big", color=(255, 255, 255), hover=False):
        """Pomocná funkcia: Vykreslí text na stred s čiernym obrysom."""
        font = self.font if size == "big" else self.small_font
        final_color = (255, 0, 0) if hover else color
        
        # Vytvorenie textu a obrysu
        text_surf = font.render(text, True, final_color)
        outline_surf = font.render(text, True, (0, 0, 0))
        rect = text_surf.get_rect(center=(self.width // 2, y))

        # Vykreslenie obrysu (tieň)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx or dy: self.screen.blit(outline_surf, rect.move(dx, dy))
        
        # Vykreslenie samotného textu
        self.screen.blit(text_surf, rect)
        return rect # Vrátime oblasť pre klikanie

    def run(self):
        """Hlavná slučka menu - ovláda všetko (Menu, Credits, Settings)."""
        view = "menu" # Premenná určuje, čo práve vidíme

        while True:
            self.screen.fill((8, 50, 20)) # Vyčistiť obrazovku
            mx, my = pygame.mouse.get_pos()
            click = False

            # --- 1. Spracovanie eventov (klikanie a vypnutie) ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    click = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if view != "menu": view = "menu" # Escape vráti vždy do menu
            
            # === HLAVNÉ MENU ===
            if view == "menu":
                self.draw_text("KTO DRUHEMU JAMU KOPE...", 100, "big", (255, 215, 0))
                
                options = ["PLAY", "SETTINGS", "CREDITS", "QUIT"]
                for i, option in enumerate(options):
                    # Vykreslíme text a zistíme, či na ňom je myš
                    rect = self.draw_text(option, 250 + i * 70, "big", hover=False)
                    
                    if rect.collidepoint((mx, my)):
                        self.draw_text(option, 250 + i * 70, "big", hover=True) # Prekreslí na červeno
                        if click:
                            if option == "PLAY": return "play"     
                            if option == "SETTINGS": view = "settings" 
                            if option == "CREDITS": view = "credits"   
                            if option == "QUIT": pygame.quit(); sys.exit()

            # === CREDITS ===
            elif view == "credits":
                self.draw_text("CREDITS", 80, "big", (255, 215, 0))
                
                lines = [
                    ("PROGRAMMING", "Meno 1, Meno 2"),
                    ("ART AND DESIGN", "Meno 3, Meno 4"),
                    ("SOUND", "Meno 5")
                ]
                
                for i, (role, name) in enumerate(lines):
                    self.draw_text(role, 180 + i * 90, "small", (200, 200, 100))
                    self.draw_text(name, 215 + i * 90, "small", (255, 255, 255))

                # Tlačidlo BACK
                rect = self.draw_text("BACK", 600, "big", hover=False)
                if rect.collidepoint((mx, my)):
                    self.draw_text("BACK", 600, "big", hover=True)
                    if click: view = "menu"

            # === SETTINGS (NASTAVENIA) ===
            elif view == "settings":
                self.draw_text("SETTINGS", 80, "big", (255, 215, 0))
                self.draw_text("Volume: 100%", 300, "big")
                self.draw_text("(Coming Soon)", 380, "small", (150, 150, 150))

                # Tlačidlo BACK
                rect = self.draw_text("BACK", 600, "big", hover=False)
                if rect.collidepoint((mx, my)):
                    self.draw_text("BACK", 600, "big", hover=True)
                    if click: view = "menu"

            pygame.display.flip()
            self.clock.tick(60)

# --- TOTO SPUSTÍŠ NA TESTOVANIE ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    menu = MainMenu(screen)
    print(f"Hra pokračuje do: {menu.run()}")