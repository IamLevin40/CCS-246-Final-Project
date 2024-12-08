# game.py

import pygame, random
from settings import *
from interface import *
from player import Player
from enemy import *
from maze import *
from key import *
from powerup import *
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
        player.safe_zone_pos = (player.x, player.y)
        player.target_pos = (player.x, player.y)
        player.current_tile = ''
    else:
        # Player spawns in the center of the player safe zone
        player = Player(rows // 2, cols // 2, INIT_SPEED_PLAYER)

    enemies = get_enemies(player)

    enemy_objects = []
    maze, door_positions = generate_maze(rows, cols)
    keys = generate_keys(maze, player.safe_zone_pos[0], player.safe_zone_pos[1])
    used_positions = set()  # Set to track used (x, y) coordinates

    # Instantiate each enemy and assign positions
    assigned_positions = []  # List to track assigned positions
    remaining_enemies = list(enemies)  # Create a copy of enemies to track unassigned ones

    while remaining_enemies:
        used_positions = set()  # Track positions in the current batch

        # Assign up to 4 positions in this batch
        for _ in range(min(4, len(remaining_enemies))):
            while True:
                enemy_x = random.choice([1, rows - 4])
                enemy_y = random.choice([1, cols - 4])
                if (enemy_x, enemy_y) not in used_positions:
                    used_positions.add((enemy_x, enemy_y))
                    assigned_positions.append((enemy_x, enemy_y))
                    break  # Exit once a unique position is found

        # Assign enemies to the positions in this batch
        for position in used_positions:
            if remaining_enemies:
                enemy_type = remaining_enemies.pop(0)  # Remove the first enemy in the list
                enemy_class = ENEMY_CLASSES[enemy_type][0]
                enemy_objects.append(enemy_class(position[0], position[1], enemy_type))
                maze = add_zone(rows, cols, maze, position[0], position[1])  # Add safe zone

    tile_map = generate_tiles(maze)
    camera = Camera(WIDTH, HEIGHT, rows, cols)

    return player, enemy_objects, maze, tile_map, door_positions, keys, camera

def get_enemies(player):
    # Filter eligible enemies based on the player's floor
    available_enemies = [
        (enemy_type, data[2])  # (Enemy name, weight)
        for enemy_type, data in ENEMY_CLASSES.items()
        if player.floor >= data[1]
    ]

    # Separate guaranteed enemies (weight = -1) from weighted selection
    guaranteed_enemies = [enemy for enemy, weight in available_enemies if weight == -1]
    weighted_enemies = [(enemy, weight) for enemy, weight in available_enemies if weight != -1]

    # Normalize weights for the remaining weighted selection
    total_weight = sum(weight for _, weight in weighted_enemies)
    normalized_weights = [(enemy, weight / total_weight) for enemy, weight in weighted_enemies]

    # Calculate the maximum number of enemies to select
    max_enemies = min(
        (INIT_MAX_ENEMIES + (math.floor((player.floor - 1) * (1 / MAX_FLOOR_TO_INCREASE_MAX_ENEMIES)))),
        len(available_enemies)
    )

    # Start with guaranteed enemies
    selected_enemy_types = list(guaranteed_enemies)

    # Fill remaining slots with weighted random unique enemies
    while len(selected_enemy_types) < max_enemies:
        # Randomly select an enemy using weighted probability
        chosen_enemy = random.choices(
            [enemy for enemy, _ in normalized_weights],
            weights=[weight for _, weight in normalized_weights],
            k=1
        )[0]

        # Ensure uniqueness in selection
        if chosen_enemy not in selected_enemy_types:
            selected_enemy_types.append(chosen_enemy)

    # Combine default and selected enemies
    enemies = list()
    enemies.extend(selected_enemy_types)
    return enemies

def game_loop():
    player, enemy_objects, maze, tile_map, door_positions, keys, camera = start_mechanics()   # Start summoning player and enemies
    active_powerups = []
    powerup_cooldown = 0
    game_over = False
    game_over_start_time = None

    clock = pygame.time.Clock()
    pygame.time.set_timer(POWERUP_SPAWN_EVENT, INIT_POWERUP_SPAWN_COOLDOWN * 1000)

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
            elif event.type == POWERUP_SPAWN_EVENT:
                if len(active_powerups) < MAX_POWERUPS:
                    new_powerup = generate_powerups(maze, player.safe_zone_pos[0], player.safe_zone_pos[1], active_powerups, POWERUP_CLASSES)
                    active_powerups.append(new_powerup)
        
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
                active_powerups = [item for item in  active_powerups if item == player.current_powerup]
                player, enemy_objects, maze, tile_map, door_positions, keys, camera = start_mechanics(player)
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

        # Activate powerup on pressing E or , key if cooldown is over
        if (key_binds[pygame.K_e] or key_binds[pygame.K_COMMA])and player.has_powerup and powerup_cooldown <= 0:
            active_powerups.remove(player.current_powerup)
            player.activate_powerup(enemy_objects)
            powerup_cooldown = INIT_POWERUP_ACTIVATE_COOLDOWN 
        
        # Check door on pressing R or . key
        if key_binds[pygame.K_r] or key_binds[pygame.K_PERIOD]:
            check_door_unlock(player, door_positions, maze)

        # Update cooldown for powerup activation
        if powerup_cooldown > 0:
            powerup_cooldown -= delta_time

        # Update player and enemy with time delta
        player.update_position(delta_time, keys, active_powerups, maze)
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

        # Get current powerup type if available
        powerup_type = None 
        powerup_name = None
        if player.current_powerup is not None:
            powerup_type = player.current_powerup.type
            powerup_name = player.current_powerup.name

        camera.follow((player.x, player.y), delta_time)
        WIN.fill(PATH_COLOR)

        draw_maze(maze, camera, tile_map)
        for key in keys:
            if not key.collected:
                key.draw(WIN, camera)
        for powerup in active_powerups:
            if not powerup.collected:
                powerup.draw(WIN, camera)
        player.draw(WIN, camera, (128 if player.is_immune else 255))
        for enemy in enemy_objects:
            enemy.draw(WIN, camera, ENEMIES[enemy.enemy_type]["offset_y"])

        display_player_stats(player.floor, player.timer)
        display_inventory(player.has_key, powerup_type, powerup_name, powerup_cooldown)
        display_movement_keybinds()
        pygame.display.update()

    pygame.quit()

def check_collision(player, enemies):
    # Check if any enemy has collided with the player
    buffer = 8
    player_rect = player.rect.inflate(-buffer, -buffer)
    for enemy in enemies:
        # Create a smaller collision box for each enemy
        enemy_rect = enemy.rect.inflate(-buffer, -buffer)
        if player_rect.colliderect(enemy_rect) and not player.is_immune:
            return True
    return False