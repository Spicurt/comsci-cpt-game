import pygame
import button

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)

#Load button images
start_img = pygame.image.load('Sprites/new.png').convert_alpha()
instr_img = pygame.image.load('Sprites/instr.png').convert_alpha()
shop_img = pygame.image.load('Sprites/shop.png').convert_alpha()
#pygame.image.load('Sprites/.png').convert_alpha()

#instances - Coding With Russ
start_btn = button.Button(50, 200, start_img, 0.8 )
instr_btn = button.Button(350, 200, instr_img, 0.8)
shop_btn = button.Button(50, 400, shop_img, 0.8)

#BUTTON FUNCTIONS

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

    # DRAWING
    screen.fill('seagreen') 

    if start_btn.draw(screen):
        print("Start")

    if instr_btn.draw(screen):
        print("Instr")
    
    if shop_btn.draw(screen):
        print("Shop")

    #if .draw(screen):
        #print("")


    pygame.display.flip()


pygame.quit()
