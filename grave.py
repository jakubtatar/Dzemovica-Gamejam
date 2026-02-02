import pygame
import random

class Grave:
    def __init__(self, x, y, size, gravestone_images):
        # náhodný typ hrobu (1–6)
        self.type = str(random.randint(1, 6))

        width = size
        height = size

        # AK JE Gravestone_6 → dvojnásobná výška
        if self.type == "6":
            height = size * 2
            y -= size  # posun hore, aby spodok ostal na zemi

        self.rect = pygame.Rect(x, y, width, height)

        # obrázok podľa typu
        self.image = gravestone_images[self.type]
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
