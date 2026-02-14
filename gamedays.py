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
        self.intro_screen()
        # 0. Štartovací quest
        self.update_gui_quest("Where am I?", "Talk to the barman.")
        
        setup_map_func("taverna")
        self.player.rect.topleft = (400, 400)
        self.game_data["gameday"] = 1
        self.player.day = "Monday"
        self.quest_step = 0
        self.day_finished = False

    def next_day_transition(self):
        self.day_finished = True
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
                    "BARMAN: Hugo! Finally awake?",
                    "BARMAN: You've been out for a while.",
                    "YOU: Yeah, I am alright, I just had a hard night.",
                    "BARMAN: Well how is the life going, did you get that job?",
                    "YOU: Yep, I was alone looking for this type of job. Oh wait...",
                    "YOU: I need to hurry, I am going to be late!",
                    "BARMAN: So, what are you waiting for?",
                    "BARMAN: Grab your tools and get to work!",
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

        # 3. KONTROLA KVÓTY (Po prvom kopnutí)
        elif self.quest_step == 2:
            # Ak hráč vykopal aspoň jeden hrob
            if len(self.game_data.get("graves", [])) > 0:
                self.quest_step = 3
                # Hráč dostane info, že má kopať ďalej (alebo že má splnené)
                self.update_gui_quest("More digging", "Check the grave orders and complete the quota.")

        # 4. SPLNENIE KVÓTY -> ÍSŤ ZA KŇAZOM
        elif self.quest_step == 3:
            # Tu môžeš zvýšiť číslo, napr. > 2, ak chceš aby kopal viac
            if len(self.game_data.get("graves", [])) >= 3: 
                self.quest_step = 4
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.")

        # 5. ROZHOVOR S KŇAZOM
        elif self.quest_step == 4:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "PRIEST: I see you've started your work, Hugo.",
                    "PRIEST: But the night is coming, and the dead are restless.",
                    "PRIEST: You must survive the night shift. Good luck.",
                    "PRIEST: Fate of the village is in your hands, protect us..."
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 5
                    self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

        # 6. PREŽITIE NOCI
        elif self.quest_step == 5:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 6
                self.update_gui_quest("Day Finished", "Monday is over. Rest now.")
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
                    self.player.money += 200
                    self.quest_step = 3
                    self.update_gui_quest("Explore", "Visit the local village store.")

        # 4. Navsteva obchodu
        elif self.quest_step == 3:
            if current_map == "store":
                if npc and getattr(npc, 'name', '') == "Shopkeeper":
                    npc.set_dialogue([
                        "Welcome to Zabkas Hugo!",
                    ])
                    if not is_talking and self.game_data.get("salary_received"):
                        self.player.money += 200
                        self.quest_step = 4
                        self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig more graves.")

        #5. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 4:
            # Tu môžeš zvýšiť číslo, napr. > 2, ak chceš aby kopal viac
            if len(self.game_data.get("graves", [])) >= 6: 
                self.quest_step = 5
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 

        # 6. ROZHOVOR S KŇAZOM
        elif self.quest_step == 5:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "PRIEST: I see you've started your work, Hugo.",
                    "PRIEST: But the night is coming, and the dead are restless.",
                    "PRIEST: You must survive the night shift. Good luck.",
                    "PRIEST: Fate of the village is in your hands, protect us..."
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 6
                    self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

        # 7. PREŽITIE NOCI
        elif self.quest_step == 6:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 7
                self.update_gui_quest("Day Finished", "Thuesday is over. Rest now.")
                self.next_day_transition()


