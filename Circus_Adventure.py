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

# TIFFANY'S VARIABLES

#font initialize / declaration
font = pygame.font.SysFont("Arial", 25)

#clown presets
clown_x = 50
clown_y = 50
clown_radius = 10 # clown radius needs to be 16 or less as tile_size is 32
clown_y_change = 0
clown_x_change = 0
x_pos_tile = 0
y_pos_tile = 0
gravity = 0.3 #will be acceleration, not constant

#moving [W, A, S, D]
moving = [0, 0, 0, 0]
shrunk = False
w_started_time = 0
holding_w_time = 0
lifted = False

#tiles (all_tiles is in rows and columns)
tile_size = 32
all_tiles = [
    [1 for i in range(20)],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
    [1 for i in range(20)],
    [1 for i in range(20)]
    ]
on_tile = False
platforms = []
level = 0 #0 = start screen, 1 = level 1, 2 = level 2

for i in range(len(all_tiles)): # creates the list of platforms and their locations (not in terms of tile numbers)
    for a in range(len(all_tiles[i])):
        if all_tiles[i][a] == 1:
            rect = pygame.Rect(a*tile_size, i*tile_size, tile_size, tile_size)
            platforms.append(rect)


#end point
end_rect = [50, 340, 70, 70] # the win condition
win_time = 0 #time from win
win_size = 50 #size of rectangle animation after win
won_level_1 = False #level 1 done or not
maxed = False #will be true when rectangle animation is off the screen
start_2 = False #starts level 2
won_level_2 = False


#loads circus image
circus_tent = pygame.image.load("circus_tent.png").convert_alpha()

#scales circus image
circus_resized = pygame.transform.scale(circus_tent, (end_rect[2], end_rect[3]))

#help box rect
help_rect = [600, 10, 30, 30]
help_question = font.render("?", True, (0, 0, 0)) #adds the question mark to the help window when closed
help_open = False #checks if the help window is open or not


#enemy
enemy_pos = [[random.randint(100, WIDTH-tile_size*2), 50, 20, 20] for i in range(4)]
enemy_action = [0 for i in range(len(enemy_pos))]
enemy_on_tile = [False for i in range(len(enemy_pos))]
x_pos_tile_enemy = [0 for i in range(len(enemy_pos))]
y_pos_tile_enemy = [0 for i in range(len(enemy_pos))]
enemy_y_change = [0 for i in range(len(enemy_pos))]
teleport = [0 for i in range(len(enemy_pos))]
enemy_time = [0 for i in range(len(enemy_pos))]
on_tile_enemy = [False for i in range(len(enemy_pos))]

# dying variable (will show end screen)
dead = False
dead_time = 0
dead_is_True = 50

#start playing
play_rect = [230, 180, 160, 80]


running = True


def text_blit(text, colour, position):
    text_para = font.render(text, True, colour)
    screen.blit(text_para, position)

# MARCELL'S VARIABLES 

# Player
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

# The Bomb
bomb_x = WIDTH//2
bomb_y = HEIGHT//2
bomb_x_speed = 5
bomb_y_speed = 5
explosion_radius = 10
explosion = False
explosion_count = 0

# Shield Powerup
shield_orb = False
shield = False 
shield_orb_x = 1000
shield_orb_y = 1000
end_game = False
shield_start_time = 0

# Darts
darts = []

# Score
score = 0
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
text_font = pygame.font.SysFont("Nunito", 40)

# Initialization (Start Screen)
initalization = False
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
tiffany = True
marcell = False 
selena = False 
james = False

# ---------------------------
running = True
while running:

    if tiffany == True:
