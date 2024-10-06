import pygame
import math

from bullet import Bullet

class Ship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.original_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (255, 255, 255), [(20, 0), (40, 40), (20, 30), (0, 40)])
        self.image = self.original_image  # Start with the original image
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.angle = 0  # Angle in degrees
        self.speed = 0  # Speed of the ship
        self.acceleration = 0.05  # Acceleration rate
        self.deceleration = 0.01  # Deceleration rate
        self.max_speed = 5  # Maximum speed

        self.bullets = pygame.sprite.Group()
        self.lives = 3  # Number of lives
        self.invincible = False  # Invincibility flag
        self.invincible_timer = 0  # Timer for invincibility
        self.invincible_duration = 3000  # 3 seconds of invincibility

    def update(self, keys, current_time):
        # Ship rotation
        if keys[pygame.K_LEFT]:
            self.angle -= 1
        if keys[pygame.K_RIGHT]:
            self.angle += 1

        # Ship acceleration
        if keys[pygame.K_UP]:
            self.speed += self.acceleration
            if self.speed > self.max_speed:
                self.speed = self.max_speed

        # Ship deceleration
        if not keys[pygame.K_UP]:
            self.speed -= self.deceleration
            if self.speed < 0:
                self.speed = 0

        # Update ship position
        angle_rad = math.radians(self.angle)

        # Update ship position based on angle and speed
        ship_dx = self.speed * math.sin(angle_rad)  # X-axis movement
        ship_dy = self.speed * math.cos(angle_rad)  # Y-axis movement

        # Invert the y-axis movement to account for Pygame's coordinate system
        self.rect.x += ship_dx
        self.rect.y -= ship_dy

        # Wrap around the screen
        if self.rect.right < 0:
            self.rect.left = self.screen_width
        elif self.rect.left > self.screen_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = self.screen_height
        elif self.rect.top > self.screen_height:
            self.rect.bottom = 0

        # Rotate the ship image
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Shooting
        if keys[pygame.K_SPACE]:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle)
            self.bullets.add(bullet)

        # Update bullets
        self.bullets.update(self.screen_width, self.screen_height)

        # Update invincibility timer
        if self.invincible:
            if current_time - self.invincible_timer > self.invincible_duration:
                self.invincible = False
    
    def draw_bullets(self, screen):
        self.bullets.draw(screen)
    
    def lose_life(self, current_time):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = current_time
            if self.lives <= 0:
                return True  # Game over
        return False