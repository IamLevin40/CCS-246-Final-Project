import pygame
import math
from queue import PriorityQueue
from settings import TILE_SIZE, RED

class EnemyAI:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed  # Control speed

        # Store floating-point positions
        self.float_x = x
        self.float_y = y
        self.color = RED
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

    def move(self, player_pos, maze):
        path = self.a_star((int(self.float_x), int(self.float_y)), player_pos, maze)
        if path:
            next_move = path[0]
            dx = next_move[0] - int(self.float_x)
            dy = next_move[1] - int(self.float_y)

            # Move towards the next path step based on speed
            self.float_x += dx * self.speed
            self.float_y += dy * self.speed
            self.x, self.y = int(self.float_x), int(self.float_y)
            self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)  # Update rect position

    def draw(self, win, camera):
        adjusted_rect = camera.apply(self)
        pygame.draw.rect(win, self.color, adjusted_rect)
