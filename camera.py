import pygame

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.smoothness = 0.08

    # Camera follows the target, with smoothness
    def update(self, target):
        target_offset = pygame.Vector2(
            target.rect.centerx - self.width // 2,
            target.rect.centery - self.height // 2
        )

        self.offset += (target_offset - self.offset) * self.smoothness

    # Apply the camera offset to a rectangle
    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)