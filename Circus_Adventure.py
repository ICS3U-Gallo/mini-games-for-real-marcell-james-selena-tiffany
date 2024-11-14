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

# MARCELL'S VARIABLES 

#Player
player_x = 320
player_y = 420

# Balloons
balloon_x = 100
balloon_y = 100
balloon_x_speed = 10
balloon_y_speed = 10

balloon_2_x = 500
balloon_2_y = 200
balloon_2_x_speed = 10
balloon_2_y_speed = 10

balloon_3_x = 400
balloon_3_y = 150
balloon_3_x_speed = 10
balloon_3_y_speed = 10

balloon_4_x = 600
balloon_4_y = 50
balloon_4_x_speed = 10
balloon_4_y_speed = 10

balloon_5_x = 350
balloon_5_y = 100
balloon_5_x_speed = 10
balloon_5_y_speed = 10

#The Bomb
bomb_x = WIDTH//2
bomb_y = HEIGHT//2
bomb_x_speed = 5
bomb_y_speed = 5
explosion_radius = 10
explosion = False
explosion_count = 0

#Powerups
shield_orb = False
shield = False 
shield_x = 1000
shield_y = 1000
end_game = False
shield_start_time = 0

darts = []

#Score
score = 0
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
text_font = pygame.font.SysFont("Nunito", 40)

#Initialization
initalization = True
initalization_start_time = pygame.time.get_ticks()
end = False
# ---------------------------

# SELENA'S VARIABLES 

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
type_font = pygame.font.SysFont("Nunito", 30, False, False)
win_message = "Congrats! You got across the stage!"
win_text = type_font.render(win_message, True, (0, 0, 0))
welcome_message = "Uh oh, there are tires rolling and falling onto the stage!"
welcome_text = type_font.render(welcome_message, True, (0, 0, 0))
instructions_message = "Get across the stage by dodging the tires."
instructions_text = type_font.render(instructions_message, True, (0, 0, 0))
directions_message = "Use arrow keys to move left, move right, and jump."
directions_text = type_font.render(directions_message, True, (0, 0, 0))
click_message = "Click to begin." 
click_text = type_font.render(click_message, True, (0, 0, 0))

# Whoever's game it is 
tiffany = False
marcell = True 
selena = False 
james = False

