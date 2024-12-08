# enemy.py

import pygame, math, random, time
from queue import PriorityQueue
from settings import *
from utils import split_and_resize_sprite

class EnemyAI:
    def __init__(self, x, y, enemy_type):
        self.x, self.y = x, y
        self.enemy_type = enemy_type

        self.float_x, self.float_y = x, y
        self.start_pos = (x, y)
        self.target_pos = (x, y)
        self.is_moving = False
        self.elapsed_time = 0
        
        # Load speed and animations from ENEMIES dictionary
        self.speed = ENEMIES[enemy_type]["init_speed"]
        self.speed_multiplier = 1.0
        self.animations = {
            state: split_and_resize_sprite(path)
            for state, path in ENEMIES[enemy_type]["sprites"].items()
        }
        
        # Load animation states
        self.current_state = "right"  # Start in default state
        self.previous_state = self.current_state
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Time per frame in seconds

        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def heuristic(self, x1, y1, x2, y2):
        # Euclidean distance
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def a_star(self, start, goal, maze, is_immune_to_wall):
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(*start, *goal)}

        def is_walkable(tile):
            return tile in {'O'} or (is_immune_to_wall and tile in {'X', 'S', 'P', 'DL', 'DU', 'DI'})

        while not open_set.empty():
            current = open_set.get()[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            x, y = current
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

            for nx, ny in neighbors:
                if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and is_walkable(maze[ny][nx]):
                    temp_g_score = g_score[current] + 1
                    if temp_g_score < g_score.get((nx, ny), float('inf')):
                        came_from[(nx, ny)] = current
                        g_score[(nx, ny)] = temp_g_score
                        f_score[(nx, ny)] = temp_g_score + self.heuristic(nx, ny, *goal)
                        open_set.put((f_score[(nx, ny)], (nx, ny)))

        return []

    def move(self, player_pos, maze, delta_time, is_immune_to_wall=False):
        if not self.is_moving:
            # Calculate new path if not moving
            path = self.a_star((int(self.float_x), int(self.float_y)), player_pos, maze, is_immune_to_wall)
            if path:
                # Set the next tile in path as the target
                next_move = path[0]
                self.start_pos = (self.float_x, self.float_y)
                self.target_pos = next_move
                self.is_moving = True
                self.elapsed_time = 0  # Reset the time elapsed for the move

        if self.is_moving:
            # Increment elapsed time
            self.elapsed_time += delta_time
            t = min(self.elapsed_time * (self.speed * self.speed_multiplier), 1)  # Normalize to [0, 1]

            # Interpolate position between start and target
            self.float_x = (1 - t) * self.start_pos[0] + t * self.target_pos[0]
            self.float_y = (1 - t) * self.start_pos[1] + t * self.target_pos[1]

            # Stop moving once the target is reached
            if t >= 1:
                self.is_moving = False
                self.x, self.y = self.target_pos  # Update integer position to target
            
            if self.target_pos[0] > self.float_x:
                self.current_state = "right"
            elif self.target_pos[0] < self.float_x:
                self.current_state = "left"
            elif self.target_pos[1] > self.float_y:
                self.current_state = "down"
            elif self.target_pos[1] < self.float_y:
                self.current_state = "up"
            
            if self.previous_state is not self.current_state:
                self.frame_index = 0
                self.previous_state = self.current_state

        # Update rect for rendering
        self.rect.topleft = (int(self.float_x * TILE_SIZE), int(self.float_y * TILE_SIZE))
        self.update_frame(delta_time)

    def update_frame(self, delta_time):
        self.animation_timer += delta_time
        frames = self.animations[self.current_state]

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

    def draw(self, win, camera, offset_y):
        # Adjust position by camera and draw enemy
        adjusted_rect = camera.apply(self)
        current_frame = self.animations[self.current_state][self.frame_index]
        adjusted_rect = adjusted_rect.move(-current_frame.get_width() // 4, (-current_frame.get_height() // 4) + offset_y)
        win.blit(current_frame, adjusted_rect)


# Subclasses for each enemy

class Pursuer(EnemyAI):
    def move(self, player, maze, delta_time):
        # Target the player directly
        target = (player.x, player.y)
        super().move(target, maze, delta_time)

class Feigner(EnemyAI):
    def __init__(self, x, y, enemy_type):
        super().__init__(x, y, enemy_type)
        self.random_target = None
        self.init_distance_away_from_player = 9
        self.init_distance_target_from_player = 9

    def get_random_distant_target(self, player, maze):
        while True:
            rand_x, rand_y = random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1)
            if maze[rand_y][rand_x] == 'O' and self.heuristic(rand_x, rand_y, player.x, player.y) < self.init_distance_target_from_player + (math.floor((player.floor - 1) * (1 / MAX_FLOOR_TO_INCREASE_MAZE_SIZE)) * 2):
                return (rand_x, rand_y)

    def move(self, player, maze, delta_time):
        distance = self.heuristic(self.x, self.y, player.x, player.y)

        # Decide target based on distance to player
        if distance > self.init_distance_away_from_player + (math.floor((player.floor - 1) * (1 / MAX_FLOOR_TO_INCREASE_MAZE_SIZE)) * 2):
            target = (player.x, player.y)  # Pursue player directly if farther than 8 tiles
            self.random_target = None
        else:
            # Use existing random target or find a new one if reached
            if not self.random_target or (self.x, self.y) == self.random_target:
                self.random_target = self.get_random_distant_target(player, maze)
            target = self.random_target

        # Move towards the chosen target
        super().move(target, maze, delta_time)

class Glimmer(EnemyAI):
    def __init__(self, x, y, enemy_type):
        super().__init__(x, y, enemy_type)
        self.random_target = None
        self.init_distance_away_from_player = 9
        self.init_distance_target_from_player = 9

    def get_random_distant_target(self, player, maze):
        while True:
            rand_x, rand_y = random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1)
            if maze[rand_y][rand_x] == 'O' and self.heuristic(rand_x, rand_y, player.x, player.y) > self.init_distance_target_from_player + (math.floor((player.floor - 1) * (1 / MAX_FLOOR_TO_INCREASE_MAZE_SIZE)) * 2):
                return (rand_x, rand_y)

    def move(self, player, maze, delta_time):
        distance = self.heuristic(self.x, self.y, player.x, player.y)

        # Decide target based on distance to player
        if distance < self.init_distance_away_from_player + (math.floor((player.floor - 1) * (1 / MAX_FLOOR_TO_INCREASE_MAZE_SIZE)) * 2):
            target = (player.x, player.y)  # Pursue player directly if closer than 8 tiles
            self.random_target = None
        else:
            # Use existing random target or find a new one if reached
            if not self.random_target or (self.x, self.y) == self.random_target:
                self.random_target = self.get_random_distant_target(player, maze)
            target = self.random_target

        # Move towards the chosen target
        super().move(target, maze, delta_time)

