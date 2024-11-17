# camera.py

import pygame
from settings import *

class Camera:
    def __init__(self, width, height, rows, cols):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.smoothness = 0.4  # Controls how fast the camera moves in pixels per second
        
        # Maximum distance the camera will "peek" at the player based on screen dimensions
        self.max_offset_x = self.width // 2
        self.max_offset_y = self.height // 2

        # Maze center position in pixels (anchor point)
        self.maze_center = pygame.Vector2(cols // 2 * TILE_SIZE, rows // 2 * TILE_SIZE)
        self.position = pygame.Vector2(self.maze_center)  # Start at maze center

    def follow(self, player_position, delta_time):
        player_x, player_y = player_position[0] * TILE_SIZE, player_position[1] * TILE_SIZE
        target_position = pygame.Vector2(player_x, player_y)

        # Calculate offset from the maze center to the player
        offset = target_position - self.maze_center

        # Limit offset based on screen dimensions to handle non-1:1 aspect ratios
        if abs(offset.x) > self.max_offset_x:
            offset.x = self.max_offset_x if offset.x > 0 else -self.max_offset_x
        if abs(offset.y) > self.max_offset_y:
            offset.y = self.max_offset_y if offset.y > 0 else -self.max_offset_y

        limited_target = self.maze_center + offset

        # Smoothly adjust the camera position towards this limited target using elapsed time
        self.position += (limited_target - self.position) * (self.smoothness * delta_time)

        # Update camera rect position
        self.camera.topleft = (self.position.x - self.width // 2, self.position.y - self.height // 2)

    def apply(self, entity):
        # Adjust entity position by camera offset for rendering
        return entity.rect.move(-self.camera.topleft[0], -self.camera.topleft[1])

    def apply_to_maze(self, x, y):
        # Adjust maze tile position by camera offset
        return (x * TILE_SIZE - self.camera.left, y * TILE_SIZE - self.camera.top)
