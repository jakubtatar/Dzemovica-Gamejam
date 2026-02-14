import pygame
import random
import math

# ==========================================
# 1. GHOST ENEMY (Duch)
# ==========================================
class GhostEnemy:
    def __init__(self, x, y, image):
        self.original_image = image.copy()
        self.image = image.copy()  
        
        self.mask_image = image.copy()
        self.mask_image.fill((255, 255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)

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
        self.bob_height = 10
        self.alpha = 0
        self.shake_offset = pygame.math.Vector2(0, 0)
        self.ethereal_offset = random.uniform(0, math.pi * 2)
        self.death_scale = 1.0
        
        self.particles = []
        self.history = [] 
        self.look_dir = pygame.math.Vector2(0, 0)

    def get_current_color(self, current_time):
        pulse = (math.sin(current_time * 0.003 + self.ethereal_offset) + 1) / 2
        if self.is_enraged:
            return (255, int(50 + pulse * 100), 0)
        else:
            return (0, int(150 + pulse * 105), 255)

    def spawn_particles(self, amount, color, speed_mult=1.0, size_mult=1.0, is_ember=False):
        for _ in range(amount):
            px = self.pos.x + random.uniform(-15, 15)
            py = self.pos.y + random.uniform(-10, 30)
            vx = random.uniform(-1.0, 1.0) * speed_mult
            vy = random.uniform(-3.0, -0.5) * speed_mult if is_ember else random.uniform(-2.0, 1.0) * speed_mult
            size = random.uniform(2, 5) * size_mult
            life = random.randint(25, 55)
            start_alpha = random.randint(150, 255)
            self.particles.append([px, py, vx, vy, size, life, life, color, start_alpha])

    def take_damage(self, amount, knockback_force):
        if self.state in ["DYING", "SPAWNING", "TELEPORT_OUT", "TELEPORT_IN"]: return
        self.health -= amount
        self.knockback = knockback_force
        
        current_time = pygame.time.get_ticks()
        p_color = self.get_current_color(current_time)
        self.spawn_particles(20, p_color, speed_mult=3.5, is_ember=True)
        
        if self.health <= 0:
            self.state = "DYING"
            self.knockback = knockback_force * 0.3
            self.spawn_particles(60, (255, 255, 255), speed_mult=5.0, size_mult=1.8, is_ember=True)
            return

        if random.random() < 0.3:
            self.state = "TELEPORT_OUT"
            self.knockback = pygame.math.Vector2(0, 0) 
            self.spawn_particles(40, (180, 50, 255), speed_mult=2.5)
            return

        if self.state in ["WINDUP", "DASH"]:
            self.state = "CHASING"
            self.speed = self.base_speed
        
        if self.health <= self.max_health * 0.4 and not self.is_enraged:
            self.is_enraged = True
            self.base_speed *= 1.6
            self.bob_speed *= 2.5 
            self.spawn_particles(70, (255, 50, 0), speed_mult=4.5, is_ember=True)
            
    def apply_swarm_separation(self, enemies):
        separation_vec = pygame.math.Vector2(0, 0)
        count = 0
        for other in enemies:
            if other is not self and not getattr(other, 'is_dead', False):
                dist = self.pos.distance_to(other.pos)
                if 0 < dist < 60: 
                    diff = self.pos - other.pos
                    separation_vec += diff.normalize() / dist
                    count += 1
        if count > 0: return (separation_vec / count) * 5.5
        return pygame.math.Vector2(0, 0)

    def update(self, player, game_data):
        current_time = pygame.time.get_ticks()
        
        self.history.insert(0, (self.pos.x, self.pos.y))
        if len(self.history) > 10: 
            self.history.pop()

        for p in self.particles[:]:
            p[0] += p[2] + math.sin(current_time * 0.01 + p[5]) * 0.5 
            p[1] += p[3]
            p[6] -= 1
            p[4] = max(0, p[4] - 0.1) 
            if p[6] <= 0 or p[4] <= 0:
                self.particles.remove(p)

        if self.state not in ["DYING", "TELEPORT_OUT", "TELEPORT_IN"] and random.random() < 0.35:
            self.spawn_particles(1, self.get_current_color(current_time), speed_mult=0.6, size_mult=0.8, is_ember=True)

        if self.dash_cooldown > 0 and self.state == "CHASING": self.dash_cooldown -= 1
        self.shake_offset = pygame.math.Vector2(0, 0) 

        target = pygame.math.Vector2(player.rect.center)
        if target.distance_to(self.pos) > 0:
            desired_dir = (target - self.pos).normalize()
            self.look_dir = self.look_dir.lerp(desired_dir, 0.1)

        if self.state == "TELEPORT_OUT":
            self.alpha = max(0, self.alpha - 25)
            if self.alpha <= 0:
                dir_from_player = (self.pos - target)
                if dir_from_player.length() > 0: self.pos = target - dir_from_player.normalize() * 160
                self.state = "TELEPORT_IN"
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            return
            
        elif self.state == "TELEPORT_IN":
            self.alpha = min(255, self.alpha + 25)
            if self.alpha >= 255:
                self.state = "CHASING"
                self.dash_cooldown = 0 
                self.spawn_particles(30, (180, 50, 255), speed_mult=3.0)
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            return

        if self.state == "SPAWNING":
            self.alpha = min(255, self.alpha + 4)
            self.pos.y -= 0.6 
            if self.alpha >= 255: self.state = "CHASING"
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            return

        if self.state == "DYING":
            self.alpha -= 7
            self.pos.y -= 3.0
            self.pos.x += math.sin(current_time * 0.02) * 5
            self.death_scale -= 0.03
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
                wave = math.sin(current_time * 0.007 + self.ethereal_offset) * 2.0
                direction = (base_dir + (perp_dir * flank_strength * wave)).normalize()
                move_vec = direction * self.speed
            
            if 60 < dist_to_player < 180 and self.dash_cooldown <= 0 and random.random() < 0.05:
                self.state = "WINDUP"
                self.state_timer = 25 
                self.dash_dir = (target - self.pos).normalize() 
                
        elif self.state == "WINDUP":
            self.state_timer -= 1
            self.shake_offset.x = random.uniform(-8, 8)
            self.shake_offset.y = random.uniform(-8, 8)
            self.spawn_particles(4, (255, 255, 255), speed_mult=0.4)
            if self.state_timer <= 0:
                self.state = "DASH"
                self.state_timer = 18 
                self.dash_cooldown = random.randint(180, 360)
                
        elif self.state == "DASH":
            self.state_timer -= 1
            move_vec = self.dash_dir * (self.base_speed * 6.5) 
            self.spawn_particles(5, self.get_current_color(current_time), speed_mult=0.3)
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
        
        wobble_x = 1.0 + math.sin(current_time * 0.004 + self.ethereal_offset) * 0.06
        wobble_y = 1.0 + math.cos(current_time * 0.005 + self.ethereal_offset) * 0.06
        
        final_scale_x = wobble_x * self.death_scale
        final_scale_y = wobble_y * self.death_scale

        current_color = self.get_current_color(current_time)
        
        if self.state not in ["TELEPORT_OUT", "TELEPORT_IN", "SPAWNING"] and len(self.history) > 1:
            for i, (hx, hy) in enumerate(self.history):
                trail_alpha = max(0, 100 - (i * 10))
                if trail_alpha > 0:
                    trail_img = self.mask_image.copy()
                    trail_img.fill((*current_color, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    
                    scale_factor = (1.0 - (i * 0.08)) * self.death_scale
                    w = int(trail_img.get_width() * scale_factor * wobble_x)
                    h = int(trail_img.get_height() * scale_factor * wobble_y)
                    
                    if w > 0 and h > 0:
                        trail_img = pygame.transform.scale(trail_img, (w, h))
                        trail_img.set_alpha(trail_alpha)
                        t_pos = camera.apply(trail_img.get_rect(center=(hx, hy))).move(0, bob * scale_factor)
                        screen.blit(trail_img, t_pos, special_flags=pygame.BLEND_RGBA_ADD)

        draw_image = self.original_image.copy()
        glow_image = self.mask_image.copy()
        glow_image.fill((*current_color, 0), special_flags=pygame.BLEND_RGBA_MULT)

        w = int(draw_image.get_width() * final_scale_x)
        h = int(draw_image.get_height() * final_scale_y)
        
        if w > 0 and h > 0:
            draw_image = pygame.transform.scale(draw_image, (w, h))
            glow_image = pygame.transform.scale(glow_image, (w, h))
            
            base_alpha = max(0, int(self.alpha))
            draw_image.set_alpha(int(base_alpha * 0.85)) 
            glow_image.set_alpha(int(base_alpha * 0.7)) 

            draw_pos = camera.apply(draw_image.get_rect(center=self.rect.center)).move(self.shake_offset.x, bob + self.shake_offset.y)

            screen.blit(draw_image, draw_pos) 
            screen.blit(glow_image, draw_pos, special_flags=pygame.BLEND_RGBA_ADD) 
            
            bloom_scale = 1.25 + (math.sin(current_time * 0.006) * 0.05)
            bw, bh = int(w * bloom_scale), int(h * bloom_scale)
            if bw > 0 and bh > 0:
                bloom_img = pygame.transform.scale(glow_image, (bw, bh))
                bloom_img.set_alpha(int(base_alpha * 0.3))
                bloom_pos = camera.apply(bloom_img.get_rect(center=self.rect.center)).move(self.shake_offset.x, bob + self.shake_offset.y)
                screen.blit(bloom_img, bloom_pos, special_flags=pygame.BLEND_RGBA_ADD)

            if self.state not in ["DYING", "TELEPORT_OUT", "TELEPORT_IN", "SPAWNING"]:
                eye_color = (255, 255, 255) 
                eye_glow = current_color 
                
                eye_offset_x = self.look_dir.x * 6 * wobble_x
                eye_offset_y = (self.look_dir.y * 4 - 10) * wobble_y
                
                eye_surf = pygame.Surface((20, 12), pygame.SRCALPHA)
                
                pygame.draw.circle(eye_surf, (*eye_glow, 150), (6, 6), 5)
                pygame.draw.circle(eye_surf, (*eye_glow, 150), (14, 6), 5)
                pygame.draw.circle(eye_surf, eye_color, (6, 6), 2)
                pygame.draw.circle(eye_surf, eye_color, (14, 6), 2)
                
                eye_pos_final = (draw_pos.centerx - 10 + eye_offset_x, draw_pos.centery - 4 + eye_offset_y)
                screen.blit(eye_surf, eye_pos_final, special_flags=pygame.BLEND_RGBA_ADD)

        for p in self.particles:
            screen_pos = camera.apply(pygame.Rect(p[0], p[1], 1, 1))
            current_alpha = int((p[6] / p[5]) * p[8])
            
            if current_alpha > 0 and p[4] > 0:
                surf_size = int(p[4]*3)
                surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
                center = surf_size // 2
                
                pygame.draw.circle(surf, (*p[7], int(current_alpha * 0.3)), (center, center), int(p[4]*1.5))
                pygame.draw.circle(surf, (*p[7], current_alpha), (center, center), int(p[4]))
                pygame.draw.circle(surf, (255, 255, 255, int(current_alpha * 0.8)), (center, center), int(p[4]*0.4))
                
                screen.blit(surf, (screen_pos.x - center, screen_pos.y - center), special_flags=pygame.BLEND_RGBA_ADD)
        
        if self.health < self.max_health and self.state not in ["DYING", "SPAWNING", "TELEPORT_OUT", "TELEPORT_IN"]:
            bar_w, bar_h = 36, 4
            ratio = max(0, self.health / self.max_health)
            bx, by = draw_pos.centerx - bar_w // 2, draw_pos.y - 25
            
            pygame.draw.rect(screen, (0, 0, 0, 180), (bx-1, by-1, bar_w+2, bar_h+2), border_radius=2) 
            pygame.draw.rect(screen, current_color, (bx, by, bar_w * ratio, bar_h), border_radius=2)

    @classmethod
    def spawn_horde(cls, player, game_data, ghost_img, count=5):
        """Metóda volaná z main.py pri štarte noci"""
        if game_data["current_map"] == "cmitermap":
            for _ in range(count):
                dist_x = random.randint(200, 400) * random.choice([-1, 1])
                dist_y = random.randint(200, 400) * random.choice([-1, 1])
                spawn_x = player.rect.x + dist_x
                spawn_y = player.rect.y + dist_y
                
                # Náhodne vyberie jeden z troch typov
                enemy_type = random.choice(["ghost", "archer", "ghoul"])
                if enemy_type == "ghost":
                    game_data["enemies"].append(cls(spawn_x, spawn_y, ghost_img))
                elif enemy_type == "archer":
                    game_data["enemies"].append(SkeletonArcher(spawn_x, spawn_y, ghost_img))
                elif enemy_type == "ghoul":
                    game_data["enemies"].append(GhoulTank(spawn_x, spawn_y, ghost_img))

# ==========================================
# 2. ARROW (Šíp pre Kostlivca)
# ==========================================
class Arrow:
    def __init__(self, x, y, target_pos, damage=15):
        self.pos = pygame.math.Vector2(x, y)
        self.rect = pygame.Rect(x, y, 8, 8)
        
        direction = target_pos - self.pos
        if direction.length() > 0:
            self.vel = direction.normalize() * 9 
        else:
            self.vel = pygame.math.Vector2(0, 0)
            
        self.damage = damage
        self.lifetime = 120 
        
    def update(self):
        self.pos += self.vel
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.lifetime -= 1

    def draw(self, screen, camera):
        screen_pos = camera.apply(self.rect).center
        end_pos = (screen_pos[0] - self.vel.x * 2.5, screen_pos[1] - self.vel.y * 2.5)
        pygame.draw.line(screen, (255, 100, 0), screen_pos, end_pos, 4)
        pygame.draw.circle(screen, (255, 255, 255), screen_pos, 3)

# ==========================================
# 3. SKELETON ARCHER (Ostreľovač na diaľku)
# ==========================================
class SkeletonArcher:
    def __init__(self, x, y, image):
        self.original_image = image.copy()
        self.image = image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)
        
        self.max_health = 40 
        self.health = self.max_health
        self.speed = 2.5
        self.damage = 15
        
        self.state = "KITING" 
        self.attack_cooldown = random.randint(60, 120)
        self.aim_timer = 0
        self.target_aim_pos = None
        self.is_dead = False
        self.knockback = pygame.math.Vector2(0, 0)
        
        # Animácie umierania
        self.alpha = 255
        self.death_scale = 1.0
        self.particles = []

    def take_damage(self, amount, knockback_force):
        if self.state == "DYING": return
        self.health -= amount
        self.knockback = knockback_force
        
        # Zelené častice pri zásahu (ako ektoplazma kostlivca)
        self.spawn_particles(15, (0, 200, 0), speed_mult=2.0)
        
        if self.state == "AIMING":
            self.state = "KITING" 
        if self.health <= 0:
            self.state = "DYING"
            self.spawn_particles(40, (255, 255, 255), speed_mult=4.0)

    def spawn_particles(self, amount, color, speed_mult=1.0):
        for _ in range(amount):
            px = self.pos.x + random.uniform(-10, 10)
            py = self.pos.y + random.uniform(-10, 10)
            vx = random.uniform(-1.5, 1.5) * speed_mult
            vy = random.uniform(-1.5, 1.5) * speed_mult
            size = random.uniform(2, 4)
            life = random.randint(20, 40)
            self.particles.append([px, py, vx, vy, size, life, life, color, 255])

    def update(self, player, game_data):
        # Update častíc
        for p in self.particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[6] -= 1
            if p[6] <= 0: self.particles.remove(p)

        if self.state == "DYING":
            self.alpha -= 8
            self.death_scale -= 0.03
            self.pos.y -= 2.0
            if self.alpha <= 0: self.is_dead = True
            return

        if self.attack_cooldown > 0 and self.state == "KITING":
            self.attack_cooldown -= 1

        target = pygame.math.Vector2(player.rect.center)
        dist_to_player = self.pos.distance_to(target)
        move_vec = pygame.math.Vector2(0, 0)

        if self.state == "KITING":
            if dist_to_player < 140:
                move_vec = (self.pos - target).normalize() * self.speed
            elif dist_to_player > 300:
                move_vec = (target - self.pos).normalize() * self.speed
            else:
                if self.attack_cooldown <= 0:
                    self.state = "AIMING"
                    self.aim_timer = 40 

        elif self.state == "AIMING":
            self.target_aim_pos = target 
            self.aim_timer -= 1
            if self.aim_timer <= 0:
                new_arrow = Arrow(self.pos.x, self.pos.y, target, self.damage)
                if "arrows" not in game_data: game_data["arrows"] = []
                game_data["arrows"].append(new_arrow)
                
                self.state = "KITING"
                self.attack_cooldown = random.randint(120, 180)

        self.pos += move_vec + self.knockback
        self.knockback *= 0.8
        if self.knockback.length() < 0.5: self.knockback = pygame.math.Vector2(0, 0)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def draw(self, screen, camera):
        # Kreslenie častíc
        for p in self.particles:
            screen_pos = camera.apply(pygame.Rect(p[0], p[1], 1, 1))
            pygame.draw.circle(screen, p[7], screen_pos.center, int(p[4]))

        draw_image = self.image.copy()
        if self.state == "DYING":
            w = int(draw_image.get_width() * self.death_scale)
            h = int(draw_image.get_height() * self.death_scale)
            if w > 0 and h > 0:
                draw_image = pygame.transform.scale(draw_image, (w, h))
        
        draw_image.set_alpha(self.alpha)
        draw_rect = draw_image.get_rect(center=self.rect.center)
        draw_pos = camera.apply(draw_rect)
        screen.blit(draw_image, draw_pos)

        if self.state == "AIMING" and self.target_aim_pos:
            start_pos = draw_pos.center
            end_pos = camera.apply(pygame.Rect(self.target_aim_pos.x, self.target_aim_pos.y, 1, 1)).center
            laser_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.02)) * 150
            pygame.draw.line(laser_surf, (255, 0, 0, int(50 + pulse)), start_pos, end_pos, 2)
            screen.blit(laser_surf, (0, 0))

