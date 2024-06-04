# pygame template

import pygame
import buttons


pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

#button images
cardback_img = pygame.image.load("card_sprites/card_back").convert_alpha()

#button instances
cardback_btn = buttons(1, 1, cardback_img, 1)

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # always the first drawing command

    cardback_btn.draw(screen)
    

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()