class Wednesday:
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

        text_surf = intro_font.render("Wednesday", True, (255, 255, 255))
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
        self.player.day = "Wednesday"
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
                    self.player.money += 200
                    self.quest_step = 3
                    self.update_gui_quest("Explore", "Visit the local village store.")

        # 4. Navsteva obchodu
        elif self.quest_step == 3:
            if current_map == "store":
                if npc and getattr(npc, 'name', '') == "Shopkeeper":
                    npc.set_dialogue([
                        "Welcome to Zabkas Hugo!",
                    ])
                    if not is_talking and self.game_data.get("salary_received"):
                        self.player.money += 200
                        self.quest_step = 4
                        self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig more graves.")

        #5. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 4:
            # Tu môžeš zvýšiť číslo, napr. > 2, ak chceš aby kopal viac
            if len(self.game_data.get("graves", [])) >= 6: 
                self.quest_step = 5
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 

        # 6. ROZHOVOR S KŇAZOM
        elif self.quest_step == 5:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "PRIEST: I see you've started your work, Hugo.",
                    "PRIEST: But the night is coming, and the dead are restless.",
                    "PRIEST: You must survive the night shift. Good luck.",
                    "PRIEST: Fate of the village is in your hands, protect us..."
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 6
                    self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

        # 7. PREŽITIE NOCI
        elif self.quest_step == 6:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 7
                self.update_gui_quest("Day Finished", "Wendsday is over. Rest now.")
                self.next_day_transition()

class Wednesday:
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

        text_surf = intro_font.render("Wednesday", True, (255, 255, 255))
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
        self.player.day = "Wednesday"
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
                    self.player.money += 200
                    self.quest_step = 3
                    self.update_gui_quest("Explore", "Visit the local village store.")

        # 4. Navsteva obchodu
        elif self.quest_step == 3:
            if current_map == "store":
                if npc and getattr(npc, 'name', '') == "Shopkeeper":
                    npc.set_dialogue([
                        "Welcome to Zabkas Hugo!",
                    ])
                    if not is_talking and self.game_data.get("salary_received"):
                        self.player.money += 200
                        self.quest_step = 4
                        self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig more graves.")

        #5. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 4:
            # Tu môžeš zvýšiť číslo, napr. > 2, ak chceš aby kopal viac
            if len(self.game_data.get("graves", [])) >= 9: 
                self.quest_step = 5
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 

        # 6. ROZHOVOR S KŇAZOM
        elif self.quest_step == 5:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "PRIEST: I see you've started your work, Hugo.",
                    "PRIEST: But the night is coming, and the dead are restless.",
                    "PRIEST: You must survive the night shift. Good luck.",
                    "PRIEST: Fate of the village is in your hands, protect us..."
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 6
                    self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

        # 7. PREŽITIE NOCI
        elif self.quest_step == 6:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 7
                self.update_gui_quest("Day Finished", "Wendsday is over. Rest now.")
                self.next_day_transition()

class Thursday:
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

        text_surf = intro_font.render("Thursday", True, (255, 255, 255))
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
        self.player.day = "Thursday"
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
                    self.player.money += 200
                    self.quest_step = 3
                    self.update_gui_quest("Explore", "Visit the local village store.")

        # 4. Navsteva obchodu
        elif self.quest_step == 3:
            if current_map == "store":
                if npc and getattr(npc, 'name', '') == "Shopkeeper":
                    npc.set_dialogue([
                        "Welcome to Zabkas Hugo!",
                    ])
                    if not is_talking and self.game_data.get("salary_received"):
                        self.player.money += 200
                        self.quest_step = 4
                        self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig 12 more graves.")

        #5. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 4:
            # Tu môžeš zvýšiť číslo, napr. > 2, ak chceš aby kopal viac
            if len(self.game_data.get("graves", [])) >= 12: 
                self.quest_step = 5
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 

        # 6. ROZHOVOR S KŇAZOM
        elif self.quest_step == 5:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "PRIEST: I see you've started your work, Hugo.",
                    "PRIEST: But the night is coming, and the dead are restless.",
                    "PRIEST: You must survive the night shift. Good luck.",
                    "PRIEST: Fate of the village is in your hands, protect us..."
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 6
                    self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

        # 7. PREŽITIE NOCI
        elif self.quest_step == 6:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 7
                self.update_gui_quest("Day Finished", "Thursday is over. Rest now.")
                self.next_day_transition()

