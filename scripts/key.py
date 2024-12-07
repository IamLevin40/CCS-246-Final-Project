# key.py

import pygame, random, math
from settings import *
from utils import *
from maze import *

KEY_OBJECTS = {state: split_and_resize_sprite(path, TILE_SIZE)[0] for state, path in KEY_SPRITES.items()}
DOOR_LOCK_EVENT = pygame.USEREVENT + 1

class Key:
    def __init__(self, x, y, is_real):
        self.x = x
        self.y = y
        self.is_real = is_real
        self.collected = False

        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    
    def draw(self, win, camera):
        x, y = camera.apply_to_maze(self.x, self.y)
        key_sprite = KEY_OBJECTS['real'] if self.is_real else KEY_OBJECTS['fake']
        win.blit(key_sprite, (x, y))

def generate_keys(maze, center_x, center_y, num_keys=4):
    min_distance_from_center = 12
    min_distance_from_key = 8
    min_distance_from_structure = 12 
    structure_tiles = {'S', 'P', 'DL', 'DU', 'DI'}
    keys = []
    real_key_added = False

    while len(keys) < num_keys:
        # Generate random coordinates within maze bounds
        x, y = random.randint(1, len(maze[0]) - 2), random.randint(1, len(maze) - 2)
        
        # Calculate distance from maze center
        distance_from_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        
        # Ensure the tile is walkable and far enough from the maze center
        if maze[y][x] == 'O' and distance_from_center >= min_distance_from_center:
            
            # Check if the new key is too close to any existing keys
            too_close_to_key = False
            for key in keys:
                distance_from_key = math.sqrt((x - key.x) ** 2 + (y - key.y) ** 2)
                if distance_from_key < min_distance_from_key:
                    too_close_to_key = True
                    break

            # Check if the new key is too close to any portal structure tile
            too_close_to_structure = False
            for i in range(max(0, y - min_distance_from_structure), 
                           min(len(maze), y + min_distance_from_structure + 1)):
                for j in range(max(0, x - min_distance_from_structure), 
                               min(len(maze[0]), x + min_distance_from_structure + 1)):
                    if maze[i][j] in structure_tiles:
                        distance_from_structure = math.sqrt((x - j) ** 2 + (y - i) ** 2)
                        if distance_from_structure < min_distance_from_structure:
                            too_close_to_structure = True
                            break
                if too_close_to_structure:
                    break
            
            # If the new key position is valid, add it to the list
            if not too_close_to_key and not too_close_to_structure:
                is_real = not real_key_added  # Set is_real for the first key only
                keys.append(Key(x, y, is_real))
                real_key_added = real_key_added or is_real

    return keys

def check_key_collection(player, keys):
    # Check if the player can collect a key
    for key in keys:
        if not key.collected and player.x == key.x and player.y == key.y and player.has_key == False:
            player.has_key = True
            player.key_is_real = key.is_real
            key.collected = True

def check_door_unlock(player, door_positions, maze):
    # Check if the player is near a door and has a key
    if player.has_key:
        pygame.time.set_timer(DOOR_LOCK_EVENT, 0)
        # Iterate for every door tiles
        for door_y, door_x in door_positions:
            if abs(player.x - door_x) + abs(player.y - door_y) == 1:  # Near the door
                if player.key_is_real:
                    toggle_door(maze, door_positions, 'unlocked')
                else:
                    toggle_door(maze, door_positions, 'incorrect')
                    pygame.time.set_timer(DOOR_LOCK_EVENT, 2500)
                    
                # Remove the key regardless of its authenticity
                player.has_key = False
                player.key_is_real = False
                player.maze_interaction_triggered = True