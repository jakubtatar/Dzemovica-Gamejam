import pygame

class NPC:
    def __init__(self, x, y, width, height, world_img_path, dialogue_lines, portrait_img):
        self.rect = pygame.Rect(x, y, width, height)
        self.dialogue_lines = dialogue_lines
        self.portrait = portrait_img  # Tu si uložíme ten veľký obrázok pre dialóg

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))

    def set_dialogue(self, new_lines):
        self.dialogue_lines = new_lines
