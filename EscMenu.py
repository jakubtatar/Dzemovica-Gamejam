import pygame
import sys

class EscMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        
        # Načítanie fontov (uisti sa, že cesta k fontu je správna)
        try:
            self.font = pygame.font.Font("Resources/Fonts/upheavtt.ttf", 60)
            self.small_font = pygame.font.Font("Resources/Fonts/upheavtt.ttf", 35)
        except:
            self.font = pygame.font.SysFont("Arial", 60)
            self.small_font = pygame.font.SysFont("Arial", 35)
        
        # Nastavenia farieb
        self.overlay_color = (0, 0, 0, 160)  # Tmavé polopriehľadné pozadie
        self.text_color = (255, 255, 255)    # Biela
        self.highlight_color = (255, 215, 0) # Zlatá (pri hoveri)
        
        # Možnosti v menu
        self.options = ["CONTINUE", "QUIT TO MENU"]

    def draw(self):
        # 1. Stmavenie obrazovky hry
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill(self.overlay_color)
        self.screen.blit(overlay, (0, 0))

        # 2. Vykreslenie nadpisu "PAUSED"
        title_surf = self.font.render("PAUSED", True, self.text_color)
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 120))
        self.screen.blit(title_surf, title_rect)

        # 3. Vykreslenie interaktívnych možností
        mouse_pos = pygame.mouse.get_pos()
        
        for i, option in enumerate(self.options):
            # Základná pozícia pre text
            pos_y = self.screen_height // 2 + (i * 70)
            
            # Vytvorenie dočasného rectu pre detekciu kolízie s myšou
            temp_surf = self.small_font.render(option, True, self.text_color)
            opt_rect = temp_surf.get_rect(center=(self.screen_width // 2, pos_y))
            
            # Kontrola, či je myš nad textom (Hover efekt)
            if opt_rect.collidepoint(mouse_pos):
                current_color = self.highlight_color
            else:
                current_color = self.text_color
                
            # Samotné vykreslenie textu
            final_surf = self.small_font.render(option, True, current_color)
            self.screen.blit(final_surf, opt_rect)

    def run(self):
        """Hlavná slučka menu. Vracia 'continue' alebo 'quit'."""
        clock = pygame.time.Clock()
        
        while True:
            self.draw()
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # Návrat do hry cez ESC
                    if event.key == pygame.K_ESCAPE:
                        return "continue"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Ľavý klik
                        mouse_pos = pygame.mouse.get_pos()
                        
                        for i, option in enumerate(self.options):
                            pos_y = self.screen_height // 2 + (i * 70)
                            # Musíme vytvoriť rect rovnako ako v draw(), aby sme vedeli, kde sa kliklo
                            temp_surf = self.small_font.render(option, True, self.text_color)
                            opt_rect = temp_surf.get_rect(center=(self.screen_width // 2, pos_y))
                            
                            if opt_rect.collidepoint(mouse_pos):
                                if option == "CONTINUE":
                                    return "continue"
                                if option == "QUIT TO MENU":
                                    return "quit"