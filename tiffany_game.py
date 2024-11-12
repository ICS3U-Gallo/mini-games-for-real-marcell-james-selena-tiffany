# clown game + balloons + face paint?
# circus end point
# fix collision detection

import pygame
import random

pygame.init()


WIDTH = 640
HEIGHT = 448

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#font initialize / declaration
font = pygame.font.SysFont("Arial", 25)

#clown presets
clown_x = 50
clown_y = 0
clown_radius = 15 # clown radius needs to be 16 or less as tile_size is 32
clown_y_change = 0
x_pos_tile = 0
y_pos_tile = 0
gravity = 0.3 #will be acceleration, not constant

#moving [W, A, S, D]
moving = [0, 0, 0, 0]
shrunk = False

#tiles (all_tiles is in rows and columns)
tile_size = 32
all_tiles = [
    [0 for i in range(20)],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0 for i in range(20)],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0 for i in range (20)],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0 for i in range(20)],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0],
    [1 for i in range(20)],
    [1 for i in range(20)]
    ]
on_tile = False
platforms = []
level = 1

for i in range(len(all_tiles)):
    for a in range(len(all_tiles[i])):
        if all_tiles[i][a] == 1:
            rect = pygame.Rect(a*tile_size, i*tile_size, tile_size, tile_size)
            platforms.append(rect)


#end point
end_rect = [270, 320, 70, 70]
win_time = 0 #time from win
win_size = 50 #size of rectangle animation after win
won_level_1 = False #level 1 done or not
maxed = False #will be true when rectangle animation is off the screen
start_2 = False #starts level 2

#loads circus image
circus_tent = pygame.image.load("circus_tent.png").convert_alpha()

#scales circus image
circus_resized = pygame.transform.scale(circus_tent, (end_rect[2], end_rect[3]))

#help box rect
help_rect = [600, 10, 30, 30]
help_question = font.render("?", True, (0, 0, 0)) #adds the question mark to the help window when closed
help_open = False #checks if the help window is open or not
help_window = font.render("W: jump; A: move left; S: shrink; D: move right", True, (0, 0, 0))
help_goal = font.render("Goal: help the clown reach the circus tent!", True, (0, 0, 0))
exit_window = font.render("Press ESC to exit this window", True, (0, 0, 0))

#enemy
enemy_pos = [[random.randint(0, WIDTH), 150, 20, 20] for i in range(4)]
time_since_action = [0 for i in range(len(enemy_pos))]
enemy_action = [0 for i in range(len(enemy_pos))]
enemy_on_tile = [False for i in range(len(enemy_pos))]
x_pos_tile_enemy = [0 for i in range(len(enemy_pos))]
y_pos_tile_enemy = [0 for i in range(len(enemy_pos))]
enemy_y_change = [0 for i in range(len(enemy_pos))]
teleport = [0 for i in range(len(enemy_pos))]

# dying variable (will show end screen)
dead = False
dead_text = font.render("You have died to your business rival: clown brother #1", True, (0, 0, 0))
dead_is_True = 50

running = True

