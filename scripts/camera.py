# camera.py

import pygame
from settings import *
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.smoothness = 0.8  # Controls how fast the camera moves in pixels per second
        self.max_offset = 36  # Maximum distance the camera will "peek" at the player

        # Maze center position in pixels (anchor point)
        self.maze_center = pygame.Vector2(COLS // 2 * TILE_SIZE, ROWS // 2 * TILE_SIZE)
        self.position = pygame.Vector2(self.maze_center)  # Start at maze center

    def follow(self, player_position, delta_time):
        player_x, player_y = player_position[0] * TILE_SIZE, player_position[1] * TILE_SIZE
        target_position = pygame.Vector2(player_x, player_y)

        # Calculate offset from the maze center to the player
        offset = target_position - self.maze_center
        distance = offset.length()

        if distance > self.max_offset:
            offset.scale_to_length(self.max_offset)

        limited_target = self.maze_center + offset

        # Smoothly adjust the camera position towards this limited target using elapsed time
        self.position += (limited_target - self.position) * (self.smoothness * delta_time)

        # Update camera rect position
        self.camera.topleft = (self.position.x - WIDTH // 2, self.position.y - HEIGHT // 2)

    def apply(self, entity):
        # Adjust entity position by camera offset for rendering
        return entity.rect.move(-self.camera.topleft[0], -self.camera.topleft[1])

    def apply_to_maze(self, x, y):
        # Adjust maze tile position by camera offset
        return (x * TILE_SIZE - self.camera.left, y * TILE_SIZE - self.camera.top)
