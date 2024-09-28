import pygame
import sys

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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button_bg_rect.collidepoint(mouse_pos):
                print("Starting new game...")
                # Here I will add the code to start the game
        elif event.type == pygame.VIDEORESIZE:
            # Handling the window resizing
            SCREEN_WIDTH, SCREEN_HEIGHT = event.size
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            title_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
            button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            button_bg_rect.center = button_rect.center

    screen.fill(BLACK)

    screen.blit(title_text, title_rect)

    screen.blit(button_bg, button_bg_rect)

    screen.blit(button_text, button_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()