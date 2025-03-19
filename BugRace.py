# Writting by Mohammad Hossein Yaghubi
# Email: m.h.yaghubi.info@gmail.com
# --------------------------------------
# Github: https://github.com/MohammadHosseinYaghubi/BugRace
# --------------------------------------
# Python Version: 3.10
# Pygame Version: 1.7
# --------------------------------------

import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Load sounds
crash_sound = pygame.mixer.Sound("lose-m.wav")
pygame.mixer.music.load("world-m.ogg")

# Game window dimensions
display_width = 800
display_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)

# Set up the game display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Race Bug')

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load bug image
bugImg = pygame.image.load("Bug.png")
bug_width = 48  # Width of the bug

def button(msg, x, y, w, h, ic, ac, action=None):
    """
    Create a button with the specified message, position, size, and colors.
    If the button is clicked, the specified action is executed.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Check if the mouse is over the button
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))  # Active color
        if click[0] == 1 and action is not None:
            action()  # Execute the action if clicked
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))  # Inactive color

    # Render the button text
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(TextSurf, TextRect)

def quitgame():
    """Quit the game and close the Pygame window."""
    pygame.quit()
    quit()

def game_intro():
    """Display the game introduction screen."""
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = text_objects("Let's Play Game", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        # Create Play and Quit buttons
        button("Play!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()

def stuff_dodged(count):
    """Display the number of obstacles dodged (score)."""
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(count), True, red)
    gameDisplay.blit(text, (0, 0))

def stuff(stuffx, stuffy, stuffw, stuffh, color):
    """Draw an obstacle on the screen."""
    pygame.draw.rect(gameDisplay, color, [stuffx, stuffy, stuffw, stuffh])

def bug(x, y):
    """Draw the bug on the screen."""
    gameDisplay.blit(bugImg, (x, y))

def text_objects(text, font):
    """Create a text surface and its rectangle for rendering."""
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    """Display a message on the screen for 2 seconds."""
    largeText = pygame.font.Font('freesansbold.ttf', 90)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

    time.sleep(2)
    game_loop()

def crash():
    """Handle the crash event."""
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    # Display crash message
    largeText = pygame.font.Font('freesansbold.ttf', 90)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Create Try Again and Quit buttons
        button("Try Again", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()

def game_loop():
    """Main game loop."""
    pygame.mixer.music.play(-1)  # Play background music in a loop

    # Initial bug position
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0  # Change in bug's x position

    # Initial obstacle position and properties
    stuff_startx = random.randrange(0, display_width)
    stuff_starty = -700
    stuff_speed = 7
    stuff_width = 100
    stuff_height = 100

    dodged = 0  # Number of obstacles dodged

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle bug movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        # Draw the obstacle
        stuff(stuff_startx, stuff_starty, stuff_width, stuff_height, red)
        stuff_starty += stuff_speed

        # Display the score
        stuff_dodged(dodged)

        # Draw the bug
        bug(x, y)

        # Check for collisions with the window edges
        if x > display_width - bug_width or x < 0:
            crash()

        # Check if the obstacle has passed the bug
        if stuff_starty > display_height:
            stuff_starty = 0 - stuff_height
            stuff_startx = random.randrange(0, display_width)
            dodged += 1
            stuff_speed += 1

        # Check for collisions with the obstacle
        if y < stuff_starty + stuff_height:
            if x > stuff_startx and x < stuff_startx + stuff_width or x + bug_width > stuff_startx and x + bug_width < stuff_startx + stuff_width:
                crash()

        pygame.display.update()
        clock.tick(60)  # Limit the frame rate to 60 FPS

# Start the game
game_intro()
game_loop()
pygame.quit()
quit()