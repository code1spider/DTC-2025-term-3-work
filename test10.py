import pygame
import sys
import os
import time

# Constants
game_state = "main"
TILE_SIZE = 40
MAP_WIDTH = 10
MAP_HEIGHT = 10
WINDOW_WIDTH = MAP_WIDTH * TILE_SIZE
WINDOW_HEIGHT = MAP_HEIGHT * TILE_SIZE
FPS = 60

# Tile map (your original)
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

# Puzzle variables
start_1 = 10
current_pin = 1
pins_clicked = [False, False, False, False]  # 4 pins
pin_rects = [
    pygame.Rect(100, 100, 40, 40),
    pygame.Rect(160, 100, 40, 40),
    pygame.Rect(220, 100, 40, 40),
    pygame.Rect(280, 100, 40, 40),
]

# Initialize Pygame
pygame.init()
font = pygame.font.SysFont(None, 24)
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
friend_image = load_image("friend.png")
end_led_off = load_image("end_led_off.png")
end_led_on = load_image("end_led_on.png")
end_led_wrong = load_image("end_led_wrong.png")

# Set up entities
player_pos = [0, 0]  # Change this to where you want the player to start
friend_pos = [8, 3]   # changed this to be friend across all instances, including sprite name

# Walkability logic
def is_walkable(x, y):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return tile_map[y][x] not in (2, 3,)  # Add more blocked tile types if needed
    return False

def show_message(text):
    msg = font.render(text, True, (255, 255, 255))  # White text
    screen.blit(msg, (20, WINDOW_HEIGHT - 40))  # Bottom-left corner

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

def draw_friend():
    screen.blit(friend_image, (friend_pos[0] * TILE_SIZE, friend_pos[1] * TILE_SIZE))
dontspam = 0  # <-- Initialize here before the game loop

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

    # Draw pins
    for i, rect in enumerate(pin_rects):
        color = (100, 100, 100) if not pins_clicked[i] else (0, 200, 0)
        pygame.draw.rect(screen, color, rect)
        pin_text = font.render(f"Pin {i+1}", True, (255, 255, 255))
        screen.blit(pin_text, (rect.x, rect.y - 20))

    # Display result LED
    if all(pins_clicked):
        if start_1 == 50:
            screen.blit(end_led_on, (400, 100))
        else:
            screen.blit(end_led_wrong, (400, 100))
    else:
        screen.blit(end_led_off, (400, 100))

    # Show current value
    value_text = font.render(f"Value: {start_1}", True, (255, 255, 0))
    screen.blit(value_text, (50, 300))

# Puzzle logic
def handle_puzzle():
    global game_state, start_1, current_pin

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_state = "main"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            for i, rect in enumerate(pin_rects):
                if rect.collidepoint(mouse_pos) and not pins_clicked[i] and i == current_pin - 1:
                    start_1 += 10
                    pins_clicked[i] = True
                    current_pin += 1

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    draw_map()
    draw_player()
    draw_friend()

    if game_state == 'puzzle':
        # update and draw puzzle screen
        handle_puzzle()
        draw_puzzle()
        pygame.display.flip()
        clock.tick(FPS)
    
    current_tile = tile_map[player_pos[1]][player_pos[0]]

    # Show message inside the main loop AFTER drawing entities
    if game_state == "main":
        if current_tile == 4:
            show_message("Press E to interact.")
            dontspam = 1
            if keys[pygame.K_e]:
                game_state = "puzzle"
        elif current_tile != 4:
            dontspam = 0

    pygame.display.flip()
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement logic
    keys = pygame.key.get_pressed()
    new_x, new_y = player_pos

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if is_walkable(new_x - 1, new_y):
            new_x -= 1
            time.sleep(0.2)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if is_walkable(new_x + 1, new_y):
            new_x += 1
            time.sleep(0.2)
    elif keys[pygame.K_w] or keys[pygame.K_UP]:
        if is_walkable(new_x, new_y - 1):
            new_y -= 1
            time.sleep(0.2)
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if is_walkable(new_x, new_y + 1):
            new_y += 1
            time.sleep(0.2)

    player_pos = [new_x, new_y]




pygame.quit()
sys.exit()
