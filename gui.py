import pygame
import time

class GUI:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        # font
        self.font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 30)
        self.start_time = time.time()

        # inventár príklad
        self.inventory = ["Sword", "Shovel", "Holy water", "Cross"]
        self.selected_index = 0  # aktívny item

    def handle_input(self, event):
        # zmeniť aktívny item šípkami
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.selected_index = (self.selected_index + 1) % len(self.inventory)
            elif event.key == pygame.K_q:
                self.selected_index = (self.selected_index - 1) % len(self.inventory)

    def draw_health(self):
        health = getattr(self.player, "health", 100)
        health_text = self.font.render(f"Health: {health}", True, (255, 0, 0))
        self.screen.blit(health_text, (10, 10))

    def draw_time(self):
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        time_text = self.font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 0))
        self.screen.blit(time_text, (10, 50))

    def draw_inventory(self):
        # pozícia inventáru v pravom dolnom rohu
        screen_width, screen_height = self.screen.get_size()
        padding = 10
        x = screen_width - padding
        y = screen_height - padding

        # vykreslenie každého itemu sprava doľava
        for i in reversed(range(len(self.inventory))):
            item = self.inventory[i]
            color = (255, 0, 0) if i == self.selected_index else (255, 255, 255)
            item_surface = self.font.render(item, True, color)
            rect = item_surface.get_rect(bottomright=(x, y))
            self.screen.blit(item_surface, rect)
            # posun pre ďalší item
            y -= rect.height + 5

    def draw(self):
        self.draw_health()
        self.draw_time()
        self.draw_inventory()
