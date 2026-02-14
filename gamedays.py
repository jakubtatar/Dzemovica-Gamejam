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

        elif self.quest_step == 2:
            total_graves = len(self.game_data.get("graves", []))
            target = 3
            if total_graves >= target: 
                self.quest_step = 3
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.")
            else:
                # Dynamic description with countdown
                remaining = target - total_graves
                self.update_gui_quest("More digging", f"Complete the quota. ({remaining} graves left to dig)")
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
        self.game_data["priest_contacted"] = False
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
                    "BARMAN: You survived! I heard some screaming from the hill.",
                    "BARMAN: Here is your pay for the first day.",
                    "BARMAN: Keep this up and you might even afford a better shovel."
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
                        self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig 6 more graves.")

        #5. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 4:
            total_graves = len(self.game_data.get("graves", []))
            target = 9
            if total_graves >= target: 
                self.quest_step = 5
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 
            else:
                remaining = target - total_graves
                self.update_gui_quest("GO TO WORK", f"Dig more graves. ({remaining} left)")
        # 6. ROZHOVOR S KŇAZOM
        elif self.quest_step == 5:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "PRIEST: I see you've been working hard, Hugo.",
                    "YOU: Had a hard time fighting them, why didn't you tell me!.",
                    "PRIEST: The souls are stronger. They no longer just crawl on the ground… they are learning..",
                    "YOU: Learning what?",
                    "PRIEST: To hate. To remember. To touch the living.",
                    "YOU: Then a sword won't be enough.",
                    "PRIEST: It won't. You need protection, not a weapon. Something to keep you between them and us.",
                    "YOU: Protection wears down over time.",
                    "PRIEST: That is why it must be renewed. And why you must pay a price for it.",
                    "YOU: Fear?",
                    "PRIEST: Faith. Or what’s left of yours.",
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
        self.intro_screen()
        
        # RESET DÁT, aby streda nezačínala s hotovými questami z utorka
        self.game_data["salary_received"] = False
        self.game_data["priest_contacted"] = False
        self.game_data["night_finished"] = False
        self.game_data["night_mode"] = False
        
        self.update_gui_quest("Morning After", "Check the cemetery for any 'leftovers'.")
        
        setup_map_func("house")
        self.player.rect.topleft = (150, 250)
        self.game_data["gameday"] = 3 
        self.player.day = "Wednesday"
        self.quest_step = 0
        self.day_finished = False

    def update_quests(self):
        if self.day_finished:
            return

        npc = self.game_data.get("npc")
        current_map = self.game_data.get("current_map")
        is_talking = self.game_data.get("dialogue_active", False)
        enemies = self.game_data.get("enemies", [])

        # 1. VYČISTENIE CINTORÍNA
        if self.quest_step == 0:
            if current_map == "house":
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
                    "BARMAN: Welcome back hugo, here is your payment for today",
                    "BARMAN: And don't forget to drink this... *puts beer on counter*",
                    "YOU: *drinks bear*"
                ])
                if is_talking:
                    self.game_data["salary_received"] = True
                
                if not is_talking and self.game_data.get("salary_received"):
                    self.player.money += 200
                    self.quest_step = 3
                    self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig more graves.")

        #5. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 3:
            total_graves = len(self.game_data.get("graves", []))
            target = 16
            if total_graves >= target: 
                self.quest_step = 4
                self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 
            else:
                remaining = target - total_graves
                self.update_gui_quest("GO TO WORK", f"Dig more graves. ({remaining} left)")
                
        # 6. ROZHOVOR S KŇAZOM
        elif self.quest_step == 4:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "YOU: Father, I had a bad dream.",
                    "PRIEST: Hugo here you are!",
                    "YOU: Father, I was dreaming about fighting ghosts in some weird cemetery.",
                    "PRIEST: No Hugo. you had an accident last night...",
                    "PRIEST: But you are the only one who can protect us.",
                    "PRIEST: Take this, it will help in the night. *gives Holy water*"
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 5
                    self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

        # 7. PREŽITIE NOCI
        elif self.quest_step == 5:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 6
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
        self.intro_screen()
        
        # RESET DÁT, aby streda nezačínala s hotovými questami z utorka
        self.game_data["salary_received"] = False
        self.game_data["priest_contacted"] = False
        self.game_data["night_finished"] = False
        self.game_data["night_mode"] = False
        
        self.update_gui_quest("Morning After", "Check the cemetery for any 'leftovers'.")
        
        setup_map_func("cmitermap")
        self.player.rect.topleft = (2700, 150)
        self.game_data["gameday"] = 3 
        self.player.day = "Thursday"
        self.quest_step = 0
        self.day_finished = False

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
                    "BARMAN: Hello Hugo...",
                    "YOU: Who is Melitele?",
                    "BARMAN: ...I...I...don't know...",
                    "BARMAN: ...maybe you should ask local priest...",
                    "BARMAN: ...But anyway...",
                    "BARMAN: Here is your money and beer.",
                    "YOU: *drinks beer*",
                ])
                if is_talking:
                    self.game_data["salary_received"] = True
                
                if not is_talking and self.game_data.get("salary_received"):
                    self.player.money += 200
                    self.quest_step = 3
                    self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.")

        elif self.quest_step == 3:
            if npc and getattr(npc, 'name', '') == "Priest":
                npc.set_dialogue([
                    "PRIEST: How are you Hugo?",
                    "YOU: Who is Melitele?",
                    "PRIEST: Some stay in the same place. Waiting for someone to look back.",
                    "PRIEST: Melitele is a place between earth and heaven.",
                    "YOU: So it is place where are ghosts?",
                    "PRIEST: Not exactly, their souls... are different...",
                    "YOU: ???",
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 4
                    self.update_gui_quest("Go to work", "Go back to cemetery and dig graves.")


        #5. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 4:
            total_graves = len(self.game_data.get("graves", []))
            target = 26
            if total_graves >= target: 
                self.quest_step = 5
                self.update_gui_quest("Night shift", "Go to cemetery and survive.") 
            else:
                remaining = target - total_graves
                self.update_gui_quest("GO TO WORK", f"Dig more graves. ({remaining} left)")

        # 7. PREŽITIE NOCI
        elif self.quest_step == 5:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 6
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
        self.intro_screen()
        
        # RESET DÁT, aby streda nezačínala s hotovými questami z utorka
        self.game_data["salary_received"] = False
        self.game_data["priest_contacted"] = False
        self.game_data["night_finished"] = False
        self.game_data["night_mode"] = False
        
        self.update_gui_quest("Morning After", "Check the cemetery for any 'leftovers'.")
        
        setup_map_func("cmitermap")
        self.player.rect.topleft = (2700, 150)
        self.game_data["gameday"] = 3 
        self.player.day = "Friday"
        self.quest_step = 0
        self.day_finished = False

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
                    "BARMAN: Here is your payment... *puts beer on counter*",
                    "YOU: *drinks beer*"
                ])
                if is_talking:
                    self.game_data["salary_received"] = True
                
                if not is_talking and self.game_data.get("salary_received"):
                    self.player.money += 200
                    self.quest_step = 3
                    self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig more graves.")

        # 2. CESTA DO LESA
        elif self.quest_step == 3:
            if current_map == "crossroad":
                self.quest_step = 4
                self.update_gui_quest("???", "Find and talk to her in forest...")

        elif self.quest_step == 4:
            if current_map == "forest":
                self.quest_step = 5

        # 6. ROZHOVOR S MELITELE
        elif self.quest_step == 5:
            if npc and getattr(npc, 'name', '') == "Melitele":
                npc.set_dialogue([
                    "???: I waited for you Hugo.",
                    "YOU: How do you know my name strange creature?",
                    "???: I know everything.",
                    "YOU: Who are you?",
                    "???: You can call me Melitele, Hugo.",
                    "YOU: Are you death?",
                    "Melitele: No.",
                    "YOU: So who are you then?",
                    "Melitele: Spirit guide.",
                    "YOU: You guide the spirits of dead?",
                    "Melitele: Exactly.",
                    "Melitele: But there is something else why are you there.",
                    "Melitele: You should quit that job and let me guide the spirits.",
                    "YOU: But they are spirits of evil! If I quit they will harm innocents!",
                    "Melitele: I don't give you choice.",
                    "Melitele: Leave or you will join my spirits...",
                    "Melitele: Choose with precision, Hugo.",
                ])
                if is_talking:
                    self.game_data["priest_contacted"] = True
                
                if not is_talking and self.game_data.get("priest_contacted"):
                    self.quest_step = 6
                    self.update_gui_quest("GO TO WORK", "Dig more graves")

        #6. KOPANIE ĎALŠÍCH HROBOV
        elif self.quest_step == 6:
            total_graves = len(self.game_data.get("graves", []))
            target = 38
            if total_graves >= target: 
                self.quest_step = 7
                self.update_gui_quest("PREPARE", "Go to shop and prepare for Melitele.") 
            else:
                remaining = target - total_graves
                self.update_gui_quest("GO TO WORK", f"Dig more graves. ({remaining} left)")

        # 7. Navsteva obchodu
        elif self.quest_step == 7:
            if current_map == "store":
                if npc and getattr(npc, 'name', '') == "Shopkeeper":
                    npc.set_dialogue([
                        "Welcome to Zabkas Hugo!",
                    ])
                    self.quest_step = 8
                    self.update_gui_quest("FINAL FIGHT", "Go to the cemetery and survive night.") 

        # 8. PREŽITIE NOCI A BOSSFIGHT
        elif self.quest_step == 8:
            if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
                self.quest_step = 9
                self.update_gui_quest("Day Finished", "Friday is over. Rest now.")
                self.next_day_transition()

