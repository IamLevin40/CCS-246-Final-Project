# settings.py

import pygame

# Display settings
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 16  # Size of each tile in pixels
ROWS, COLS = 33, 33
INIT_SPEED_PLAYER = 7.2
INIT_SPEED_ENEMY = 6.0

# Colors
PATH_COLOR = (10, 10, 10)
# WALL_COLOR = (107, 51, 189)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (50, 190, 50)

# Paths to sprite images
PLAYER_SPRITES = {
    "rest": "sprites/player/rest.png",
    "up": "sprites/player/up.png",
    "down": "sprites/player/down.png",
    "left": "sprites/player/left.png",
    "right": "sprites/player/right.png"
}

ENEMY_SPRITES = {
    "rest": "sprites/enemy/rest.png",
    "up": "sprites/enemy/up.png",
    "down": "sprites/enemy/down.png",
    "left": "sprites/enemy/left.png",
    "right": "sprites/enemy/right.png"
}

PATH_TILE_SPRITES = {
    "all_sides": "sprites/path_tiles/all_sides.png",
    "up_down": "sprites/path_tiles/all_sides.png",
    "left_right": "sprites/path_tiles/all_sides.png",
    "up_right": "sprites/path_tiles/all_sides.png",
    "up_left": "sprites/path_tiles/all_sides.png",
    "down_right": "sprites/path_tiles/all_sides.png",
    "down_left": "sprites/path_tiles/all_sides.png",
    "up_right_down": "sprites/path_tiles/all_sides.png",
    "up_left_down": "sprites/path_tiles/all_sides.png",
    "up_left_right": "sprites/path_tiles/all_sides.png",
    "down_left_right": "sprites/path_tiles/all_sides.png",
    "only_up": "sprites/path_tiles/all_sides.png",
    "only_right": "sprites/path_tiles/all_sides.png",
    "only_down": "sprites/path_tiles/all_sides.png",
    "only_left": "sprites/path_tiles/all_sides.png",
    "no_sides": "sprites/path_tiles/all_sides.png",
}

WALL_TILE_SPRITES = {
    "all_sides": "sprites/wall_tiles/all_sides.png",
    "up_down": "sprites/wall_tiles/up_down.png",
    "left_right": "sprites/wall_tiles/left_right.png",
    "up_right": "sprites/wall_tiles/up_right.png",
    "up_left": "sprites/wall_tiles/up_left.png",
    "down_right": "sprites/wall_tiles/down_right.png",
    "down_left": "sprites/wall_tiles/down_left.png",
    "up_right_down": "sprites/wall_tiles/up_right_down.png",
    "up_left_down": "sprites/wall_tiles/up_left_down.png",
    "up_left_right": "sprites/wall_tiles/up_left_right.png",
    "down_left_right": "sprites/wall_tiles/down_left_right.png",
    "only_up": "sprites/wall_tiles/only_up.png",
    "only_right": "sprites/wall_tiles/only_right.png",
    "only_down": "sprites/wall_tiles/only_down.png",
    "only_left": "sprites/wall_tiles/only_left.png",
    "no_sides": "sprites/wall_tiles/no_sides.png",
}

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Labyrinth")

# Frame rate
FPS = 60
clock = pygame.time.Clock()
