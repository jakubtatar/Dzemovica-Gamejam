import pygame
import random

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.smoothness = 0.08
        self.shake_amount = 0

    def shake(self, intensity):
        self.shake_amount = intensity

    # TÁTO METÓDA TI CHÝBALA ALEBO SI JU VYMAZAL
    def apply(self, rect):
        """Vráti nový obdĺžnik posunutý o offset kamery."""
        return rect.move(-self.offset.x, -self.offset.y)

    def update(self, target):
        # Cieľový bod, kam sa má kamera centrovať
        target_offset = pygame.Vector2(
            target.rect.centerx - self.width // 2,
            target.rect.centery - self.height // 2
        )

        # Plynulý pohyb (lerp)
        self.offset += (target_offset - self.offset) * self.smoothness

        # Pridanie trasenia (screenshake)
        if self.shake_amount > 0:
            self.offset.x += random.randint(-self.shake_amount, self.shake_amount)
            self.offset.y += random.randint(-self.shake_amount, self.shake_amount)
            self.shake_amount -= 1