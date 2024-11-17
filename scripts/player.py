# player.py

import pygame
from settings import *
from utils import *
from key import *

class Player:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.has_key = False
        self.key_is_real = False
        self.maze_interaction_triggered = False
        self.is_immune = False
        self.floor = 1

        self.float_x, self.float_y = x, y
        self.start_pos = (x, y)
        self.target_pos = (x, y)
        self.current_tile = ''
        self.is_moving = False
        self.elapsed_time = 0
        self.floor_up_start_time = None

        # Timer attributes
        self.init_time = INIT_TIMER
        self.timer = INIT_TIMER
        self.bonus_time = INIT_TIMER
        self.min_bonus_limit = INIT_MIN_BONUS_LIMIT
        
        # Load animations for each state
        self.animations = {
            state: split_and_resize_sprite(path, TILE_SIZE) 
            for state, path in PLAYER_SPRITES.items()
        }
        self.current_state = "rest"  # Start in resting state
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Time per frame in seconds

        # Player rectangle for rendering
        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def move(self, dx, dy, maze):
        # Only set a new target if not already moving
        if not self.is_moving:
            new_x = self.x + dx
            new_y = self.y + dy

            # Check if the new target position is walkable
            if maze[new_y][new_x] not in {'X', 'DL', 'DI'}:
                # Initialize movement state
                self.start_pos = (self.float_x, self.float_y)
                self.target_pos = (new_x, new_y)
                self.current_tile = maze[new_y][new_x]
                self.is_moving = True
                self.elapsed_time = 0  # Reset time elapsed

                # Set animation state based on direction
                if dy == -1:
                    self.current_state = "up"
                elif dy == 1:
                    self.current_state = "down"
                elif dx == -1:
                    self.current_state = "left"
                elif dx == 1:
                    self.current_state = "right"

    def update_position(self, delta_time, door_positions, keys, maze):        
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

        # Update rect for rendering
        self.rect.topleft = (int(self.float_x * TILE_SIZE), int(self.float_y * TILE_SIZE))
        self.update_frame(delta_time)

        # Check for key collection and door
        check_key_collection(self, keys)
        check_door_unlock(self, door_positions, maze)
    
    def update_frame(self, delta_time):
        self.animation_timer += delta_time
        frames = self.animations[self.current_state]

        # Advance to the next frame based on the timer
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

    def draw(self, win, camera):
        # Adjust position by camera and draw player
        adjusted_rect = camera.apply(self)
        current_frame = self.animations[self.current_state][self.frame_index]
        win.blit(current_frame, adjusted_rect)

    def update_timer(self, delta_time):
        # Decrement the timer by the elapsed time
        self.timer -= delta_time
        if self.timer < 0:
            self.timer = 0

    def calculate_bonus_time(self):
        # Calculate the bonus time using the given formula
        return self.bonus_time - ((self.init_time / self.min_bonus_limit) / 2) + ((self.floor - 1) * 0.05)

    def floor_up(self):
        # Handles player increasing floor
        self.floor += 1
        self.has_key = False
        self.key_is_real = False
        
        # Apply bonus time and update timer
        self.bonus_time = self.calculate_bonus_time()
        
        # Ensure bonus time doesn't go below min limit
        if self.bonus_time < self.min_bonus_limit:
            self.bonus_time = self.min_bonus_limit
        
        self.timer += self.bonus_time

        self.floor_up_start_time = None