# class Saturday:
#     def __init__(self, screen, player, gui, game_data):
#         self.screen = screen
#         self.player = player
#         self.gui = gui
#         self.game_data = game_data
#         self.quest_step = 0
#         self.day_finished = False
#         self.quests = []

#     def intro_screen(self):
#         try:
#             intro_font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 100)
#         except:
#             intro_font = pygame.font.SysFont("Arial", 100)

#         text_surf = intro_font.render("Saturday", True, (255, 255, 255))
#         text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
#         self.screen.fill((0, 0, 0))
#         self.screen.blit(text_surf, text_rect)
#         pygame.display.flip()
#         time.sleep(2)

#     def update_gui_quest(self, title, desc):
#         self.gui.current_quest = {"title": title, "desc": desc}

#     def start(self, setup_map_func):
#         self.intro_screen()
        
#         # RESET DÁT, aby streda nezačínala s hotovými questami z utorka
#         self.game_data["salary_received"] = False
#         self.game_data["priest_contacted"] = False
#         self.game_data["night_finished"] = False
#         self.game_data["night_mode"] = False
        
#         self.update_gui_quest("Morning After", "Check the cemetery for any 'leftovers'.")
        
#         setup_map_func("cmitermap")
#         self.player.rect.topleft = (2700, 150)
#         self.game_data["gameday"] = 3 
#         self.player.day = "Saturday"
#         self.quest_step = 0
#         self.day_finished = False