class Ambusher(EnemyAI):
    def move(self, player, maze, delta_time):
        direction_map = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
            "rest": (0, 0)
        }

        # Get the direction vector based on player's direction
        dx, dy = direction_map[player.current_state]
        target = (player.x + 4 * dx, player.y + 4 * dy)

        # Ensure target is within maze bounds and not a wall
        target_x, target_y = target
        if 0 <= target_x < len(maze[0]) and 0 <= target_y < len(maze) and maze[target_y][target_x] == 'O':
            super().move(target, maze, delta_time)
        else:
            # Fallback: if the tile is outside bounds or blocked, target the player's position
            super().move((player.x, player.y), maze, delta_time)

class Specter(EnemyAI):
    def __init__(self, x, y, enemy_type):
        super().__init__(x, y, enemy_type)
        self.last_visited_position = None
        self.last_visited_time = None
        self.double_speed = self.speed * 2
        self.half_speed = self.speed / 2
        self.cooldown_timer = 0
        self.cooldown_duration = 3.0
        self.active_timer = 0
        self.active_duration = 3.0
        self.is_doubled_speed_active = False

    def move(self, player, maze, delta_time):
        current_time = time.time()

        if self.is_doubled_speed_active:
            # If doubled speed is active, target last visited position
            target = self.last_visited_position
            self.speed = self.double_speed
            self.current_state = "special"
            # Check if the active duration has passed
            if (self.x, self.y) == self.last_visited_position or (current_time - self.active_timer) >= self.active_duration:
                self.is_doubled_speed_active = False
                self.cooldown_timer = current_time  # Start cooldown
        else:
            # If not in doubled speed mode, move towards player at half speed
            target = (player.x, player.y)
            self.speed = self.half_speed
            # Enable doubled speed after cooldown
            if (current_time - self.cooldown_timer) >= self.cooldown_duration:
                self.is_doubled_speed_active = True
                self.active_timer = current_time
                # Record the player's last position
                self.last_visited_position = (player.x, player.y)
                self.last_visited_time = current_time

            # Reset to directional states
            if self.target_pos[0] > self.float_x:
                self.current_state = "right"
            elif self.target_pos[0] < self.float_x:
                self.current_state = "left"
            elif self.target_pos[1] > self.float_y:
                self.current_state = "down"
            elif self.target_pos[1] < self.float_y:
                self.current_state = "up"
            
            if self.previous_state is not self.current_state:
                self.frame_index = 0
                self.previous_state = self.current_state

        super().move(target, maze, delta_time)

class Slender(EnemyAI):
    def __init__(self, x, y, enemy_type):
        super().__init__(x, y, enemy_type)
        self.wall_pass_enabled = False
        self.wall_pass_threshold = 7  # Distance to enable passing through walls

    def move(self, player, maze, delta_time):
        # Calculate distance to player
        distance = self.heuristic(self.x, self.y, player.x, player.y)

        # Enable or disable wall pass based on distance
        self.wall_pass_enabled = distance > self.wall_pass_threshold
        if self.wall_pass_enabled:
            self.current_state = "special"
        else:
            # Reset to directional states
            if self.target_pos[0] > self.float_x:
                self.current_state = "right"
            elif self.target_pos[0] < self.float_x:
                self.current_state = "left"
            elif self.target_pos[1] > self.float_y:
                self.current_state = "down"
            elif self.target_pos[1] < self.float_y:
                self.current_state = "up"
            
            if self.previous_state is not self.current_state:
                self.frame_index = 0
                self.previous_state = self.current_state

        target = (player.x, player.y)
        super().move(target, maze, delta_time, self.wall_pass_enabled)


ENEMY_CLASSES = {
    # Format: (Class, required_floor, weight)
    "pursuer": (Pursuer, 1, -1),
    "feigner": (Feigner, 1, 1.0),
    "glimmer": (Glimmer, 1, 0.9),
    "ambusher": (Ambusher, 1, 0.8),
    "specter": (Specter, 1 + (MAX_FLOOR_TO_UNLOCK_NEW_ENEMY * 1), 0.7),
    "slender": (Slender, 1 + (MAX_FLOOR_TO_UNLOCK_NEW_ENEMY * 2), 0.6)
}