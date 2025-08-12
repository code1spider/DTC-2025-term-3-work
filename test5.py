import pygame
import sys
import os
import random

# Constants
TILE_SIZE = 40
MAP_WIDTH = 10
MAP_HEIGHT = 10
WINDOW_WIDTH = MAP_WIDTH * TILE_SIZE
WINDOW_HEIGHT = MAP_HEIGHT * TILE_SIZE
FPS = 60

def generate_random_map(width, height):
    return [[random.choice([0, 0, 0, 1, 1, 2]) for _ in range(width)] for _ in range(height)]

tile_map = generate_random_map(MAP_WIDTH, MAP_HEIGHT)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2D Tile Game with Sprites")
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

# --- PLAYER SPRITE SHEET LOADING FOR ANIMATION ---

def load_player_frames(sheet_name, frame_count):
    sheet = pygame.image.load(os.path.join("assets", sheet_name)).convert_alpha()
    frames = []
    for i in range(frame_count):
        rect = pygame.Rect(i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
        frame = sheet.subsurface(rect)
        frames.append(frame)
    return frames

player_frames = load_player_frames("player_spritesheet.png", 4)  # Make sure your sprite sheet has 4 frames in a row
player_frame_index = 0
animation_timer = 0
ANIMATION_SPEED = 10  # Lower is faster animation

enemy_image = load_image("enemy.png")  # Enemy image

# Player setup
x_position = random.randint(1, 9)
y_position = random.randint(1, 9)
player_pos = [x_position, y_position]

# Enemy setup (make sure enemy spawns in walkable tile, not player position)
while True:
    enemy_x = random.randint(0, MAP_WIDTH - 1)
    enemy_y = random.randint(0, MAP_HEIGHT - 1)
    if (enemy_x, enemy_y) != (player_pos[0], player_pos[1]) and tile_map[enemy_y][enemy_x] != 2:
        enemy_pos = [enemy_x, enemy_y]
        break

def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = tile_map[y][x]
            image = tile_images.get(tile)
            screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def draw_player():
    current_frame = player_frames[player_frame_index]
    screen.blit(current_frame, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

def draw_enemy():
    screen.blit(enemy_image, (enemy_pos[0] * TILE_SIZE, enemy_pos[1] * TILE_SIZE))

def is_walkable(x, y):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return tile_map[y][x] != 2  # not a wall
    return False

def move_enemy_towards_player(enemy_pos, player_pos):
    ex, ey = enemy_pos
    px, py = player_pos
    dx = px - ex
    dy = py - ey

    if abs(dx) > abs(dy):
        step_x = 1 if dx > 0 else -1
        new_pos = (ex + step_x, ey)
        if is_walkable(*new_pos):
            return list(new_pos)
        # Try vertical if blocked
        step_y = 1 if dy > 0 else -1
        new_pos = (ex, ey + step_y)
        if is_walkable(*new_pos):
            return list(new_pos)
    else:
        step_y = 1 if dy > 0 else -1
        new_pos = (ex, ey + step_y)
        if is_walkable(*new_pos):
            return list(new_pos)
        # Try horizontal if blocked
        step_x = 1 if dx > 0 else -1
        new_pos = (ex + step_x, ey)
        if is_walkable(*new_pos):
            return list(new_pos)
    return enemy_pos

# Control enemy movement timing
enemy_move_event = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_move_event, 500)  # enemy moves every 500 ms

running = True
while running:
    screen.fill((0, 0, 0))
    draw_map()
    draw_player()
    draw_enemy()
    pygame.display.flip()
    clock.tick(FPS)

    moving = False  # Track if player moved this frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == enemy_move_event:
            enemy_pos = move_enemy_towards_player(enemy_pos, player_pos)

    keys = pygame.key.get_pressed()
    new_x, new_y = player_pos

    if keys[pygame.K_LEFT] and is_walkable(new_x - 1, new_y):
        new_x -= 1
        moving = True
    elif keys[pygame.K_RIGHT] and is_walkable(new_x + 1, new_y):
        new_x += 1
        moving = True
    elif keys[pygame.K_UP] and is_walkable(new_x, new_y - 1):
        new_y -= 1
        moving = True
    elif keys[pygame.K_DOWN] and is_walkable(new_x, new_y + 1):
        new_y += 1
        moving = True

    if moving:
        # Advance animation frame on movement
        animation_timer += 1
        if animation_timer >= ANIMATION_SPEED:
            animation_timer = 0
            player_frame_index = (player_frame_index + 1) % len(player_frames)
    else:
        # Reset to first frame if not moving
        player_frame_index = 0
        animation_timer = 0

    player_pos = [new_x, new_y]

    # Check for collision: enemy catches player
    if player_pos == enemy_pos:
        print("Game Over! The enemy caught you.")
        running = False

pygame.quit()
sys.exit()
