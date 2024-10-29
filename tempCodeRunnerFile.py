# ENEMY FOR THE GAME

import pygame
import math
from queue import PriorityQueue
from settings import TILE_SIZE, RED

class EnemyAI:
    def __init__(self, x, y):
        # Position in pixels (center of the tile)
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.color = RED
        self.speed = 75.0  # Pixels per second (can be float)
        self.path = []  # Store the current path to the player

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

    def move(self, player_pos, dt, maze):
        if not self.path or (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)) == self.path[0]:
            # Calculate a new path if needed
            self.path = self.a_star((int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)), player_pos, maze)

        if self.path:
            # Move smoothly toward the next target tile
            target_x, target_y = self.path[0]
            target_x *= TILE_SIZE
            target_y *= TILE_SIZE

            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist > 0:
                # Normalize direction and move incrementally
                self.x += (dx / dist) * self.speed * dt
                self.y += (dy / dist) * self.speed * dt

    def draw(self, win):
        pygame.draw.rect(win, self.color, 
                         (self.x, self.y, TILE_SIZE, TILE_SIZE))
