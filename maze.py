import random
from settings import ROWS, COLS

def generate_maze(rows, cols):
    # Initialize the maze with walls ('X')
    maze = [['X' for _ in range(cols)] for _ in range(rows)]

    # Ensure the border remains as walls
    for i in range(rows):
        maze[i][0] = 'X'
        maze[i][cols - 1] = 'X'
    for j in range(cols):
        maze[0][j] = 'X'
        maze[rows - 1][j] = 'X'

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

    # Function to ensure no dead-ends by connecting single-exit paths to adjacent paths
    def remove_dead_ends():
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if maze[i][j] == 'O':
                    # Count the number of open paths around the current cell
                    exits = sum(1 for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                                if maze[i + dy][j + dx] == 'O')
                    # If it has only one exit, add an additional connection
                    if exits == 1:
                        for dx, dy in random.sample([(0, 1), (1, 0), (0, -1), (-1, 0)], 4):
                            nx, ny = j + dx, i + dy
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

def add_zone(maze, enemy_x, enemy_y):
    # zone for the player (center of the maze)
    center_x, center_y = ROWS // 2, COLS // 2
    for i in range(center_x - 1, center_x + 2):
        for j in range(center_y - 1, center_y + 2):
            maze[i][j] = 'S'

    # Enemy zone in a corner
    enemy_zone_x = enemy_x
    enemy_zone_y = enemy_y
    for i in range(enemy_zone_x, enemy_zone_x + 3):
        for j in range(enemy_zone_y, enemy_zone_y + 3):
            maze[i][j] = 'E'

    return maze
