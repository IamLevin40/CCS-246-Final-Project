# settings.py

import pygame

# Display settings
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 16  # Size of each tile in pixels
ROWS, COLS = 29, 29
INIT_SPEED_PLAYER = 7.2
INIT_SPEED_ENEMY = 6.0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game with AI Enemy")

# Frame rate
FPS = 60
clock = pygame.time.Clock()
