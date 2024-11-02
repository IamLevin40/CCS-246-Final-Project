# main.py

import pygame, random, inspect
from settings import *
from player import Player
from enemy import *
from maze import *
from tilemap import *
from camera import Camera

def draw_maze(maze, camera, tile_map):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            tile_sprite = tile_map[i][j]
            x, y = camera.apply_to_maze(j, i)
            
            if tile_sprite:  # Only draw if tile_sprite is not None
                WIN.blit(tile_sprite, (x, y))

def title_screen():
    running = True
    button_color = DARK_GREEN  # Green color for the button
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)  # Button rectangle

    while running:
        WIN.fill(PATH_COLOR)  # Clear the window with a white background

        # Render title text
        font = pygame.font.Font(None, 64)  # Use a default font with size 64
        title_surface = font.render("Dungeon Labyrinth", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        WIN.blit(title_surface, title_rect)  # Draw the title

        # Draw the play button
        pygame.draw.rect(WIN, button_color, button_rect)  # Draw the button
        button_font = pygame.font.Font(None, 36)
        button_surface = button_font.render("Play", True, WHITE)  # Button text color
        button_text_rect = button_surface.get_rect(center=button_rect.center)
        WIN.blit(button_surface, button_text_rect)  # Draw the button text

        pygame.display.update()  # Update the display

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button press
                if event.button == 1:  # Left mouse button
                    if button_rect.collidepoint(event.pos):  # Check if clicked inside button
                        running = False  # Exit the title screen loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Check if Enter is pressed
                    running = False  # Exit the title screen loop

def start_mechanics():
    # Player spawns in the center of the player safe zone
    player_start_x = ROWS // 2
    player_start_y = COLS // 2
    player = Player(player_start_x, player_start_y, INIT_SPEED_PLAYER)

    # Dictionary mapping enemy type names to their classes
    ENEMY_CLASSES = {
        "pursuer": Pursuer,
        "feigner": Feigner,
        "glimmer": Glimmer,
        "ambusher": Ambusher
    }
    enemies = ENEMY_DEFAULT_LIST
    random.shuffle(ENEMY_CHOICES)
    enemies.extend(ENEMY_CHOICES[:MAX_RANDOM_ENEMIES])  # Add two randomly selected enemy types

    enemy_objects = []
    maze = generate_maze(ROWS, COLS)
    used_positions = set()  # Set to track used (x, y) coordinates

    # Instantiate each enemy and add a safe zone for them in the maze
    for enemy_type in enemies:
        enemy_x, enemy_y = None, None
        # Find a unique position for each enemy
        while True:
            enemy_x = random.choice([1, ROWS - 4])
            enemy_y = random.choice([1, COLS - 4])
            if (enemy_x, enemy_y) not in used_positions:
                used_positions.add((enemy_x, enemy_y))
                break  # Exit loop once we find a unique position

        maze = add_zone(maze, enemy_x, enemy_y)  # Add safe zone for the enemy
        enemy_class = ENEMY_CLASSES[enemy_type]
        enemy_objects.append(enemy_class(enemy_x, enemy_y, enemy_type))

    tile_map = generate_tiles(maze)
    camera = Camera(WIDTH, HEIGHT)

    return player, enemy_objects, maze, tile_map, camera

def game_loop():
    player, enemy_objects, maze, tile_map, camera = start_mechanics()   # Start summoning player and enemies
    running = True
    while running:
        delta_time = clock.tick(FPS) / 1000.0  # Convert to seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, -1, maze)
        if keys[pygame.K_s]:
            player.move(0, 1, maze)
        if keys[pygame.K_a]:
            player.move(-1, 0, maze)
        if keys[pygame.K_d]:
            player.move(1, 0, maze)

        # Update player and enemy with time delta
        player.update_position(delta_time)
        for enemy in enemy_objects:
            params = inspect.signature(enemy.move).parameters
            if 'player_direction' in params:
                enemy.move((player.x, player.y), player.current_state, maze, delta_time)
            else:
                enemy.move((player.x, player.y), maze, delta_time)
        camera.follow((player.x, player.y), delta_time)

        WIN.fill(PATH_COLOR)
        draw_maze(maze, camera, tile_map)
        
        player.draw(WIN, camera)
        for enemy in enemy_objects:
            enemy.draw(WIN, camera)
        pygame.display.update()

    pygame.quit()

def main():
    title_screen()      # Show the title screen first
    game_loop()         # Start game looping
    

if __name__ == "__main__":
    main()
