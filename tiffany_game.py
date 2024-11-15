import pygame
import random

pygame.init()


WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

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

while running:
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

                print(on_tile_enemy)
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
    
    pygame.display.flip()
    clock.tick(30)
