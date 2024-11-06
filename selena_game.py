import random 
import pygame


pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

char_x = WIDTH/2
char_y = 400
going_right = False 
going_left = False 
jumping = False 
jump_speed = 20 
curtain_x = 50 
tire_list = [] 
for i in range(10): 
    tire_x = random.randrange(WIDTH)
    tire_y = random.randrange(HEIGHT) 
    tire = (tire_x, -tire_y)
    tire_list.append(tire)

# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: 
                going_right = True 
            elif event.key == pygame.K_LEFT: 
                going_left = True 
            elif event.key == pygame.K_UP: 
                jumping = True 
                jump_speed *= -1 
        elif event.type == pygame.KEYUP: 
            going_right = False 
            going_left = False 

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    if going_right == True: 
        char_x += 10 
    if going_left == True: 
        char_x -= 10 
    if jumping == True: 
        char_y += jump_speed
    if char_y < 340: 
        jump_speed *= -1
    if char_y > 400: 
        jumping = False 

    # DRAWING
    screen.fill((175, 25, 25))  # always the first drawing command

    # Drawing the background 
    for i in range(50, WIDTH, 125): 
        pygame.draw.polygon(screen, (200, 50, 50), ((i, 0), (i + 50, 0), (i + 75, 400), (i -25, 400)))
    pygame.draw.circle(screen, (175, 100, 50), (WIDTH/2, HEIGHT + 550), 700)

    # Drawing the clown
    pygame.draw.circle(screen, (255, 225, 200), (char_x, char_y), 40)
    pygame.draw.circle(screen, (255, 0, 0), (char_x, char_y + 7), 10)
    pygame.draw.circle(screen, (0, 0, 0), (char_x - 15, char_y - 13), 5)
    pygame.draw.circle(screen, (0, 0, 0), (char_x + 15, char_y - 13), 5)
    pygame.draw.circle(screen, (0, 0, 255), (char_x - 40, char_y - 10), 13)
    pygame.draw.circle(screen, (0, 0, 255), (char_x - 30, char_y - 30), 13)
    pygame.draw.circle(screen, (0, 0, 255), (char_x - 10, char_y - 40), 13)
    pygame.draw.circle(screen, (0, 0, 255), (char_x + 10, char_y - 40), 13)
    pygame.draw.circle(screen, (0, 0, 255), (char_x + 30, char_y - 30), 13)
    pygame.draw.circle(screen, (0, 0, 255), (char_x + 40, char_y - 10), 13)
    pygame.draw.line(screen, (0, 0, 0), (char_x - 15, char_y + 25), (char_x + 15, char_y + 25), 2)


    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
