# game.py

import pygame, random, inspect
from settings import *
from interface import *
from player import Player
from enemy import *
from maze import *
from key import *
from tilemap import *
from camera import Camera

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
    enemies.extend(ENEMY_CHOICES[:(MAX_ENEMIES - len(ENEMY_DEFAULT_LIST))])  # Add two randomly selected enemy types

    enemy_objects = []
    maze, door_positions = generate_maze(ROWS, COLS)
    keys = generate_keys(maze, ROWS // 2, COLS // 2)
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

    camera = Camera(WIDTH, HEIGHT)

    return player, enemy_objects, maze, door_positions, keys, camera

def game_loop():
    player, enemy_objects, maze, door_positions, keys, camera = start_mechanics()   # Start summoning player and enemies
    tile_map = generate_tiles(maze)
    game_over = False
    game_over_start_time = None

    running = True
    while running:
        delta_time = clock.tick(FPS) / 1000.0  # Convert to seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == DOOR_LOCK_EVENT:
                toggle_door(maze, door_positions, 'locked')
                player.maze_interaction_triggered = True
                pygame.time.set_timer(DOOR_LOCK_EVENT, 0)
        
        # If game over, wait for 2 seconds and show game over screen
        if game_over:
            if time.time() - game_over_start_time > 2:
                if game_over_screen():
                    return  # Return to title screen
                game_over = False
            continue

        key_binds = pygame.key.get_pressed()
        if key_binds[pygame.K_w]:
            player.move(0, -1, maze)
        if key_binds[pygame.K_s]:
            player.move(0, 1, maze)
        if key_binds[pygame.K_a]:
            player.move(-1, 0, maze)
        if key_binds[pygame.K_d]:
            player.move(1, 0, maze)

        # Update player and enemy with time delta
        player.update_position(delta_time, door_positions, keys, maze)
        for enemy in enemy_objects:
            params = inspect.signature(enemy.move).parameters
            if 'player_direction' in params:
                enemy.move((player.x, player.y), player.current_state, maze, delta_time)
            else:
                enemy.move((player.x, player.y), maze, delta_time)

        # Check for collision with enemies
        if check_collision(player, enemy_objects):
            game_over = True
            game_over_start_time = time.time()
            continue

        # Check if the maze was modified
        if player.maze_interaction_triggered:
            tile_map = generate_tiles(maze)
            player.maze_interaction_triggered = False

        camera.follow((player.x, player.y), delta_time)
        WIN.fill(PATH_COLOR)

        draw_maze(maze, camera, tile_map)
        for key in keys:
            if not key.collected:
                key.draw(WIN, camera)
        
        player.draw(WIN, camera)
        for enemy in enemy_objects:
            enemy.draw(WIN, camera)

        pygame.display.update()

    pygame.quit()

def check_collision(player, enemies):
    # Check if any enemy has collided with the player
    buffer = 10
    player_rect = player.rect.inflate(-buffer, -buffer)
    for enemy in enemies:
        # Create a smaller collision box for each enemy
        enemy_rect = enemy.rect.inflate(-buffer, -buffer)
        if player_rect.colliderect(enemy_rect) and not player.is_immune:
            return True
    return False