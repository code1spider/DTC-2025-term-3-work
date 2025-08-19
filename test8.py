import pygame
import sys
import os

# Constants
game_state = "main"
TILE_SIZE = 40
MAP_WIDTH = 10
MAP_HEIGHT = 10
WINDOW_WIDTH = MAP_WIDTH * TILE_SIZE
WINDOW_HEIGHT = MAP_HEIGHT * TILE_SIZE
FPS = 60

# Tile map
tile_map = [
    [0, 0, 4, 3, 3, 3, 3, 4, 2, 0],
    [0, 0, 0, 4, 3, 3, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 0, 0, 0, 0],
    [2, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 2, 0, 0],
    [0, 0, 2, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 2, 0, 1, 1, 0, 0, 0, 2],
    [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
]



pygame.init()
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tile Map with Entities")
clock = pygame.time.Clock()

# Dummy images (replace these with your actual images)
def create_dummy_surface(color):
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(color)
    return surf

tile_images = {
    0: create_dummy_surface((100, 100, 100)),
    1: create_dummy_surface((150, 150, 150)),
    2: create_dummy_surface((50, 50, 50)),
    3: create_dummy_surface((0, 0, 255)),
    4: create_dummy_surface((0, 255, 0)),
    5: create_dummy_surface((255, 255, 0)),
}

player_image = create_dummy_surface((255, 0, 0))
friend_image = create_dummy_surface((0, 255, 255))

player_pos = [0, 0]
friend_pos = [8, 3]





def is_walkable(x, y):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return tile_map[y][x] not in (2, 3)
    return False

def show_message(text):
    msg = font.render(text, True, (255, 255, 255))
    screen.blit(msg, (20, WINDOW_HEIGHT - 40))

def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = tile_map[y][x]
            image = tile_images.get(tile)
            if image:
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

def draw_player():
    screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

def draw_friend():
    screen.blit(friend_image, (friend_pos[0] * TILE_SIZE, friend_pos[1] * TILE_SIZE))

def handle_puzzle():
    global game_state
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:  # Escape to leave puzzle
        game_state = "main"

def draw_puzzle():
    screen.fill((10, 10, 10))
    big_font = pygame.font.SysFont(None, 48)
    text = big_font.render("Circuit Puzzle: Solve the numbers!", True, (0, 255, 0))
    screen.blit(text, (50, WINDOW_HEIGHT // 2 - 24))

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_state == "main":
        draw_map()
        draw_player()
        draw_friend()

        current_tile = tile_map[player_pos[1]][player_pos[0]]

        if current_tile == 4:
            show_message("Press E to interact.")
            if keys[pygame.K_e]:
                game_state = "puzzle"
        else:
            # no message
            pass

        # Movement controls (no sleep!)
        new_x, new_y = player_pos
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and is_walkable(new_x - 1, new_y):
            new_x -= 1
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and is_walkable(new_x + 1, new_y):
            new_x += 1
        elif (keys[pygame.K_w] or keys[pygame.K_UP]) and is_walkable(new_x, new_y - 1):
            new_y -= 1
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and is_walkable(new_x, new_y + 1):
            new_y += 1

        if [new_x, new_y] != player_pos:
            player_pos = [new_x, new_y]
            pygame.time.wait(150)  # short delay to prevent super-fast moves

    elif game_state == "puzzle":
        handle_puzzle()
        draw_puzzle()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
