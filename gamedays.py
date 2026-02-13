import pygame
import time

class Monday:
    def __init__(self, screen, player, gui, game_data):
        self.screen = screen
        self.player = player
        self.gui = gui
        self.game_data = game_data
        self.quest_step = 0
        
        # Nastavíme počiatočný quest
        self.update_gui_quest("Pondelok", "Choď do taverny za barmanom.")

    def intro_screen(self):
        """Zobrazí čiernu obrazovku s nápisom MONDAY."""
        # Použijeme veľký font
        intro_font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 100)
        text_surf = intro_font.render("MONDAY", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        # 1. Čierna obrazovka
        self.screen.fill((0, 0, 0))
        self.screen.blit(text_surf, text_rect)
        pygame.display.flip()
        
        # 2. Pauza, aby si to hráč stihol prečítať (napr. 2 sekundy)
        time.sleep(2)

    def update_gui_quest(self, title, desc):
        self.gui.current_quest = {"title": title, "desc": desc}

    def start(self, setup_map_func):
        # Najprv ukážeme nápis
        self.intro_screen()
        
        # Potom nahráme mapu
        setup_map_func("taverna")
        self.player.rect.topleft = (400, 400)
        self.game_data["gameday"] = 1

    def update_quests(self):
        npc = self.game_data.get("npc")
        if self.quest_step == 0 and npc and getattr(npc, 'name', '') == "Barman":
            self.quest_step = 0
            self.update_gui_quest("Where am I?", "Talk to the barman.")
        elif self.quest_step == 1:
            self.update_gui_quest("Back to the work", "Find your way to the cemetery.")