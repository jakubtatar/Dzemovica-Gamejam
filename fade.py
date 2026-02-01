import pygame

class Fade:
    def __init__(self, screen, speed=5):
        self.screen = screen
        self.speed = speed

        self.overlay = pygame.Surface(screen.get_size())
        self.overlay.fill((0, 0, 0))

        self.alpha = 0
        self.active = False
        self.mode = None  # "in" alebo "out"

    def fade_in(self):
        self.alpha = 255
        self.mode = "in"
        self.active = True

    def fade_out(self):
        self.alpha = 0
        self.mode = "out"
        self.active = True

    def update(self):
        if not self.active:
            return False

        if self.mode == "in":
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.alpha = 0
                self.active = False

        elif self.mode == "out":
            self.alpha += self.speed
            if self.alpha >= 255:
                self.alpha = 255
                self.active = False

        return True

    def draw(self):
        if self.active:
            self.overlay.set_alpha(self.alpha)
            self.screen.blit(self.overlay, (0, 0))
