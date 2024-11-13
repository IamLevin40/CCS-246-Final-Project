# key.py

import pygame, random, math, time
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
        # Assuming you have a key sprite loaded in utils
        x, y = camera.apply_to_maze(self.x, self.y)
        key_sprite = KEY_OBJECTS['real'] if self.is_real else KEY_OBJECTS['fake']
        win.blit(key_sprite, (x, y))

def generate_keys(maze, center_x, center_y, num_keys=4, min_distance=12):
    keys = []
    real_key_added = False

    while len(keys) < num_keys:
        x, y = random.randint(1, len(maze[0]) - 2), random.randint(1, len(maze) - 2)
        
        # Calculate distance from center
        distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        
        if maze[y][x] == 'O' and distance >= min_distance:
            # Set is_real to True for the real key and False for fake keys
            is_real = not real_key_added
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