# to do: add story aspect, blit images or create compound shapes for the enemies and platforms, fix level 2 (enemy physics)

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
clown_x = 250
clown_y = 250
clown_radius = 10 # clown radius needs to be 16 or less as tile_size is 32
clown_y_change = 0
clown_x_change = 0
x_pos_tile = 0
y_pos_tile = 0
gravity = 0.3 #will be acceleration, not constant

#moving [W, A, S, D]
moving = [0, 0, 0, 0]
shrunk = False
jumping = False

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
end_rect = [50, 320, 70, 70] # the win condition
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
enemy_pos = [[random.randint(0+tile_size, WIDTH-tile_size*2), 100, 20, 20] for i in range(4)]
enemy_action = [0 for i in range(len(enemy_pos))]
enemy_on_tile = [False for i in range(len(enemy_pos))]
x_pos_tile_enemy = [0 for i in range(len(enemy_pos))]
y_pos_tile_enemy = [0 for i in range(len(enemy_pos))]
enemy_y_change = [0 for i in range(len(enemy_pos))]
teleport = [0 for i in range(len(enemy_pos))]
reset_enemy_pos = 0

# dying variable (will show end screen)
dead = False

dead_is_True = 50

#start playing
play_rect = [230, 180, 160, 80]


running = True


def text_blit(text, colour, position):
    text_para = font.render(text, True, colour)
    screen.blit(text_para, position)

