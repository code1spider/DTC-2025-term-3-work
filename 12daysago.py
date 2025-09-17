
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

# Map definitions
map_one = [
    [0, 0, 4, 3, 3, 3, 3, 4, 2, 0],
    [0, 0, 0, 4, 3, 3, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 0, 0, 0, 0],
    [2, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [2, 0, 0, 0, 1, 1, 0, 0, 11, 0],
    [0, 0, 0, 0, 1, 1, 0, 2, 0, 0],
    [0, 0, 2, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 2, 0, 1, 1, 0, 0, 0, 2],
    [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
]

map_two = [
    [6, 6, 6, 6, 5, 5, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [9, 1, 1, 1, 1, 1, 1, 1, 1, 8],
    [9, 1, 1, 1, 1, 1, 1, 1, 1, 8],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
    [6, 6, 6, 6, 1, 1, 6, 6, 6, 6],
]

map_three = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

map_four = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 10, 0, 0, 0, 9],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
# Puzzle variables
start_1 = 0
pins_clicked = [False] * 8
pin_values = [10, 5, 15, 20, 5, 10, -5, -10]  # Combination translates to a series of numbers usable for a password/pin
pin_rects = []
for i in range(8):
    col = i % 4
    row = i // 4
    x = 100 + col * 60
    y = 100 + row * 60
    pin_rects.append(pygame.Rect(x, y, 40, 40))

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
    4: load_image("floor.png"),  # Marker for friend spawn
    5: load_image("doorshadow.png"),
    6: load_image("floor.png"),
    8: load_image("doorshadow.png"),
    9: load_image("doorshadow.png"),
    10: load_image("letter.png"),
    11: load_image("friend.png")
}

# Load entities
player_image = load_image("player.png")
friend_image = load_image("friend.png")
end_led_off = load_image("end_led_off.png")
end_led_on = load_image("end_led_on.png")
end_led_wrong = load_image("end_led_wrong.png")

# Utility to find the first tile with a given value
def find_tile(tile_value, tile_map):
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == tile_value:
                return x, y
    return None

# Prompt for player name
def get_player_name_and_code():
    name_input = ""
    input_active = True
    input_box = pygame.Rect(100, 200, 200, 40)
    font_big = pygame.font.SysFont(None, 36)

    while input_active:
        screen.fill((0, 0, 0))
        prompt = font_big.render("Enter your name:", True, (255, 255, 255))
        screen.blit(prompt, (100, 150))

        txt_surface = font_big.render(name_input, True, (255, 255, 0))
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name_input:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                else:
                    name_input += event.unicode

        pygame.display.flip()
        clock.tick(30)

    # Compute access code
    if len(name_input) < 2:
        return name_input, 17
        name_input = 2517
        return name_input, 2517
    second = name_input[1].lower()
    if not second.isalpha():
        return name_input, 17
        return name_input, 2517
    value = ord(second) - ord('a') + 1
    return name_input, 71 if value < 10 else value
    return name_input, 2571 if value < 10 else value

player_name, access_code_room3 = get_player_name_and_code()
# Current map and player position — start on map_two tile 5
current_map = map_two
player_pos = list(find_tile(5, current_map))

friend_pos = [8, 3]  # stays static for now

# Walkability
def is_walkable(x, y):
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        return current_map[y][x] not in (2, 3)
    return False

# Draw map
def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = current_map[y][x]
            image = tile_images.get(tile)
            if image:
                screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

# Draw entities
def draw_player():
    screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

def draw_friend():
    screen.blit(friend_image, (friend_pos[0] * TILE_SIZE, friend_pos[1] * TILE_SIZE))

# Show interaction message
def show_message(text):
    msg = font.render(text, True, (255, 255, 255))
    screen.blit(msg, (20, WINDOW_HEIGHT - 40))

# Draw puzzle screen
def draw_puzzle():
    screen.fill((10, 10, 10))
    big_font = pygame.font.SysFont(None, 48)
    text = big_font.render("Circuit Puzzle: Solve the numbers!", True, (0, 255, 0))
    screen.blit(text, (50, 20))

    for i, rect in enumerate(pin_rects):
        color = (100, 100, 100) if not pins_clicked[i] else (0, 200, 0)
        pygame.draw.rect(screen, color, rect)
        pin_text = font.render(f"Pin {i+1}", True, (255, 255, 255))
        screen.blit(pin_text, (rect.x, rect.y - 20))

    if all(pins_clicked):
        if start_1 == 50:
            screen.blit(end_led_on, (400, 100))
            win_text = font.render("Correct combination!", True, (0, 255, 0))
            screen.blit(win_text, (400, 160))
        else:
            screen.blit(end_led_wrong, (400, 100))
            lose_text = font.render("Incorrect. Try again.", True, (255, 0, 0))
            screen.blit(lose_text, (400, 160))
    else:
        screen.blit(end_led_off, (400, 100))

    value_text = font.render(f"Value: {start_1}", True, (255, 255, 0))
    screen.blit(value_text, (50, 300))

# Puzzle logic
def handle_puzzle():
    global game_state, start_1, pins_clicked

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_state = "main"
            start_1 = 0
            pins_clicked = [False] * 8
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(pin_rects):
                if rect.collidepoint(mouse_pos) and not pins_clicked[i]:
                    start_1 += pin_values[i]
                    pins_clicked[i] = True

# Game loop
running = True
dontspam = 0
new_x, new_y = player_pos

while running:
    screen.fill((0, 0, 0))

    if game_state == 'puzzle':
        handle_puzzle()
        draw_puzzle()
        pygame.display.flip()
        clock.tick(FPS)
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    draw_map()
    draw_player()
    draw_friend()

    current_tile = current_map[player_pos[1]][player_pos[0]]

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

    # Movement logic
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

    # After moving, check if on tile 5 to switch maps
    current_tile = current_map[player_pos[1]][player_pos[0]]
    if current_tile == 5:
        if current_map == map_one:
            current_map = map_two
            player_pos = (4, 1)
            new_x, new_y = player_pos
        else:
            current_map = map_one
            player_pos = (4, 8)
            new_x, new_y = player_pos

    if current_tile == 8 and current_map == map_two:
        code_input = ""
        input_box = pygame.Rect(100, 200, 200, 40)
        font_big = pygame.font.SysFont(None, 36)
        entering = True
        while entering:
            screen.fill((0, 0, 0))
            prompt = font_big.render(f"Access Code Required, {player_name}:", True, (255, 255, 255))
            screen.blit(prompt, (50, 150))
            txt_surface = font_big.render(code_input, True, (255, 255, 0))
            pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if code_input.isdigit() and int(code_input) == access_code_room3:
                            access_code_room3 = 25 + access_code_room3
                            current_map = map_three
                            player_pos = [1, 4]
                            entering = False
                    elif event.key == pygame.K_BACKSPACE:
                        code_input = code_input[:-1]
                    else:
                        if len(code_input) < 4 and event.unicode.isdigit():
                            code_input += event.unicode
        new_x, new_y = player_pos
    elif current_tile == 8 and current_map == map_three:
        current_map = map_two
        player_pos = [8,4]
        new_x, new_y = player_pos


    if current_tile == 9:
        if current_map == map_four:
            current_map = map_two
            player_pos = (1,5)
            new_x, new_y = player_pos
        else:
        if current_map == map_two:
            current_map = map_four
            player_pos = (8,4)
            new_x, new_y = player_pos
        else:
            current_map = map_two
            player_pos = (1,5)
            new_x, new_y = player_pos

    if current_tile == 10:
        if keys[pygame.K_e]:
            screen = pygame.display.set_mode((400, 400))  # or pygame.FULLSCREEN
            pygame.display.set_caption("Letter Overlay Example")

            # Load your letter image
            letter_image = pygame.image.load("code.png")

            # Optionally scale it to fit the screen
            letter_image = pygame.transform.scale(letter_image, screen.get_size())

            # Main loop
            show_letter = True
            while show_letter:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        show_letter = False
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        # Press any key or click to exit the letter view
                        show_letter = False

                # Fill background (optional)
                screen.fill((0, 0, 0))  # Black background

                # Draw the letter image
                screen.blit(letter_image, (0, 0))

                # Update the screen
                pygame.display.flip()

            # Quit Pygame
    

pygame.quit()
sys.exit()
