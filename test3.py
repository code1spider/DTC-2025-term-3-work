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
#the above elements make the game fit the windowed game
# Map: 0 = grass, 1 = water, 2 = wall
import random

# Tile IDs: 0 = grass, 1 = water, 2 = wall
def generate_random_map(width, height):
    return [[random.choice([0, 0, 0, 1, 1, 2]) for _ in range(width)] for _ in range(height)]

tile_map = generate_random_map(MAP_WIDTH, MAP_HEIGHT)

#the above code is a tile map
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#the screen variable makes the window update- i think
pygame.display.set_caption("2D Tile Game with Sprites")
#title
clock = pygame.time.Clock()

# Load images
def load_image(name):
    path = os.path.join("assets", name)
    return pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE))

tile_images = {
    0: load_image("grass.png"),
    1: load_image("water.png"),
    2: load_image("wall.png")
}

player_image = load_image("player.png")

# Player setup
x_position = random.randint(1, 9) 

y_position = random.randint(1, 9) 
player_pos = [x_position, y_position]  # in grid coordinates

def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = tile_map[y][x]
            image = tile_images.get(tile)
            screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def draw_player():
    screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

def is_walkable(x, y):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return tile_map[y][x] != 2  # not a wall
    return False

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen
    draw_map()
    draw_player()
    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_x, new_y = player_pos
    if keys[pygame.K_LEFT]:
        new_x -= 1
        time.sleep(0.1)
    if keys[pygame.K_RIGHT]:
        new_x += 1
        time.sleep(0.1)
    if keys[pygame.K_UP]:
        new_y -= 1
        time.sleep(0.1)
    if keys[pygame.K_DOWN]:
        new_y += 1
        time.sleep(0.1)

    if is_walkable(new_x, new_y):
        player_pos = [new_x, new_y]

pygame.quit()
sys.exit()
