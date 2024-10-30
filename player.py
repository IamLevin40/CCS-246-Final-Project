# player.py

import pygame
from settings import TILE_SIZE, BLUE

class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed  # Speed now influences movement
        self.color = BLUE

        # Store precise floating point positions for smooth movement
        self.float_x = x
        self.float_y = y
        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def move(self, dx, dy, maze):
        # Calculate new potential positions using floating points
        new_x = self.float_x + dx * self.speed
        new_y = self.float_y + dy * self.speed

        # Only update the integer positions if the move is valid
        if maze[int(new_y)][int(new_x)] != 'X':
            self.float_x = new_x
            self.float_y = new_y
            self.x, self.y = int(self.float_x), int(self.float_y)
            self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)  # Update rect position

    def draw(self, win, camera):
        adjusted_rect = camera.apply(self)
        pygame.draw.rect(win, self.color, adjusted_rect)
