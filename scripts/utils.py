# utils.py

import pygame

def load_animation_sprites(path, tile_size):
    # Load the full sprite sheet
    sheet = pygame.image.load(path).convert_alpha()
    width, height = sheet.get_size()
    
    # Calculate the size of each sprite based on the smallest possible square frame
    sprite_size = min(width, height)
    frame_count = width // sprite_size  # Calculate the number of frames (columns) in the image
    
    # Extract and scale each frame to tile_size
    frames = [
        pygame.transform.scale(
            sheet.subsurface(pygame.Rect(i * sprite_size, 0, sprite_size, sprite_size)),
            (tile_size, tile_size)
        ) 
        for i in range(frame_count)
    ]
    
    return frames