# maze.py

import random
from settings import *
from utils import *

PATH_TILES = {state: split_and_resize_sprite(path, TILE_SIZE) for state, path in PATH_TILE_SPRITES.items()}
WALL_TILES = {state: split_and_resize_sprite(path, TILE_SIZE) for state, path in WALL_TILE_SPRITES.items()}

def generate_maze(rows, cols):
    # Initialize the maze with walls ('X')
    maze = [['X' for _ in range(cols)] for _ in range(rows)]

    # Ensure the border remains as walls
    for i in range(rows):
        maze[i][0] = 'B'
        maze[i][cols - 1] = 'B'
    for j in range(cols):
        maze[0][j] = 'B'
        maze[rows - 1][j] = 'B'

    # Carve paths within the inner area only (1 to rows-2 and 1 to cols-2)
    def carve_path(x, y):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the next cell and the cell between the current and next cell are within bounds
            if 1 <= nx < rows - 1 and 1 <= ny < cols - 1 and maze[nx][ny] == 'X':
                maze[nx][ny] = 'O'  # Carve out path at target cell
                maze[x + dx // 2][y + dy // 2] = 'O'  # Carve out path in between
                carve_path(nx, ny)  # Recur for the next cell

    # Start carving from a central cell
    start_x, start_y = 1, 1
    maze[start_x][start_y] = 'O'
    carve_path(start_x, start_y)

    # Remove dead-ends by adding extra paths where needed
    remove_dead_ends(rows, cols, maze)

    # Further ensure no accidental border openings by checking the edges again
    for i in range(rows):
        maze[i][0] = 'X'
        maze[i][cols - 1] = 'X'
    for j in range(cols):
        maze[0][j] = 'X'
        maze[rows - 1][j] = 'X'

    return maze

def remove_dead_ends(rows, cols, maze):
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if maze[i][j] == 'O':
                # Count the number of open paths around the current cell
                exits = sum(1 for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                            if maze[i + dx][j + dy] == 'O')
                # If it has only one exit, add an additional connection
                if exits == 1:
                    for dx, dy in random.sample([(0, 1), (1, 0), (0, -1), (-1, 0)], 4):
                        nx, ny = i + dx, j + dy
                        if maze[nx][ny] == 'X':  # Make an opening to avoid dead-end
                            maze[nx][ny] = 'O'
                            maze[i + dx // 2][j + dy // 2] = 'O'
                            break

def add_zone(maze, enemy_x, enemy_y):
    # Zone for the player (center of the maze)
    center_x, center_y = ROWS // 2, COLS // 2
    for i in range(center_x - 1, center_x + 2):
        for j in range(center_y - 1, center_y + 2):
            maze[i][j] = 'O'

    # Enemy zone in a corner
    for i in range(enemy_x, enemy_x + 3):
        for j in range(enemy_y, enemy_y + 3):
            if 0 <= i < ROWS and 0 <= j < COLS:
                maze[j][i] = 'O'

    return maze

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
        (True, False, True, False): 'up_right',
        (True, False, False, True): 'up_left',
        (False, True, True, False): 'down_right',
        (False, True, False, True): 'down_left',
        (True, True, True, False): 'up_right_down',
        (True, True, False, True): 'up_left_down',
        (True, False, True, True): 'up_left_right',
        (False, True, True, True): 'down_left_right',
        (True, False, False, False): 'only_up',
        (False, False, True, False): 'only_right',
        (False, True, False, False): 'only_down',
        (False, False, False, True): 'only_left',
        (False, False, False, False): 'no_sides',
    }

    # Create a tuple of the connection values
    connection_tuple = (connections['up'], connections['down'], connections['left'], connections['right'])

    # Get the type key from the mapping
    return connection_map.get(connection_tuple, 'unknown')  # Default to 'unknown' if not found