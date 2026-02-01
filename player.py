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
    def handle_keys(self, screen_width, screen_height):
        keys = pygame.key.get_pressed()

        #Detect diagonal movement
        moving_x = (keys[pygame.K_LEFT] or keys[pygame.K_a]) or (keys[pygame.K_RIGHT] or keys[pygame.K_d])
        moving_y = (keys[pygame.K_UP] or keys[pygame.K_w]) or (keys[pygame.K_DOWN] or keys[pygame.K_s])

        if moving_x and moving_y:
            current_speed = self.player_speed_diagonal  # diagonal speed
        else:
            current_speed = self.speed  # normal speed

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x > 0:
            self.rect.x -= current_speed  # CHANGED: use current_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < screen_width:
            self.rect.x += current_speed  # CHANGED
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y > 0:
            self.rect.y -= current_speed  # CHANGED
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < screen_height:
            self.rect.y += current_speed  # CHANGED

    # Draw the player on the given surface
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
