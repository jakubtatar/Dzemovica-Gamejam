import pygame
import math

class Player:
    def __init__(self, x, y, width, height, color):
        # --- NASTAVENIE RÝCHLOSTI ---
        self.base_speed = 5
        self.speed = self.base_speed
        
        # --- GRAFIKA ---
        self.image_width = width
        self.image_height = height
        
        # --- HITBOX ---
        self.hitbox_w = width - 12
        self.hitbox_h = 20
        start_rect_x = x + (self.image_width - self.hitbox_w) // 2
        start_rect_y = y + (self.image_height - self.hitbox_h)
        
        self.rect = pygame.Rect(start_rect_x, start_rect_y, self.hitbox_w, self.hitbox_h)
        self.color = color
        self.money = 100
        self.health = 100
        self.last_damage_time = 0

        # --- ANIMÁCIE ---
        self.direction = "down"
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15 
        self.is_moving = False

        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }

        def load_img(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (self.image_width, self.image_height))
            except:
                surf = pygame.Surface((self.image_width, self.image_height))
                surf.fill(self.color)
                return surf

        # Načítanie Right animácií (1=stojí, 2-5=pohyb)
        # Použil som range(1, 6) podľa tvojho kódu (teda 5 obrázkov celkovo)
        for i in range(1, 6):
            img_right = load_img(f"Resources/Hugo/Hugo_Right{i}.png")
            self.animations["right"].append(img_right)
            
            # AUTOMATICKÉ VRÁTENIE (FLIP) PRE LEFT
            img_left = pygame.transform.flip(img_right, True, False)
            self.animations["left"].append(img_left)

            img_back = load_img(f"Resources/Hugo/Hugo_Back{i}.png")
            self.animations["up"].append(img_back)

            img_front = load_img(f"Resources/Hugo/Hugo_Front{i}.png")
            self.animations["down"].append(img_front)
        
        # Ostatné smery

        self.current_image = self.animations[self.direction][0]

    def handle_keys_with_collision(self, screen_width, screen_height, collidable_walls):
        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0
        self.is_moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -1
            self.direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = 1
            self.direction = "right"

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y = -1
            self.direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y = 1
            self.direction = "down"

        if move_x != 0 or move_y != 0:
            self.is_moving = True
            if move_x != 0 and move_y != 0:
                move_x *= 0.7071
                move_y *= 0.7071

        dx, dy = move_x * self.speed, move_y * self.speed
        
        self.rect.x += dx
        for wall in collidable_walls:
            if self.rect.colliderect(wall):
                if dx > 0: self.rect.right = wall.left
                if dx < 0: self.rect.left = wall.right

        self.rect.y += dy
        for wall in collidable_walls:
            if self.rect.colliderect(wall):
                if dy > 0: self.rect.bottom = wall.top
                if dy < 0: self.rect.top = wall.bottom

        # --- UNIVERZÁLNA LOGIKA ANIMÁCIE ---
        if self.is_moving:
            # Kontrolujeme, či pre aktuálny smer máme dosť obrázkov na animáciu
            if len(self.animations[self.direction]) > 1:
                self.animation_timer += self.animation_speed
                if self.animation_timer >= 1:
                    self.animation_timer = 0
                    self.frame_index += 1
                    # Ak máš 5 obrázkov, indexy sú 0,1,2,3,4. 
                    # Index 0 je "stojí", takže pohyb cyklíme od 1 po 4.
                    if self.frame_index >= len(self.animations[self.direction]):
                        self.frame_index = 1
                self.current_image = self.animations[self.direction][self.frame_index]
            else:
                self.current_image = self.animations[self.direction][0]
        else:
            # Stojíme -> prvý obrázok
            self.frame_index = 0
            self.current_image = self.animations[self.direction][0]

    def draw(self, surface, camera):
        rect_on_screen = camera.apply(self.rect)
        draw_x = rect_on_screen.x - (self.image_width - self.hitbox_w) // 2
        draw_y = rect_on_screen.y - (self.image_height - self.hitbox_h)
        surface.blit(self.current_image, (draw_x, draw_y))