#     def update_quests(self):
#         if self.day_finished:
#             return

#         npc = self.game_data.get("npc")
#         current_map = self.game_data.get("current_map")
#         is_talking = self.game_data.get("dialogue_active", False)
#         enemies = self.game_data.get("enemies", [])

#         # 1. VYČISTENIE CINTORÍNA
#         if self.quest_step == 0:
#             if current_map == "cmitermap":
#                 if len(enemies) == 0:
#                     self.quest_step = 1
#                     self.update_gui_quest("Payday", "Go to the Tavern and ask the Barman for your coins.")
#                 else:
#                     self.update_gui_quest("Clean Up", f"Exorcise the remaining spirits ({len(enemies)} left).")

#         # 2. CESTA DO TAVERNY
#         elif self.quest_step == 1:
#             if current_map == "taverna":
#                 self.quest_step = 2

#         # 3. ROZHOVOR S BARMANOM
#         elif self.quest_step == 2:
#             if npc and getattr(npc, 'name', '') == "Barman":
#                 npc.set_dialogue([
#                     "You survived! I heard some screaming from the hill.",
#                     "Here is your pay for the first two days.",
#                     "Keep this up and you might even afford a better shovel."
#                 ])
#                 if is_talking:
#                     self.game_data["salary_received"] = True
                
