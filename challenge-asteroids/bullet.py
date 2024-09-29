import math
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (2, 2), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 10

    def update(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        angle_rad = math.radians(self.angle)
        self.rect.x += self.speed * math.sin(angle_rad)
        self.rect.y -= self.speed * math.cos(angle_rad)

        # Remove the bullet if it goes off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()