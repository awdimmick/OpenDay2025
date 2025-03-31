# Program: Single player snake game

# Library with PyGame functions
import pygame
import random

# Define constants (in CAPITALS!) for our game settings
MAX_X = 640         # Define the size of the game display window in pixels
MAX_Y = 640
TILE_SIZE = 16      # Define the size in pixels of each tile in the game (same size as snake and apple)
FPS = 15            # Set the frames per second (refresh rate)

# Define constants for colours in (r,g,b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED =   (255, 0, 0)
GREEN = (0, 155, 0)


# Get PyGame initialised
pygame.init()
# setup sound mixer to avoid sound lag
# pygame.mixer.pre_init(44100, -16, 2, 2048)
# Setup the apple eating sound
# apple_sound = pygame.mixer.Sound('apple_bite.wav')

# Run some music in the background
# pygame.mixer.music.load("background_music.wav")
# pygame.mixer.music.play(-1)         # the -1 is the loops, so here is infinite
# pygame.mixer.music.set_volume(0.2)
 
# Setup surface / canvas (Entered as a Tuple () - return pygame object
display = pygame.display.set_mode((MAX_X, MAX_Y))

# Change the window title
pygame.display.set_caption('Snake Game V3.0')

# Add an icon to the game window
icon = pygame.image.load('snake_icon.png')
pygame.display.set_icon(icon)

# Include a background image
background = pygame.image.load("background.png")

# Define clock
clock = pygame.time.Clock()


class Game:
    # States are "intro", "playing", "paused", "game_over", "quit"
    state = "intro"
    score = 0


class Snake:
    x = MAX_X / 2           # Horizontal snake start position
    y = MAX_Y / 2           # Vertical snake start position
    direction = "right"     # Define the snake head direction
    x_change = 0            # Start not moving in either axis
    y_change = 0
    tail = []               # Declare a list to hold coordinates for the snake's tail as (x, y) tuples
    # Load image, convert with transparency
    img = pygame.image.load('snakeHead.png').convert_alpha()


class Apple:
    # Choose a random X and Y between 0 and the screen size, in multiples of TILE_SIZE to align to our grid
    x = random.randrange(0, MAX_X, TILE_SIZE)
    y = random.randrange(0, MAX_Y, TILE_SIZE)
    # Load image, convert with transparency
    img = pygame.image.load('apple.png').convert_alpha()


# Helper procedure to write text on screen. Defaults for y_displace (0) and font (small = 24px) size are shown
def draw_text(text, colour, y_displace=0, size=24):
    font = pygame.font.SysFont("comicsanms", size)              # Generate the font at the specified size (24 is smallish, 48 is medium, 80 for titles)
    
    text_surface = font.render(text, True, colour)              # Get the surface containing the actual message drawn in the right colour

    text_rect = text_surface.get_rect()                         # Get the rectangle the text is drawn in
    text_rect.center = (MAX_X / 2), (MAX_Y / 2) + y_displace    # Setup the centre point adjusted by the y_displace
    
    display.blit(text_surface, text_rect)                       # Place the text on the display


# A message at the beginning of the game
def intro():
    # Respond to events first
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:    # Press any key to start
            Game.state = "playing"

    # Draw intro message
    display.fill(WHITE)
    draw_text("The Snake Game", GREEN, -100, 80)
    draw_text("Eat the apples", BLACK, -30)
    draw_text("The more apples you eat, the longer you get", BLACK, 10)
    draw_text("Do not touch the edges or yourself", BLACK, 40)
    draw_text("Press any key to start", BLACK, 80)


def paused():
    # Handle pause events first
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quitting by clicking red X
            Game.state = "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # C to Continue
                Game.state = "playing"
            elif event.key == pygame.K_q:  # Q to Quit
                Game.state = "quit"

    # Draw the game in the background like normal
    game_draw()

    # Draw pause menu message on top
    draw_text("Paused", GREEN, -100, 80)
    draw_text("Press - C to continue, Q to quit", BLACK)


# Handle all the events while the game is being played
def game_events():
    for event in pygame.event.get():        # Loop through each event this frame
        if event.type == pygame.QUIT:       # Respond to clicking the quit button
            Game.state = "quit"
        elif event.type == pygame.KEYDOWN:  # Check the different keys
            if event.key == pygame.K_p:     # If 'P' is pressed
                Game.state = "paused"
            if event.key == pygame.K_LEFT:
                Snake.direction = 'left'
            elif event.key == pygame.K_RIGHT:
                Snake.direction = 'right'
            elif event.key == pygame.K_UP:
                Snake.direction = 'up'
            elif event.key == pygame.K_DOWN:
                Snake.direction = 'down'


