
# clown game + balloons + face paint?

import pygame

pygame.init()


WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#clown presets
clown_x = 100
clown_y = 100
clown_radius = 20

#moving [W, A, S, D]
moving = [0, 0, 0, 0]

running = True

while running:
    screen.fill((170, 200, 255))
    #EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # pressed a key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving[3] = 1 
            
        
        # let go of key
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving[3] = 0


    #GAME STATE UPDATES

    # checks if key is still pressed and moves accordingly
    if moving[3] == 1:
        clown_x += 10


    #DRAWING
    #draw the clown
    pygame.draw.circle(screen, (255, 255, 255), (clown_x, clown_y), clown_radius) #head
    pygame.draw.circle(screen, (0, 0, 0), (clown_x-10, clown_y), 5) #left eye
    pygame.draw.circle(screen, (0, 0, 0), (clown_x+10, clown_y), 5) #right eye
    pygame.draw.circle(screen, (255, 100, 100), (clown_x, clown_y+10), 5) #nose


    pygame.display.flip()
    clock.tick(30)
