import pygame
import random
import math

class GhostEnemy:
    def __init__(self, x, y, image):
        self.original_image = image.copy()
        self.image = self.original_image.copy()
        
        self.glow_surf_normal = image.copy()
        self.glow_surf_normal.fill((0, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        self.glow_surf_enraged = image.copy()
        self.glow_surf_enraged.fill((255, 100, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery + 40)
        
        self.max_health = 60 
        self.health = self.max_health
        self.base_speed = random.uniform(1.3, 1.8)
        self.speed = self.base_speed
        self.damage = 10
        self.is_enraged = False
        
        self.knockback = pygame.math.Vector2(0, 0)
        self.knockback_resistance = 0.85
        self.state = "SPAWNING"
        self.is_dead = False
        
        self.dash_cooldown = random.randint(150, 300)
        self.dash_dir = pygame.math.Vector2(0, 0)
        self.state_timer = 0
        self.flank_direction = random.choice([-1, 1]) 
        
        self.bob_offset = random.uniform(0, 100)
        self.bob_speed = 0.005
        self.bob_height = 8
        self.alpha = 0
        self.shake_offset = pygame.math.Vector2(0, 0)
        self.ethereal_offset = random.uniform(0, math.pi * 2)
        self.death_scale = 1.0
        
        self.particles = []
        self.history = [] 
        self.look_dir = pygame.math.Vector2(0, 0)

    def spawn_particles(self, amount, color, speed_mult=1.0, size_mult=1.0):
        for _ in range(amount):
            px = self.pos.x + random.uniform(-15, 15)
            py = self.pos.y + random.uniform(-20, 20)
            vx = random.uniform(-1.5, 1.5) * speed_mult
            vy = random.uniform(-2.5, 1.0) * speed_mult
            size = random.uniform(2, 6) * size_mult
            life = random.randint(20, 45)
            start_alpha = random.randint(150, 255)
            self.particles.append([px, py, vx, vy, size, life, life, color, start_alpha])

    def take_damage(self, amount, knockback_force):
        if self.state in ["DYING", "SPAWNING", "TELEPORT_OUT", "TELEPORT_IN"]: return
        self.health -= amount
        self.knockback = knockback_force
        
        p_color = (255, 120, 0) if self.is_enraged else (0, 255, 255)
        self.spawn_particles(15, p_color, speed_mult=3.0)
        
        if self.health <= 0:
            self.state = "DYING"
            self.knockback = knockback_force * 0.3
            self.spawn_particles(50, (255, 255, 255), speed_mult=4.5, size_mult=1.5)
            return

        if random.random() < 0.3:
            self.state = "TELEPORT_OUT"
            self.knockback = pygame.math.Vector2(0, 0) 
            self.spawn_particles(30, (150, 50, 255), speed_mult=2.0)
            return

        if self.state in ["WINDUP", "DASH"]:
            self.state = "CHASING"
            self.speed = self.base_speed
        
        if self.health <= self.max_health * 0.4 and not self.is_enraged:
            self.is_enraged = True
            self.base_speed *= 1.6
            self.bob_speed *= 2 
            self.spawn_particles(60, (255, 50, 0), speed_mult=4.0)
            
    def apply_swarm_separation(self, enemies):
        separation_vec = pygame.math.Vector2(0, 0)
        count = 0
        for other in enemies:
            if other is not self and not other.is_dead:
                dist = self.pos.distance_to(other.pos)
                if 0 < dist < 55: 
                    diff = self.pos - other.pos
                    separation_vec += diff.normalize() / dist
                    count += 1
        if count > 0: return (separation_vec / count) * 5.0
        return pygame.math.Vector2(0, 0)

    def update(self, player, game_data):
        current_time = pygame.time.get_ticks()
        
        self.history.insert(0, (self.pos.x, self.pos.y))
        if len(self.history) > 8: 
            self.history.pop()

        for p in self.particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[6] -= 1
            p[4] = max(0, p[4] - 0.15) 
            if p[6] <= 0 or p[4] <= 0:
                self.particles.remove(p)

        if self.state not in ["DYING", "TELEPORT_OUT", "TELEPORT_IN"] and random.random() < 0.3:
            amb_color = (255, 80, 0) if self.is_enraged else (0, 200, 255)
            self.spawn_particles(1, amb_color, speed_mult=0.5, size_mult=0.9)

        if self.dash_cooldown > 0 and self.state == "CHASING": self.dash_cooldown -= 1
        self.shake_offset = pygame.math.Vector2(0, 0) 

        target = pygame.math.Vector2(player.rect.center)
        if target.distance_to(self.pos) > 0:
            self.look_dir = (target - self.pos).normalize()

        if self.state == "TELEPORT_OUT":
            self.alpha = max(0, self.alpha - 30)
            if self.alpha <= 0:
                dir_from_player = (self.pos - target)
                if dir_from_player.length() > 0: self.pos = target - dir_from_player.normalize() * 150
                self.state = "TELEPORT_IN"
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            return
            
        elif self.state == "TELEPORT_IN":
            self.alpha = min(255, self.alpha + 30)
            if self.alpha >= 255:
                self.state = "CHASING"
                self.dash_cooldown = 0 
                self.spawn_particles(25, (150, 50, 255), speed_mult=2.5)
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            return

        if self.state == "SPAWNING":
            self.alpha = min(255, self.alpha + 4)
            self.pos.y -= 0.6 
            if self.alpha >= 255: self.state = "CHASING"
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            return

        if self.state == "DYING":
            self.alpha -= 6
            self.pos.y -= 2.5
            self.pos.x += math.sin(current_time * 0.02) * 4
            self.death_scale -= 0.025
            if self.alpha <= 0 or self.death_scale <= 0:
                self.is_dead = True
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            return

        dist_to_player = self.pos.distance_to(target)
        move_vec = pygame.math.Vector2(0, 0)

        if self.state == "CHASING":
            if dist_to_player > 0:
                base_dir = (target - self.pos).normalize()
                perp_dir = pygame.math.Vector2(-base_dir.y, base_dir.x) * self.flank_direction
                flank_strength = min(1.0, dist_to_player / 180.0) 
                wave = math.sin(current_time * 0.006 + self.ethereal_offset) * 1.8
                direction = (base_dir + (perp_dir * flank_strength * wave)).normalize()
                move_vec = direction * self.speed
            
            if 60 < dist_to_player < 200 and self.dash_cooldown <= 0 and random.random() < 0.05:
                self.state = "WINDUP"
                self.state_timer = 30 
                self.dash_dir = (target - self.pos).normalize() 
                
        elif self.state == "WINDUP":
            self.state_timer -= 1
            self.shake_offset.x = random.uniform(-7, 7)
            self.shake_offset.y = random.uniform(-7, 7)
            self.spawn_particles(3, (255, 255, 255), speed_mult=0.3)
            if self.state_timer <= 0:
                self.state = "DASH"
                self.state_timer = 20 
                self.dash_cooldown = random.randint(180, 360)
                
        elif self.state == "DASH":
            self.state_timer -= 1
            move_vec = self.dash_dir * (self.base_speed * 6.0) 
            self.spawn_particles(4, (255, 100, 0) if self.is_enraged else (0, 255, 255), speed_mult=0.2)
            if self.state_timer <= 0:
                self.state = "CHASING"

        if self.state != "WINDUP": 
            separation = self.apply_swarm_separation(game_data["enemies"])
            self.pos += move_vec + separation + self.knockback
        else:
            self.pos += self.knockback 
        
        self.knockback *= self.knockback_resistance
        if self.knockback.length() < 0.5: self.knockback = pygame.math.Vector2(0, 0)
            
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

    def draw(self, screen, camera):
        current_time = pygame.time.get_ticks()
        bob = math.sin(current_time * self.bob_speed + self.bob_offset) * self.bob_height
        
        wobble_x = 1.0 + math.sin(current_time * 0.003 + self.ethereal_offset) * 0.08
        wobble_y = 1.0 + math.cos(current_time * 0.004 + self.ethereal_offset) * 0.08
        
        final_scale_x = wobble_x * self.death_scale
        final_scale_y = wobble_y * self.death_scale

        if self.state not in ["TELEPORT_OUT", "TELEPORT_IN", "SPAWNING"] and len(self.history) > 1:
            for i, (hx, hy) in enumerate(self.history):
                trail_alpha = max(0, 120 - (i * 15))
                if trail_alpha > 0:
                    base_trail = self.glow_surf_enraged if self.is_enraged else self.glow_surf_normal
                    trail_img = base_trail.copy()
                    
                    scale_factor = (1.0 - (i * 0.1)) * self.death_scale
                    w = int(trail_img.get_width() * scale_factor * wobble_x)
                    h = int(trail_img.get_height() * scale_factor * wobble_y)
                    
                    if w > 0 and h > 0:
                        trail_img = pygame.transform.scale(trail_img, (w, h))
                        trail_img.set_alpha(trail_alpha)
                        trail_rect = trail_img.get_rect(center=(hx, hy))
                        t_pos = camera.apply(trail_rect).move(0, bob * scale_factor)
                        screen.blit(trail_img, t_pos, special_flags=pygame.BLEND_RGBA_ADD)

        draw_image = self.original_image.copy()
        
        w = int(draw_image.get_width() * final_scale_x)
        h = int(draw_image.get_height() * final_scale_y)
        if w > 0 and h > 0:
            draw_image = pygame.transform.scale(draw_image, (w, h))
            glow_image = pygame.transform.scale(self.glow_surf_enraged if self.is_enraged else self.glow_surf_normal, (w, h))
        else:
            glow_image = draw_image 

        base_alpha = max(0, int(self.alpha))
        draw_image.set_alpha(int(base_alpha * 0.8)) 
        glow_image.set_alpha(int(base_alpha * 0.6)) 

        draw_rect = draw_image.get_rect(center=self.rect.center)
        draw_pos = camera.apply(draw_rect).move(self.shake_offset.x, bob + self.shake_offset.y)

        screen.blit(draw_image, draw_pos)
        screen.blit(glow_image, draw_pos, special_flags=pygame.BLEND_RGBA_ADD)

        if self.state not in ["DYING", "TELEPORT_OUT", "TELEPORT_IN", "SPAWNING"]:
            eye_color = (255, 80, 0) if self.is_enraged else (0, 255, 255)
            eye_offset_x = self.look_dir.x * 5 * wobble_x
            eye_offset_y = (self.look_dir.y * 3 - 10) * wobble_y
            
            eye_surf = pygame.Surface((14, 8), pygame.SRCALPHA)
            pygame.draw.circle(eye_surf, eye_color, (4, 4), 3)
            pygame.draw.circle(eye_surf, eye_color, (10, 4), 3)
            
            eye_pos_final = (draw_pos.centerx - 7 + eye_offset_x, draw_pos.centery + eye_offset_y)
            screen.blit(eye_surf, eye_pos_final, special_flags=pygame.BLEND_RGBA_ADD)

        for p in self.particles:
            screen_pos = camera.apply(pygame.Rect(p[0], p[1], 1, 1))
            current_alpha = int((p[6] / p[5]) * p[8])
            
            if current_alpha > 0 and p[4] > 0:
                surf = pygame.Surface((int(p[4]*2.5), int(p[4]*2.5)), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*p[7], current_alpha), (int(p[4]*1.25), int(p[4]*1.25)), int(p[4]))
                pygame.draw.circle(surf, (255, 255, 255, int(current_alpha*0.5)), (int(p[4]*1.25), int(p[4]*1.25)), int(p[4]*1.2))
                
                screen.blit(surf, (screen_pos.x - int(p[4]*1.25), screen_pos.y - int(p[4]*1.25)), special_flags=pygame.BLEND_RGBA_ADD)
        
        if self.health < self.max_health and self.state not in ["DYING", "SPAWNING", "TELEPORT_OUT", "TELEPORT_IN"]:
            bar_w, bar_h = 40, 4
            ratio = max(0, self.health / self.max_health)
            bx, by = draw_pos.centerx - bar_w // 2, draw_pos.y - 20
            pygame.draw.rect(screen, (0, 0, 0, 150), (bx, by, bar_w, bar_h)) 
            fg_col = (255, 100, 0) if self.is_enraged else (0, 220, 180)
            pygame.draw.rect(screen, fg_col, (bx, by, bar_w * ratio, bar_h))

    @classmethod
    def spawn_horde(cls, player, game_data, ghost_img, count=5):
        if game_data["current_map"] == "cmitermap":
            for _ in range(count):
                dist_x = random.randint(400, 750) * random.choice([-1, 1])
                dist_y = random.randint(400, 750) * random.choice([-1, 1])
                game_data["enemies"].append(cls(player.rect.x + dist_x, player.rect.y + dist_y, ghost_img))