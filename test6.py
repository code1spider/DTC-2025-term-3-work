import pygame
import sys
import os

# Constants
TILE_SIZE = 40
MAP_WIDTH = 10
MAP_HEIGHT = 10
WINDOW_WIDTH = MAP_WIDTH * TILE_SIZE
WINDOW_HEIGHT = MAP_HEIGHT * TILE_SIZE
FPS = 60

# Predetermined tile map
tile_map = [
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Big Map Overlay + Tilemap")
clock = pygame.time.Clock()

# Load images
def load_image(name):
    path = os.path.join("assets", name)
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), (TILE_SIZE, TILE_SIZE))

tile_images = {
    0: load_image("grass.png"),
    1: load_image("water.png"),
    2: load_image("wall.png")
}

player_image = load_image("player.png")
enemy_image = load_image("enemy.png")

# Load big background image (make sure it is exactly 400x400)
big_map_image = pygame.image.load(os.path.join("assets", "big_map.png")).convert()

# Player setup (start position on a walkable tile)
player_pos = [1, 1]

# Enemy setup (start on walkable tile and not on player)
enemy_pos = [8, 8]

def draw_map():
    # Optional: draw the tiles for overlays (if you want)
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = tile_map[y][x]
            image = tile_images.get(tile)
            screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def draw_player():
    screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

def draw_enemy():
    screen.blit(enemy_image, (enemy_pos[0] * TILE_SIZE, enemy_pos[1] * TILE_SIZE))

def is_walkable(x, y):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return tile_map[y][x] != 2  # Wall is not walkable
    return False

running = True
while running:
    screen.fill((0, 0, 0))

    # Draw big background first (the big map overlay)
    screen.blit(big_map_image, (0, 0))

    # Optionally draw tile overlays (like walls) to highlight collision areas
    # draw_map()  # Uncomment if you want tile images overlaid on big_map

    draw_player()
    draw_enemy()

    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_x, new_y = player_pos
    if keys[pygame.K_LEFT]:
        if is_walkable(new_x - 1, new_y):
            new_x -= 1
    if keys[pygame.K_RIGHT]:
        if is_walkable(new_x + 1, new_y):
            new_x += 1
    if keys[pygame.K_UP]:
        if is_walkable(new_x, new_y - 1):
            new_y -= 1
    if keys[pygame.K_DOWN]:
        if is_walkable(new_x, new_y + 1):
            new_y += 1

    player_pos = [new_x, new_y]

pygame.quit()
sys.exit()
