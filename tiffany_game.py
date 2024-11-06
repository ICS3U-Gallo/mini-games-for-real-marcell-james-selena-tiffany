# clown game + balloons + face paint?
# circus end point

import pygame
import math

pygame.init()


WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#clown presets
clown_x = 0
clown_y = 0
clown_radius = 20

#moving [W, A, S, D]
moving = [0, 0, 0, 0]
shrunk = False

#platforms
platform = [[0, 380, 640, 100], [0, 200, 80, 20], [300, 200, 10, 10]]
closest = 0
distance_final = 100000000000

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

    
    #gravity settings
    distance_final = 10000
    for i in range(len(platform)):

        # if clown_y - clown_radius > platform[i][1] + platform[i][3]:
        #     distance_final = 100000

        distance = math.sqrt((platform[i][0] - clown_x)**2 + (platform[i][1] - clown_y)**2)
        print("c", closest, distance, distance_final)

        if distance <= distance_final:
            distance_final = distance
            closest = i
        
    if clown_y + clown_radius < platform[closest][1] or clown_y - clown_radius > platform[closest][1] + platform[closest][3]:
        clown_y += 5
    elif (clown_x > platform[closest][0] + platform[closest][2]) or (clown_x < platform[closest][0]):
        clown_y += 5


    #DRAWING
    #draw the clown
    pygame.draw.circle(screen, (255, 255, 255), (clown_x, clown_y), clown_radius) #head
    pygame.draw.circle(screen, (0, 0, 0), (clown_x-10, clown_y), clown_radius - 15) #left eye
    pygame.draw.circle(screen, (0, 0, 0), (clown_x+10, clown_y), clown_radius - 15) #right eye
    pygame.draw.circle(screen, (255, 100, 100), (clown_x, clown_y+10), clown_radius - 15) #nose

    for i in range(len(platform)):
        pygame.draw.rect(screen, (100, 100, 0), platform[i])


    pygame.display.flip()
    clock.tick(30)
