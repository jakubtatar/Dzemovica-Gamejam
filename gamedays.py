import pygame
import time

class Monday:
    def __init__(self, screen, player, gui, game_data):
        self.screen = screen
        self.player = player
        self.gui = gui
        self.game_data = game_data
        self.quest_step = 0
        self.day_finished = False
        
        # Počiatočný quest
        self.update_gui_quest("Where am I?", "Talk to the barman.")

    def intro_screen(self):
        intro_font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 100)
        text_surf = intro_font.render("MONDAY", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.fill((0, 0, 0))
        self.screen.blit(text_surf, text_rect)
        pygame.display.flip()
        time.sleep(2)

    def update_gui_quest(self, title, desc):
        self.gui.current_quest = {"title": title, "desc": desc}

    def start(self, setup_map_func):
        self.intro_screen()
        setup_map_func("taverna")
        self.player.rect.topleft = (400, 400)
        self.game_data["gameday"] = 1
        self.player.day = "Monday" # Uisti sa, že hráč má nastavený deň

    def next_day_transition(self):
        """Prepne hru na Utorok."""
        self.day_finished = True
        self.player.day = "Tuesday"
        self.game_data["gameday"] = 2
        self.update_gui_quest("Tuesday", "New day, new problems.")
        print("Prechod na utorok úspešný!")

    def update_quests(self):
        if self.day_finished:
            return

        npc = self.game_data.get("npc")
        current_map = self.game_data.get("current_map")

        # QUEST 1: Rozhovor s Barmanom
        if self.quest_step == 0:
            if npc and getattr(npc, 'name', '') == "Barman" and self.game_data.get("dialogue_active"):
                self.quest_step = 1
                self.update_gui_quest("Back to work", "Find your way to the cemetery.")

        # QUEST 2: Príchod na cintorín
        elif self.quest_step == 1:
            if current_map == "cmitermap":
                self.quest_step = 2
                self.update_gui_quest("Grave Digger", "Dig at least one grave.")

        # QUEST 3: Vykopanie prvého hrobu
        elif self.quest_step == 2:
            if len(self.game_data.get("graves", [])) > 0:
                self.quest_step = 3
                self.update_gui_quest("Village Priest", "Talk to the Priest in the village.")

        # QUEST 4: Rozhovor s kňazom
        elif self.quest_step == 3:
            if npc and getattr(npc, 'name', '') == "Priest" and self.game_data.get("dialogue_active"):
                self.quest_step = 4
                self.update_gui_quest("Night Shift", "Survive the night (Right click to start).")

        # QUEST 5: Prežitie noci (aktivácia Night Mode)
        elif self.quest_step == 4:
            if self.game_data.get("night_mode") == True:
                self.quest_step = 5
                self.next_day_transition()