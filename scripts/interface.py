# interface.py

import pygame
from settings import *

def draw_maze(maze, camera, tile_map):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            tile_sprite = tile_map[i][j]
            x, y = camera.apply_to_maze(j, i)
            if tile_sprite:  # Only draw if tile_sprite is not None
                WIN.blit(tile_sprite, (x, y))

def title_screen():
    running = True
    button_color = DARK_GREEN  # Green color for the button
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)  # Button rectangle

    while running:
        WIN.fill(PATH_COLOR)  # Clear the window with a white background

        # Render title text
        font = pygame.font.Font(None, 64)  # Use a default font with size 64
        title_surface = font.render("Dungeon Labyrinth", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        WIN.blit(title_surface, title_rect)  # Draw the title

        # Draw the play button
        pygame.draw.rect(WIN, button_color, button_rect)  # Draw the button
        button_font = pygame.font.Font(None, 36)
        button_surface = button_font.render("Play", True, WHITE)  # Button text color
        button_text_rect = button_surface.get_rect(center=button_rect.center)
        WIN.blit(button_surface, button_text_rect)  # Draw the button text

        pygame.display.update()  # Update the display

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button press
                if event.button == 1:  # Left mouse button
                    if button_rect.collidepoint(event.pos):  # Check if clicked inside button
                        running = False  # Exit the title screen loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Check if Enter is pressed
                    running = False  # Exit the title screen loop
    
    from game import game_loop
    game_loop()

def game_over_screen():
    running = True
    button_color = WHITE  # Green color for the button
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)  # Button rectangle

    while running:
        WIN.fill(PATH_COLOR)  # Clear the window with a white background

        # Render title text
        font = pygame.font.Font(None, 64)  # Use a default font with size 64
        title_surface = font.render("Game Over", True, RED)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        WIN.blit(title_surface, title_rect)  # Draw the title

        # Draw the play button
        pygame.draw.rect(WIN, button_color, button_rect)  # Draw the button
        button_font = pygame.font.Font(None, 36)
        button_surface = button_font.render("Back", True, BLACK)  # Button text color
        button_text_rect = button_surface.get_rect(center=button_rect.center)
        WIN.blit(button_surface, button_text_rect)  # Draw the button text

        pygame.display.update()  # Update the display

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button press
                if event.button == 1:  # Left mouse button
                    if button_rect.collidepoint(event.pos):  # Check if clicked inside button
                        running = False  # Exit the title screen loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Check if Enter is pressed
                    running = False  # Exit the title screen loop

    title_screen()