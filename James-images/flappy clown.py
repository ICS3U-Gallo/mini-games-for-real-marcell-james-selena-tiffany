import random
import sys
import pygame


pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)
GRAVITY = 1
JUMP_VELOCITY = -10
GROUND_LEVEL = HEIGHT - 150


screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
fps = 120

cloonie = pygame.image.load("cloonie.png")
cloonie1 = pygame.transform.scale(cloonie, (40, 40))
beckground = pygame.image.load("background.png")
ground = pygame.image.load("ground.png")
ground1 = pygame.transform.scale(ground, (700, 137))
image_rect = cloonie1.get_rect()
image_rect.center = [150, 240]
ground_scroll = 0
scroll_speed = 5
velocity_y = 0


# ---------------------------
# Initialize global variables

velocity_y += 0.5
if image_rect.bottom < 350:
    image_rect.y += int(velocity_y)

# ---------------------------

running = True
while running:

    clock.tick(fps)

    # EVENT HANDLING
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        velocity_y = JUMP_VELOCITY

    velocity_y += GRAVITY

    image_rect.y += velocity_y

    if image_rect.bottom >= GROUND_LEVEL:
        image_rect.bottom = GROUND_LEVEL
        velocity_y = 0
    
    if image_rect.top <= -27:
        image_rect.top = -26
    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command
    #background
    screen.blit(beckground, (0, 0))
    #background and scroll
    screen.blit(ground1, (ground_scroll, 350))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 60:
        ground_scroll = 0
    #clown
    screen.blit(cloonie1, image_rect.center)
    
    


    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()