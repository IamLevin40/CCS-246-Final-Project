# enemy.py

import pygame, math, random
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
        self.speed = ENEMIES[enemy_type]["speed"]
        self.animations = {
            state: split_and_resize_sprite(path, TILE_SIZE)
            for state, path in ENEMIES[enemy_type]["sprites"].items()
        }
        
        # Load animation states
        self.current_state = "rest"  # Start in resting state
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Time per frame in seconds

        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def heuristic(self, x1, y1, x2, y2):
        # Euclidean distance
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def a_star(self, start, goal, maze):
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(*start, *goal)}

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
                if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and (maze[ny][nx] != 'X' and maze[ny][nx] != 'S' and maze[ny][nx] != 'P'):
                    temp_g_score = g_score[current] + 1

                    if temp_g_score < g_score.get((nx, ny), float('inf')):
                        came_from[(nx, ny)] = current
                        g_score[(nx, ny)] = temp_g_score
                        f_score[(nx, ny)] = temp_g_score + self.heuristic(nx, ny, *goal)
                        open_set.put((f_score[(nx, ny)], (nx, ny)))

        return []

    def move(self, player_pos, maze, delta_time):
        if not self.is_moving:
            # Calculate new path if not moving
            path = self.a_star((int(self.float_x), int(self.float_y)), player_pos, maze)
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
            t = min(self.elapsed_time * self.speed, 1)  # Normalize to [0, 1]

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

        # Update rect for rendering
        self.rect.topleft = (int(self.float_x * TILE_SIZE), int(self.float_y * TILE_SIZE))

    def update_frame(self, delta_time):
        self.animation_timer += delta_time
        frames = self.animations[self.current_state]

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

    def draw(self, win, camera):
        # Adjust position by camera and draw enemy
        adjusted_rect = camera.apply(self)
        current_frame = self.animations[self.current_state][self.frame_index]
        win.blit(current_frame, adjusted_rect)


# Subclasses for each enemy

class Pursuer(EnemyAI):
    def move(self, player_pos, maze, delta_time):
        # Target the player directly
        target = player_pos
        super().move(target, maze, delta_time)

class Feigner(EnemyAI):
    def __init__(self, x, y, enemy_type):
        super().__init__(x, y, enemy_type)
        self.random_target = None
        self.distance_away_from_player = 8
        self.distance_target_from_player = 8

    def get_random_distant_target(self, player_pos, maze):
        while True:
            rand_x, rand_y = random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1)
            if maze[rand_y][rand_x] == 'O' and self.heuristic(rand_x, rand_y, player_pos[0], player_pos[1]) < self.distance_target_from_player:
                return (rand_x, rand_y)

    def move(self, player_pos, maze, delta_time):
        distance = self.heuristic(self.x, self.y, player_pos[0], player_pos[1])

        # Decide target based on distance to player
        if distance > self.distance_away_from_player:
            target = player_pos  # Pursue player directly if farther than 8 tiles
            self.random_target = None
        else:
            # Use existing random target or find a new one if reached
            if not self.random_target or (self.x, self.y) == self.random_target:
                self.random_target = self.get_random_distant_target(player_pos, maze)
            target = self.random_target

        # Move towards the chosen target
        super().move(target, maze, delta_time)

class Glimmer(EnemyAI):
    def __init__(self, x, y, enemy_type):
        super().__init__(x, y, enemy_type)
        self.random_target = None
        self.distance_away_from_player = 8
        self.distance_target_from_player = 8

    def get_random_distant_target(self, player_pos, maze):
        while True:
            rand_x, rand_y = random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1)
            if maze[rand_y][rand_x] == 'O' and self.heuristic(rand_x, rand_y, player_pos[0], player_pos[1]) > self.distance_target_from_player:
                return (rand_x, rand_y)

    def move(self, player_pos, maze, delta_time):
        distance = self.heuristic(self.x, self.y, player_pos[0], player_pos[1])

        # Decide target based on distance to player
        if distance < self.distance_away_from_player:
            target = player_pos  # Pursue player directly if closer than 8 tiles
            self.random_target = None
        else:
            # Use existing random target or find a new one if reached
            if not self.random_target or (self.x, self.y) == self.random_target:
                self.random_target = self.get_random_distant_target(player_pos, maze)
            target = self.random_target

        # Move towards the chosen target
        super().move(target, maze, delta_time)

class Ambusher(EnemyAI):
    def move(self, player_pos, player_direction, maze, delta_time):
        direction_map = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
            "rest": (0, 0)
        }

        # Get the direction vector based on player's direction
        dx, dy = direction_map[player_direction]
        target = (player_pos[0] + 4 * dx, player_pos[1] + 4 * dy)

        # Ensure target is within maze bounds and not a wall
        target_x, target_y = target
        if 0 <= target_x < len(maze[0]) and 0 <= target_y < len(maze) and maze[target_y][target_x] == 'O':
            super().move(target, maze, delta_time)
        else:
            # Fallback: if the tile is outside bounds or blocked, target the player's position
            super().move(player_pos, maze, delta_time)