#                 if not is_talking and self.game_data.get("salary_received"):
#                     self.player.money += 200
#                     self.quest_step = 3
#                     self.update_gui_quest("Explore", "Visit the local village store.")

#         # 4. Navsteva obchodu
#         elif self.quest_step == 3:
#             if current_map == "store":
#                 if npc and getattr(npc, 'name', '') == "Shopkeeper":
#                     npc.set_dialogue([
#                         "Welcome to Zabkas Hugo!",
#                     ])
#                     if not is_talking and self.game_data.get("salary_received"):
#                         self.player.money += 200
#                         self.quest_step = 4
#                         self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig more graves.")

#         #5. KOPANIE ĎALŠÍCH HROBOV
#         elif self.quest_step == 4:
#             total_graves = len(self.game_data.get("graves", []))
#             target = 42
#             if total_graves >= target: 
#                 self.quest_step = 5
#                 self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 
#             else:
#                 remaining = target - total_graves
#                 self.update_gui_quest("GO TO WORK", f"Dig more graves. ({remaining} left)")

#         # 6. ROZHOVOR S KŇAZOM
#         elif self.quest_step == 5:
#             if npc and getattr(npc, 'name', '') == "Priest":
#                 npc.set_dialogue([
#                     "PRIEST: I see you've started your work, Hugo.",
#                     "PRIEST: But the night is coming, and the dead are restless.",
#                     "PRIEST: You must survive the night shift. Good luck.",
#                     "PRIEST: Fate of the village is in your hands, protect us..."
#                 ])
#                 if is_talking:
#                     self.game_data["priest_contacted"] = True
                
#                 if not is_talking and self.game_data.get("priest_contacted"):
#                     self.quest_step = 6
#                     self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

#         # 7. PREŽITIE NOCI
#         elif self.quest_step == 6:
#             if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
#                 self.quest_step = 7
#                 self.update_gui_quest("Day Finished", "Saturday is over. Rest now.")
#                 self.next_day_transition()

# class Sunday:
#     def __init__(self, screen, player, gui, game_data):
#         self.screen = screen
#         self.player = player
#         self.gui = gui
#         self.game_data = game_data
#         self.quest_step = 0
#         self.day_finished = False
#         self.quests = []

#     def intro_screen(self):
#         try:
#             intro_font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 100)
#         except:
#             intro_font = pygame.font.SysFont("Arial", 100)

#         text_surf = intro_font.render("Sunday", True, (255, 255, 255))
#         text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
#         self.screen.fill((0, 0, 0))
#         self.screen.blit(text_surf, text_rect)
#         pygame.display.flip()
#         time.sleep(2)

#     def update_gui_quest(self, title, desc):
#         self.gui.current_quest = {"title": title, "desc": desc}

#     def start(self, setup_map_func):
#         self.intro_screen()
        
#         # RESET DÁT, aby streda nezačínala s hotovými questami z utorka
#         self.game_data["salary_received"] = False
#         self.game_data["priest_contacted"] = False
#         self.game_data["night_finished"] = False
#         self.game_data["night_mode"] = False
        
