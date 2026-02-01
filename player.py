import pygame

class Player:
    player_speed = 5
    player_speed_diagonal = player_speed / 1.4142  # Approximate for diagonal movement
    is_moving_diagonal = False
    
    # Initialize the player with position, size, and color
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = self.player_speed

    # Handle key presses for movement with screen collision detection
    def handle_keys_with_collision(self, screen_width, screen_height, collidable_walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        # --- pôvodný pohyb ---
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x > 0:
            dx -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < screen_width:
            dx += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y > 0:
            dy -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < screen_height:
            dy += self.speed

        # --- pohyb a kontrola kolízií ---
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


    # Draw the player on the given surface
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
