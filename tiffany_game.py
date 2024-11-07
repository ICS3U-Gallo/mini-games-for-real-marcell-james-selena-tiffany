# clown game + balloons + face paint?
# circus end point

import pygame

pygame.init()


WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#clown presets
clown_x = 50
clown_y = 50
clown_radius = 20
clown_y_change = 0
x_pos_tile = 0
y_pos_tile = 0

#moving [W, A, S, D]
moving = [0, 0, 0, 0]
shrunk = False

#tiles (all_tiles is in rows and columns)
tile_size = 64
all_tiles = [
    [0 for i in range(10)],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0 for i in range(10)],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0 for i in range (10)],
    [1 for i in range(10)],
    [1 for i in range(10)]
    ]

running = True

while running:
    screen.fill((170, 200, 255))
    #EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # pressed a key
        elif event.type == pygame.KEYDOWN:
            # able to press multiple keys and move in two directions at once
            if event.key == pygame.K_w:
                clown_y -= 20
            if event.key == pygame.K_a:
                moving[1] = 1 
            if event.key == pygame.K_s:
                clown_radius -= 10

                if shrunk == False:
                    shrunk = True
                elif shrunk == True:
                    shrunk = False

            if event.key == pygame.K_d:
                moving[3] = 1 
            
        
        # let go of key
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w: #only able to jump one at a time
                moving[0] = 0
            if event.key == pygame.K_a:
                moving[1] = 0
            if event.key == pygame.K_s: #a toggle
                if shrunk == False:
                    clown_radius = 10
                elif shrunk == True:
                    clown_radius = 20
            if event.key == pygame.K_d:
                moving[3] = 0


    #GAME STATE UPDATES

    # checks if key is still pressed and moves accordingly (S is only shrink once)
    if moving[1] == 1: #A - move left
        clown_x -= 5
    if moving[3] == 1: #D - move right
        clown_x += 5

    
    #gravity settings --- need to check which multiple of 64 the clown is between
    for i in range(WIDTH//64):
        if clown_x > 64*i and clown_x < 64*(i+1):
            x_pos_tile = i
        
    for i in range(HEIGHT//64):
        if clown_y > 64*i and clown_y < 64*(i+1):
            y_pos_tile = i

    clown_y += clown_y_change
    if all_tiles[(HEIGHT // clown_y)][(WIDTH // clown_x)] == 1: #logic faulty
        clown_y_change = 0
    
    else:
        clown_y_change = 0.5

    #DRAWING
    #draw the clown
    pygame.draw.circle(screen, (255, 255, 255), (clown_x, clown_y), clown_radius) #head
    pygame.draw.circle(screen, (0, 0, 0), (clown_x-10, clown_y), clown_radius - 15) #left eye
    pygame.draw.circle(screen, (0, 0, 0), (clown_x+10, clown_y), clown_radius - 15) #right eye
    pygame.draw.circle(screen, (255, 100, 100), (clown_x, clown_y+10), clown_radius - 15) #nose

    for i in range(len(all_tiles)):
        for a in range(len(all_tiles[i])):
            if all_tiles[i][a] != 0:
                pygame.draw.rect(screen, (100, 100, 0), [a*64, i*64, 64, 64])


    pygame.display.flip()
    clock.tick(30)
