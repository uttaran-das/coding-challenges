import pygame
import random

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(0, screen_height)
        self.speed_x = random.uniform(-0.2, 0.2)
        self.speed_y = random.uniform(-0.2, 0.2)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        points = [(random.randint(0, 50), random.randint(0, 50)) for _ in range(10)]
        pygame.draw.polygon(self.image, (255, 255, 255), points)

    def update(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        # Wrap around the screen
        if self.rect.right < 0:
            self.rect.left = self.screen_width
            self.pos_x = self.rect.x
        elif self.rect.left > self.screen_width:
            self.rect.right = 0
            self.pos_x = self.rect.x
        if self.rect.bottom < 0:
            self.rect.top = self.screen_height
            self.pos_y = self.rect.y
        elif self.rect.top > self.screen_height:
            self.rect.bottom = 0
            self.pos_y = self.rect.y