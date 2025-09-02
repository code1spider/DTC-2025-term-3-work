import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display (you can use FULLSCREEN or a fixed resolution)
screen = pygame.display.set_mode((800, 600))  # or pygame.FULLSCREEN
pygame.display.set_caption("Letter Overlay Example")

# Load your letter image
letter_image = pygame.image.load("grass.png")

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
