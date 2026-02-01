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
        self.inventory = ["Sword", "Shovel", "Holy water", "Cross"]
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
            if event.key == pygame.K_e:
                self.selected_index = (self.selected_index + 1) % len(self.inventory)
            elif event.key == pygame.K_q:
                self.selected_index = (self.selected_index - 1) % len(self.inventory)

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
        day = getattr(self.player, "day", 1)
        self.draw_outlined_text(
            f"Day: {day}",
            10, 70,
            (0, 255, 0)
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