# TIFFANY'S GAME
        current_time = pygame.time.get_ticks()
        clown_rect = pygame.Rect(clown_x-clown_radius, clown_y-clown_radius, clown_radius*2, clown_radius*2)
        lifted = False
            
        #EVENT HANDLING
        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False
            
            # pressed a key
            elif event.type == pygame.KEYDOWN:
                if help_open == False and dead == False and level != 0: #cannot win by pressing randomly while help window is open
                # able to press multiple keys and move in two directions at once
                    if on_tile == True and current_time - w_started_time >= 200:
                        if event.key == pygame.K_w: #so clown can't phase upwards
                            moving[0] = 1
                            w_started_time = current_time
                            holding_w_time = current_time
                            lifted = False
            
                    if event.key == pygame.K_a: # move left
                        moving[1] = 1
                    if event.key == pygame.K_s: # shrink size of clown
                        if shrunk == False:
                            shrunk = True
                        elif shrunk == True:
                            shrunk = False
                    if event.key == pygame.K_d: # move right
                        moving[3] = 1 
                
                if event.key == pygame.K_ESCAPE:
                    help_open = False


            # let go of key
            elif event.type == pygame.KEYUP and level != 0:
                if event.key == pygame.K_w: #only able to jump one at a time
                    moving[0] = 0
                if event.key == pygame.K_a:
                    moving[1] = 0
    
                if event.key == pygame.K_s: #a toggle
                    
                    if shrunk == False:
                        clown_radius = 10
                    elif shrunk == True:
                        clown_radius = 5
                        
                if event.key == pygame.K_d:
                    moving[3] = 0
            
            elif event.type == pygame.MOUSEBUTTONDOWN: #checks if clicking help box or the start playing box
                if mouse_x > help_rect[0] and mouse_x < help_rect[0] + help_rect[2] and mouse_y > help_rect[1] and mouse_y < help_rect[1] + help_rect[3] and level != 0:
                    help_open = True
            
                elif mouse_x > play_rect[0] and mouse_x < play_rect[0] + play_rect[2] and mouse_y > play_rect[1] and mouse_y < play_rect[1] + play_rect[3] and level == 0:
                    level = 1

        # checks if key is still pressed and moves accordingly (S is only shrink once)

        if moving[1] == 1: # moving left and not colliding
            new_clown_x = clown_x - 3
            for i in platforms:  
                new_rect = pygame.Rect(new_clown_x-clown_radius, clown_y-clown_radius-3, clown_radius*2, clown_radius*2) #checks in advance whether it hits or not

                if new_rect.colliderect(i):
                    new_clown_x = clown_x
                    break
            clown_x = new_clown_x

        if moving[3] == 1: # moving right and not colliding
            new_clown_x = clown_x + 3
            for i in platforms:  
                new_rect = pygame.Rect(new_clown_x-clown_radius, clown_y-clown_radius-3, clown_radius*2, clown_radius*2) #checks in advance whether it hits or not

                if new_rect.colliderect(i):
                    new_clown_x = clown_x
                    break
            
            clown_x = new_clown_x
        
        if moving[0] == 1: # moving up and not colliding
            platform_above = 0

            for i in platforms:
                new_rect = pygame.Rect(clown_x-clown_radius, clown_y-clown_radius-3, clown_radius*2, clown_radius*2)
                if new_rect.colliderect(i):
                    moving[0] = 0
                    platform_above = 1
                    break

            if current_time - holding_w_time <= 450:
                if platform_above == 0:
                    clown_y_change = -3
                
                elif platform_above == 1:
                    clown_y_change = 3
                
            else:
                lifted = True #if key should not be pressed for longer
                moving[0] = 0
                
        if won_level_2 == True and event.type == pygame.MOUSEBUTTONDOWN: # Game Switcher
            tiffany = False
            marcell = True
            initalization = True
            initalization_start_time = pygame.time.get_ticks() 
        #GAME STATE UPDATES - level
        # re-makes the level with a second platform setting
        if level == 2:
            all_tiles = [
            [1 for i in range(20)],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1 for i in range(20)],
            [1 for i in range(20)],
            [1 for i in range(20)]
            ]

        #GAME STATE UPDATES --- player
        if level != 0:
            on_tile = False

            #gravity settings
            if moving[0] != 1:
                for i in platforms:
                    new_rect = pygame.Rect(clown_x-clown_radius, clown_y-clown_radius-4, clown_radius*2, clown_radius*2-gravity+6) #checks if collides wtih a platform below
                    if clown_y_change >= -3 and new_rect.colliderect(i) and i[1] > new_rect[1]:
                        on_tile = True
                        clown_y_change = 0
                        clown_y = i.top - clown_radius

                        break

                for i in platforms:
                    if on_tile == False and new_rect.colliderect(i) and i[1] < new_rect[1]: #checks if collides with the bottom of a platform
                        clown_y_change += 1.5
                        break
            
            if on_tile == False and moving[0] == 0: #freefall
                clown_y_change += gravity #acceleration from gravity
        
            if moving[1] == 0 and moving[3] == 0:
                clown_x_change = 0
        
            clown_y += clown_y_change #kinda like compounding it 


        if level != 0:
            clown_y += clown_y_change
            clown_x += clown_x_change
            
            if on_tile == True:
                clown_y_change = -0.5

            #checks if the clown touches the endpoint/goal
            if clown_rect.colliderect(end_rect) and dead == False and level == 1: 
                won_level_1 = True
            if won_level_1 == True and win_size > 5: #happens when level changes
                    if win_size < WIDTH and maxed == False:
                        win_size += 5
                    if win_size > WIDTH//2:
                        maxed = True
                    if maxed == True and win_size > 0: #need to reset all values again
                        win_size -= 5
                        level = 2
                        clown_x = 340
                        clown_y = 230
                        end_rect = [30, 30, 30, 30]
                        dead = False #may die while animation to switch levels is playing

                        platforms = []
                        for i in range(len(all_tiles)):
                            for a in range(len(all_tiles[i])):
                                if all_tiles[i][a] == 1:
                                    rect = pygame.Rect(a*tile_size, i*tile_size, tile_size, tile_size)
                                    platforms.append(rect)
                    win_time = current_time
                

                
            if clown_rect.colliderect(end_rect) and level == 2 and dead == False:
                won_level_2 = True


        #GAME STATE UPDATES --- enemy:
        if dead == False and (level == 1 and won_level_1 == False) or (level == 2 and won_level_2 == False):
            for i in range(len(enemy_action)): # enemy random movements
                if level == 1 or (level == 2 and current_time - win_time >= 500):
                    enemy_rect = pygame.Rect(enemy_pos[i]) #creates enemy hitbox
                    on_tile_enemy[i] = False

                    for a in range(len(platforms)): #checks for enemy collision with platforms so that enemy doesn't phase through them
                        if enemy_rect.colliderect(platforms[a]):
                            #going right, bounces back to left
                            if enemy_action[i] == 0 and all_tiles[y_pos_tile_enemy[i]][x_pos_tile_enemy[i]+1] == 1:
                                    enemy_action[i] = 1
                            #going left, bounces back to right
                            elif enemy_action[i] == 1 and all_tiles[y_pos_tile_enemy[i]][x_pos_tile_enemy[i]-1] == 1:
                                    enemy_action[i] = 0
                
                    if enemy_action[i] == 0:
                        enemy_pos[i][0] += 3 # enemy moves right
                    elif enemy_action[i] == 1:
                        enemy_pos[i][0] -= 3 # enemy moves left
                
                    if enemy_pos[i][1] < 0:
                        enemy_pos[i][1] += 5
                    

                    #gravity settings (same principle as player gravity settings)
                    for a in platforms:
                        new_rect = pygame.Rect(enemy_pos[i][0], enemy_pos[i][1]-4, enemy_pos[i][2], enemy_pos[i][3]-gravity+6) #checks if collides wtih a platform below
                        if enemy_y_change[i] >= -3 and new_rect.colliderect(a) and a[1] > new_rect[1]:
                            on_tile_enemy[i] = True
                            enemy_y_change[i] = 0
                            enemy_pos[i][1] = a.top - enemy_pos[i][3]

                            break
                            
                    for a in platforms:
                        if on_tile_enemy[i] == False and new_rect.colliderect(a) and a[1] < new_rect[1]: #checks if collides with the bottom of a platform
                            enemy_y_change[i] += 1.5
                            break
                
                    if on_tile_enemy[i] == False: #freefall
                        enemy_y_change[i] += gravity #acceleration from gravity
                    
                    enemy_pos[i][1] += enemy_y_change[i] #kinda like compounding it 
                
                    
                if clown_rect.colliderect(enemy_rect):
                    dead = True #needed so that the rectangle doesn't disappear
                    dead_time = current_time
                
                if current_time - enemy_time[i] >= random.randint(6000, 10000):
                    enemy_pos[i][1] = 50
                    enemy_pos[i][0] = random.randint(100, WIDTH-100)
                    enemy_time[i] = current_time

            #DRAWING
        if level != 0:
            screen.fill((170, 200, 255))


            #draw the clown
            pygame.draw.circle(screen, (255, 255, 255), (clown_x, clown_y), clown_radius) #head
            pygame.draw.circle(screen, (0, 0, 0), (clown_x-8, clown_y), clown_radius - 5) #left eye
            pygame.draw.circle(screen, (0, 0, 0), (clown_x+8, clown_y), clown_radius - 5) #right eye
            pygame.draw.circle(screen, (255, 100, 100), (clown_x, clown_y+8), clown_radius - 4) #nose

            for i in range(len(all_tiles)): #y_pos
                for a in range(len(all_tiles[i])): #x_pos
                    if all_tiles[i][a] == 1:
                        pygame.draw.rect(screen, (100, 100, 0), [a*tile_size, i*tile_size, tile_size, tile_size])
            
            #draw the enemy
            for i in range(len(enemy_pos)):
                pygame.draw.rect(screen, (255, 0, 0), (enemy_pos[i][0], enemy_pos[i][1], 20, 20))
                pygame.draw.rect(screen, (0, 0, 0), (enemy_pos[i][0] + 5, enemy_pos[i][1] + 5, 10, 10))

            #how pygame.draw.rect(screen, (0, 0, 0), end_rect)
            screen.blit(circus_resized, pygame.Rect(end_rect))

            #help box and window --- text
            pygame.draw.rect(screen, (225, 225, 100), help_rect)
            screen.blit(help_question, (help_rect[0]+8, help_rect[1], help_rect[2], help_rect[3]))

            if help_open == True: # checks if help box is open to show text
                screen.fill((255, 255, 255))
                text_blit("W: jump (hold); A: move left; S: shrink; D: move right", (0, 0, 0), (90, 50, 540, 100))
                text_blit("Goal: help the clown reach the circus tent!", (0, 0, 0), (115, 100, 300, 100))
                text_blit("NOTE: ENEMIES WILL TELEPORT EVERY SO OFTEN!! BEWARE!", (0, 0, 0), (5, 200, 540, 100))
                text_blit("Press ESC to exit this window", (0, 0, 0), (180, 400, 300, 100))
            

            #draws a rectangle increasing in side lengths to go to dead screen 
            if dead == True:
                if current_time - dead_time > 200 and dead_is_True <= WIDTH//2:
                    dead_is_True += 5
                pygame.draw.rect(screen, (255, 0, 0), (WIDTH//2-dead_is_True, HEIGHT//2-dead_is_True+50, dead_is_True*2, dead_is_True*2-80))

                if dead_is_True > WIDTH//2:
                    text_blit("You have died to your business rival: clown brother #1", (0, 0, 0), (60, 200, 300, 100))
            
            
            elif dead == False:# draws a rectangle with increasing side lengths to transition to the next level
                if won_level_1 == True:
                    pygame.draw.rect(screen, (0, 0, 0), (WIDTH//2-win_size, HEIGHT//2-win_size+50, win_size*2, win_size*2-80))
                
                if won_level_2 == True:
                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
                    text_blit("You've arrived at the circus!", (255, 255, 255), (180, 100, 50, 50))

            
        #play start screen
        if level == 0:
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (210, 50, 90), play_rect)
            text_blit("PLAY", (0, 0, 0), (play_rect[0]+55, play_rect[1]+25, play_rect[2], play_rect[3]))
            text_blit("CIRCUS ADVENTURE", (255, 255, 255), (play_rect[0]-20, play_rect[1]-50, 100, 50))
# -----------------------------------------------------------------------------------------------------------
    # MARCELL'S GAME 
    if marcell == True: 
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Shooting Function
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dart = [player_x,player_y-25]
                    darts.append(dart)
            
            # Game Switcher
            elif event.type == pygame.MOUSEBUTTONDOWN and end == True:
                marcell = False
                selena = True
                end = False

        # GAME STATE UPDATES ------------------------------------------
        
        # Start Screen
        if initalization == True:
            draw_text("Pop 50 Balloons to Win!", text_font, (255,255,255), 150,190)
            draw_text("Mouse to Move, SPACE to Shoot!", text_font, (255,255,255), 90,220)
            draw_text("Careful of the Bomb!", text_font, (255,255,255), 170,250)
            if pygame.time.get_ticks() - initalization_start_time > 5000:
                initalization = False
        
        # Win Condition
        if score >= 50:
            end = True
        
        # Win Screen
        if end == True:
            bomb_x = -1000
            bomb_x_speed = 0
            pygame.draw.rect(screen, (0, 0, 0), (0,0,WIDTH,HEIGHT))
            draw_text("Congratulations! You Won!!", text_font, (255,255,255), 130,200)
            draw_text("Click to Continue", text_font, (255,255,255), 190,230)
        
        # Gameplay
        if initalization == False and score < 50:
            
            # Darts  
            for pos in darts:
                pos[1] -= 30 # Dart Speed
                
                # Balloon + Dart 1
                if pos[1] <= balloon_y+30 and pos[1] >= balloon_y-30 and pos[0] >= balloon_x-30 and pos[0] <= balloon_x+30: # Manual Dart + Balloon Collision Detection
                    score += 1
                    shield_orb_random = random.randrange(0,15)     # RNG for powerup orb to spawn
                    if shield_orb_random == 0 and shield_orb_y > HEIGHT:     # Checking for random number and if powerup orb already exists on the screen
                        shield_orb_x = random.randrange(1,WIDTH-20)     # Spawning powerup orb
                        shield_orb_y = -20
                        shield_orb = True     # Allowing the powerup orb to move downwards
                    pos[0] = 1000             # Teleporting dart off screen to avoid repeat collisions
                    pos[1] = 1000
                    balloon_x = random.randrange(50,600,10)     # Respawning balloon at a random location
                    balloon_y = random.randrange(50,230,10)
                
                # Balloon + Dart 2
                if pos[1] <= balloon_2_y+30 and pos[1] >= balloon_2_y-30 and pos[0] >= balloon_2_x-30 and pos[0] <= balloon_2_x+30:
                    score += 1
                    shield_orb_random = random.randrange(0,15)
                    if shield_orb_random == 0 and shield_orb_y > HEIGHT:
                        shield_orb_x = random.randrange(1,WIDTH-20)
                        shield_orb_y = -20
                        shield_orb = True
                    pos[0] = 1000
                    pos[1] = 1000
                    balloon_2_x = random.randrange(50,600,10)
                    balloon_2_y = random.randrange(50,230,10)

                # Balloon + Dart 3
                if pos[1] <= balloon_3_y+30 and pos[1] >= balloon_3_y-30 and pos[0] >= balloon_3_x-30 and pos[0] <= balloon_3_x+30:
                    score += 1
                    shield_orb_random = random.randrange(0,15)
                    if shield_orb_random == 0 and shield_orb_y > HEIGHT:
                        shield_orb_x = random.randrange(1,WIDTH-20)
                        shield_orb_y = -20
                        shield_orb = True
                    pos[0] = 1000
                    pos[1] = 1000
                    balloon_3_x = random.randrange(50,600,10)
                    balloon_3_y = random.randrange(50,230,10)
               
                # Balloon + Dart 4
                if pos[1] <= balloon_4_y+30 and pos[1] >= balloon_4_y-30 and pos[0] >= balloon_4_x-30 and pos[0] <= balloon_4_x+30:
                    score += 1
                    shield_orb_random = random.randrange(0,15)
                    if shield_orb_random == 0 and shield_orb_y > HEIGHT:
                        shield_orb_x = random.randrange(1,WIDTH-20)
                        shield_orb_y = -20
                        shield_orb = True
                    pos[0] = 1000
                    pos[1] = 1000
                    balloon_4_x = random.randrange(50,600,10)
                    balloon_4_y = random.randrange(50,230,10)
                
                # Balloon + Dart 5
                if pos[1] <= balloon_5_y+30 and pos[1] >= balloon_5_y-30 and pos[0] >= balloon_5_x-30 and pos[0] <= balloon_5_x+30:
                    score += 1
                    shield_orb_random = random.randrange(0,15)
                    if shield_orb_random == 0 and shield_orb_y > HEIGHT:
                        shield_orb_x = random.randrange(1,WIDTH-20)
                        shield_orb_y = -20
                        shield_orb = True
                    pos[0] = 1000
                    pos[1] = 1000
                    balloon_5_x = random.randrange(50,600,10)
                    balloon_5_y = random.randrange(50,230,10)
                
                # Dart + Bomb Collision
                if pos[1] <= bomb_y+50 and pos[1] >= bomb_y-50 and pos[0] >= bomb_x-50 and pos[0] <= bomb_x+50:
                    pos[0] = 1000
                    pos[1] = 1000
                    explosion = True
            
            # Bomb Movement and Hitbox
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

            # Shield 
                # Shield Orb Hitbox
            shield_orb_hitbox = pygame.Rect(shield_orb_x,shield_orb_y,20,20)
            
                # Shield Effect (Removing Player Hitbox)
            if shield == True:
                player_hitbox = pygame.Rect(1000,player_y-30,60,60)
            if shield == False:
                player_hitbox = pygame.Rect(player_x-30,player_y-30,60,60)
            
                # Shield Orb Movement
            if shield_orb == True:
                shield_orb_y += 5
            
                # Shield Orb Collision Detection
            if shield_orb_hitbox.colliderect(player_hitbox):
                shield_orb_x = 1000
                shield = True
                shield_start_time = pygame.time.get_ticks()
            
                # Shield Timer
            if pygame.time.get_ticks() - shield_start_time > 5000:
                shield = False

            # Clown + Bomb Collision Detection
            if player_hitbox.colliderect(bomb_hitbox):
                player_x = 1000
                player_y = 1000
                explosion = True
            
            # Explosion
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
            
            # Balloon Movement 
                # Balloon 1
            if balloon_x+30 == WIDTH or balloon_x-30 == 0:
                balloon_x_speed *= -1
            balloon_x += balloon_x_speed
            balloon_x_switcher = random.randrange(0,50) # 1/50 Chance every frame to change x direction
            if balloon_x_switcher == 0:
                balloon_x_speed *=-1
                balloon_x += balloon_x_speed
            if balloon_y+30 == 300 or balloon_y-30 == 0:
                balloon_y_speed *= -1
            balloon_y += balloon_y_speed
            balloon_y_switcher = random.randrange(0,50) # 1/50 Chance every frame to change y direction
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
                
                # Balloon 3
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
                
                # Balloon 4
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
                
                # Balloon 5
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

            # DRAWING ---------------------------------------------------------
            screen.fill((255, 255, 255))  # always the first drawing command
            
            # Background
            pygame.draw.rect(screen, (160,105,25), (0,350,WIDTH,180)) # Floor
            pygame.draw.rect(screen, (120,0,0), (0,0,WIDTH,350)) # Red Tent
            pygame.draw.polygon(screen, (205,133,63), [(0,0), (0,300), (125,0)],width=0) #Brown Coloring 1
            pygame.draw.polygon(screen, (205,133,63), [(200,0), (150,350), (300,350), (350,0)],width=0) #Brown Coloring 2
            pygame.draw.polygon(screen, (205,133,63), [(425,0), (450,350), (600,350), (525,0)],width=0) #Brown Coloring 3
            pygame.draw.polygon(screen, (205,133,63), [(600,0), (680, 300), (WIDTH,0)],width=0) #Brown Coloring 4
            
            # Clown
            pygame.draw.circle(screen, (250,240,230), (player_x, player_y), 35) # Face
            pygame.draw.circle(screen, (0,0,0), (player_x-10, player_y-10), 7) # Eye 1
            pygame.draw.circle(screen, (0,0,0), (player_x+10, player_y-10), 7) # Eye 2
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
            
            # Shield
            pygame.draw.rect(screen, (0,0,255), shield_orb_hitbox) # Shield Orb
            if shield == True:
                pygame.draw.circle(screen, (0,255,0), (player_x, player_y),60,width=7) # Active Shield

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
                
            # Explosion
            if explosion == True:
                pygame.time.wait(500)
                pygame.draw.circle(screen, (255,69,0), (bomb_x,bomb_y), explosion_radius)
                
            # Score Counter
            draw_text(f"Score: {score}", text_font, (0,0,0), 5,400)
    # ----------------------------------------------------------------
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
