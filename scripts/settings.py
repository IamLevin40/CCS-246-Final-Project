# settings.py

import pygame

# Display settings
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 16  # Size of each tile in pixels
ROWS, COLS = 29, 29
INIT_SPEED_PLAYER = 7.2
INIT_SPEED_ENEMY = 6.0

# Colors
PATH_COLOR = (10, 10, 10)
WALL_COLOR = (107, 51, 189)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (50, 190, 50)

# Paths to sprite images
PLAYER_SPRITES = {
    "rest": "sprites/player_rest.png",
    "up": "sprites/player_up.png",
    "down": "sprites/player_down.png",
    "left": "sprites/player_left.png",
    "right": "sprites/player_right.png"
}

ENEMY_SPRITES = {
    "rest": "sprites/enemy_rest.png",
    "up": "sprites/enemy_up.png",
    "down": "sprites/enemy_down.png",
    "left": "sprites/enemy_left.png",
    "right": "sprites/enemy_right.png"
}

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Labyrinth")

# Frame rate
FPS = 60
clock = pygame.time.Clock()