# ==========================================
# 4. GHOUL TANK (Ťažký útočník na blízko)
# ==========================================
class GhoulTank:
    def __init__(self, x, y, image):
        self.original_image = image.copy()
        w, h = self.original_image.get_size()
        self.image = pygame.transform.scale(self.original_image, (int(w*1.4), int(h*1.4)))
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)
        
        self.max_health = 180 
        self.health = self.max_health
        self.speed = 1.0 
        self.damage = 25 
        
        self.state = "CHASING"
        self.smash_timer = 0
        self.is_dead = False
        self.knockback = pygame.math.Vector2(0, 0)
        
        # Animácie umierania
        self.alpha = 255
        self.death_scale = 1.0
        self.particles = []

    def take_damage(self, amount, knockback_force):
        if self.state == "DYING": return
        self.health -= amount
        self.knockback = knockback_force * 0.1 
        
        # Červené častice krvi pri zásahu
        self.spawn_particles(10, (150, 0, 0), speed_mult=1.5)
        
        if self.health <= 0:
            self.state = "DYING"
            self.spawn_particles(60, (100, 100, 100), speed_mult=3.0, size_mult=2.0)

    def spawn_particles(self, amount, color, speed_mult=1.0, size_mult=1.0):
        for _ in range(amount):
            px = self.pos.x + random.uniform(-20, 20)
            py = self.pos.y + random.uniform(-20, 20)
            vx = random.uniform(-1.0, 1.0) * speed_mult
            vy = random.uniform(-1.0, 1.0) * speed_mult
            size = random.uniform(3, 6) * size_mult
            life = random.randint(30, 60)
            self.particles.append([px, py, vx, vy, size, life, life, color, 255])

    def update(self, player, game_data):
        for p in self.particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[6] -= 1
            if p[6] <= 0: self.particles.remove(p)

        if self.state == "DYING":
            self.alpha -= 5
            self.death_scale -= 0.02
            self.pos.y -= 1.0
            if self.alpha <= 0: self.is_dead = True
            return

        target = pygame.math.Vector2(player.rect.center)
        dist_to_player = self.pos.distance_to(target)
        move_vec = pygame.math.Vector2(0, 0)

        if self.state == "CHASING":
            if dist_to_player > 0:
                move_vec = (target - self.pos).normalize() * self.speed
            if dist_to_player < 70:
                self.state = "SMASH_WINDUP"
                self.smash_timer = 50 

        elif self.state == "SMASH_WINDUP":
            self.smash_timer -= 1
            if self.smash_timer <= 0:
                if dist_to_player < 90:
                    if not hasattr(player, 'last_damage_time'): player.last_damage_time = 0
                    current_time = pygame.time.get_ticks()
                    if current_time - player.last_damage_time >= 500:
                        player.health -= self.damage
                        player.last_damage_time = current_time
                self.state = "CHASING"

        self.pos += move_vec + self.knockback
        self.knockback *= 0.85
        if self.knockback.length() < 0.5: self.knockback = pygame.math.Vector2(0, 0)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def draw(self, screen, camera):
        for p in self.particles:
            screen_pos = camera.apply(pygame.Rect(p[0], p[1], 1, 1))
            pygame.draw.circle(screen, p[7], screen_pos.center, int(p[4]))

        draw_image = self.image.copy()
        if self.state == "DYING":
            w = int(draw_image.get_width() * self.death_scale)
            h = int(draw_image.get_height() * self.death_scale)
            if w > 0 and h > 0: draw_image = pygame.transform.scale(draw_image, (w, h))
        
        draw_image.set_alpha(self.alpha)
        draw_rect = draw_image.get_rect(center=self.rect.center)
        draw_pos = camera.apply(draw_rect)

        if self.state == "SMASH_WINDUP":
            shake = random.randint(-4, 4)
            draw_pos = draw_pos.move(shake, shake)
            tinted_img = draw_image.copy()
            tinted_img.fill((150, 0, 0, 100), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(tinted_img, draw_pos)
        else:
            screen.blit(draw_image, draw_pos)

# ==========================================
# 5. SHADOW WRAITH (Rýchly, otravný)
# ==========================================
class ShadowWraith:
    def __init__(self, x, y, image):
        self.original_image = image.copy()
        w, h = self.original_image.get_size()
        self.image = pygame.transform.scale(self.original_image, (int(w*0.7), int(h*0.7)))
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)
        
        self.max_health = 20 
        self.health = self.max_health
        self.speed = random.uniform(3.5, 4.5) 
        self.damage = 10
        
        self.state = "ORBITING"
        self.orbit_angle = random.uniform(0, math.pi * 2)
        self.orbit_direction = random.choice([-1, 1]) 
        self.orbit_distance = random.randint(120, 160)
        
        self.action_timer = random.randint(60, 150)
        self.is_dead = False
        self.knockback = pygame.math.Vector2(0, 0)
        
        # Animácie umierania
        self.alpha = 160
        self.death_scale = 1.0
        self.particles = []

    def take_damage(self, amount, knockback_force):
        if self.state == "DYING": return
        self.health -= amount
        self.knockback = knockback_force * 1.5 
        self.spawn_particles(12, (100, 0, 200), speed_mult=3.0)
        
        if self.health <= 0:
            self.state = "DYING"
            self.spawn_particles(50, (180, 50, 255), speed_mult=5.0)

    def spawn_particles(self, amount, color, speed_mult=1.0):
        for _ in range(amount):
            px = self.pos.x + random.uniform(-10, 10)
            py = self.pos.y + random.uniform(-10, 10)
            vx = random.uniform(-2.0, 2.0) * speed_mult
            vy = random.uniform(-2.0, 2.0) * speed_mult
            size = random.uniform(2, 4)
            life = random.randint(15, 30)
            self.particles.append([px, py, vx, vy, size, life, life, color, 255])

    def update(self, player, game_data):
        for p in self.particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[6] -= 1
            if p[6] <= 0: self.particles.remove(p)

        if self.state == "DYING":
            self.alpha -= 10
            self.death_scale -= 0.04
            if self.alpha <= 0: self.is_dead = True
            return

        target = pygame.math.Vector2(player.rect.center)
        dist_to_player = self.pos.distance_to(target)
        move_vec = pygame.math.Vector2(0, 0)

        if self.state == "ORBITING":
            self.orbit_angle += 0.08 * self.orbit_direction
            desired_pos = target + pygame.math.Vector2(math.cos(self.orbit_angle), math.sin(self.orbit_angle)) * self.orbit_distance
            dir_to_desired = desired_pos - self.pos
            if dir_to_desired.length() > 0:
                move_vec = dir_to_desired.normalize() * self.speed
            self.action_timer -= 1
            if self.action_timer <= 0:
                self.state = "STRIKE"
                self.action_timer = 20

        elif self.state == "STRIKE":
            self.action_timer -= 1
            if dist_to_player > 0:
                move_vec = (target - self.pos).normalize() * (self.speed * 2.5) 
            if dist_to_player < 35:
                if not hasattr(player, 'last_damage_time'): player.last_damage_time = 0
                current_time = pygame.time.get_ticks()
                if current_time - player.last_damage_time >= 500:
                    player.health -= self.damage
                    player.last_damage_time = current_time
                self.state = "FLEE"
                self.action_timer = 40 
            if self.action_timer <= 0:
                self.state = "FLEE"
                self.action_timer = 40

        elif self.state == "FLEE":
            self.action_timer -= 1
            if dist_to_player > 0:
                move_vec = (self.pos - target).normalize() * (self.speed * 1.5)
            if self.action_timer <= 0:
                self.state = "ORBITING"
                self.orbit_direction *= -1
                self.action_timer = random.randint(80, 160)

        self.pos += move_vec + self.knockback
        self.knockback *= 0.8
        if self.knockback.length() < 0.5: self.knockback = pygame.math.Vector2(0, 0)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def draw(self, screen, camera):
        for p in self.particles:
            screen_pos = camera.apply(pygame.Rect(p[0], p[1], 1, 1))
            pygame.draw.circle(screen, p[7], screen_pos.center, int(p[4]))

        draw_image = self.image.copy()
        if self.state == "DYING":
            w = int(draw_image.get_width() * self.death_scale)
            h = int(draw_image.get_height() * self.death_scale)
            if w > 0 and h > 0: draw_image = pygame.transform.scale(draw_image, (w, h))

        draw_image.fill((80, 0, 150, 0), special_flags=pygame.BLEND_RGBA_ADD)
        draw_image.set_alpha(self.alpha)
        draw_rect = draw_image.get_rect(center=self.rect.center)
        draw_pos = camera.apply(draw_rect)
        
        if self.state in ["STRIKE", "FLEE"]:
            for i in range(1, 3):
                trail_img = draw_image.copy()
                trail_img.set_alpha(80 - (i * 30))
                screen.blit(trail_img, draw_pos.move(random.randint(-15,15), random.randint(-15,15)))
                
        screen.blit(draw_image, draw_pos)