class Friday:
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

        text_surf = intro_font.render("Friday", True, (255, 255, 255))
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
        self.player.day = "Wednesday"
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
                    self.player.money += 200
                    self.quest_step = 3
                    self.update_gui_quest("Explore", "Visit the local village store.")

        # 4. Navsteva obchodu
        elif self.quest_step == 3:
            if current_map == "store":
                if npc and getattr(npc, 'name', '') == "Shopkeeper":
                    npc.set_dialogue([
                        "Welcome to Zabkas Hugo!",
                    ])
                    if not is_talking and self.game_data.get("salary_received"):
                        self.player.money += 200
                        self.quest_step = 4
                        self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig 15 more graves.")

        #5. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 4:
            # Tu môžeš zvýšiť číslo, napr. > 2, ak chceš aby kopal viac
            if len(self.game_data.get("graves", [])) >= 15: 
                self.quest_step = 5
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 

        # 6. ROZHOVOR S KŇAZOM
        elif self.quest_step == 5:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "PRIEST: I see you've started your work, Hugo.",
                    "PRIEST: But the night is coming, and the dead are restless.",
                    "PRIEST: You must survive the night shift. Good luck.",
                    "PRIEST: Fate of the village is in your hands, protect us..."
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 6
                    self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

        # 7. PREŽITIE NOCI
        elif self.quest_step == 6:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 7
                self.update_gui_quest("Day Finished", "Friday is over. Rest now.")
                self.next_day_transition()

class Saturday:
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

        text_surf = intro_font.render("Saturday", True, (255, 255, 255))
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
        self.player.day = "Wednesday"
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
                    self.player.money += 200
                    self.quest_step = 3
                    self.update_gui_quest("Explore", "Visit the local village store.")

        # 4. Navsteva obchodu
        elif self.quest_step == 3:
            if current_map == "store":
                if npc and getattr(npc, 'name', '') == "Shopkeeper":
                    npc.set_dialogue([
                        "Welcome to Zabkas Hugo!",
                    ])
                    if not is_talking and self.game_data.get("salary_received"):
                        self.player.money += 200
                        self.quest_step = 4
                        self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig 20 more graves.")

        #5. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 4:
            # Tu môžeš zvýšiť číslo, napr. > 2, ak chceš aby kopal viac
            if len(self.game_data.get("graves", [])) >= 20: 
                self.quest_step = 5
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 

        # 6. ROZHOVOR S KŇAZOM
        elif self.quest_step == 5:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "PRIEST: I see you've started your work, Hugo.",
                    "PRIEST: But the night is coming, and the dead are restless.",
                    "PRIEST: You must survive the night shift. Good luck.",
                    "PRIEST: Fate of the village is in your hands, protect us..."
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 6
                    self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

        # 7. PREŽITIE NOCI
        elif self.quest_step == 6:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 7
                self.update_gui_quest("Day Finished", "Saturday is over. Rest now.")
                self.next_day_transition()

class Sunday:
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

        text_surf = intro_font.render("Sunday", True, (255, 255, 255))
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
        self.player.day = "Wednesday"
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
                    self.player.money += 200
                    self.quest_step = 3
                    self.update_gui_quest("Explore", "Visit the local village store.")

        # 4. Navsteva obchodu
        elif self.quest_step == 3:
            if current_map == "store":
                if npc and getattr(npc, 'name', '') == "Shopkeeper":
                    npc.set_dialogue([
                        "Welcome to Zabkas Hugo!",
                    ])
                    if not is_talking and self.game_data.get("salary_received"):
                        self.player.money += 200
                        self.quest_step = 4
                        self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig 30 more graves.")

        #5. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 4:
            # Tu môžeš zvýšiť číslo, napr. > 2, ak chceš aby kopal viac
            if len(self.game_data.get("graves", [])) >= 30: 
                self.quest_step = 5
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 

        # 6. ROZHOVOR S KŇAZOM
        elif self.quest_step == 5:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "PRIEST: I see you've started your work, Hugo.",
                    "PRIEST: But the night is coming, and the dead are restless.",
                    "PRIEST: You must survive the night shift. Good luck.",
                    "PRIEST: Fate of the village is in your hands, protect us..."
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 6
                    self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

        # 7. PREŽITIE NOCI
        elif self.quest_step == 6:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 7
                self.update_gui_quest("Day Finished", "Sunday is over. Rest now.")
                self.next_day_transition()

   