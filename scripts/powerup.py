# powerup.py

import pygame, random, math, threading
from settings import *
from utils import *
from maze import *

POWERUP_OBJECTS = {name: split_and_resize_sprite(path, TILE_SIZE)[0] for name, path in POWERUP_SPRITES.items()}
POWERUP_SPAWN_EVENT = pygame.USEREVENT + 2 

class Powerup:
    def __init__(self, x, y, type, duration):
        self.x = x
        self.y = y
        self.type = type
        self.duration = duration
        self.collected = False
        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    
    def draw(self, win, camera):
        x, y = camera.apply_to_maze(self.x, self.y)
        powerup_sprite = POWERUP_OBJECTS[self.type]
        win.blit(powerup_sprite, (x, y))
    
    def activate(self, player, enemies):
        pass

# Subclasses for each powerup

class RocketBoost(Powerup):
    def __init__(self, x, y):
        super().__init__(x, y, "rocket_boost", 4.0)

    def activate(self, player, enemies):
        player.speed_multiplier += 0.5
        threading.Timer(self.duration, self.deactivate, args=(player,)).start()

    def deactivate(self, player):
        player.speed_multiplier -= 0.5

class Retreat(Powerup):
    def __init__(self, x, y):
        super().__init__(x, y, "retreat", 2.5)

    def activate(self, player, enemies):
        player.speed_multiplier -= 0.75
        threading.Timer(self.duration, self.deactivate, args=(player,)).start()

    def deactivate(self, player):
        player.speed_multiplier += 0.75
        player.teleport_to_safe_zone()

class Immunity(Powerup):
    def __init__(self, x, y):
        super().__init__(x, y, "immunity", 5.0)

    def activate(self, player, enemies):
        player.is_immune = True
        player.can_collect = False
        threading.Timer(self.duration, self.deactivate, args=(player,)).start()

    def deactivate(self, player):
        player.is_immune = False
        player.can_collect = True

class SlowMove(Powerup):
    def __init__(self, x, y):
        super().__init__(x, y, "slow_move", 5.0)

    def activate(self, player, enemies):
        for enemy in enemies:
            enemy.speed_multiplier -= 0.25
        threading.Timer(self.duration, self.deactivate, args=(enemies,)).start()

    def deactivate(self, enemies):
        for enemy in enemies:
            enemy.speed_multiplier += 0.25


def generate_powerups(maze, center_x, center_y, active_powerups, powerup_classes):
    min_distance_from_center = 12
    min_distance_from_powerup = 8
    min_distance_from_structure = 12
    structure_tiles = {'S', 'P', 'DL', 'DU', 'DI'}
    new_powerup = None

    while new_powerup is None:
        # Generate random coordinates within maze bounds
        x, y = random.randint(1, len(maze[0]) - 2), random.randint(1, len(maze) - 2)

        # Calculate distance from maze center
        distance_from_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

        # Ensure the tile is walkable and far enough from the maze center
        if maze[y][x] == 'O' and distance_from_center >= min_distance_from_center:
            # Check if the new powerup is too close to any existing powerups
            too_close_to_powerup = any(
                math.sqrt((x - powerup.x) ** 2 + (y - powerup.y) ** 2) < min_distance_from_powerup
                for powerup in active_powerups
            )

            # Check if the new powerup is too close to any portal structure tile
            too_close_to_structure = any(
                math.sqrt((x - j) ** 2 + (y - i) ** 2) < min_distance_from_structure
                for i in range(max(0, y - min_distance_from_structure), min(len(maze), y + min_distance_from_structure + 1))
                for j in range(max(0, x - min_distance_from_structure), min(len(maze[0]), x + min_distance_from_structure + 1))
                if maze[i][j] in structure_tiles
            )

            powerup_types = list(powerup_classes.keys())
            weights = [powerup_classes[ptype][1] for ptype in powerup_types]

            # If the new powerup position is valid, add it to the list
            if not too_close_to_powerup and not too_close_to_structure:
                powerup_type = random.choices(powerup_types, weights=weights, k=1)[0]
                powerup_class = POWERUP_CLASSES[powerup_type][0]
                new_powerup = powerup_class(x, y)

    return new_powerup

def check_powerup_collection(player, powerups):
    # Check if the player can collect a powerup
    for powerup in powerups:
        if not powerup.collected and player.x == powerup.x and player.y == powerup.y and not player.has_powerup:
            player.current_powerup = powerup
            player.has_powerup = True
            powerup.collected = True
            break


POWERUP_CLASSES = {
    # Format: (Class, weight)
    "rocket_boost": (RocketBoost, 1.0),
    "retreat": (Retreat, 0.85),
    "immunity": (Immunity, 0.75),
    "slow_move": (SlowMove, 0.95)
}