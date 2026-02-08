import pygame

class Quest:
    def __init__(self, name, description, is_completed=False):
        self.name = name
        self.description = description
        self.is_completed = is_completed
    
    def complete(self):
        self.is_completed = True

    def display(self, screen, x, y):
        font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 24)
        name_surf = font.render(self.name, True, (255, 255, 255))
        desc_surf = font.render(self.description, True, (255, 255, 255))
        screen.blit(name_surf, (x, y))
        screen.blit(desc_surf, (x, y + 30))