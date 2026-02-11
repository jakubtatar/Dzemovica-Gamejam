import pygame

class Dialogue:
    def __init__(self, font, text, typeSpeed=30):
        self.font = font
        self.text = text
        self.typeSpeed = typeSpeed
        self.current_index = 0
        self.displayed_text = ""
        self.done = False

    def update(self, dt):
        if not self.done:
            self.current_index += dt // self.typeSpeed
            if self.current_index >= len(self.text):
                self.current_index = len(self.text)
                self.done = True
            self.displayed_text = self.text[:int(self.current_index)]

    def draw(self, screen, x, y, color=(255,255,255)):
        text_surf = self.font.render(self.displayed_text, True, color)
        screen.blit(text_surf, (x, y))

    def reset(self, new_text):
        self.text = new_text
        self.current_index = 0
        self.displayed_text = ""
        self.done = False