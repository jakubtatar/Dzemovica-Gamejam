import pygame
import random
import math

class GhostEnemy:
    def __init__(self, x, y, image):
        self.image = image.copy() # Kópia obrázka kvôli úprave priehľadnosti (fade efekt)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)
        
        # Štatistiky
        self.max_health = 30
        self.health = self.max_health
        self.speed = random.uniform(1.2, 1.8) # Mierna náhodnosť, aby nechodili všetci rovnako
        self.damage = 10
        
        # Fyzika (vektorový knockback)
        self.knockback = pygame.math.Vector2(0, 0)
        self.knockback_resistance = 0.85
        
        # Vizuál: Vznášanie (Bobbing)
        self.bob_offset = random.uniform(0, 100) # Každý duch sa vznáša inak
        self.bob_speed = 0.005
        self.bob_height = 8
        
        # Stavy nepriateľa
        self.is_dead = False
        self.alpha = 0
        self.image.set_alpha(self.alpha) # Priehľadný pri spawne
        self.state = "SPAWNING"
        
    def take_damage(self, amount, knockback_force):
        if self.state == "DYING": return
        self.health -= amount
        self.knockback = knockback_force
        if self.health <= 0:
            self.state = "DYING"
            
    def update(self, player):
        # 1. Fade-In pri objavení
        if self.state == "SPAWNING":
            self.alpha += 5
            if self.alpha >= 255:
                self.alpha = 255
                self.state = "CHASING"
            self.image.set_alpha(self.alpha)
            return

        # 2. Fade-Out pri smrti
        if self.state == "DYING":
            self.alpha -= 10
            if self.alpha <= 0:
                self.is_dead = True
            self.image.set_alpha(max(0, self.alpha))
            return

        # 3. Chasing (Plynulý 8-smerný pohyb pomocou vektorov)
        target = pygame.math.Vector2(player.rect.center)
        direction = target - self.pos
        
        if direction.length() > 0:
            direction = direction.normalize() # Normalizácia = rovnaká rýchlosť aj diagonálne
        
        # 4. Aplikácia rýchlosti a knockbacku
        self.pos += direction * self.speed + self.knockback
        self.knockback *= self.knockback_resistance # Postupné brzdenie odhodenia
        
        if self.knockback.length() < 0.5:
            self.knockback = pygame.math.Vector2(0, 0)
            
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

    def draw(self, screen, camera):
        # Animácia vznášania nahor a nadol (cez sínusoidu)
        current_time = pygame.time.get_ticks()
        bob = math.sin(current_time * self.bob_speed + self.bob_offset) * self.bob_height
        
        draw_pos = camera.apply(self.rect).move(0, bob)
        screen.blit(self.image, draw_pos)
        
        # Kreslenie healthbaru (len keď je zranený a žije)
        if self.health < self.max_health and self.state != "DYING":
            bar_width = 40
            bar_height = 6
            health_ratio = max(0, self.health / self.max_health)
            
            bar_x = draw_pos.centerx - bar_width // 2
            bar_y = draw_pos.y - 10
            
            pygame.draw.rect(screen, (150, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

    @classmethod
    def spawn_horde(cls, player, game_data, ghost_img, count=5):
        if game_data["current_map"] == "cmitermap":
            for _ in range(count):
                dist_x = random.randint(300, 600) * random.choice([-1, 1])
                dist_y = random.randint(300, 600) * random.choice([-1, 1])
                new_ghost = cls(player.rect.x + dist_x, player.rect.y + dist_y, ghost_img)
                game_data["enemies"].append(new_ghost)