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
        self.quests = []
        # TU už nevoláme update_gui_quest, aby sme neprepísali GUI predčasne

    def intro_screen(self):
        """Zobrazí nápis MONDAY cez celú obrazovku."""
        try:
            intro_font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 100)
        except:
            intro_font = pygame.font.SysFont("Arial", 100)
            
        text_surf = intro_font.render("MONDAY", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        self.screen.fill((0, 0, 0))
        self.screen.blit(text_surf, text_rect)
        pygame.display.flip()
        time.sleep(2)

    def update_gui_quest(self, title, desc):
        self.gui.current_quest = {"title": title, "desc": desc}

    def start(self, setup_map_func):
        # QUESTY NASTAVUJEME AŽ TU
        self.intro_screen()
        self.update_gui_quest("Where am I?", "Talk to the barman.")
        
        setup_map_func("taverna")
        self.player.rect.topleft = (400, 400)
        self.game_data["gameday"] = 1
        self.player.day = "Monday"
        self.quest_step = 0
        self.day_finished = False

    def next_day_transition(self):
        """Prechod na Utorok."""
        self.day_finished = True
        # Tu len povieme, že deň skončil, main.py sa postará o prepnutie manažéra
        print("Pondelok skončil, čakám na prepnutie v main.py")

    def update_quests(self):
        if self.day_finished:
            return

        npc = self.game_data.get("npc")
        current_map = self.game_data.get("current_map")
        is_talking = self.game_data.get("dialogue_active", False)

        # 1. ROZHOVOR S BARMANOM
        if self.quest_step == 0:
            if npc and getattr(npc, 'name', '') == "Barman":
                npc.set_dialogue([
                    "Hugo! Finally awake?",
                    "You've been out for a while.",
                    "The Priest was looking for you. Go to the cemetery."
                ])
                if is_talking:
                    self.game_data["barman_contacted"] = True
                
                if not is_talking and self.game_data.get("barman_contacted"):
                    self.quest_step = 1
                    self.update_gui_quest("Back to work", "Find your way to the cemetery.")

        # 2. PRÍCHOD NA CINTORÍN
        elif self.quest_step == 1:
            if current_map == "cmitermap":
                self.quest_step = 2
                self.update_gui_quest("Grave Digger", "Dig at least one grave.")

        # 3. VYKOPANIE HROBU
        elif self.quest_step == 2:
            if len(self.game_data.get("graves", [])) > 0:
                self.quest_step = 3
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.")

        # 4. ROZHOVOR S KŇAZOM
        elif self.quest_step == 3:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "I see you've started your work, Hugo.",
                    "But the night is coming, and the dead are restless.",
                    "You must survive the night shift. Good luck."
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 4
                    self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

        # 5. PREŽITIE NOCI
        elif self.quest_step == 4:
            # Ak noc skončila (night_mode je False a timer je na nule)
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 5
                self.next_day_transition()


class Tuesday:
    def __init__(self, screen, player, gui, game_data):
        self.screen = screen
        self.player = player
        self.gui = gui
        self.game_data = game_data
        self.quest_step = 0
        self.day_finished = False
        self.quests = []

    def intro_screen(self):
        try:
            intro_font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 100)
        except:
            intro_font = pygame.font.SysFont("Arial", 100)

        text_surf = intro_font.render("TUESDAY", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        self.screen.fill((0, 0, 0))
        self.screen.blit(text_surf, text_rect)
        pygame.display.flip()
        time.sleep(2)

    def update_gui_quest(self, title, desc):
        self.gui.current_quest = {"title": title, "desc": desc}

    def start(self, setup_map_func):
        # UTORKOVÝ QUEST SA NASTAVÍ AŽ TU
        self.intro_screen()
        self.update_gui_quest("Morning After", "Check the cemetery for any 'leftovers'.")
        
        setup_map_func("cmitermap")
        self.player.rect.topleft = (2700, 150)
        self.game_data["gameday"] = 2
        self.player.day = "Tuesday"
        self.game_data["night_mode"] = False
        self.game_data["night_finished"] = False
        self.quest_step = 0

    def update_quests(self):
        if self.day_finished:
            return

        npc = self.game_data.get("npc")
        current_map = self.game_data.get("current_map")
        is_talking = self.game_data.get("dialogue_active", False)
        enemies = self.game_data.get("enemies", [])

        # 1. VYČISTENIE CINTORÍNA
        if self.quest_step == 0:
            if current_map == "cmitermap":
                if len(enemies) == 0:
                    self.quest_step = 1
                    self.update_gui_quest("Payday", "Go to the Tavern and ask the Barman for your coins.")
                else:
                    self.update_gui_quest("Clean Up", f"Exorcise the remaining spirits ({len(enemies)} left).")

        # 2. CESTA DO TAVERNY
        elif self.quest_step == 1:
            if current_map == "taverna":
                self.quest_step = 2

        # 3. ROZHOVOR S BARMANOM
        elif self.quest_step == 2:
            if npc and getattr(npc, 'name', '') == "Barman":
                npc.set_dialogue([
                    "You survived! I heard some screaming from the hill.",
                    "Here is your pay for the first two days.",
                    "Keep this up and you might even afford a better shovel."
                ])
                if is_talking:
                    self.game_data["salary_received"] = True
                
                if not is_talking and self.game_data.get("salary_received"):
                    self.player.money += 100
                    self.quest_step = 3
                    self.update_gui_quest("Rest", "Go home and prepare for Wednesday.")

        # 4. KONIEC DŇA
        elif self.quest_step == 3:
            if current_map == "house":
                self.day_finished = True
                print("Tuesday finished!")