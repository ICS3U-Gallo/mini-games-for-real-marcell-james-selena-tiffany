
import pygame


pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

char_x = 200
char_y = 200

# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    # Drawing the clown
    pygame.draw.circle(screen, (255, 225, 200), (char_x, char_y), 45)
    pygame.draw.circle(screen, (255, 0, 0), (char_x, char_y + 10), 10)
    pygame.draw.circle(screen, (0, 0, 0), (char_x - 15, char_y - 10), 5)
    pygame.draw.circle(screen, (0, 0, 0), (char_x + 15, char_y - 10), 5)
    pygame.draw.circle(screen, (0, 0, 255), (char_x - 40, char_y - 10), 15)
    pygame.draw.circle(screen, (0, 0, 255), (char_x - 30, char_y - 30), 15)
    pygame.draw.circle(screen, (0, 0, 255), (char_x - 10, char_y - 40), 15)
    pygame.draw.circle(screen, (0, 0, 255), (char_x + 10, char_y - 40), 15)
    pygame.draw.circle(screen, (0, 0, 255), (char_x + 30, char_y - 30), 15)
    pygame.draw.circle(screen, (0, 0, 255), (char_x + 40, char_y - 10), 15)
    pygame.draw.line(screen, (0, 0, 0), (char_x - 15, char_y + 28), (char_x + 15, char_y + 28), 2)

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
