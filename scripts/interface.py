# interface.py

import pygame
from settings import *
from utils import *

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
    # Load UI icon images
    stats_holder_image = pygame.image.load(UI_ICON_SPRITES["stats_holder"]).convert_alpha()
    floor_icon_image = UI_ICON_OBJECTS["floor"][0]
    clock_icon_image = UI_ICON_OBJECTS["clock"][0]

    # Resize images for consistent appearance
    stats_holder_size = (180, 45)  # Size of the stats holder background
    icon_size = (32, 32)  # Size of the floor and clock icons
    stats_holder_image = pygame.transform.scale(stats_holder_image, stats_holder_size)
    floor_icon_image = pygame.transform.scale(floor_icon_image, icon_size)
    clock_icon_image = pygame.transform.scale(clock_icon_image, icon_size)

    # Define font settings
    label_font = pygame.font.Font(None, 14)
    value_font = pygame.font.Font(None, 28)
    value_font.set_bold(True)

    # Render the texts for labels and values
    floor_label_text = label_font.render("FLOOR", True, WHITE)
    floor_value_text = value_font.render(str(floor), True, WHITE)

    timer_label_text = label_font.render("TIMER", True, WHITE)
    timer_value_text = value_font.render(f"{timer:.1f}s", True, WHITE)

    # Positioning for the stats holders
    center_x = WIDTH // 2
    top_margin = 10
    floor_box_pos = (center_x - stats_holder_size[0] - 10, top_margin)
    timer_box_pos = (center_x + 10, top_margin)

    # Draw the stats holders
    WIN.blit(stats_holder_image, floor_box_pos)
    WIN.blit(stats_holder_image, timer_box_pos)

    # Positioning for icons inside the boxes
    icon_padding = 16
    floor_icon_pos = (floor_box_pos[0] + icon_padding, floor_box_pos[1] + (stats_holder_size[1] - icon_size[1]) // 2)
    clock_icon_pos = (timer_box_pos[0] + icon_padding, timer_box_pos[1] + (stats_holder_size[1] - icon_size[1]) // 2)

    WIN.blit(floor_icon_image, floor_icon_pos)
    WIN.blit(clock_icon_image, clock_icon_pos)

    # Text alignment inside the stats holders
    text_padding = icon_padding + icon_size[0] + 10  # Space for the icon and padding
    floor_label_pos = (floor_box_pos[0] + text_padding, floor_box_pos[1] + 10)
    floor_value_pos = (floor_box_pos[0] + text_padding, floor_box_pos[1] + 20)

    timer_label_pos = (timer_box_pos[0] + text_padding, timer_box_pos[1] + 10)
    timer_value_pos = (timer_box_pos[0] + text_padding, timer_box_pos[1] + 20)

    # Render the texts in the boxes
    WIN.blit(floor_label_text, floor_label_pos)
    WIN.blit(floor_value_text, floor_value_pos)

    WIN.blit(timer_label_text, timer_label_pos)
    WIN.blit(timer_value_text, timer_value_pos)

def display_inventory(has_key, powerup_type=None, powerup_name="", powerup_cooldown=0):
    # Define fonts for cooldown text and powerup name
    cooldown_font = pygame.font.Font(None, 20)
    cooldown_font.set_bold(True)
    name_font = pygame.font.Font(None, 16)
    name_font.set_bold(True)

    # Load holder and keypad images
    holder_image = UI_ICON_OBJECTS["inventory_holder"][0]
    keypad_e_image = KEYPAD_OBJECTS["keypad_e"][0]
    keypad_r_image = KEYPAD_OBJECTS["keypad_r"][0]

    # Resize images to fixed dimensions
    holder_size = 40
    keypad_size = 24
    holder_image = pygame.transform.scale(holder_image, (holder_size, holder_size))
    keypad_e_image = pygame.transform.scale(keypad_e_image, (keypad_size, keypad_size))
    keypad_r_image = pygame.transform.scale(keypad_r_image, (keypad_size, keypad_size))

    # Define inventory positions
    to_center = 10
    box_padding = 8
    bottom_padding = HEIGHT - holder_size - 40  # Padding from the bottom
    holder1_x = (WIDTH // 2) - holder_size - box_padding
    holder2_x = (WIDTH // 2) + box_padding
    keypad_y = bottom_padding + holder_size

    # Draw inventory holders
    WIN.blit(holder_image, (holder1_x, bottom_padding))
    WIN.blit(holder_image, (holder2_x, bottom_padding))

    # Draw keypads below holders
    WIN.blit(keypad_e_image, (holder1_x + (holder_size // 2) - (keypad_size // 2), keypad_y))
    WIN.blit(keypad_r_image, (holder2_x + (holder_size // 2) - (keypad_size // 2), keypad_y))

    # Render powerup image if `powerup_type` is provided
    if powerup_type:
        powerup_image = POWERUP_OBJECTS.get(powerup_type)
        powerup_image = pygame.transform.scale(powerup_image, (holder_size - to_center, holder_size - to_center))
        shadow = create_shadow(powerup_image)
        WIN.blit(shadow, (holder1_x + (to_center // 2) + 1, bottom_padding + (to_center // 2) + 1))
        WIN.blit(powerup_image, (holder1_x + (to_center // 2) - 1, bottom_padding + (to_center // 2) - 1))

        # Render powerup name above the first holder
        name_text = name_font.render(powerup_name.upper(), True, WHITE)
        name_rect = name_text.get_rect(center=(holder1_x + holder_size // 2, bottom_padding - 8))
        WIN.blit(name_text, name_rect)

    # Render cooldown overlay and text if `powerup_cooldown` > 0
    if powerup_cooldown > 0:
        # Create a semi-transparent copy of the holder image for overlay
        overlay = holder_image.copy()
        overlay.fill((0, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)  # Add semi-transparency
        WIN.blit(overlay, (holder1_x, bottom_padding))

        # Render cooldown text
        cooldown_text = cooldown_font.render(f"{powerup_cooldown:.1f}s", True, BLACK)
        text_rect = cooldown_text.get_rect(center=(holder1_x + holder_size // 2, bottom_padding + holder_size // 2))
        WIN.blit(cooldown_text, text_rect)

    # Render key image if `has_key` is True
    if has_key:
        key_image = KEY_OBJECTS["real"]
        key_image = pygame.transform.scale(key_image, (holder_size - to_center, holder_size - to_center))
        shadow = create_shadow(key_image)
        WIN.blit(shadow, (holder2_x + (to_center // 2) + 1, bottom_padding + (to_center // 2) + 1))
        WIN.blit(key_image, (holder2_x + (to_center // 2) - 1, bottom_padding + (to_center // 2) - 1))

def display_movement_keybinds():
    # Define fonts for the title
    title_font = pygame.font.Font(None, 18)
    title_font.set_bold(True)

    # Load keypad images
    keypad_w_image = KEYPAD_OBJECTS["keypad_w"][0]
    keypad_a_image = KEYPAD_OBJECTS["keypad_a"][0]
    keypad_s_image = KEYPAD_OBJECTS["keypad_s"][0]
    keypad_d_image = KEYPAD_OBJECTS["keypad_d"][0]

    # Resize keypads to fixed dimensions
    keypad_size = 24  # Fixed size for keypads
    keypad_w_image = pygame.transform.scale(keypad_w_image, (keypad_size, keypad_size))
    keypad_a_image = pygame.transform.scale(keypad_a_image, (keypad_size, keypad_size))
    keypad_s_image = pygame.transform.scale(keypad_s_image, (keypad_size, keypad_size))
    keypad_d_image = pygame.transform.scale(keypad_d_image, (keypad_size, keypad_size))

    # Calculate positions for the keypads
    base_x = 20
    base_y = HEIGHT - keypad_size - 40
    keybind_padding = 4

    # Position each keypad relative to the base position
    keypad_s_x, keypad_s_y = base_x + keypad_size, base_y + keypad_size
    keypad_w_x, keypad_w_y = keypad_s_x, keypad_s_y - keypad_size
    keypad_a_x, keypad_a_y = keypad_s_x - keypad_size - keybind_padding, keypad_s_y
    keypad_d_x, keypad_d_y = keypad_s_x + keypad_size + keybind_padding, keypad_s_y

    # Draw keypads
    WIN.blit(keypad_s_image, (keypad_s_x, keypad_s_y))
    WIN.blit(keypad_w_image, (keypad_w_x, keypad_w_y))
    WIN.blit(keypad_a_image, (keypad_a_x, keypad_a_y))
    WIN.blit(keypad_d_image, (keypad_d_x, keypad_d_y))

    # Render the "MOVEMENT" text
    movement_text = title_font.render("MOVEMENT", True, WHITE)  # White text
    movement_text_rect = movement_text.get_rect(center=(keypad_s_x + keypad_size // 2, keypad_w_y - 10))
    WIN.blit(movement_text, movement_text_rect)

def create_shadow(image, shadow_color=(0, 0, 0, 100)):
    shadow = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    shadow.fill(shadow_color)
    shadow.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return shadow