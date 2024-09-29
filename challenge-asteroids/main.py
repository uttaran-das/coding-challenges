import pygame
import sys

from asteroid import Asteroid

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Asteroids")

font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 48)

title_text = font.render("Asteroids", True, WHITE)
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

button_text = button_font.render("Start New Game", True, BLACK)
button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

button_bg = pygame.Surface((button_rect.width + 20, button_rect.height + 20))
button_bg.fill(WHITE)
button_bg_rect = button_bg.get_rect(center=button_rect.center)

# Ship settings
ship_image = pygame.Surface((40, 40), pygame.SRCALPHA)
ship_rect = ship_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
pygame.draw.polygon(ship_image, WHITE, [(20, 0), (40, 40), (20, 30), (0, 40)])

# Game state
game_state = "menu"
asteroids = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if game_state == "menu" and button_bg_rect.collidepoint(mouse_pos):
                game_state = "playing"
                asteroids.empty()
                for _ in range(10):
                    asteroids.add(Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT))
        elif event.type == pygame.VIDEORESIZE:
            # Handling the window resizing
            SCREEN_WIDTH, SCREEN_HEIGHT = event.size
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            title_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
            button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            button_bg_rect.center = button_rect.center
            ship_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    screen.fill(BLACK)

    if game_state == "menu":
        screen.blit(title_text, title_rect)
        screen.blit(button_bg, button_bg_rect)
        screen.blit(button_text, button_rect)
    elif game_state == "playing":
        # Draw the ship
        screen.blit(ship_image, ship_rect)
        # Update and draw asteroids
        asteroids.update()
        asteroids.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()