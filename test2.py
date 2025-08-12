import pygame
import sys

# Initialize Pygame
pygame.init()

# Define screen size
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Interactive Dialogue")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define font
font = pygame.font.Font(None, 36)

# Load background image
background = pygame.Surface((800, 600))
background.fill((255, 255, 255))  # White background

# Define options in the dialogue box
option1 = pygame.Rect(300, 400, 200, 50)
option2 = pygame.Rect(300, 500, 200, 50)

# Display text
def display_text(text, x, y):
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (x, y))

# Game loop
running = True
while running:
    screen.fill(WHITE)  # Fill the screen with white color
    screen.blit(background, (0, 0))  # Display background image

    # Draw dialogue box options
    pygame.draw.rect(screen, (0, 0, 255), option1)
    pygame.draw.rect(screen, (0, 255, 0), option2)

    # Display option texts
    display_text("Option 1: Talk to NPC", 310, 410)
    display_text("Option 2: Leave", 310, 510)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if option1.collidepoint(event.pos):
                print("Option 1 clicked: Talk to NPC")
                background.fill((255, 255, 0))
            elif option2.collidepoint(event.pos):
                print("Option 2 clicked: Leave")
                background.fill((0, 255, 255))

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
