import pygame

class Player:
    player_speed = 5
    player_speed_diagonal = player_speed / 1.4142  # Approximate for diagonal movement
    is_moving_diagonal = False
    
    # Initialize the player with position, size, and color
    def __init__(self, x, y, width, height, color):
        # --- NASTAVENIE HITBOXU ---
        self.full_height = height  # Uložíme si celú výšku obrázka
        self.hitbox_height = 25    # Výška kolíznej zóny (nohy)

        # Rect teraz reprezentuje LEN nohy.
        # Y súradnicu posunieme dole o (celá výška - výška nôh)
        self.rect = pygame.Rect(x, y + height - self.hitbox_height, width, self.hitbox_height)
        
        self.color = color
        self.speed = self.player_speed
        self.money = 0

        # --- NAČÍTANIE OBRÁZKOV ---
        self.images = {
            "down": pygame.image.load("Resources/Hugo/Hugo_Front1.png").convert_alpha(),
            "up": pygame.image.load("Resources/Hugo/Hugo_Back1.png").convert_alpha(),
            "left": pygame.image.load("Resources/Hugo/Hugo_Left1.png").convert_alpha(),
            "right": pygame.image.load("Resources/Hugo/Hugo_Right1.png").convert_alpha()
        }

        # Zmenšíme obrázky na veľkosť hráča
        for key in self.images:
            self.images[key] = pygame.transform.scale(
                self.images[key], (width, height)
            )

        self.direction = "down"
        self.current_image = self.images[self.direction]

    # Handle key presses for movement with screen collision detection
    def handle_keys_with_collision(self, screen_width, screen_height, collidable_walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
            self.direction = "left"

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
            self.direction = "right"

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
            self.direction = "up"

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
            self.direction = "down"

        # --- pohyb a kontrola kolízií (Hitbox sú len nohy) ---
        self.rect.x += dx
        for wall in collidable_walls:
            if self.rect.colliderect(wall):
                if dx > 0:  # pohyb doprava
                    self.rect.right = wall.left
                elif dx < 0:  # pohyb doľava
                    self.rect.left = wall.right

        self.rect.y += dy
        for wall in collidable_walls:
            if self.rect.colliderect(wall):
                if dy > 0:  # pohyb dole
                    self.rect.bottom = wall.top
                elif dy < 0:  # pohyb hore
                    self.rect.top = wall.bottom

        self.current_image = self.images[self.direction]

    # Draw the player on the given surface
    def draw(self, surface, camera):
        # Získame pozíciu hitboxu (nôh) na obrazovke
        rect_on_screen = camera.apply(self.rect)
        
        # Obrázok musíme vykresliť vyššie, aby nohy sedeli v hitboxe
        # Vypočítame Y pozíciu pre obrázok: (Y hitboxu) - (rozdiel výšok)
        draw_y = rect_on_screen.y - (self.full_height - self.hitbox_height)
        
        surface.blit(self.current_image, (rect_on_screen.x, draw_y))