import pygame
import math

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

    def update(self, keys):
        # Ship rotation
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5

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