# ---------------------------
running = True
while running:

    # MARCELL'S GAME 
    if marcell == True: 
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dart = [player_x,player_y-25]
                    darts.append(dart)
            elif event.type == pygame.MOUSEBUTTONDOWN and end == True:
                marcell = False
                selena = True
                end = False
        # GAME STATE UPDATES
        # All game math and comparisons happen here
        if initalization == True:
            draw_text("Pop 50 Balloons to Win!", text_font, (255,255,255), 150,190)
            draw_text("Mouse to Move, SPACE to Shoot!", text_font, (255,255,255), 110,220)
            draw_text("Careful of the Bomb!", text_font, (255,255,255), 170,250)
            if pygame.time.get_ticks() - initalization_start_time > 5000:
                initalization = False
        if score >= 50:
            end = True
        if end == True:
            bomb_x = -1000
            bomb_x_speed = 0
            pygame.draw.rect(screen, (0, 0, 0), (0,0,WIDTH,HEIGHT))
            draw_text("Congratulations! You Won!!", text_font, (255,255,255), 130,200)
            draw_text("Click to Continue", text_font, (255,255,255), 190,230)
        if initalization == False and score < 50:
            shield_orb_hitbox = pygame.Rect(shield_x,shield_y,20,20)
            # Darts  
            for pos in darts:
                pos[1] -= 30
                if pos[1] <= balloon_y+30 and pos[1] >= balloon_y-30 and pos[0] >= balloon_x-30 and pos[0] <= balloon_x+30: 
                    score += 1
                    shield_orb_random = random.randrange(0,15)
                    if shield_orb_random == 0 and shield_y > HEIGHT:
                        shield_x = random.randrange(1,WIDTH-20)
                        shield_y = -20
                        shield_orb = True
                    pos[0] = 1000
                    pos[1] = 1000
                    balloon_x = random.randrange(50,600,10)
                    balloon_y = random.randrange(50,230,10)
                if pos[1] <= balloon_2_y+30 and pos[1] >= balloon_2_y-30 and pos[0] >= balloon_2_x-30 and pos[0] <= balloon_2_x+30:
                    score += 1
                    shield_orb_random = random.randrange(0,15)
                    if shield_orb_random == 0 and shield_y > HEIGHT:
                        shield_x = random.randrange(1,WIDTH-20)
                        shield_y = -20
                        shield_orb = True
                    pos[0] = 1000
                    pos[1] = 1000
                    balloon_2_x = random.randrange(50,600,10)
                    balloon_2_y = random.randrange(50,230,10)
                if pos[1] <= balloon_3_y+30 and pos[1] >= balloon_3_y-30 and pos[0] >= balloon_3_x-30 and pos[0] <= balloon_3_x+30:
                    score += 1
                    shield_orb_random = random.randrange(0,15)
                    if shield_orb_random == 0 and shield_y > HEIGHT:
                        shield_x = random.randrange(1,WIDTH-20)
                        shield_y = -20
                        shield_orb = True
                    pos[0] = 1000
                    pos[1] = 1000
                    balloon_3_x = random.randrange(50,600,10)
                    balloon_3_y = random.randrange(50,230,10)
                if pos[1] <= balloon_4_y+30 and pos[1] >= balloon_4_y-30 and pos[0] >= balloon_4_x-30 and pos[0] <= balloon_4_x+30:
                    score += 1
                    shield_orb_random = random.randrange(0,15)
                    if shield_orb_random == 0 and shield_y > HEIGHT:
                        shield_x = random.randrange(1,WIDTH-20)
                        shield_y = -20
                        shield_orb = True
                    pos[0] = 1000
                    pos[1] = 1000
                    balloon_4_x = random.randrange(50,600,10)
                    balloon_4_y = random.randrange(50,230,10)
                if pos[1] <= balloon_5_y+30 and pos[1] >= balloon_5_y-30 and pos[0] >= balloon_5_x-30 and pos[0] <= balloon_5_x+30:
                    score += 1
                    shield_orb_random = random.randrange(0,15)
                    if shield_orb_random == 0 and shield_y > HEIGHT:
                        shield_x = random.randrange(1,WIDTH-20)
                        shield_y = -20
                        shield_orb = True
                    pos[0] = 1000
                    pos[1] = 1000
                    balloon_5_x = random.randrange(50,600,10)
                    balloon_5_y = random.randrange(50,230,10)
                if pos[1] <= bomb_y+50 and pos[1] >= bomb_y-50 and pos[0] >= bomb_x-50 and pos[0] <= bomb_x+50:
                    pos[0] = 1000
                    pos[1] = 1000
                    explosion = True
            # Bomb
            bomb_x += bomb_x_speed
            if bomb_x >= WIDTH-50 or bomb_x <= 50:
                bomb_x_speed *= -1
            bomb_y += bomb_y_speed
            if bomb_y >= HEIGHT-50 or bomb_y <= 50:
                bomb_y_speed *= -1
            bomb_hitbox = pygame.Rect(bomb_x-40,bomb_y-40,80,80)
            # Mouse Control
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player_x = mouse_x
            if shield == True:
                player_hitbox = pygame.Rect(1000,player_y-30,60,60)
            if shield == False:
                player_hitbox = pygame.Rect(player_x-30,player_y-30,60,60)
            #Balloons
                #Balloon 1
            if balloon_x+30 == WIDTH or balloon_x-30 == 0:
                balloon_x_speed *= -1
            balloon_x += balloon_x_speed
            balloon_x_switcher = random.randrange(0,50)
            if balloon_x_switcher == 0:
                balloon_x_speed *=-1
                balloon_x += balloon_x_speed
            
            if balloon_y+30 == 300 or balloon_y-30 == 0:
                balloon_y_speed *= -1
            balloon_y += balloon_y_speed
            balloon_y_switcher = random.randrange(0,50)
            if balloon_y_switcher == 0:
                balloon_y_speed *=-1
                balloon_y += balloon_y_speed
                # Balloon 2
            if balloon_2_x+30 == WIDTH or balloon_2_x-30 == 0:
                balloon_2_x_speed *= -1
            balloon_2_x += balloon_2_x_speed
            balloon_2_x_switcher = random.randrange(0,50)
            if balloon_2_x_switcher == 0:
                balloon_2_x_speed *=-1
                balloon_2_x += balloon_2_x_speed
            
            if balloon_2_y+30 == 300 or balloon_2_y-30 == 0:
                balloon_2_y_speed *= -1
            balloon_2_y += balloon_2_y_speed
            balloon_2_y_switcher = random.randrange(0,50)
            if balloon_2_y_switcher == 0:
                balloon_2_y_speed *=-1
                balloon_2_y += balloon_2_y_speed 
                #Balloon 3
            if balloon_3_x+30 == WIDTH or balloon_3_x-30 == 0:
                balloon_3_x_speed *= -1
            balloon_3_x += balloon_3_x_speed
            balloon_3_x_switcher = random.randrange(0,50)
            if balloon_3_x_switcher == 0:
                balloon_3_x_speed *=-1
                balloon_3_x += balloon_3_x_speed
            
            if balloon_3_y+30 == 300 or balloon_3_y-30 == 0:
                balloon_3_y_speed *= -1
            balloon_3_y += balloon_3_y_speed
            balloon_3_y_switcher = random.randrange(0,50)
            if balloon_3_y_switcher == 0:
                balloon_3_y_speed *=-1
                balloon_3_y += balloon_3_y_speed
                #Balloon 4
            if balloon_4_x+30 == WIDTH or balloon_4_x-30 == 0:
                balloon_4_x_speed *= -1
            balloon_4_x += balloon_4_x_speed
            balloon_4_x_switcher = random.randrange(0,50)
            if balloon_4_x_switcher == 0:
                balloon_4_x_speed *=-1
                balloon_4_x += balloon_4_x_speed
            
            if balloon_4_y+30 == 300 or balloon_4_y-30 == 0:
                balloon_4_y_speed *= -1
            balloon_4_y += balloon_4_y_speed
            balloon_4_y_switcher = random.randrange(0,50)
            if balloon_4_y_switcher == 0:
                balloon_4_y_speed *=-1
                balloon_4_y += balloon_4_y_speed
                #Balloon 5
            if balloon_5_x+30 == WIDTH or balloon_5_x-30 == 0:
                balloon_5_x_speed *= -1
            balloon_5_x += balloon_5_x_speed
            balloon_5_x_switcher = random.randrange(0,50)
            if balloon_5_x_switcher == 0:
                balloon_5_x_speed *=-1
                balloon_5_x += balloon_5_x_speed
            
            if balloon_5_y+30 == 300 or balloon_5_y-30 == 0:
                balloon_5_y_speed *= -1
            balloon_5_y += balloon_5_y_speed
            balloon_5_y_switcher = random.randrange(0,50)
            if balloon_5_y_switcher == 0:
                balloon_5_y_speed *=-1
                balloon_5_y += balloon_5_y_speed
                # Clown + Bomb Collision
            if player_hitbox.colliderect(bomb_hitbox):
                player_x = 1000
                player_y = 1000
                explosion = True
                #Powerups
            if shield_orb == True:
                shield_y += 5
            if shield_orb_hitbox.colliderect(player_hitbox):
                shield_x = 1000
                shield = True
                shield_start_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - shield_start_time > 5000:
                shield = False
                #Explosion
            if explosion == True:
                explosion_radius += 100
                explosion_count += 1
                if explosion_count == 8:
                    explosion_radius = 0
                    player_x = mouse_x
                    player_y = 420
                    score = 0
                    explosion_count = 0
                    shield = True
                    explosion = False

            # DRAWING
            screen.fill((255, 255, 255))  # always the first drawing command
            # Background
            pygame.draw.rect(screen, (160,105,25), (0,350,WIDTH,180)) #Floor
            pygame.draw.rect(screen, (120,0,0), (0,0,WIDTH,350)) # Red Tent
            pygame.draw.polygon(screen, (205,133,63), [(0,0), (0,300), (125,0)],width=0) #Brown Coloring 1
            pygame.draw.polygon(screen, (205,133,63), [(200,0), (150,350), (300,350), (350,0)],width=0) #Brown Coloring 2
            pygame.draw.polygon(screen, (205,133,63), [(425,0), (450,350), (600,350), (525,0)],width=0) #Brown Coloring 3
            pygame.draw.polygon(screen, (205,133,63), [(600,0), (680, 300), (WIDTH,0)],width=0) #Brown Coloring 4
            # Ugly ass background must change
            
            # Clown
            pygame.draw.circle(screen, (250,240,230), (player_x, player_y), 35) # Face
            pygame.draw.circle(screen, (0,0,0), (player_x-10, player_y-10), 7) # Eye 1
            pygame.draw.circle(screen, (0,0,0), (player_x+10, player_y-10), 7) # Eye 1
            pygame.draw.ellipse(screen, (0,0,0), (player_x-10, player_y+17, 20,7)) # Mouth
            pygame.draw.circle(screen, (255,0,0), (player_x, player_y+5), 8) # Nose 
            pygame.draw.circle(screen, (0,255,0), (player_x-35, player_y-10), 15) # Hair
            pygame.draw.circle(screen, (0,0,255), (player_x-20, player_y-30), 15) # Hair
            pygame.draw.circle(screen, (255,0,255), (player_x, player_y-35), 15) # Hair
            pygame.draw.circle(screen, (255,255,0), (player_x+20, player_y-30), 15) # Hair
            pygame.draw.circle(screen, (0,255,255), (player_x+35, player_y-10), 15) # Hair
            # Darts
            for i in darts:
                pygame.draw.ellipse(screen, (0,0,0), (i[0],i[1],5,10))
            # Bomb
            pygame.draw.circle(screen, (0,0,0), (bomb_x,bomb_y), 50)
            pygame.draw.circle(screen, (200,0,0), (bomb_x,bomb_y+25), 10)
            pygame.draw.polygon(screen, (200,0,0), [(bomb_x-10,bomb_y+9), (bomb_x-15, bomb_y-40), (bomb_x+15, bomb_y-40), (bomb_x+10,bomb_y+9)])
            pygame.draw.rect(screen, (0,0,0), (bomb_x-20,bomb_y-60,40,15))
            pygame.draw.line(screen, (0,0,0), (bomb_x,bomb_y-60),(bomb_x,bomb_y-75),width=2)
            pygame.draw.line(screen, (0,0,0), (bomb_x,bomb_y-75),(bomb_x+10,bomb_y-85),width=2)
            # Balloons
                #Balloon 1
            pygame.draw.polygon(screen, (255,0,0), [(balloon_x-10,balloon_y+35),(balloon_x, balloon_y+5),(balloon_x+10, balloon_y+35)], width=0)
            pygame.draw.circle(screen, (255,0,0), (balloon_x,balloon_y),30)
            pygame.draw.line(screen, (0,0,0), (balloon_x,balloon_y+35),(balloon_x,balloon_y+40),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_x,balloon_y+40),(balloon_x-5,balloon_y+45),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_x-5,balloon_y+45),(balloon_x-5,balloon_y+55),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_x-5,balloon_y+55),(balloon_x-2,balloon_y+65),width=1)
                #Balloon 2
            pygame.draw.polygon(screen, (255,0,0), [(balloon_2_x-10,balloon_2_y+35),(balloon_2_x, balloon_2_y+5),(balloon_2_x+10, balloon_2_y+35)], width=0)
            pygame.draw.circle(screen, (255,0,0), (balloon_2_x,balloon_2_y),30)
            pygame.draw.line(screen, (0,0,0), (balloon_2_x,balloon_2_y+35),(balloon_2_x,balloon_2_y+40),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_2_x,balloon_2_y+40),(balloon_2_x-5,balloon_2_y+45),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_2_x-5,balloon_2_y+45),(balloon_2_x-5,balloon_2_y+55),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_2_x-5,balloon_2_y+55),(balloon_2_x-2,balloon_2_y+65),width=1)
                #Balloon 3
            pygame.draw.polygon(screen, (255,0,0), [(balloon_3_x-10,balloon_3_y+35),(balloon_3_x, balloon_3_y+5),(balloon_3_x+10, balloon_3_y+35)], width=0)
            pygame.draw.circle(screen, (255,0,0), (balloon_3_x,balloon_3_y),30)
            pygame.draw.line(screen, (0,0,0), (balloon_3_x,balloon_3_y+35),(balloon_3_x,balloon_3_y+40),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_3_x,balloon_3_y+40),(balloon_3_x-5,balloon_3_y+45),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_3_x-5,balloon_3_y+45),(balloon_3_x-5,balloon_3_y+55),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_3_x-5,balloon_3_y+55),(balloon_3_x-2,balloon_3_y+65),width=1)
                #Balloon 4
            pygame.draw.polygon(screen, (255,0,0), [(balloon_4_x-10,balloon_4_y+35),(balloon_4_x, balloon_4_y+5),(balloon_4_x+10, balloon_4_y+35)], width=0)
            pygame.draw.circle(screen, (255,0,0), (balloon_4_x,balloon_4_y),30)
            pygame.draw.line(screen, (0,0,0), (balloon_4_x,balloon_4_y+35),(balloon_4_x,balloon_4_y+40),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_4_x,balloon_4_y+40),(balloon_4_x-5,balloon_4_y+45),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_4_x-5,balloon_4_y+45),(balloon_4_x-5,balloon_4_y+55),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_4_x-5,balloon_4_y+55),(balloon_4_x-2,balloon_4_y+65),width=1)
                #Balloon 5
            pygame.draw.polygon(screen, (255,0,0), [(balloon_5_x-10,balloon_5_y+35),(balloon_5_x, balloon_5_y+5),(balloon_5_x+10, balloon_5_y+35)], width=0)
            pygame.draw.circle(screen, (255,0,0), (balloon_5_x,balloon_5_y),30)
            pygame.draw.line(screen, (0,0,0), (balloon_5_x,balloon_5_y+35),(balloon_5_x,balloon_5_y+40),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_5_x,balloon_5_y+40),(balloon_5_x-5,balloon_5_y+45),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_5_x-5,balloon_5_y+45),(balloon_5_x-5,balloon_5_y+55),width=1)
            pygame.draw.line(screen, (0,0,0), (balloon_5_x-5,balloon_5_y+55),(balloon_5_x-2,balloon_5_y+65),width=1)
                # Powerups
            pygame.draw.rect(screen, (0,0,255), shield_orb_hitbox)
            if shield == True:
                pygame.draw.circle(screen, (0,255,0), (player_x, player_y),60,width=7)
                # Explosion
            if explosion == True:
                pygame.time.wait(500)
                pygame.draw.circle(screen, (255,69,0), (bomb_x,bomb_y), explosion_radius)
                # Game End
            draw_text(f"Score: {score}", text_font, (0,0,0), 5,400)

    # SELENA'S GAME
    if selena == True:
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
                if welcome_screen == True: 
                    welcome_screen = False
                elif win == True: 
                    selena = False 
                    james = True 

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

        # Display welcome screen 
        if welcome_screen == True: 
            screen.fill((255, 210, 210))
            # Banner decorations 
            for i in range(0, WIDTH, 40): 
                pygame.draw.polygon(screen, (255, 100, 100), ((i, 50), (i+30, 50), (i+15, 100)))
            pygame.draw.line(screen, (0, 0, 0), (0, 50), (WIDTH, 50), 3)
            # Tire decorations 
            pygame.draw.circle(screen, (0, 0, 0), (100, 400), 30, 20)
            pygame.draw.circle(screen, (128, 128, 128), (100, 400), 20, 8)
            pygame.draw.circle(screen, (0, 0, 0), (550, 400), 30, 20)
            pygame.draw.circle(screen, (128, 128, 128), (550, 400), 20, 8)
            # Text instructions 
            screen.blit(welcome_text, (60, 150))
            screen.blit(instructions_text, (100, 225))
            screen.blit(directions_text, (80, 300))
            screen.blit(click_text, (250, 375))

        # Display end screen after win
        if win == True: 
            screen.fill((150, 255, 150))
            # Banner decorations 
            for i in range(0, WIDTH, 40): 
                pygame.draw.polygon(screen, (0, 100, 0), ((i, 50), (i+30, 50), (i+15, 100)))
            pygame.draw.line(screen, (0, 0, 0), (0, 50), (WIDTH, 50), 3)
            # Balloon decorations 
            pygame.draw.line(screen, (0, 0, 0), (80, 320), (80, 450))
            pygame.draw.ellipse(screen, (0, 175, 255), (50, 250, 60, 80))
            pygame.draw.polygon(screen, (0, 175, 255), ((80, 320), (95, 340), (65, 340)))
            pygame.draw.line(screen, (0, 0, 0), (530, 320), (530, 450))
            pygame.draw.ellipse(screen, (0, 175, 255), (500, 250, 60, 80))
            pygame.draw.polygon(screen, (0, 175, 255), ((530, 320), (545, 340), (515, 340)))
            # Congratulations text
            screen.blit(win_text, (140, 180))

    # JAMES' GAME 
    if james == True: 
        screen.fill((255, 0, 0))
    

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------
pygame.quit()
