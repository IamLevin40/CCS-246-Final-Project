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
    "rest": "sprites/player/player_rest.png",
    "up": "sprites/player/player_up.png",
    "down": "sprites/player/player_down.png",
    "left": "sprites/player/player_left.png",
    "right": "sprites/player/player_right.png"
}

ENEMY_SPRITES = {
    "rest": "sprites/enemy/enemy_rest.png",
    "up": "sprites/enemy/enemy_up.png",
    "down": "sprites/enemy/enemy_down.png",
    "left": "sprites/enemy/enemy_left.png",
    "right": "sprites/enemy/enemy_right.png"
}

PATH_TILE_SPRITES = {
    "all_sides": "",
    "up_down": "",
    "left_right": "",
    "up_right": "",
    "up_left": "",
    "down_right": "",
    "down_left": "",
    "up_right_down": "",
    "up_left_down": "",
    "up_left_right": "",
    "down_left_right": "",
    "only_up": "",
    "only_right": "",
    "only_down": "",
    "only_left": "",
    "no_sides": "",
}

WALL_TILE_SPRITES = {
    "all_sides": "",
    "up_down": "",
    "left_right": "",
    "up_right": "",
    "up_left": "",
    "down_right": "",
    "down_left": "",
    "up_right_down": "",
    "up_left_down": "",
    "up_left_right": "",
    "down_left_right": "",
    "only_up": "",
    "only_right": "",
    "only_down": "",
    "only_left": "",
    "no_sides": "",
}

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Labyrinth")

# Frame rate
FPS = 60
clock = pygame.time.Clock()
