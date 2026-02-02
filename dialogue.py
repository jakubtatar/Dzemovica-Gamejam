import pygame

class Dialogue:
    def __init__(self, text, typeSpeed, typeSound=None):
        self.font = pygame.font.Font(r".\Resources\Fonts\upheavtt.ttf", 24)
        self.text = text 
        self.typeSpeed = typeSpeed
        self.typeSound = typeSound
    
    def typeText(self, screen, x, y):
        displayed_text = ""
        for i in range(len(self.text)):
            displayed_text += self.text[i]
            text_surf = self.font.render(displayed_text, True, (255, 255, 255))
            screen.blit(text_surf, (x, y))
            pygame.display.flip()
            pygame.time.delay(self.typeSpeed)