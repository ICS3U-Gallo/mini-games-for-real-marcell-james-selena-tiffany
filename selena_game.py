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

char_x = 0
char_y = 400
going_right = False 
going_left = False 
jumping = False 
jump_speed = 12 
tire_list = [] 
for i in range(10): 
    tire_x = random.randrange(100, WIDTH)
    tire_y = random.randrange(-600, -30) 
    tire = [tire_x, tire_y]
    tire_list.append(tire)

roll_x = -100 

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
    
    for item in tire_list: 
        item[1] += 7 
        if item[1] > HEIGHT + 50: 
            item[0] = random.randrange(100, WIDTH)
            item[1] = random.randrange(-100, -30)

    chance = random.randrange(100)
    if chance == 1 and roll_x < -100: 
        roll_x = 700

    roll_x -= 15 

    # DRAWING
    screen.fill((175, 25, 25))  # always the first drawing command

    # Drawing the background 
    for i in range(50, WIDTH, 125): 
        pygame.draw.polygon(screen, (200, 50, 50), ((i, 0), (i + 50, 0), (i + 75, 400), (i -25, 400)))
    pygame.draw.circle(screen, (175, 100, 50), (WIDTH/2, HEIGHT + 550), 700)

    # Drawing the clown
    pygame.draw.circle(screen, (255, 225, 200), (char_x, char_y), 35)
    pygame.draw.circle(screen, (255, 0, 0), (char_x, char_y + 5), 10)
    pygame.draw.circle(screen, (0, 0, 0), (char_x - 15, char_y - 13), 5)
    pygame.draw.circle(screen, (0, 0, 0), (char_x + 15, char_y - 13), 5)
    pygame.draw.circle(screen, (0, 0, 255), (char_x - 38, char_y - 8), 13)
    pygame.draw.circle(screen, (0, 0, 255), (char_x - 28, char_y - 28), 13)
    pygame.draw.circle(screen, (0, 0, 255), (char_x - 10, char_y - 38), 13)
    pygame.draw.circle(screen, (0, 0, 255), (char_x + 10, char_y - 38), 13)
    pygame.draw.circle(screen, (0, 0, 255), (char_x + 28, char_y - 28), 13)
    pygame.draw.circle(screen, (0, 0, 255), (char_x + 38, char_y - 8), 13)
    pygame.draw.line(screen, (0, 0, 0), (char_x - 15, char_y + 23), (char_x + 15, char_y + 23), 2)

    # Drawing the tires falling down 
    for item in tire_list: 
        pygame.draw.circle(screen, (0, 0, 0), (item[0], item[1]), 30)
        pygame.draw.circle(screen, (128, 128, 128), (item[0], item[1]), 25)
        pygame.draw.circle(screen, (0, 0, 0), (item[0], item[1]), 15)
    
    # Drawing the tire rolling on the ground 
    pygame.draw.circle(screen, (0, 0, 0), (roll_x, 450), 25)
    pygame.draw.circle(screen, (128, 128, 128), (roll_x, 450), 20)
    pygame.draw.circle(screen, (0, 0, 0), (roll_x, 450), 10)

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
