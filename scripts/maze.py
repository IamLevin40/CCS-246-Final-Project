# maze.py

import random, math
from settings import *
from utils import *

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

                # Add extra connections randomly to create multiple paths
                if random.random() < 0.4:
                    additional_connection(x, y, rows, cols, maze)

    # Start carving from a central cell
    start_x, start_y = 1, 1
    maze[start_x][start_y] = 'O'
    carve_path(start_x, start_y)
    remove_dead_ends(rows, cols, maze)

    door_positions = add_portal_structure(rows, cols, maze, PORTAL_STRUCTURE_SIZE)
    ensure_border_closed(rows, cols, maze)

    return maze, door_positions

def additional_connection(x, y, rows, cols, maze):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 1 <= nx < rows - 1 and 1 <= ny < cols - 1 and maze[nx][ny] == 'X':
            maze[nx][ny] = 'O'
            break

def remove_dead_ends(rows, cols, maze):
    # Remove dead-ends by adding extra paths where needed
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

def ensure_border_closed(rows, cols, maze):
    # Further ensure no accidental border openings by checking the edges again
    for i in range(rows):
        maze[i][0] = 'X'
        maze[i][cols - 1] = 'X'
    for j in range(cols):
        maze[0][j] = 'X'
        maze[rows - 1][j] = 'X'

def add_zone(rows, cols, maze, enemy_x, enemy_y):
    # Zone for the player (center of the maze)
    center_x, center_y = rows // 2, cols // 2
    for i in range(center_x - 1, center_x + 2):
        for j in range(center_y - 1, center_y + 2):
            maze[i][j] = 'O'

    # Enemy zone in a corner
    for i in range(enemy_x, enemy_x + 3):
        for j in range(enemy_y, enemy_y + 3):
            if 0 <= i < rows and 0 <= j < cols:
                maze[j][i] = 'O'

    return maze

def add_portal_structure(rows, cols, maze, dimension):
    # Calculate sizes based on the dimension
    wall_size = dimension + 2  # Wall boundary size
    path_size = dimension + 4  # Path boundary size
    
    # Define possible structure positions
    structure_positions = {
        'top': (-1, cols // 2 - math.ceil(wall_size / 2)),
        'bottom': (rows - (wall_size + 1), cols // 2 - math.ceil(wall_size / 2)),
        'left': (rows // 2 - math.ceil(wall_size / 2), -1),
        'right': (rows // 2 - math.ceil(wall_size / 2), cols - (wall_size + 1))
    }
    
    selected_key = random.choice(list(structure_positions.keys()))
    position = structure_positions[selected_key]
    struct_x, struct_y = position

    # Create the path boundary
    for i in range(struct_x, struct_x + path_size):
        for j in range(struct_y, struct_y + path_size):
            if 0 <= i < rows and 0 <= j < cols:
                maze[i][j] = 'O'  # Initialize as path

    # Create the wall boundary around the structure
    for i in range(struct_x + 1, struct_x + (wall_size + 1)):
        for j in range(struct_y + 1, struct_y + (wall_size + 1)):
            if (i == struct_x + 1 or i == struct_x + wall_size or
                j == struct_y + 1 or j == struct_y + wall_size):
                maze[i][j] = 'X'  # Wall boundary

    # Create the structure in the center
    for i in range(struct_x + 2, struct_x + wall_size):
        for j in range(struct_y + 2, struct_y + wall_size):
            maze[i][j] = 'S'  # Structure floor

    # Define door and portal positions based on the selected key
    door_positions = []
    door_position_map = {
        'top': (struct_x + wall_size, range(struct_y + 2, struct_y + wall_size)),
        'bottom': (struct_x + 1, range(struct_y + 2, struct_y + wall_size)),
        'left': (range(struct_x + 2, struct_x + wall_size), struct_y + wall_size),
        'right': (range(struct_x + 2, struct_x + wall_size), struct_y + 1)
    }

    portal_position_map = {
        'top': (struct_x + dimension, range(struct_y + 2, struct_y + wall_size)),
        'bottom': (struct_x + dimension, range(struct_y + 2, struct_y + wall_size)),
        'left': (range(struct_x + 2, struct_x + wall_size), struct_y + dimension),
        'right': (range(struct_x + 2, struct_x + wall_size), struct_y + dimension)
    }

    # Create door and portal using the combined function
    def create_structure(structure_type, position_info):
        row, col = position_info
        if isinstance(row, int):  # For top and bottom structures
            for j in col:
                maze[row][j] = structure_type
                if structure_type == 'DL':
                    door_positions.append((row, j))
        else:  # For left and right structures
            for i in row:
                maze[i][col] = structure_type
                if structure_type == 'DL':
                    door_positions.append((i, col))

    # Create door and portal using the combined function
    create_structure('DL', door_position_map[selected_key])  # Create door
    create_structure('P', portal_position_map[selected_key])  # Create portal

    return door_positions

def toggle_door(maze, door_positions, toggler):
    # Toggle the state of all doors between locked and unlocked
    toggles = {
        'locked': 'DL',
        'unlocked': 'DU',
        'incorrect': 'DI'
    }
    for pos in door_positions:
        maze[pos[0]][pos[1]] = toggles[toggler]