# Run the game logic for each frame: move elements, check collisions etc.
def game_update():
    # 🐍 Move Snake 🐍
    Snake.tail.append((Snake.x, Snake.y))   # Add the current head position to the tail list

    directions = {
        'left': (-TILE_SIZE, 0),
        'right': (TILE_SIZE, 0),
        'up': (0, -TILE_SIZE),
        'down': (0, TILE_SIZE)
    }

    Snake.x_change, Snake.y_change = directions[Snake.direction]

    Snake.x += Snake.x_change
    Snake.y += Snake.y_change  # Add the x or y change to the current position to move the head

    # 🍎 Check Apple collision 🍎
    if Snake.x == Apple.x and Snake.y == Apple.y:
        Game.score += 1                                     # Add 1 to the score
        
        Apple.x = random.randrange(TILE_SIZE, MAX_X-TILE_SIZE, TILE_SIZE)     # Generate new location for the apple
        Apple.y = random.randrange(TILE_SIZE, MAX_Y-TILE_SIZE, TILE_SIZE)
    else:
        Snake.tail.pop(0)   # If the snake didn't eat an apple, remove the first item from the list (end of the tail)

    # Check wall collisions
    if Snake.x < 0 or Snake.x >= MAX_X or Snake.y < 0 or Snake.y >= MAX_Y:
        Game.state = "game_over"
    # Check tail collisions
    for XnY in Snake.tail:
        if XnY == (Snake.x, Snake.y):
            Game.state = "game_over"
        

# Draw all the sprites that make up the game
def game_draw():
    # 🖼 Draw the background first at (0, 0) the top left corner 🖼
    display.fill(WHITE)
    display.blit(background, (0, 0))

    # 🍎 Draw the Apple using its coordinates 🍎
    display.blit(Apple.img, (Apple.x, Apple.y))

    # 🐍 Start drawing the Snake 🐍
    head = Snake.img    # Define the head of the snake
    # Determine if the snake head should be rotated
    if Snake.direction == 'right':
        head = pygame.transform.rotate(Snake.img, 270)
    elif Snake.direction == 'left':
        head = pygame.transform.rotate(Snake.img, 90)
    elif Snake.direction == 'down':
        head = pygame.transform.rotate(Snake.img, 180)
    # Draw the head
    display.blit(head, (Snake.x, Snake.y))

    # Iterate through each snake block and display them
    for XnY in Snake.tail:
        # rect in [] list   x,y,w,h  0,0 is top left
        pygame.draw.rect(display, GREEN, [XnY[0], XnY[1], TILE_SIZE, TILE_SIZE])

    # 🏆 Draw the score 🏆
    draw_text("Score: " + str(Game.score), BLACK, -300)


def game_over():
    # Handle events first
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quitting by clicking red X
            Game.state = "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:     # R to Restart
                restart()
                Game.state = "playing"
            elif event.key == pygame.K_q:   # Q to Quit
                Game.state = "quit"

    # Draw the game in the background like normal
    display.fill(WHITE)
    draw_text("Game Over", RED, -100, 80)
    draw_text("Your score was: " + str(Game.score), BLACK, -30, 48)
    draw_text("Press R to Play Again", BLACK, 40)
    draw_text("Press Q to Quit", BLACK, 70)


def restart():
    Snake.x = MAX_X / 2
    Snake.y = MAX_Y / 2
    Snake.direction = "right"
    Snake.x_change = 0
    Snake.y_change = 0
    Snake.tail = []
    
    Apple.x = random.randrange(0, MAX_X, TILE_SIZE)
    Apple.y = random.randrange(0, MAX_Y, TILE_SIZE)

    Game.score = 0
    Game.state = "playing"


# Game loop
while Game.state != "quit":

    # Check what state the game is in and respond every frame
    if Game.state == "playing":
        game_events()
        game_update()
        game_draw()
    elif Game.state == "intro":
        intro()
    elif Game.state == "paused":
        paused()
    elif Game.state == "game_over":
        game_over()

    # 🎇 Actually update the display 🎇
    pygame.display.update()
    # ⏱ Tick the clock every frame by the desired FPS ⏱
    clock.tick(FPS)

pygame.quit()   # Tidy but not necessary
quit()
