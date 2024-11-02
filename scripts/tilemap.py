# tilemap.py

import random
from settings import *
from utils import *

PATH_TILES = {state: split_and_resize_sprite(path, TILE_SIZE) for state, path in PATH_TILE_SPRITES.items()}
WALL_TILES = {state: split_and_resize_sprite(path, TILE_SIZE) for state, path in WALL_TILE_SPRITES.items()}

def get_tile_type(x, y, maze, tile_type):
    # Determine tile type based on surrounding tiles and select a random sprite variation
    up = maze[y - 1][x] if y > 0 else None
    down = maze[y + 1][x] if y < len(maze) - 1 else None
    left = maze[y][x - 1] if x > 0 else None
    right = maze[y][x + 1] if x < len(maze[0]) - 1 else None

    connections = {
        'up': up == tile_type,
        'down': down == tile_type,
        'left': left == tile_type,
        'right': right == tile_type
    }

    # Determine the type key based on connections
    type_key = get_connection_type(connections)
    if tile_type == 'X':
        return random.choice(WALL_TILES[type_key])
    elif tile_type == 'O':
        return random.choice(PATH_TILES[type_key])
    
def generate_tiles(maze):
    # Generates the correct tile sprites for the entire maze
    tile_map = []
    for y, row in enumerate(maze):
        tile_row = []
        for x, tile in enumerate(row):
            tile_sprite = get_tile_type(x, y, maze, tile)
            tile_row.append(tile_sprite)
        tile_map.append(tile_row)
    return tile_map

def get_connection_type(connections):
    # Mapping of connection combinations to their respective type keys
    connection_map = {
        (True, True, True, True): 'all_sides',
        (True, True, False, False): 'up_down',
        (False, False, True, True): 'left_right',
        (True, False, False, True): 'up_right',
        (True, False, True, False): 'up_left',
        (False, True, False, True): 'down_right',
        (False, True, True, False): 'down_left',
        (True, True, False, True): 'up_right_down',
        (True, True, True, False): 'up_left_down',
        (True, False, True, True): 'up_left_right',
        (False, True, True, True): 'down_left_right',
        (True, False, False, False): 'only_up',
        (False, False, False, True): 'only_right',
        (False, True, False, False): 'only_down',
        (False, False, True, False): 'only_left',
        (False, False, False, False): 'no_sides',
    }

    # Create a tuple of the connection values
    connection_tuple = (connections['up'], connections['down'], connections['left'], connections['right'])

    # Get the type key from the mapping
    return connection_map.get(connection_tuple, 'unknown')  # Default to 'unknown' if not found