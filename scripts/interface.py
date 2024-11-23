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
    if not running:
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

def display_player_stats(floor, timer=0):
    # Define font settings
    font_label = pygame.font.Font(None, 24)
    font_value = pygame.font.Font(None, 32)
    font_value.set_bold(True)
    
    # Render the texts for labels and values
    floor_label_text = font_label.render("FLOOR", True, BLACK)
    floor_value_text = font_value.render(str(floor), True, BLACK)
    
    timer_label_text = font_label.render("TIMER", True, BLACK)
    timer_value_text = font_value.render(f"{timer:.1f}s", True, BLACK)
    
    # Calculate positions
    # Background box dimensions
    box_width = 120
    box_height = 60
    box_padding = 10

    # Get screen center for horizontal alignment
    center_x = WIDTH // 2

    # Box position
    floor_box_rect = pygame.Rect(center_x - box_width - box_padding, 10, box_width, box_height)
    timer_box_rect = pygame.Rect(center_x + box_padding, 10, box_width, box_height)
    
    # Draw background rectangles
    pygame.draw.rect(WIN, FLOOR_BG_COLOR, floor_box_rect)
    pygame.draw.rect(WIN, TIMER_BG_COLOR, timer_box_rect)
    
    # Draw borders for better visibility
    pygame.draw.rect(WIN, WHITE, floor_box_rect, 4)
    pygame.draw.rect(WIN, WHITE, timer_box_rect, 4)
    
    # Calculate text positions for center alignment within the boxes
    floor_label_pos = floor_label_text.get_rect(center=(floor_box_rect.centerx, floor_box_rect.y + 18))
    floor_value_pos = floor_value_text.get_rect(center=(floor_box_rect.centerx, floor_box_rect.y + 40))
    
    timer_label_pos = timer_label_text.get_rect(center=(timer_box_rect.centerx, timer_box_rect.y + 18))
    timer_value_pos = timer_value_text.get_rect(center=(timer_box_rect.centerx, timer_box_rect.y + 40))
    
    # Render the texts on the screen
    WIN.blit(floor_label_text, floor_label_pos)
    WIN.blit(floor_value_text, floor_value_pos)
    
    WIN.blit(timer_label_text, timer_label_pos)
    WIN.blit(timer_value_text, timer_value_pos)
