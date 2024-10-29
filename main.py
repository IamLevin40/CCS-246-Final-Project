# main.py

import pygame, random
from settings import *
from player import Player
from enemy import EnemyAI
from maze import generate_maze, add_zone
from camera import Camera

def draw_maze(maze, camera):
    for i in range(ROWS):
        for j in range(COLS):
            color = BLACK if maze[i][j] == 'X' else WHITE
            x, y = camera.apply_to_maze(j, i)
            pygame.draw.rect(WIN, color, (x, y, TILE_SIZE, TILE_SIZE))

def main():
    # Player spawns in the center of the player safe zone
    player_start_x = ROWS // 2
    player_start_y = COLS // 2
    player = Player(player_start_x, player_start_y, INIT_SPEED_PLAYER)

    # Enemy spawns in the center of the enemy safe zone
    enemy_start_x = random.choice([1, ROWS - 4])  # Center of safe zone
    enemy_start_y = random.choice([1, COLS - 4])
    enemy = EnemyAI(enemy_start_x, enemy_start_y, INIT_SPEED_ENEMY)

    maze = generate_maze(ROWS, COLS)
    maze = add_zone(maze, enemy_start_x, enemy_start_y)

    camera = Camera(WIDTH, HEIGHT)

    running = True
    while running:
        clock.tick(FPS)

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

        enemy.move((player.x, player.y), maze)
        camera.follow(player)

        WIN.fill(WHITE)
        draw_maze(maze, camera)
        player.draw(WIN, camera)
        enemy.draw(WIN, camera)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
