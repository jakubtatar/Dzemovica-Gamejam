import pygame
import math

class Grenade:
    def __init__(self, start_pos, target_pos):
        self.rect = pygame.Rect(start_pos[0], start_pos[1], 15, 15)
        self.color = (50, 100, 50) # Tmavozelená
        
        # Výpočet smeru k myši
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        
        self.speed = 7
        self.velocity_x = (dx / distance) * self.speed
        self.velocity_y = (dy / distance) * self.speed
        
        self.timer = 60  # Granát vybuchne po 60 framoch (cca 1 sekunda)
        self.explosion_radius = 250
        self.exploded = False

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.timer -= 1
        if self.timer <= 0:
            self.exploded = True

    def draw(self, screen, camera):
        pygame.draw.circle(screen, self.color, camera.apply(self.rect).center, 8)

class Explosion:
    def __init__(self, x, y, max_radius):
        self.x = x
        self.y = y
        self.radius = 10
        self.max_radius = max_radius
        self.alpha = 255  # Priehľadnosť
        self.finished = False

    def update(self):
        self.radius += 8  # Rýchlosť rozširovania
        self.alpha -= 10  # Postupné miznutie
        if self.radius >= self.max_radius or self.alpha <= 0:
            self.finished = True

    def draw(self, screen, camera):
        # Vytvoríme pomocný povrch pre priehľadný kruh
        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        # Nakreslíme oranžovo-žltý kruh s nastavenou priehľadnosťou
        pygame.draw.circle(s, (255, 150, 50, self.alpha), (self.radius, self.radius), self.radius)
        
        # Určíme pozíciu na obrazovke pomocou kamery
        screen_pos = camera.apply(pygame.Rect(self.x - self.radius, self.y - self.radius, 0, 0))
        screen.blit(s, screen_pos.topleft)