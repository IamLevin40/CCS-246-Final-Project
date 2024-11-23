# settings.py

import pygame

# Display settings
WIDTH, HEIGHT = 960, 640
TILE_SIZE = 16  # Size of each tile in pixels
INIT_ROWS, INIT_COLS = 33, 33
PORTAL_STRUCTURE_SIZE = 3

# Colors
PATH_COLOR = (10, 10, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (50, 190, 50)
FLOOR_BG_COLOR = (248, 24, 87)
TIMER_BG_COLOR = (248, 199, 24)

# Paths to sprite images
PLAYER_SPRITES = {
    "rest": "sprites/player/rest.png",
    "up": "sprites/player/up.png",
    "down": "sprites/player/down.png",
    "left": "sprites/player/left.png",
    "right": "sprites/player/right.png"
}

PURSUER_SPRITES = {
    "rest": "sprites/enemies/pursuer/rest.png",
    "up": "sprites/enemies/pursuer/up.png",
    "down": "sprites/enemies/pursuer/down.png",
    "left": "sprites/enemies/pursuer/left.png",
    "right": "sprites/enemies/pursuer/right.png"
}

FEIGNER_SPRITES = {
    "rest": "sprites/enemies/feigner/rest.png",
    "up": "sprites/enemies/feigner/up.png",
    "down": "sprites/enemies/feigner/down.png",
    "left": "sprites/enemies/feigner/left.png",
    "right": "sprites/enemies/feigner/right.png"
}

AMBUSHER_SPRITES = {
    "rest": "sprites/enemies/ambusher/rest.png",
    "up": "sprites/enemies/ambusher/up.png",
    "down": "sprites/enemies/ambusher/down.png",
    "left": "sprites/enemies/ambusher/left.png",
    "right": "sprites/enemies/ambusher/right.png"
}

GLIMMER_SPRITES = {
    "rest": "sprites/enemies/glimmer/rest.png",
    "up": "sprites/enemies/glimmer/up.png",
    "down": "sprites/enemies/glimmer/down.png",
    "left": "sprites/enemies/glimmer/left.png",
    "right": "sprites/enemies/glimmer/right.png"
}

SPECTER_SPRITES = {
    "rest": "sprites/enemies/specter/rest.png",
    "up": "sprites/enemies/specter/up.png",
    "down": "sprites/enemies/specter/down.png",
    "left": "sprites/enemies/specter/left.png",
    "right": "sprites/enemies/specter/right.png"
}

SLENDER_SPRITES = {
    "rest": "sprites/enemies/slender/rest.png",
    "up": "sprites/enemies/slender/up.png",
    "down": "sprites/enemies/slender/down.png",
    "left": "sprites/enemies/slender/left.png",
    "right": "sprites/enemies/slender/right.png"
}

PATH_TILE_SPRITES = {
    # Four-direction patterns
    "side_end": "sprites/path_tiles/all_sides.png",
    "adjacent": "sprites/path_tiles/all_sides.png",
    "l_junction": "sprites/path_tiles/all_sides.png",
    "t_junction": "sprites/path_tiles/all_sides.png",
    "cross": "sprites/path_tiles/all_sides.png",
    "no_side": "sprites/path_tiles/all_sides.png",
    # Eight-direction patterns
    "edge": "sprites/path_tiles/all_sides.png",
    "violin": "sprites/path_tiles/all_sides.png",
    "axe": "sprites/path_tiles/all_sides.png",
    "rectangle": "sprites/path_tiles/all_sides.png",
    "fish": "sprites/path_tiles/all_sides.png",
    "chameleon": "sprites/path_tiles/all_sides.png",
    "butterfly": "sprites/path_tiles/all_sides.png",
    "one_twisted": "sprites/path_tiles/all_sides.png",
    "all_sides": "sprites/path_tiles/all_sides.png",
}

WALL_TILE_SPRITES = {
    # Four-direction patterns
    "side_end": "sprites/wall_tiles/side_end.png",
    "adjacent": "sprites/wall_tiles/adjacent.png",
    "l_junction": "sprites/wall_tiles/l_junction.png",
    "t_junction": "sprites/wall_tiles/t_junction.png",
    "cross": "sprites/wall_tiles/cross.png",
    "no_side": "sprites/wall_tiles/no_side.png",
    # Eight-direction patterns
    "edge": "sprites/wall_tiles/edge.png",
    "violin": "sprites/wall_tiles/violin.png",
    "axe": "sprites/wall_tiles/axe.png",
    "rectangle": "sprites/wall_tiles/rectangle.png",
    "fish": "sprites/wall_tiles/fish.png",
    "chameleon": "sprites/wall_tiles/chameleon.png",
    "butterfly": "sprites/wall_tiles/butterfly.png",
    "one_twisted": "sprites/wall_tiles/one_twisted.png",
    "all_sides": "sprites/wall_tiles/all_sides.png",
}

KEY_SPRITES = {
    "real": "sprites/keys/real.png",
    "fake": "sprites/keys/fake.png"
}

DOOR_TILE_SPRITES = {
    "locked": {
        "side_end": "sprites/structure_tiles/door/locked/side_end.png",
        "adjacent": "sprites/structure_tiles/door/locked/adjacent.png"
    },
    "unlocked": {
        "side_end": "sprites/structure_tiles/door/unlocked/side_end.png",
        "adjacent": "sprites/structure_tiles/door/unlocked/adjacent.png"
    },
    "incorrect": {
        "side_end": "sprites/structure_tiles/door/incorrect/side_end.png",
        "adjacent": "sprites/structure_tiles/door/incorrect/adjacent.png"
    }
}

STRUCTURE_FLOOR_TILE_SPRITES = {
    "side_end": "sprites/structure_tiles/floor/all_sides.png",
    "adjacent": "sprites/structure_tiles/floor/all_sides.png",
    "l_junction": "sprites/structure_tiles/floor/all_sides.png",
    "t_junction": "sprites/structure_tiles/floor/all_sides.png",
    "cross": "sprites/structure_tiles/floor/all_sides.png",
    "no_side": "sprites/structure_tiles/floor/all_sides.png"
}

STRUCTURE_PORTAL_TILE_SPRITES = {
    "side_end": "sprites/structure_tiles/portal/side_end.png",
    "adjacent": "sprites/structure_tiles/portal/adjacent.png"
}

# Initial attributes
INIT_TIMER = 60
INIT_MIN_BONUS_LIMIT = 30
INIT_SPEED_PLAYER = 100.0
ENEMIES = {
    "pursuer": {
        "init_speed": 5.6,
        "sprites": PURSUER_SPRITES
    },
    "feigner": {
        "init_speed": 5.6,
        "sprites": FEIGNER_SPRITES
    },
    "glimmer": {
        "init_speed": 5.6,
        "sprites": GLIMMER_SPRITES
    },
    "ambusher": {
        "init_speed": 5.6,
        "sprites": AMBUSHER_SPRITES
    },
    "specter": {
        "init_speed": 5.6,
        "sprites": SPECTER_SPRITES
    },
    "slender": {
        "init_speed": 5.6,
        "sprites": SLENDER_SPRITES
    }
}
INIT_MAX_ENEMIES = 3
MAX_FLOOR_TO_INCREASE_MAX_ENEMIES = 3
MAX_FLOOR_TO_INCREASE_MAZE_SIZE = 1

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Labyrinth")

# Frame rate
FPS = 60
clock = pygame.time.Clock()
