# utils.py

import pygame

def split_and_resize_sprite(path, tile_size=0):
    # Load the full sprite sheet
    sheet = pygame.image.load(path).convert_alpha()
    width, height = sheet.get_size()
    
    # Calculate the size of each sprite based on the smallest possible square frame
    sprite_size = min(width, height)
    frame_count = width // sprite_size  # Calculate the number of frames (columns) in the image
    
    # Extract and scale each frame to tile_size
    if tile_size == 0:
        tile_size = sprite_size
    frames = [
        pygame.transform.scale(
            sheet.subsurface(pygame.Rect(i * sprite_size, 0, sprite_size, sprite_size)),
            (tile_size, tile_size)
        ) 
        for i in range(frame_count)
    ]
    
    return frames