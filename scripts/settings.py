# settings.py

import pygame
from utils import *


# Display settings
WIDTH, HEIGHT = 960, 640
TILE_SIZE = 16  # Size of each tile in pixels
INIT_ROWS, INIT_COLS = 33, 33
PORTAL_STRUCTURE_SIZE = 3

# Colors
PATH_COLOR = (10, 10, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHADOW = (15, 15, 15)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (50, 190, 50)
FLOOR_BG_COLOR = (254, 80, 109)
TIMER_BG_COLOR = (248, 199, 24)

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tomb Rush")

# Frame rate
FPS = 60

# Paths to resources
FONTS = {
    "colonna": "resources/fonts/colonna.ttf"
}

AUDIO = {
    "music": {
        "the_labyrinth": "resources/audio/music/niviro-the_labyrinth.mp3",
        "haunted_pumpkin": "resources/audio/music/haunted_pumpkin.mp3"
    },
    "sfx": {
        "button_pressed": ["resources/audio/sfx/button_pressed_1.mp3", "resources/audio/sfx/button_pressed_2.mp3"],
        "key_collected": "resources/audio/sfx/key_collected.mp3",
        "real_key_used": "resources/audio/sfx/real_key_used.mp3",
        "fake_key_used": "resources/audio/sfx/fake_key_used.mp3",
        "powerup_collected": "resources/audio/sfx/powerup_collected.mp3",
        "skill_activated": "resources/audio/sfx/skill_activated.mp3",
        "retreat_teleported_to_safe_zone": "resources/audio/sfx/retreat_teleported_to_safe_zone.mp3",
        "portal_teleporting": "resources/audio/sfx/portal_teleporting.mp3",
        "pursuer_ambient": "resources/audio/sfx/pursuer_ambient.mp3",
        "feigner_ambient": "resources/audio/sfx/feigner_ambient.mp3",
        "ambusher_ambient": "resources/audio/sfx/ambusher_ambient.mp3",
        "glimmer_ambient": "resources/audio/sfx/glimmer_ambient.mp3",
        "specter_special_ambient": "resources/audio/sfx/specter_special_ambient.mp3",
        "slender_special_ambient": "resources/audio/sfx/slender_special_ambient.mp3"
    }
}

# Paths to sprite images
PLAYER_SPRITES = {
    "up": "sprites/player/up.png",
    "down": "sprites/player/down.png",
    "left": "sprites/player/left.png",
    "right": "sprites/player/right.png"
}

PURSUER_SPRITES = {
    "up": "sprites/enemies/pursuer/up.png",
    "down": "sprites/enemies/pursuer/down.png",
    "left": "sprites/enemies/pursuer/left.png",
    "right": "sprites/enemies/pursuer/right.png"
}

FEIGNER_SPRITES = {
    "up": "sprites/enemies/feigner/up.png",
    "down": "sprites/enemies/feigner/down.png",
    "left": "sprites/enemies/feigner/left.png",
    "right": "sprites/enemies/feigner/right.png"
}

AMBUSHER_SPRITES = {
    "up": "sprites/enemies/ambusher/up.png",
    "down": "sprites/enemies/ambusher/down.png",
    "left": "sprites/enemies/ambusher/left.png",
    "right": "sprites/enemies/ambusher/right.png"
}

GLIMMER_SPRITES = {
    "up": "sprites/enemies/glimmer/up.png",
    "down": "sprites/enemies/glimmer/down.png",
    "left": "sprites/enemies/glimmer/left.png",
    "right": "sprites/enemies/glimmer/right.png"
}

SPECTER_SPRITES = {
    "up": "sprites/enemies/specter/up.png",
    "down": "sprites/enemies/specter/down.png",
    "left": "sprites/enemies/specter/left.png",
    "right": "sprites/enemies/specter/right.png",
    "special": "sprites/enemies/specter/special.png"
}

SLENDER_SPRITES = {
    "up": "sprites/enemies/slender/up.png",
    "down": "sprites/enemies/slender/down.png",
    "left": "sprites/enemies/slender/left.png",
    "right": "sprites/enemies/slender/right.png",
    "special": "sprites/enemies/slender/special.png"
}

PATH_TILE_SPRITES = {
    # Four-direction patterns
    "side_end": "sprites/path_tiles/side_end.png",
    "adjacent": "sprites/path_tiles/adjacent.png",
    "l_junction": "sprites/path_tiles/l_junction.png",
    "t_junction": "sprites/path_tiles/t_junction.png",
    "cross": "sprites/path_tiles/cross.png",
    "no_side": "sprites/path_tiles/no_side.png",
    # Eight-direction patterns
    "edge": "sprites/path_tiles/edge.png",
    "violin": "sprites/path_tiles/violin.png",
    "axe": "sprites/path_tiles/axe.png",
    "rectangle": "sprites/path_tiles/rectangle.png",
    "fish": "sprites/path_tiles/fish.png",
    "chameleon": "sprites/path_tiles/chameleon.png",
    "butterfly": "sprites/path_tiles/butterfly.png",
    "one_twisted": "sprites/path_tiles/one_twisted.png",
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

POWERUP_SPRITES = {
    "rocket_boost": "sprites/powerups/rocket_boost.png",
    "retreat": "sprites/powerups/retreat.png",
    "immunity": "sprites/powerups/immunity.png",
    "slow_move": "sprites/powerups/slow_move.png"
}

KEYPAD_SPRITES = {
    "keypad_w": "sprites/keypads/keypad_w.png",
    "keypad_a": "sprites/keypads/keypad_a.png",
    "keypad_s": "sprites/keypads/keypad_s.png",
    "keypad_d": "sprites/keypads/keypad_d.png",
    "keypad_e": "sprites/keypads/keypad_e.png",
    "keypad_r": "sprites/keypads/keypad_r.png"
}

UI_ICON_SPRITES = {
    "title_screen_bg": "sprites/ui_icons/title_screen_bg.png",
    "title": "sprites/ui_icons/title.png",
    "start_button": "sprites/ui_icons/start_button.png",
    "exit_button": "sprites/ui_icons/exit_button.png",
    "hover_icon": "sprites/ui_icons/hover_icon.png",
    "inventory_holder": "sprites/ui_icons/inventory_holder.png",
    "stats_holder": "sprites/ui_icons/stats_holder.png",
    "floor": "sprites/ui_icons/floor.png",
    "clock": "sprites/ui_icons/clock.png",
    "game_over_bg": "sprites/ui_icons/game_over_bg.png",
    "died_text": "sprites/ui_icons/died_text.png",
    "back_button": "sprites/ui_icons/back_button.png"
}

PATH_TILES = {state: split_and_resize_sprite(path, TILE_SIZE) for state, path in PATH_TILE_SPRITES.items()}
WALL_TILES = {state: split_and_resize_sprite(path, TILE_SIZE) for state, path in WALL_TILE_SPRITES.items()}
DOOR_TILES = {state: {pattern: split_and_resize_sprite(path, TILE_SIZE) for pattern, path in patterns.items()} for state, patterns in DOOR_TILE_SPRITES.items()}
STRUCTURE_FLOOR_TILES = {state: split_and_resize_sprite(path, TILE_SIZE) for state, path in STRUCTURE_FLOOR_TILE_SPRITES.items()}
STRUCTURE_PORTAL_TILES = {state: split_and_resize_sprite(path, TILE_SIZE) for state, path in STRUCTURE_PORTAL_TILE_SPRITES.items()}

KEY_OBJECTS = {state: split_and_resize_sprite(path, TILE_SIZE)[0] for state, path in KEY_SPRITES.items()}
POWERUP_OBJECTS = {name: split_and_resize_sprite(path, TILE_SIZE)[0] for name, path in POWERUP_SPRITES.items()}
KEYPAD_OBJECTS = {name: split_and_resize_sprite(path) for name, path in KEYPAD_SPRITES.items()}
UI_ICON_OBJECTS = {name: split_and_resize_sprite(path) for name, path in UI_ICON_SPRITES.items()}


# Initial attributes
INIT_TIMER = 60
INIT_MIN_BONUS_LIMIT = 30
INIT_SPEED_PLAYER = 108.0
ENEMIES = {
    "pursuer": {
        "init_speed": 6.4,
        "sprites": PURSUER_SPRITES,
        "offset_y": -8.0
    },
    "feigner": {
        "init_speed": 6.4,
        "sprites": FEIGNER_SPRITES,
        "offset_y": -8.0
    },
    "glimmer": {
        "init_speed": 6.4,
        "sprites": GLIMMER_SPRITES,
        "offset_y": -8.0
    },
    "ambusher": {
        "init_speed": 6.4,
        "sprites": AMBUSHER_SPRITES,
        "offset_y": 0
    },
    "specter": {
        "init_speed": 6.4,
        "sprites": SPECTER_SPRITES,
        "offset_y": -4.0
    },
    "slender": {
        "init_speed": 6.4,
        "sprites": SLENDER_SPRITES,
        "offset_y": -8.0
    }
}
INIT_MAX_ENEMIES = 3
MAX_FLOOR_TO_INCREASE_MAX_ENEMIES = 3
MAX_FLOOR_TO_UNLOCK_NEW_ENEMY = 3
MAX_FLOOR_TO_INCREASE_MAZE_SIZE = 1
INIT_POWERUP_ACTIVATE_COOLDOWN = 2.5
INIT_POWERUP_SPAWN_COOLDOWN = 8
MAX_POWERUPS = 4
MAX_KEYS = 4
