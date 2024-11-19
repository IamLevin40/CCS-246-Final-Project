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

def start_mechanics(existing_player=None):
    # Calculate rows and cols based on the player floor
    rows = INIT_ROWS
    cols = INIT_COLS
    
    # Player spawns in the center of the player safe zone
    if existing_player:
        player = existing_player
        
        # Calculate rows and cols based on the player floor
        rows = rows + (math.floor((player.floor - 1) * (1 / MAX_FLOOR_TO_INCREASE_MAZE_SIZE)) * 2)
        cols = cols + (math.floor((player.floor - 1) * (1 / MAX_FLOOR_TO_INCREASE_MAZE_SIZE)) * 2)
        
        player.x, player.y = rows // 2, cols // 2  # Reset player position
        player.float_x, player.float_y = player.x, player.y
        player.target_pos = (player.x, player.y)
        player.current_tile = ''
    else:
        # Player spawns in the center of the player safe zone
        player = Player(rows // 2, cols // 2, INIT_SPEED_PLAYER)

    # Dictionary mapping enemy type names to their classes
    ENEMY_CLASSES = {
        "pursuer": Pursuer,
        "feigner": Feigner,
        "glimmer": Glimmer,
        "ambusher": Ambusher
    }
    enemies = ENEMY_DEFAULT_LIST
    selected_enemies = random.sample(ENEMY_CHOICES, (MAX_ENEMIES - len(ENEMY_DEFAULT_LIST)))
    enemies.extend(selected_enemies)

    enemy_objects = []
    maze, door_positions = generate_maze(rows, cols)
    keys = generate_keys(maze, rows // 2, cols // 2)
    used_positions = set()  # Set to track used (x, y) coordinates

    # Instantiate each enemy and add a safe zone for them in the maze
    for enemy_type in enemies:
        enemy_x, enemy_y = None, None
        # Find a unique position for each enemy
        while True:
            enemy_x = random.choice([1, rows - 4])
            enemy_y = random.choice([1, cols - 4])
            if (enemy_x, enemy_y) not in used_positions:
                used_positions.add((enemy_x, enemy_y))
                break  # Exit loop once we find a unique position

        maze = add_zone(rows, cols, maze, enemy_x, enemy_y)  # Add safe zone for the enemy
        enemy_class = ENEMY_CLASSES[enemy_type]
        enemy_objects.append(enemy_class(enemy_x, enemy_y, enemy_type))

    camera = Camera(WIDTH, HEIGHT, rows, cols)

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

        # Check if player is on 'P' tile to trigger level up after 2 seconds
        if player.current_tile == 'P':
            if player.floor_up_start_time is None:
                player.floor_up_start_time = time.time()
            elif time.time() - player.floor_up_start_time >= 1:
                player.floor_up()
                player, enemy_objects, maze, door_positions, keys, camera = start_mechanics(player)
                tile_map = generate_tiles(maze)
        else:
            player.floor_up_start_time = None

        # Key binds for the player
        key_binds = pygame.key.get_pressed()
        if key_binds[pygame.K_w] or key_binds[pygame.K_UP]:
            player.move(0, -1, maze)
        if key_binds[pygame.K_s] or key_binds[pygame.K_DOWN]:
            player.move(0, 1, maze)
        if key_binds[pygame.K_a] or key_binds[pygame.K_LEFT]:
            player.move(-1, 0, maze)
        if key_binds[pygame.K_d] or key_binds[pygame.K_RIGHT]:
            player.move(1, 0, maze)

        # Update player and enemy with time delta
        player.update_position(delta_time, door_positions, keys, maze)
        player.update_timer(delta_time)

        # Update enemy movement
        for enemy in enemy_objects:
            enemy.move(player, maze, delta_time)

        # Check for collision with enemies or remaining time
        if check_collision(player, enemy_objects) or player.timer <= 0:
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

        display_player_stats(player.floor, player.timer)
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