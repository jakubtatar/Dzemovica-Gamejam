import pygame
import time

class GUI:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        # fonty - Používame tvoj Upheavtt font
        self.font_path = r".\Resources\Fonts\upheavtt.ttf"
        self.font = pygame.font.Font(self.font_path, 30)
        self.quest_font = pygame.font.Font(self.font_path, 22)
        self.inv_font = pygame.font.Font(self.font_path, 16) # Malý font pre čísla v inventári
        self.start_time = time.time()

        # inventory - max_slots definuje flexibilitu
        self.inventory = ["Sword", "Shovel"]
        self.selected_index = 0
        self.max_slots = 9 

        # questy
        self.current_quest = {}

        self.shop_open = False
        self.shop_items = [
            {"name": "Health Potion", "price": 100, "type": "consumable", "desc": "+20 HP"},
            {"name": "Steel Shovel", "price": 150, "type": "upgrade", "desc": "Dig faster"},
            {"name": "Stamina Boots", "price": 400, "type": "upgrade", "desc": "+20% Speed"},
            {"name": "Money Bag", "price": 600, "type": "upgrade", "desc": "+10% Income"},
            {"name": "Shotgun", "price": 1500, "type": "weapon", "desc": "More damage"},
            {"name": "Holy hand grenade", "price": 1000, "type": "weapon", "desc": "Holy FU*K"},
        ]
        self.shop_selected_index = 0
            
    def draw_outlined_text(self, text, x, y, color, outline_color=(0, 0, 0), outline_width=2, anchor="topleft", font=None):
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
            # Klávesy 1-5 pre inventár
            if pygame.K_1 <= event.key <= pygame.K_5:
                # Nastavíme index bez ohľadu na to, či tam niečo je (aby hra nespadla)
                self.selected_index = event.key - pygame.K_1

    def get_selected_item(self):
        """Bezpečne vráti názov predmetu alebo None, ak je slot prázdny."""
        if 0 <= self.selected_index < len(self.inventory):
            return self.inventory[self.selected_index]
        return None # Vráti None namiesto chyby Index Out of Range

    def draw_health(self):
        health = getattr(self.player, "health", 100)
        self.draw_outlined_text(f"Health: {health}", 10, 10, (255, 50, 50))

    def draw_money(self):
        money = getattr(self.player, "money", 0)
        self.draw_outlined_text(f"Money: {money}", 10, 40, (255, 215, 0))

    def draw_day(self):
        day = getattr(self.player, "day", "Monday")
        self.draw_outlined_text(f"Day: {day}", 10, 70, (100, 255, 100))

    def draw_quest(self):
        if not self.current_quest: return
        screen_width = self.screen.get_width()
        padding = 15
        title_w, title_h = self.font.size(self.current_quest["title"])
        desc_w, desc_h = self.quest_font.size(self.current_quest["desc"])
        box_width = max(title_w, desc_w) + (padding * 2)
        box_height = title_h + desc_h + (padding * 2) + 5
        x, y = screen_width - box_width - 10, 10

        quest_bg = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        quest_bg.fill((0, 0, 0, 160)) 
        pygame.draw.rect(quest_bg, (255, 215, 0, 200), (0, 0, box_width, box_height), 2)
        self.screen.blit(quest_bg, (x, y))

        self.draw_outlined_text(self.current_quest["title"], x + padding, y + padding, (255, 215, 0), outline_width=1)
        self.draw_outlined_text(self.current_quest["desc"], x + padding, y + padding + title_h + 5, (255, 255, 255), font=self.quest_font, outline_width=1)

    def draw_inventory(self):
            # Konfigurácia
            slot_size = 55
            gap = 8
            
            # Výpočet celkovej šírky inventára pre vycentrovanie
            total_width = (self.max_slots * slot_size) + ((self.max_slots - 1) * gap)
            start_x = (self.screen.get_width() // 2) - (total_width // 2)
            start_y = self.screen.get_height() - slot_size - 25

            for i in range(self.max_slots):
                rect = pygame.Rect(start_x + i * (slot_size + gap), start_y, slot_size, slot_size)
                
                # Farba slotu (ešte tmavšia podľa tvojho priania)
                bg_color = (20, 20, 20, 220) 
                border_color = (80, 80, 80) # Menej výrazný okraj pre nevybrané
                
                if i == self.selected_index:
                    bg_color = (40, 45, 70, 240) # Mierne modrastá pre vybraný
                    border_color = (255, 215, 0) # Zlatá pre vybraný
                
                # Kreslenie pozadia slotu
                slot_surf = pygame.Surface((slot_size, slot_size), pygame.SRCALPHA)
                slot_surf.fill(bg_color)
                self.screen.blit(slot_surf, rect.topleft)
                
                # Kreslenie okraja
                border_width = 3 if i == self.selected_index else 1
                pygame.draw.rect(self.screen, border_color, rect, border_width)

                # Číslo slotu v ľavom hornom rohu (používame tvoj font)
                self.draw_outlined_text(str(i + 1), rect.x + 5, rect.y + 2, (150, 150, 150), font=self.inv_font, outline_width=1)

                # Predmety
                if i < len(self.inventory):
                    item_name = self.inventory[i]
                    # Skrátený názov, aby netrčal z políčka
                    display_name = item_name if len(item_name) < 7 else item_name[:5] + "."
                    self.draw_outlined_text(display_name, rect.centerx, rect.centery + 5, (255, 255, 255), 
                                            font=self.inv_font, anchor="center", outline_width=1)

    def draw_shop(self):
        if not self.shop_open: return
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        shop_rect = pygame.Rect(200, 100, 400, 400)
        pygame.draw.rect(self.screen, (30, 30, 30), shop_rect)
        pygame.draw.rect(self.screen, (255, 215, 0), shop_rect, 3)

        self.draw_outlined_text("ZABKAS STORE", 400, 130, (255, 215, 0), anchor="center")

        for i, item in enumerate(self.shop_items):
            color = (200, 200, 200)
            if i == self.shop_selected_index:
                color = (255, 255, 255)
                pygame.draw.rect(self.screen, (255, 215, 0), (210, 175 + i*45, 380, 40), 1)
                self.draw_outlined_text(">", 215, 182 + i*45, (255, 215, 0), font=self.quest_font)

            text = f"{item['name']}"
            price_text = f"{item['price']}g"
            self.draw_outlined_text(text, 240, 182 + i*45, color, font=self.quest_font)
            self.draw_outlined_text(price_text, 580, 182 + i*45, (255, 215, 0), font=self.quest_font, anchor="topright")
        
        self.draw_outlined_text("[E] Buy   [ESC] Exit", 400, 470, (150, 150, 150), anchor="center", font=self.quest_font)

    def draw(self):
        self.draw_health()
        self.draw_money()
        self.draw_day()
        self.draw_quest()
        self.draw_inventory()
        self.draw_shop()