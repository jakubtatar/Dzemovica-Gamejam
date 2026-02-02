import pygame
import time

class GUI:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        # font
        self.font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 30)
        self.start_time = time.time()

        # inventory
        self.inventory = ["[1] Sword", "[2] Shovel", "[3] Holy water", "[4] Cross"]
        self.selected_index = 0

    def draw_outlined_text(
        self,
        text,
        x,
        y,
        color,
        outline_color=(0, 0, 0),
        outline_width=2,
        anchor="topleft"
    ):
        text_surf = self.font.render(text, True, color)
        outline_surf = self.font.render(text, True, outline_color)

        rect = text_surf.get_rect()
        setattr(rect, anchor, (x, y))

        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    self.screen.blit(outline_surf, rect.move(dx, dy))

        self.screen.blit(text_surf, rect)

    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            # Priamy výber klávesmi 1 až 4
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
        self.draw_outlined_text(
            f"Health: {health}",
            10, 10,
            (255, 0, 0)
        )

    def draw_money(self):
        money = getattr(self.player, "money", 0)
        self.draw_outlined_text(
            f"Money: {money}",
            10, 40,
            (255, 215, 0)
        )
        
    def draw_day(self):
        # 1. Zoznam názvov dní
        dni = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        elapsed_seconds = int(time.time() - self.start_time)
        
        # Dlzka dna v sekundach
        sekundy_na_den = 480
        
        # Vyberani dna
        index_dna = (elapsed_seconds // sekundy_na_den) % len(dni)
        aktualny_nazov = dni[index_dna]

        # Vykreslenie na obrazovku
        self.draw_outlined_text(
            f"Day: {aktualny_nazov}",
            600, 40,
            (0, 255, 0)
        )

    def draw_time(self):
        # 1. Zistíme, koľko reálnych sekúnd ubehlo
        real_seconds = time.time() - self.start_time
        
        # 2. Prepočítame na herné minúty
        game_minutes_total = int(real_seconds * 3)
        
        # 3. Vypočítame hodiny a minúty pre formát 00:00
        hours = (game_minutes_total // 60) % 24
        minutes = game_minutes_total % 60
        
        time_str = f"{hours:02}:{minutes:02}"
        
        self.draw_outlined_text(
            f"Time: {time_str}",
            600, 10,
            (0, 0, 255)
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
        self.draw_inventory()
        self.draw_time()
