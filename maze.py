# maze.py

import random
from settings import ROWS, COLS

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
    def carve_path(y, x):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dy, dx in directions:
            ny, nx = y + dy, x + dx

            # Check if the next cell and the cell between the current and next cell are within bounds
            if 1 <= ny < rows - 1 and 1 <= nx < cols - 1 and maze[ny][nx] == 'X':
                maze[ny][nx] = 'O'  # Carve out path at target cell
                maze[y + dy // 2][x + dx // 2] = 'O'  # Carve out path in between
                carve_path(ny, nx)  # Recur for the next cell

    # Start carving from a central cell
    start_y, start_x = 1, 1
    maze[start_y][start_x] = 'O'
    carve_path(start_y, start_x)

    # Function to ensure no dead-ends by connecting single-exit paths to adjacent paths
    def remove_dead_ends():
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if maze[i][j] == 'O':
                    # Count the number of open paths around the current cell
                    exits = sum(1 for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                                if maze[i + dy][j + dx] == 'O')
                    # If it has only one exit, add an additional connection
                    if exits == 1:
                        for dy, dx in random.sample([(0, 1), (1, 0), (0, -1), (-1, 0)], 4):
                            ny, nx = i + dy, j + dx
                            if maze[ny][nx] == 'X':  # Make an opening to avoid dead-end
                                maze[ny][nx] = 'O'
                                maze[i + dy // 2][j + dx // 2] = 'O'
                                break

    # Remove dead-ends by adding extra paths where needed
    remove_dead_ends()

    # Further ensure no accidental border openings by checking the edges again
    for i in range(rows):
        maze[i][0] = 'X'
        maze[i][cols - 1] = 'X'
    for j in range(cols):
        maze[0][j] = 'X'
        maze[rows - 1][j] = 'X'

    return maze

def add_zone(maze, enemy_y, enemy_x):
    # zone for the player (center of the maze)
    center_y, center_x = ROWS // 2, COLS // 2
    for i in range(center_y - 1, center_y + 2):
        for j in range(center_x - 1, center_x + 2):
            maze[i][j] = 'S'

    # enemy zone in a corner
    for i in range(enemy_y, enemy_y + 3):
        for j in range(enemy_x, enemy_x + 3):
            maze[i][j] = 'E'

    return maze
