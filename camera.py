# camera.py

import pygame
from settings import TILE_SIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  # The area covered by the camera
        self.width = width
        self.height = height

    def follow(self, target):
        # Follow the player by centering the camera on the player's position
        self.camera.center = (target.x * TILE_SIZE + TILE_SIZE // 2,
                              target.y * TILE_SIZE + TILE_SIZE // 2)

    def apply(self, entity):
        # Adjust entity position by camera offset for smooth rendering
        return entity.rect.move(-self.camera.topleft[0], -self.camera.topleft[1])

    def apply_to_maze(self, x, y):
        # Return the adjusted position of maze tiles by the camera offset
        return (x * TILE_SIZE - self.camera.left,
                y * TILE_SIZE - self.camera.top)
