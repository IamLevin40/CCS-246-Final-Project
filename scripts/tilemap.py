# tilemap.py

import pygame, random
from settings import *

FOUR_DIRECTIONS = ['up', 'right', 'down', 'left']
ALL_DIRECTIONS = ['up', 'up_right', 'right', 'down_right', 'down', 'down_left', 'left', 'up_left']
connection_map = {
    # Four-direction patterns
    (True, False, False, False): 'side_end',
    (True, False, True, False): 'adjacent',
    (True, True, False, False): 'l_junction',
    (True, True, True, False): 't_junction',
    (True, True, True, True): 'cross',
    (False, False, False, False): 'no_side',
    # Eight-direction patterns
    (True, True, True, False, False, False, False, False): 'edge',
    (True, False, True, True, True, False, False, False): 'violin',
    (True, True, True, False, True, False, False, False): 'axe',
    (True, True, True, True, True, False, False, False): 'rectangle',
    (True, True, True, False, True, False, True, False): 'fish',
    (True, True, True, True, True, False, True, False): 'chameleon',
    (True, True, True, False, True, True, True, False): 'butterfly',
    (True, True, True, True, True, True, True, False): 'one_twisted',
    (True, True, True, True, True, True, True, True): 'all_sides',
}

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

def get_tile_type(x, y, maze, tile_type):
    # Guarantee a four-direction pattern match first
    connections_four = get_tile_connections(x, y, maze, tile_type, directions=FOUR_DIRECTIONS)
    type_key_four, rotation_four = get_pattern_with_rotation(connections_four, use_all_directions=False)

    # Check if the four-direction pattern key exists in the appropriate tile set
    tile_sprite = None
    if tile_type == 'X':
        tile_sprite = random.choice(WALL_TILES[type_key_four])
    elif tile_type == 'O':
        tile_sprite = random.choice(PATH_TILES[type_key_four])
    elif tile_type in ['DL', 'DU', 'DI']:
        door_state = {
            'DL': 'locked',
            'DU': 'unlocked',
            'DI': 'incorrect'
        }.get(tile_type)
        if door_state in DOOR_TILES:
            tile_sprite = random.choice(DOOR_TILES[door_state][type_key_four])
    elif tile_type == 'S':
        tile_sprite = random.choice(STRUCTURE_FLOOR_TILES[type_key_four])
    elif tile_type == 'P':
        tile_sprite = random.choice(STRUCTURE_PORTAL_TILES[type_key_four])

    # Next, check for an eight-direction pattern to potentially replace the four-direction pattern
    connections_eight = get_tile_connections(x, y, maze, tile_type, directions=ALL_DIRECTIONS)
    type_key_eight, rotation_eight = get_pattern_with_rotation(connections_eight, use_all_directions=True)

    # Update to eight-direction pattern if found in tile sets
    if tile_type == 'X' and type_key_eight in WALL_TILES:
        tile_sprite = random.choice(WALL_TILES[type_key_eight])
        rotation_needed = rotation_eight
    elif tile_type == 'O' and type_key_eight in PATH_TILES:
        tile_sprite = random.choice(PATH_TILES[type_key_eight])
        rotation_needed = rotation_eight
    else:
        # If no eight-direction pattern is found, use the four-direction pattern rotation
        rotation_needed = rotation_four
    
    # Rotate the sprite as required by the calculated rotation
    if tile_sprite is not None:
        tile_sprite = pygame.transform.rotate(tile_sprite, rotation_needed)

    return tile_sprite

def get_tile_connections(x, y, maze, tile_type, directions):
    connections = {}
    for direction in directions:
        dx, dy = get_offset(direction)
        nx, ny = x + dx, y + dy
        connections[direction] = (0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] == tile_type)
    return connections

def get_pattern_with_rotation(connections, use_all_directions=False):
    # Generate connection pattern
    pattern = tuple(connections[dir] for dir in (ALL_DIRECTIONS if use_all_directions else FOUR_DIRECTIONS))
    
    # Try to match the pattern or any of its rotations in the connection map
    for i, (rotated_pattern, rotation_degrees) in enumerate(get_rotations(pattern, use_all_directions)):
        if rotated_pattern in connection_map:
            return connection_map[rotated_pattern], rotation_degrees

    # Return 'unknown' if no pattern matches, with no rotation
    return 'unknown', 0

def get_rotations(pattern, use_all_directions):
    # Generate all rotations of the pattern and corresponding rotation angles in degrees
    rotation_count = 4 if not use_all_directions else 8
    rotations = []
    current_pattern = pattern

    for i in range(1, rotation_count + 1):
        # Calculate the rotation in degrees based on the iteration (90 degrees per rotation)
        rotation_degrees = i * 90
        current_pattern = rotate_pattern(current_pattern, use_all_directions)
        rotations.append((current_pattern, rotation_degrees))
    
    return rotations

def rotate_pattern(pattern, use_all_directions):
    # Rotate the pattern to simulate a 90-degree
    if use_all_directions:
        return pattern[-2:] + pattern[:-2]  # Rotate by one position in all directions
    else:
        return pattern[-1:] + pattern[:-1]  # Rotate by one position in four directions

def get_offset(direction):
    offsets = {
        'up': (0, -1),
        'up_right': (1, -1),
        'right': (1, 0),
        'down_right': (1, 1),
        'down': (0, 1),
        'down_left': (-1, 1),
        'left': (-1, 0),
        'up_left': (-1, -1)
    }
    return offsets[direction]