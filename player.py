# player.py

import pygame
from settings import TILE_SIZE

class Player:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color

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

    def draw(self, win, camera):
        # Adjust position by camera and draw player
        adjusted_rect = camera.apply(self)
        pygame.draw.rect(win, self.color, adjusted_rect)