while running:
    screen.fill((170, 200, 255))
    current_time = pygame.time.get_ticks()
        
    #EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # pressed a key
        elif event.type == pygame.KEYDOWN:
            if help_open == False and dead == False:
            # able to press multiple keys and move in two directions at once
                if on_tile == True:
                    if event.key == pygame.K_w:
                        started_w_time = current_time
                        clown_y -= 50

                        for i in range(len(platforms)): #if collides with platform while jumping
                            if clown_rect.colliderect(platforms[i]):
                                clown_y += 2
            
                #cannot win by pressing randomly while help window is open
                if event.key == pygame.K_a:
                    moving[1] = 1 
                if event.key == pygame.K_s:
                    if shrunk == False:
                        shrunk = True
                    elif shrunk == True:
                        shrunk = False
                if event.key == pygame.K_d:
                    moving[3] = 1 
            
            if event.key == pygame.K_ESCAPE:
                help_open = False

            
        
        # let go of key
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w: #only able to jump one at a time
                moving[0] = 0
            if event.key == pygame.K_a:
                moving[1] = 0
            if event.key == pygame.K_s: #a toggle
                
                if shrunk == False:
                    clown_radius = 15
                elif shrunk == True:
                    clown_radius = 10
                    
            if event.key == pygame.K_d:
                moving[3] = 0
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if mouse_x > help_rect[0] and mouse_x < help_rect[0] + help_rect[2] and mouse_y > help_rect[1] and mouse_y < help_rect[1] + help_rect[3]:
                help_open = True


    #GAME STATE UPDATES --- player
    clown_rect = pygame.Rect(clown_x-clown_radius, clown_y-clown_radius, clown_radius*2, clown_radius*2)

    #checks if the clown touches the endpoint/goal
    if clown_rect.colliderect(end_rect): 
        won_level_1 = True
    if current_time - win_time > 20 and won_level_1 == True:
            if win_size < WIDTH and maxed == False:
                win_size += 5
            if win_size > WIDTH//2:
                maxed = True
            if maxed == True and win_size > 0: #need to reset all values again
                win_size -= 5
                level = 2
                clown_x = 350
                clown_y = 300
                end_rect = [50, 50, 30, 30]

                platforms = []
                for i in range(len(all_tiles)):
                    for a in range(len(all_tiles[i])):
                        if all_tiles[i][a] == 1:
                            rect = pygame.Rect(a*tile_size, i*tile_size, tile_size, tile_size)
                            platforms.append(rect)
            win_time = current_time

    # checks if key is still pressed and moves accordingly (S is only shrink once)
    if moving[1] == 1: #A - move left
        clown_x -= 5

        for i in range(len(platforms)):
            if clown_rect.colliderect(platforms[i]):
                clown_x += 6
            
    if moving[3] == 1: #D - move right
        clown_x += 5

        for i in range(len(platforms)):
            if clown_rect.colliderect(platforms[i]):
                clown_x -= 6

    #gravity settings --- need to check which multiple of 32 (tile_size) the clown is between
    for i in range(WIDTH//tile_size): # current x number tile clown is on
        if clown_x > tile_size*i and clown_x < tile_size*(i+1):
            x_pos_tile = i
        
    for i in range(HEIGHT//tile_size): # current y number tile clown is on
        if clown_y > tile_size*i and clown_y < tile_size*(i+1):
            y_pos_tile = i

    clown_y += clown_y_change #moving downwards from gravity
    clown_y_change += gravity #continues to add to it to have acceleration due to gravity

    if all_tiles[y_pos_tile+1][x_pos_tile] == 0:
        on_tile = False

    
    #checks if tile below clown is a platform and clown's position is just above it    
    if all_tiles[y_pos_tile+1][x_pos_tile] == 1 and y_pos_tile*tile_size <= clown_y+clown_radius: 
        clown_y_change = 0
        on_tile = True

    #checks if clown is off the screen
    if clown_x > WIDTH:
        clown_x -= 5
    
    elif clown_x < 0:
        clown_x += 5
    
    if clown_y > HEIGHT:
        clown_y -= 5
    
    elif clown_y < 0:
        clown_y += 5


    #GAME STATE UPDATES --- enemy:

    for i in range(len(time_since_action)):
        if current_time - time_since_action[i] >= 1000:
            teleport[i] = random.randint(0, 20)
            time_since_action[i] = current_time
    
    for i in range(len(enemy_action)): # enemy random movements
        if level == 1 or (level == 2 and current_time - win_time == 3000):
            if enemy_action[i] == 0 and enemy_pos[i][0] < WIDTH:
                enemy_pos[i][0] += 3 # enemy moves right
            elif enemy_action[i] == 1 and enemy_pos[i][0] > 0:
                enemy_pos[i][0] -= 3 # enemy moves left
            if teleport[i] == 2:
                enemy_pos[i][0] = random.randint(0, WIDTH) # teleports enemy to random position if it hits the lucky chance
                enemy_pos[i][1] = 50
                teleport[i] = 40
        
            if enemy_pos[i][1] < 0:
                enemy_pos[i][1] += 5
            
            
            # enemy gravity settings
            enemy_pos[i][1] += enemy_y_change[i]
            

            for a in range(WIDTH//tile_size): # current x number tile clown is on
                if enemy_pos[i][0] > tile_size*a and enemy_pos[i][0] < tile_size*(a+1):
                    x_pos_tile_enemy[i] = a
            
            for a in range(HEIGHT//tile_size): # current y number tile clown is on
                if enemy_pos[i][1]+20 > tile_size*a and enemy_pos[i][1]+20 < tile_size*(a+1):
                    y_pos_tile_enemy[i] = a
            
            #makes enemy stand on platforms
            if all_tiles[y_pos_tile_enemy[i]+1][x_pos_tile_enemy[i]] == 1 and enemy_pos[i][1] >= y_pos_tile_enemy[i]*tile_size:
                enemy_y_change[i] = 0
            
            else:
                enemy_y_change[i] += gravity

            
            # makes sure enemy doesn't go off the screen
            if enemy_pos[i][0] + enemy_pos[i][2] > WIDTH:
                enemy_pos[i][0] -= tile_size
            elif enemy_pos[i][0] < 0:
                enemy_pos[i][0] += tile_size
            if enemy_pos[i][1] + enemy_pos[i][3] > HEIGHT:
                enemy_pos[i][1] -= tile_size
            elif enemy_pos[i][1] < 0:
                enemy_pos[i][1] += tile_size
            
            if enemy_pos[i][0] + enemy_pos[i][2] >= WIDTH-tile_size:
                enemy_action[i] = 1
            elif enemy_pos[i][0] < 0:
                enemy_action[i] = 0
        
            enemy_rect = pygame.Rect(enemy_pos[i])
        
            
            for a in range(len(platforms)): #checks for enemy collision with platforms so that enemy doesn't phase through them
                if enemy_rect.colliderect(platforms[a]):
                    if enemy_action[i] == 0 and all_tiles[y_pos_tile_enemy[i]][x_pos_tile_enemy[i]+1] == 1 and enemy_pos[i][0]+enemy_pos[i][2] < WIDTH-tile_size:
                        enemy_action[i] = 1
                        enemy_pos[i][0] -= 5
                        print(enemy_action)
                    elif enemy_action[i] == 1 and all_tiles[y_pos_tile_enemy[i]][x_pos_tile_enemy[i]-1] == 1 and enemy_pos[i][0] > 0:
                        enemy_action[i] = 0
                        enemy_pos[i][0] += 5
            

    #DRAWING
    #draw the clown
    pygame.draw.circle(screen, (255, 255, 255), (clown_x, clown_y), clown_radius) #head
    pygame.draw.circle(screen, (0, 0, 0), (clown_x-10, clown_y), clown_radius - 10) #left eye
    pygame.draw.circle(screen, (0, 0, 0), (clown_x+10, clown_y), clown_radius - 10) #right eye
    pygame.draw.circle(screen, (255, 100, 100), (clown_x, clown_y+10), clown_radius - 10) #nose

    for i in range(len(all_tiles)): #y_pos
        for a in range(len(all_tiles[i])): #x_pos
            if all_tiles[i][a] == 1:
                pygame.draw.rect(screen, (100, 100, 0), [a*tile_size, i*tile_size, tile_size, tile_size])
    
    #draw the enemy
    for i in range(len(enemy_pos)):
        if level == 1 or (level == 2 and current_time - win_time >= 3000):
            pygame.draw.rect(screen, (255, 0, 0), (enemy_pos[i][0], enemy_pos[i][1], 20, 20))

    #how pygame.draw.rect(screen, (0, 0, 0), end_rect)
    screen.blit(circus_resized, pygame.Rect(end_rect))

    #help box and window --- text
    pygame.draw.rect(screen, (225, 225, 100), help_rect)
    screen.blit(help_question, (help_rect[0]+8, help_rect[1], help_rect[2], help_rect[3]))

    if help_open == True: # checks if help box is open to show text
        screen.fill((255, 255, 255))
        screen.blit(help_window, (100, 50, 540, 100))
        screen.blit(help_goal, (115, 100, 300, 100))
        screen.blit(exit_window, (180, 400, 300, 100))
        

    
    # draws a rectangle with increasing side lengths to transition to the next level
    if won_level_1 == True:
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH//2-win_size, HEIGHT//2-win_size+50, win_size*2, win_size*2-80))

    # re-makes the level with a second platform setting
    if level == 2:
        all_tiles = [
        [0 for i in range(20)],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0 for i in range(20)],
        [1 for i in range(20)],
        [1 for i in range(20)],
        ]


    if clown_rect.colliderect(enemy_rect):
        dead = True #needed so that the rectangle doesn't disappear

    #draws another rectangle increasing in size 
    if dead == True and won_level_1 == False:
        if current_time - win_time > 200 and dead_is_True <= WIDTH//2:
            dead_is_True += 5
        pygame.draw.rect(screen, (255, 0, 0), (WIDTH//2-dead_is_True, HEIGHT//2-dead_is_True+50, dead_is_True*2, dead_is_True*2-80))

        if dead_is_True > WIDTH//2:
            screen.blit(dead_text, (60, 200, 300, 100))

    pygame.display.flip()
    clock.tick(30)
