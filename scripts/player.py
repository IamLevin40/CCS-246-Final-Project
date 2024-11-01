# player.py

import pygame
from settings import *
from utils import *

class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        
        # Load animations for each state
        self.animations = {state: split_and_resize_sprite(path, TILE_SIZE) for state, path in PLAYER_SPRITES.items()}
        self.current_state = "rest"  # Start in resting state
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Time per frame in seconds

        # Current, start, and target positions
        self.float_x = x
        self.float_y = y
        self.start_pos = (x, y)
        self.target_pos = (x, y)
        self.is_moving = False
        self.elapsed_time = 0

        # Player rectangle for rendering
        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def move(self, dx, dy, maze):
        # Only set a new target if not already moving
        if not self.is_moving:
            new_x = self.x + dx
            new_y = self.y + dy

            # Check if the new target position is walkable
            if maze[new_y][new_x] != 'X':
                # Initialize movement state
                self.start_pos = (self.float_x, self.float_y)
                self.target_pos = (new_x, new_y)
                self.is_moving = True
                self.elapsed_time = 0  # Reset time elapsed

                # Set animation state based on direction
                if dx == 1:
                    self.current_state = "right"
                elif dx == -1:
                    self.current_state = "left"
                elif dy == -1:
                    self.current_state = "up"
                elif dy == 1:
                    self.current_state = "down"

    def update_position(self, delta_time):
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
