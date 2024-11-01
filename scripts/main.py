# main.py

import pygame, random
from settings import *
from player import Player
from enemy import EnemyAI
from maze import *
from camera import Camera

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
        WIN.fill(WHITE)  # Clear the window with a white background

        # Render title text
        font = pygame.font.Font(None, 64)  # Use a default font with size 74
        title_surface = font.render("Dungeon Labyrinth", True, BLACK)
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

def start_mechanics():
    # Player spawns in the center of the player safe zone
    player_start_x = ROWS // 2
    player_start_y = COLS // 2
    player = Player(player_start_x, player_start_y, INIT_SPEED_PLAYER)

    # Enemy spawns in the center of the enemy safe zone
    enemy_start_y = random.choice([1, ROWS - 4])  # Center of safe zone
    enemy_start_x = random.choice([1, COLS - 4])
    enemy = EnemyAI(enemy_start_x, enemy_start_y, INIT_SPEED_ENEMY)

    maze = generate_maze(ROWS, COLS)
    maze = add_zone(maze, enemy_start_x, enemy_start_y)
    tile_map = generate_tiles(maze)

    camera = Camera(WIDTH, HEIGHT)
    return player, enemy, maze, tile_map, camera

def game_loop():
    player, enemy, maze, tile_map, camera = start_mechanics()   # Start summoning player and enemies
    running = True
    while running:
        delta_time = clock.tick(FPS) / 1000.0  # Convert to seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, -1, maze)
        if keys[pygame.K_s]:
            player.move(0, 1, maze)
        if keys[pygame.K_a]:
            player.move(-1, 0, maze)
        if keys[pygame.K_d]:
            player.move(1, 0, maze)

        # Update player and enemy with time delta
        player.update_position(delta_time)
        enemy.move((player.x, player.y), maze, delta_time)

        camera.follow((player.x, player.y), delta_time)

        WIN.fill(WHITE)
        draw_maze(maze, camera, tile_map)
        
        player.draw(WIN, camera)
        enemy.draw(WIN, camera)
        pygame.display.update()

    pygame.quit()

def main():
    title_screen()      # Show the title screen first
    game_loop()         # Start game looping
    

if __name__ == "__main__":
    main()
