import pygame
import time

class GUI:

    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        # font
        self.font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 30)
        self.quest_font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 22) # Menší font pre popis
        self.start_time = time.time()

        # inventory
        self.inventory = ["[1] Sword", "[2] Shovel", "[3] Holy water", "[4] Cross"]
        self.selected_index = 0

        # questy - môžeš meniť počas hry
        self.current_quest = {
            "title": "Grave Digger",
            "desc": "Dig 3 graves before nightfall."
        }
    
    def draw_outlined_text(
        self,
        text,
        x,
        y,
        color,
        outline_color=(0, 0, 0),
        outline_width=2,
        anchor="topleft",
        font=None
    ):
        target_font = font if font else self.font
        text_surf = target_font.render(text, True, color)
        outline_surf = target_font.render(text, True, outline_color)

        rect = text_surf.get_rect()
        setattr(rect, anchor, (x, y))

        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    self.screen.blit(outline_surf, rect.move(dx, dy))

        self.screen.blit(text_surf, rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                self.selected_index = 0
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                self.selected_index = 1
            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                self.selected_index = 2
            elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                self.selected_index = 3

    def get_selected_item(self):
        return self.inventory[self.selected_index]

    def draw_health(self):
        health = getattr(self.player, "health", 100)
        self.draw_outlined_text(f"Health: {health}", 10, 10, (255, 0, 0))

    def draw_money(self):
        money = getattr(self.player, "money", 0)
        self.draw_outlined_text(f"Money: {money}", 10, 40, (255, 215, 0))

    def draw_day(self):
        day = getattr(self.player, "day", "Monday")
        self.draw_outlined_text(f"Day: {day}", 10, 70, (0, 255, 0))

    def draw_quest(self):
        if not self.current_quest:
            return

        screen_width = self.screen.get_width()
        padding = 15
        
        # 1. VÝPOČET POTREBNEJ ŠÍRKY
        # Zistíme, ktorý text je širší (nadpis vs popis)
        title_w, title_h = self.font.size(self.current_quest["title"])
        desc_w, desc_h = self.quest_font.size(self.current_quest["desc"])
        
        # Šírka okna bude maximálna šírka textu + padding z oboch strán
        box_width = max(title_w, desc_w) + (padding * 2)
        box_height = title_h + desc_h + (padding * 2) + 5 # +5 je medzera medzi riadkami

        # Pozícia (stále vpravo hore)
        x = screen_width - box_width - 10
        y = 10

        # 2. VYKRESLENIE POZADIA (Škálované)
        quest_bg = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        quest_bg.fill((0, 0, 0, 160)) 
        pygame.draw.rect(quest_bg, (255, 215, 0, 200), (0, 0, box_width, box_height), 2)
        self.screen.blit(quest_bg, (x, y))

        # 3. VYKRESLENIE TEXTU
        # Nadpis
        self.draw_outlined_text(
            self.current_quest["title"], 
            x + padding, y + padding, 
            (255, 215, 0), outline_width=1
        )

        # Popis (posunutý pod nadpis)
        self.draw_outlined_text(
            self.current_quest["desc"], 
            x + padding, y + padding + title_h + 5, 
            (255, 255, 255), 
            font=self.quest_font, outline_width=1
        )

    def draw_inventory(self):
        screen_width, screen_height = self.screen.get_size()
        padding = 10
        x = screen_width - padding
        y = screen_height - padding

        for i in reversed(range(len(self.inventory))):
            item = self.inventory[i]
            color = (255, 0, 0) if i == self.selected_index else (255, 255, 255)

            text_surf = self.font.render(item, True, color)
            outline_surf = self.font.render(item, True, (0, 0, 0))

            rect = text_surf.get_rect(bottomright=(x, y))

            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx != 0 or dy != 0:
                        self.screen.blit(outline_surf, rect.move(dx, dy))

            self.screen.blit(text_surf, rect)
            y -= rect.height + 5

    def draw(self):
        self.draw_health()
        self.draw_money()
        self.draw_day()
        self.draw_quest() # Pridané volanie kreslenia úlohy
        self.draw_inventory()