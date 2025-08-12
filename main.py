import pygame
import sys
import os
import time

# Constants
TILE_SIZE = 40
MAP_WIDTH = 10
MAP_HEIGHT = 10
WINDOW_WIDTH = MAP_WIDTH * TILE_SIZE
WINDOW_HEIGHT = MAP_HEIGHT * TILE_SIZE
FPS = 60

# Tile map (your original)
tile_map = [
    [0, 0, 0, 3, 3, 3, 3, 0, 2, 0],
    [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 4, 0, 0],
    [2, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 2, 0, 0],
    [0, 0, 2, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 2, 0, 1, 1, 0, 0, 0, 2],
    [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tile Map with Entities")
clock = pygame.time.Clock()

# Load image helper
def load_image(name):
    path = os.path.join("assets", name)
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), (TILE_SIZE, TILE_SIZE))

# Load tiles
tile_images = {
    0: load_image("floor.png"),
    1: load_image("path.png"),
    2: load_image("debris.png"),
    3: load_image("machine.png"),
    4: load_image("floor.png"),  # Used as a marker for friend spawn
    5: load_image("doorshadow.png"),
}

# Load entities
player_image = load_image("player.png")
enemy_image = load_image("enemy.png")

# Set up entities
player_pos = [0, 0]  # Change this to where you want the player to start
enemy_pos = [8, 8]   # Same for the enemy

# Walkability logic
def is_walkable(x, y):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return tile_map[y][x] not in (2, 3,)  # Add more blocked tile types if needed
    return False

# Draw map
def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = tile_map[y][x]
            image = tile_images.get(tile)
            if image:
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

# Draw entities
def draw_player():
    screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

def draw_enemy():
    screen.blit(enemy_image, (enemy_pos[0] * TILE_SIZE, enemy_pos[1] * TILE_SIZE))

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))

    draw_map()
    draw_player()
    draw_enemy()

    pygame.display.flip()
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement logic
    keys = pygame.key.get_pressed()
    new_x, new_y = player_pos

    if keys[pygame.K_LEFT]:
        if is_walkable(new_x - 1, new_y):
            new_x -= 1
            time.sleep(0.2)
    elif keys[pygame.K_RIGHT]:
        if is_walkable(new_x + 1, new_y):
            new_x += 1
            time.sleep(0.2)
    elif keys[pygame.K_UP]:
        if is_walkable(new_x, new_y - 1):
            new_y -= 1
            time.sleep(0.2)
    elif keys[pygame.K_DOWN]:
        if is_walkable(new_x, new_y + 1):
            new_y += 1
            time.sleep(0.2)

    player_pos = [new_x, new_y]

pygame.quit()
sys.exit()