#         self.update_gui_quest("Morning After", "Check the cemetery for any 'leftovers'.")
        
#         setup_map_func("cmitermap")
#         self.player.rect.topleft = (2700, 150)
#         self.game_data["gameday"] = 3 
#         self.player.day = "Sunday"
#         self.quest_step = 0
#         self.day_finished = False

#     def update_quests(self):
#         if self.day_finished:
#             return

#         npc = self.game_data.get("npc")
#         current_map = self.game_data.get("current_map")
#         is_talking = self.game_data.get("dialogue_active", False)
#         enemies = self.game_data.get("enemies", [])

#         # 1. VYČISTENIE CINTORÍNA
#         if self.quest_step == 0:
#             if current_map == "cmitermap":
#                 if len(enemies) == 0:
#                     self.quest_step = 1
#                     self.update_gui_quest("Payday", "Go to the Tavern and ask the Barman for your coins.")
#                 else:
#                     self.update_gui_quest("Clean Up", f"Exorcise the remaining spirits ({len(enemies)} left).")

#         # 2. CESTA DO TAVERNY
#         elif self.quest_step == 1:
#             if current_map == "taverna":
#                 self.quest_step = 2

#         # 3. ROZHOVOR S BARMANOM
#         elif self.quest_step == 2:
#             if npc and getattr(npc, 'name', '') == "Barman":
#                 npc.set_dialogue([
#                     "You survived! I heard some screaming from the hill.",
#                     "Here is your pay for the first two days.",
#                     "Keep this up and you might even afford a better shovel."
#                 ])
#                 if is_talking:
#                     self.game_data["salary_received"] = True
                
#                 if not is_talking and self.game_data.get("salary_received"):
#                     self.player.money += 200
#                     self.quest_step = 3
#                     self.update_gui_quest("Explore", "Visit the local village store.")

#         # 4. Navsteva obchodu
#         elif self.quest_step == 3:
#             if current_map == "store":
#                 if npc and getattr(npc, 'name', '') == "Shopkeeper":
#                     npc.set_dialogue([
#                         "Welcome to Zabkas Hugo!",
#                     ])
#                     if not is_talking and self.game_data.get("salary_received"):
#                         self.player.money += 200
#                         self.quest_step = 4
#                         self.update_gui_quest("GO TO WORK", "Go back to the cemetery and dig more graves.")

#         #5. KOPANIE ĎALŠÍCH HROBOV
#         elif self.quest_step == 4:
#             total_graves = len(self.game_data.get("graves", []))
#             target = 58
#             if total_graves >= target: 
#                 self.quest_step = 5
#                 self.update_gui_quest("Village Priest", "Go back to the village and talk to the Priest.") 
#             else:
#                 remaining = target - total_graves
#                 self.update_gui_quest("GO TO WORK", f"Dig more graves. ({remaining} left)")

#         # 6. ROZHOVOR S KŇAZOM
#         elif self.quest_step == 5:
#             if npc and getattr(npc, 'name', '') == "Priest":
#                 npc.set_dialogue([
#                     "PRIEST: I see you've started your work, Hugo.",
#                     "PRIEST: But the night is coming, and the dead are restless.",
#                     "PRIEST: You must survive the night shift. Good luck.",
#                     "PRIEST: Fate of the village is in your hands, protect us..."
#                 ])
#                 if is_talking:
#                     self.game_data["priest_contacted"] = True
                
#                 if not is_talking and self.game_data.get("priest_contacted"):
#                     self.quest_step = 6
#                     self.update_gui_quest("Night Shift", "Go to the cemetery and survive (Right click).")

#         # 7. PREŽITIE NOCI
#         elif self.quest_step == 6:
#             if self.game_data.get("night_mode") == False and self.game_data.get("night_finished") == True:
#                 self.quest_step = 7
#                 self.update_gui_quest("Day Finished", "Sunday is over. Rest now.")
#                 self.next_day_transition()