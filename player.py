import pygame
import math

class Player:
    def __init__(self, x, y, width, height, color):
        # --- NASTAVENIE RÝCHLOSTI ---
        self.base_speed = 5
        self.speed = self.base_speed
        
        # --- GRAFIKA (CELÁ POSTAVA) ---
        self.image_width = width
        self.image_height = height
        
        # --- HITBOX (PREČO JE TAKÝTO?) ---
        # 1. Výška 20px: Iba chodidlá, aby si mohol chodiť "za" stenami.
        # 2. Šírka -12px: Hitbox je užší ako obrázok. 
        #    Dôvod: Aby sa ti "ramená" nezasekávali o rohy stien. Je to oveľa plynulejšie.
        self.hitbox_w = width - 12
        self.hitbox_h = 20
        
        # Centrovanie hitboxu na spodok postavy
        # X: posunieme ho o polovicu rozdielu šírok, aby bol v strede
        # Y: posunieme ho úplne dole
        start_rect_x = x + (self.image_width - self.hitbox_w) // 2
        start_rect_y = y + (self.image_height - self.hitbox_h)
        
        self.rect = pygame.Rect(start_rect_x, start_rect_y, self.hitbox_w, self.hitbox_h)
        self.color = color
        self.money = 0

        # --- NAČÍTANIE OBRÁZKOV ---
        try:
            self.images = {
                "down": pygame.image.load("Resources/Hugo/Hugo_Front1.png").convert_alpha(),
                "up": pygame.image.load("Resources/Hugo/Hugo_Back1.png").convert_alpha(),
                "left": pygame.image.load("Resources/Hugo/Hugo_Left1.png").convert_alpha(),
                "right": pygame.image.load("Resources/Hugo/Hugo_Right1.png").convert_alpha()
            }
        except:
            # Fallback ak nenájde obrázky (červený obdĺžnik)
            surf = pygame.Surface((width, height))
            surf.fill(color)
            self.images = {"down": surf, "up": surf, "left": surf, "right": surf}

        # Škálovanie obrázkov
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (width, height))

        self.direction = "down"
        self.current_image = self.images[self.direction]

    def handle_keys_with_collision(self, screen_width, screen_height, collidable_walls):
        keys = pygame.key.get_pressed()
        
        move_x = 0
        move_y = 0

        # Vstupy
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

        # --- NORMALIZÁCIA RÝCHLOSTI (Aby po uhlopriečke nešiel rýchlejšie) ---
        if move_x != 0 and move_y != 0:
            # Ak ideš šikmo, vydelíme rýchlosť odmocninou z 2 (~1.414)
            # Matematicky: vector length = 1
            move_x *= 0.7071
            move_y *= 0.7071

        # Aplikovanie rýchlosti
        dx = move_x * self.speed
        dy = move_y * self.speed

        # --- KOLÍZIE X ---
        self.rect.x += dx
        for wall in collidable_walls:
            if self.rect.colliderect(wall):
                if dx > 0: self.rect.right = wall.left
                if dx < 0: self.rect.left = wall.right

        # --- KOLÍZIE Y ---
        self.rect.y += dy
        for wall in collidable_walls:
            if self.rect.colliderect(wall):
                if dy > 0: self.rect.bottom = wall.top
                if dy < 0: self.rect.top = wall.bottom

        # Aktualizácia spritu
        if move_x != 0 or move_y != 0:
            self.current_image = self.images[self.direction]

    def draw(self, surface, camera):
        # 1. Kde je hitbox na obrazovke?
        rect_on_screen = camera.apply(self.rect)
        
        # 2. Vypočítame, kde má byť OBRÁZOK relatívne k hitboxu
        # X: Posunúť doľava o rozdiel šírok / 2
        draw_x = rect_on_screen.x - (self.image_width - self.hitbox_w) // 2
        # Y: Posunúť hore o rozdiel výšok
        draw_y = rect_on_screen.y - (self.image_height - self.hitbox_h)
        
        surface.blit(self.current_image, (draw_x, draw_y))
        
        # DEBUG: Odkomentuj tento riadok, ak chceš vidieť hitbox (červený obdĺžnik pri nohách)
        # pygame.draw.rect(surface, (255, 0, 0), rect_on_screen, 1)