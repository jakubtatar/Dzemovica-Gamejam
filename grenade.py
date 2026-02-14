import pygame
import random
import math
import os

pygame.mixer.init()

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

class SmokeParticle:
    def __init__(self, x, y):
        self.x = x + random.uniform(-10, 10)
        self.y = y + random.uniform(-10, 10)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.2, -1.0)
        self.radius = random.uniform(10, 20)
        self.alpha = 180
        gray = random.randint(100, 180)
        self.color = (gray, gray, gray)
        self.fade_speed = random.uniform(0.5, 1.2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.radius += 0.2
        self.alpha -= self.fade_speed
        if self.alpha < 0: self.alpha = 0

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(4, 10)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.radius = random.randint(2, 4)
        self.alpha = 255
        self.color = (255, 200, 50)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha -= 8
        if self.radius > 0.5: self.radius *= 0.95

class Explosion:
    # Statická premenná pre zvuk, aby sme ho nenačítavali z disku pri každom jednom výbuchu
    # (šetrí to výkon aj pamäť)
    _sound = None

    def __init__(self, x, y, max_radius=60):
        self.x = x
        self.y = y
        
        # 1. ZVUKOVÝ EFEKT
        if Explosion._sound is None:
            # Cesta podľa tvojej štruktúry: Resources -> Music -> Explosion.mp3
            path = os.path.join("Resources", "Music", "Explosion.mp3")
            try:
                Explosion._sound = pygame.mixer.Sound(path)
                Explosion._sound.set_volume(0.5)
            except Exception as e:
                print(f"Nepodarilo sa načítať zvuk: {e}")

        if Explosion._sound:
            Explosion._sound.play()

        # 2. VIZUÁLNE PRVKY
        self.circle_radius = 10
        self.max_radius = max_radius
        self.circle_alpha = 255
        self.particles = [Particle(x, y) for _ in range(20)]
        self.smoke_particles = [SmokeParticle(x, y) for _ in range(12)]
        self.finished = False

    def update(self):
        if self.circle_alpha > 0:
            self.circle_radius += 7
            self.circle_alpha -= 12
        
        for p in self.particles: p.update()
        self.particles = [p for p in self.particles if p.alpha > 0]

        for s in self.smoke_particles: s.update()
        self.smoke_particles = [s for s in self.smoke_particles if s.alpha > 0]

        if self.circle_alpha <= 0 and not self.particles and not self.smoke_particles:
            self.finished = True

    def draw(self, screen, camera):
        # Kreslenie dymu
        for s in self.smoke_particles:
            temp_surface = pygame.Surface((int(s.radius * 2), int(s.radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*s.color, int(s.alpha)), (int(s.radius), int(s.radius)), int(s.radius))
            screen_pos = camera.apply(pygame.Rect(s.x - s.radius, s.y - s.radius, 0, 0))
            screen.blit(temp_surface, screen_pos.topleft)

        # Kreslenie rázovej vlny
        if self.circle_alpha > 0:
            wave_surf = pygame.Surface((int(self.circle_radius * 2), int(self.circle_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(wave_surf, (255, 150, 50, self.circle_alpha), 
                               (int(self.circle_radius), int(self.circle_radius)), int(self.circle_radius), 4)
            screen_pos = camera.apply(pygame.Rect(self.x - self.circle_radius, self.y - self.circle_radius, 0, 0))
            screen.blit(wave_surf, screen_pos.topleft)

        # Kreslenie iskier
        for p in self.particles:
            p_surf = pygame.Surface((int(p.radius * 2), int(p.radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*p.color, p.alpha), (int(p.radius), int(p.radius)), int(p.radius))
            screen_pos = camera.apply(pygame.Rect(p.x - p.radius, p.y - p.radius, 0, 0))
            screen.blit(p_surf, screen_pos.topleft)