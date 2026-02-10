import pygame
import random

class Grave:
    def __init__(self, x, y, tile_size, images):
        
        # self.rect sluzi na logicku poziciu (miesto v gride)
        self.rect = pygame.Rect(x, y, tile_size, tile_size)
        self.images = images

        # Vyberie nahodny obrazok a ulozi si ho
        self.type = random.choice(list(images.keys()))
        self.image = images[self.type]

    def draw(self, screen, camera):
        draw_x = camera.apply(self.rect).x
        draw_y = camera.apply(self.rect).y + self.rect.height - self.image.get_height()
        
        screen.blit(self.image, (draw_x, draw_y))
