# enemy.py

import pygame
import math
from queue import PriorityQueue
from settings import TILE_SIZE
class EnemyAI:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed  # Control speed
        self.color = color

        # Store floating-point positions
        self.float_x = x
        self.float_y = y
        self.start_pos = (x, y)
        self.target_pos = (x, y)
        self.is_moving = False
        self.elapsed_time = 0

        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def heuristic(self, x1, y1, x2, y2):
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
                if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] != 'X':
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

        # Update rect for rendering
        self.rect.topleft = (int(self.float_x * TILE_SIZE), int(self.float_y * TILE_SIZE))

    def draw(self, win, camera):
        adjusted_rect = camera.apply(self)
        pygame.draw.rect(win, self.color, adjusted_rect)