while running:
    current_time = pygame.time.get_ticks()
    clown_rect = pygame.Rect(clown_x-clown_radius, clown_y-clown_radius, clown_radius*2, clown_radius*2)
        
    #EVENT HANDLING
    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            running = False
        
        # pressed a key
        elif event.type == pygame.KEYDOWN:
            if help_open == False and dead == False and level != 0: #cannot win by pressing randomly while help window is open
            # able to press multiple keys and move in two directions at once
                print(on_tile)
                if on_tile == True:
                    if event.key == pygame.K_w: #so clown can't phase upwards
                        moving[0] = 1
                        jumping = True
        
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
            new_rect = pygame.Rect(new_clown_x-clown_radius, clown_y-clown_radius, clown_radius*2, clown_radius*2) #checks in advance whether it hits or not

            if new_rect.colliderect(i):
                new_clown_x = clown_x
                break
        clown_x = new_clown_x

    if moving[3] == 1: # moving right and not colliding
        new_clown_x = clown_x + 3
        for i in platforms:  
            new_rect = pygame.Rect(new_clown_x-clown_radius, clown_y-clown_radius, clown_radius*2, clown_radius*2) #checks in advance whether it hits or not

            if new_rect.colliderect(i):
                new_clown_x = clown_x
                break
        
        clown_x = new_clown_x
    
    if moving[0] == 1: # moving up and not colliding
        platform_above = 0
        for i in platforms:
            new_rect = pygame.Rect(clown_x-clown_radius, clown_y-clown_radius, clown_radius*2, clown_radius*2-5)
            if new_rect.colliderect(i):
                moving[0] = 0
                platform_above = 1
        if platform_above == 0:
            clown_y_change = -3
        
        elif platform_above == 1:
            clown_y_change = 3
        
        clown_y += clown_y_change


    if level != 0:
        on_tile = False

        if on_tile == False and moving[0] == 0:
            clown_y_change += gravity
            clown_y += clown_y_change

        for i in platforms:
            new_rect = pygame.Rect(clown_x-clown_radius, clown_y-clown_radius, clown_radius*2, clown_radius*2+gravity)
            if clown_y_change >= -1 and new_rect.colliderect(i):
                on_tile = True
                clown_y_change = 0
                clown_y = i.top - clown_radius
                break
            else:
                on_tile = False
            
    
        if moving[1] == 0 and moving[3] == 0:
            clown_x_change = 0
    

    
    #GAME STATE UPDATES - level
    # re-makes the level with a second platform setting
    if level == 2:
        all_tiles = [
        [1 for i in range(20)],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1 for i in range(20)],
        [1 for i in range(20)],
        ]

    #GAME STATE UPDATES --- player
    if level != 0:
        clown_y += clown_y_change
        clown_x += clown_x_change
        
        if on_tile == True:
            clown_y_change = -0.5
            jumping = False

        #checks if the clown touches the endpoint/goal
        if clown_rect.colliderect(end_rect): 
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
                    clown_y = 250
                    end_rect = [50, 50, 30, 30]
                    dead = False #may die while animation to switch levels is playing

                    platforms = []
                    for i in range(len(all_tiles)):
                        for a in range(len(all_tiles[i])):
                            if all_tiles[i][a] == 1:
                                rect = pygame.Rect(a*tile_size, i*tile_size, tile_size, tile_size)
                                platforms.append(rect)
                win_time = current_time

            
        if clown_rect.colliderect(end_rect) and level == 2:
            won_level_2 = True

            
    #GAME STATE UPDATES --- enemy:
        for i in range(len(enemy_action)): # enemy random movements
            if level == 1 or (level == 2 and current_time - win_time >= 500):
                enemy_rect = pygame.Rect(enemy_pos[i]) #creates enemy hitbox

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
            
            if reset_enemy_pos == 0 and level == 2:
                for i in range(len(enemy_pos)):
                    enemy_pos[i][0] = random.randint(tile_size*1.5, WIDTH-tile_size*1.5)
                    enemy_pos[i][1] = 50
                    clown_y_change = 0 #needed as this variable (reset_enemy_pos) is a toggle and only works in one instant unlike the clown settings above
                
                reset_enemy_pos = 1
                
            if clown_rect.colliderect(enemy_rect):
                dead = True #needed so that the rectangle doesn't disappear

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

        #how pygame.draw.rect(screen, (0, 0, 0), end_rect)
        screen.blit(circus_resized, pygame.Rect(end_rect))

        #help box and window --- text
        pygame.draw.rect(screen, (225, 225, 100), help_rect)
        screen.blit(help_question, (help_rect[0]+8, help_rect[1], help_rect[2], help_rect[3]))

        if help_open == True: # checks if help box is open to show text
            screen.fill((255, 255, 255))
            text_blit("W: jump (hold); A: move left; S: shrink; D: move right", (0, 0, 0), (90, 50, 540, 100))
            text_blit("Goal: help the clown reach the circus tent!", (0, 0, 0), (115, 100, 300, 100))
            text_blit("Press ESC to exit this window", (0, 0, 0), (180, 400, 300, 100))
            

        if won_level_1 == True and current_time - win_time < 500 and level == 2:
            dead = False
        

        # draws a rectangle with increasing side lengths to transition to the next level
        if won_level_1 == True:
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH//2-win_size, HEIGHT//2-win_size+50, win_size*2, win_size*2-80))
        
        if won_level_2 == True:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
            text_blit("You've arrived at the circus!", (255, 255, 255), (150, 100, 50, 50))



        #draws another rectangle increasing in size 
        if dead == True:
            if current_time - win_time > 200 and dead_is_True <= WIDTH//2:
                dead_is_True += 5
            pygame.draw.rect(screen, (255, 0, 0), (WIDTH//2-dead_is_True, HEIGHT//2-dead_is_True+50, dead_is_True*2, dead_is_True*2-80))

            if dead_is_True > WIDTH//2:
                text_blit("You have died to your business rival: clown brother #1", (0, 0, 0), (60, 200, 300, 100))
        
        
    #play start screen
    if level == 0:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (210, 50, 90), play_rect)
        text_blit("PLAY", (0, 0, 0), (play_rect[0]+55, play_rect[1]+25, play_rect[2], play_rect[3]))
        text_blit("CIRCUS ADVENTURE", (255, 255, 255), (play_rect[0]-20, play_rect[1]-50, 100, 50))

    pygame.display.flip()
    clock.tick(30)
