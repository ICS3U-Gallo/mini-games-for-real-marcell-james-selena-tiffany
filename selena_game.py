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

# Character variables 
char_x = 0
char_y = 400
going_right = False 
going_left = False 
jumping = False 
jump_speed = 12 
char_colour = (255, 225, 200)
flash_start = 0 

# Tire variables 
tire_list = [] 
tire_rects = [] 
for i in range(10): 
    tire_x = random.randrange(100, WIDTH)
    tire_y = random.randrange(-600, -30) 
    tire = [tire_x, tire_y]
    tire_list.append(tire)
    rect = pygame.Rect(tire_x - 25, tire_y - 25, 50, 50)
    tire_rects.append(rect)

roll_x = -100 

# System and text variables 
welcome_screen = True 
win = False 
text_font = pygame.font.SysFont("Nunito", 30, False, False)
win_message = "Congrats! You got across the stage!"
win_text = text_font.render(win_message, True, (0, 0, 0))
welcome_message = "Uh oh, there are tires rolling and falling onto the stage!"
welcome_text = text_font.render(welcome_message, True, (0, 0, 0))
instructions_message = "Get across the stage by dodging the tires."
instructions_text = text_font.render(instructions_message, True, (0, 0, 0))
directions_message = "Use arrow keys to move left, move right, and jump."
directions_text = text_font.render(directions_message, True, (0, 0, 0))
click_message = "Click to begin." 
click_text = text_font.render(click_message, True, (0, 0, 0))

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
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            welcome_screen = False 

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # Character moving left and right 
    if going_right == True: 
        char_x += 10 
    if going_left == True: 
        char_x -= 10 
    
    # Character jumping 
    if jumping == True: 
        char_y += jump_speed
    if char_y < 340: 
        jump_speed *= -1
    if char_y > 400: 
        jumping = False 
    
    # Make sure character can't go completely off screen
    if char_x < 0: 
        char_x = 0 
    
    char_rect = pygame.Rect(char_x - 40, char_y - 40, 80, 70)
    
    # Tires moving 
    for i in range(len(tire_list)): 
        tire_list[i][1] += 7 
        rect = pygame.Rect(tire_list[i][0] - 25, tire_list[i][1] - 25, 50, 50)
        tire_rects[i] = rect 
        if tire_list[i][1] > HEIGHT + 50: 
            new_x = random.randrange(100, WIDTH)
            new_y = random.randrange(-100, -30) 
            tire_list[i][0] = new_x 
            tire_list[i][1] = new_y 

    # Checking for collision between character and falling tires 
    # Brings character back to starting point and turns them red for a second 
    for item in tire_rects: 
        if char_rect.colliderect(item): 
            char_colour = (255, 80, 80)
            char_x = 0 
            char_y = 400
            flash_start = pygame.time.get_ticks() 

    # A random chance that a tire might roll on the ground towards the character  
    chance = random.randrange(100)
    if chance == 1 and roll_x < -100: 
        roll_x = 700

    roll_x -= 15 
    roll_rect = pygame.Rect(roll_x - 20, 420, 40, 40)

    # Checking for collision between character and the rolling tire
    # Brings character back to starting point and turns them red for a second 
    if char_rect.colliderect(roll_rect): 
        char_colour = (255, 80, 80)
        char_x = 0 
        char_y = 400 
        flash_start = pygame.time.get_ticks() 

    # Turns character back to normal colour after getting hit 
    if pygame.time.get_ticks() - flash_start > 200: 
        char_colour = (255, 225, 200)

    # Win condition 
    if char_x > WIDTH: 
        win = True 

    # DRAWING 
    screen.fill((175, 25, 25))  # always the first drawing command

    # Drawing the background 
    for i in range(50, WIDTH, 125): 
        pygame.draw.polygon(screen, (200, 50, 50), ((i, 0), (i + 50, 0), (i + 75, 400), (i -25, 400)))
    pygame.draw.circle(screen, (175, 100, 50), (WIDTH/2, HEIGHT + 550), 700)

    # Drawing the clown
    pygame.draw.circle(screen, char_colour, (char_x, char_y), 35)
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
        pygame.draw.circle(screen, (0, 0, 0), (item[0], item[1]), 30, 20)
        pygame.draw.circle(screen, (128, 128, 128), (item[0], item[1]), 20, 8)
    
    # Drawing the tire rolling on the ground 
    pygame.draw.circle(screen, (0, 0, 0), (roll_x, 440), 25, 15)
    pygame.draw.circle(screen, (128, 128, 128), (roll_x, 440), 18, 6)

    if welcome_screen == True: 
        screen.fill((255, 210, 210))
        screen.blit(welcome_text, (60, 100))
        screen.blit(instructions_text, (100, 175))
        screen.blit(directions_text, (80, 250))
        screen.blit(click_text, (250, 325))

    if win == True: 
        screen.fill((150, 255, 150))
        screen.blit(win_text, (125, 200))

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
