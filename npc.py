import pygame

class NPC:
    def __init__(self, x, y, width, height, image_path, dialogue_lines):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.dialogue_lines = dialogue_lines

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
