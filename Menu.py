import random
import os
import sys
import pygame
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()

pygame.init()
#GREEN CODE: does not work, or work on it later

WIDTH = 1280
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)

def mainGame():
    global background, game_paused, WIDTH, HEIGHT, SIZE
    if background == "bjs.png":
        screen.fill((34, 177, 76))
    if background == "bjs2.png":
        screen.fill((94, 254, 255))
    if pause_btn.draw(screen):
        game_paused = True

#REGULUS'S code from here
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

#ALL OF THESE are the variables that cannot go into the function, or are more convenient left outside
#game variables
game_state = 'starting screen'
game_paused = False
menu_state = 'main'
background = "bjs.png"
#shop variables
SHOP_ITEMS = [0, 0, 0]
PRICES = [20, 10, 500]
second_item_randoms = [5, 5, 5, 10, 10, 100, -10, -10, -5, -5, 0, 0, 0]
result = 0
CHIPS = 1000

# Display time for text - Chat GPT
show_error = False
error_start_time = 0
ERROR_DISPLAY_DURATION = 500 

# Display time for text 2 - Regulus
show_not_enough_chips = False
error_start_time2 = 0
ERROR_DISPLAY_DURATION2 = 500 

# Display time for text 3 - Regulus
show_chips_added_or_subtracted = False
error_start_time3 = 0
ERROR_DISPLAY_DURATION3 = 500

# Display time for text 4 - Regulus
show_not_bought = False
error_start_time4 = 0
ERROR_DISPLAY_DURATION4 = 500

# Display time for text 5 - Regulus
show_already_bought = False
error_start_time5 = 0
ERROR_DISPLAY_DURATION5 = 500

#Button Class - Coding With Russ
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def draw(self, surface):
        action = False

        #get mouse pos
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            #allows more clicks
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

#Button images
resume_img = pygame.image.load("button_sprites/resume.png").convert_alpha()
options_img = pygame.image.load("button_sprites/menu.png").convert_alpha()
quit_img = pygame.image.load("button_sprites/quit.png").convert_alpha()
change_background_img = pygame.image.load('button_sprites/change_background.png').convert_alpha()
audio_img = pygame.image.load('button_sprites/audio.png').convert_alpha() #red
keys_img = pygame.image.load('button_sprites/keys.png').convert_alpha() #green
back_img = pygame.image.load('button_sprites/back.png').convert_alpha() #red
pause_img = pygame.image.load("button_sprites/pause.png").convert_alpha() 
start_img = pygame.image.load('button_sprites/new.png').convert_alpha() #red
instr_img = pygame.image.load('button_sprites/instr.png').convert_alpha()
shop_img = pygame.image.load('button_sprites/shop.png').convert_alpha()

#Sprite images
question_img = pygame.image.load("button_sprites/question_card.png").convert_alpha()
starting_img = pygame.image.load("images/cards/back.png").convert_alpha()
bjs_blue_img = pygame.image.load("images/blue.png").convert_alpha()
mystery_img = pygame.image.load("button_sprites/mystery.png").convert_alpha()
switch_img = pygame.image.load("images/switchcolors.png").convert_alpha()

#Button instances
resume_btn = Button(200, 80, resume_img, 1)
options_btn = Button(200, 220, options_img, 1)
quit_btn = Button(200, 370, quit_img, 1)
change_background_btn = Button(WIDTH -500, 75, change_background_img, 1)
audio_btn = Button(WIDTH -300, 200, audio_img, 1)
keys_btn = Button(WIDTH -300, 325, keys_img, 1)
back_btn = Button(20, 20, back_img, 0.8)
pause_btn = Button(20, 20, pause_img, 0.8)
start_btn = Button(500, 180, start_img, 1)
instr_btn = Button(492, 340, instr_img, 1)
shop_btn = Button(535, 500, shop_img, 1)

#sprite instances
question_btn = Button(75, 200, question_img, 0.5)
gamble_btn = Button(450, 250, mystery_img, 0.5)
bjs_blue_btn = Button(785, 250, bjs_blue_img, 1)
pwerup_sprite = Button(1100, 500, question_img, 0.2)
switch_btn = Button(450, 200, switch_img, 2)

#Pause function, in-game menu. When I click pause button, I will get into the pause menu.

#drawing text - Coding With Russ
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


#I put all my code in a function so that Darren's buttons can work
def regulus_code():
    global CHIPS, game_paused, game_state, menu_state, SHOP_ITEMS, PRICES, second_item_randoms, show_not_enough_chips, show_chips_added_or_subtracted, error_start_time2, error_start_time3, ERROR_DISPLAY_DURATION2, ERROR_DISPLAY_DURATION3, result, background, show_not_bought, error_start_time4, ERROR_DISPLAY_DURATION4, show_already_bought, error_start_time5, ERROR_DISPLAY_DURATION5

    WIDTH = 1280
    HEIGHT = 700
    SIZE = (WIDTH, HEIGHT)

    screen = pygame.display.set_mode(SIZE)

    #game variables - I put this here so that once the regulus_code() function is called (thus bringing the player back to the starting screen), all gave variables are reset
    game_state = 'starting screen'
    game_paused = False
    menu_state = 'main'

    #fonts
    font = pygame.font.SysFont("serif", 40)
    font2 = pygame.font.SysFont("arvo", 13)
    font3 = pygame.font.SysFont("serif", 30)
    font4 = pygame.font.SysFont("serif", 60)

    #text color
    TEXT_COL = (255, 255, 255)
    TEXT_COL2 = ("darkgoldenrod1")
    TEXT_COL3 = ("gray0")
    TEXT_COL4 = ((147, 187, 191))

    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    # Shop function when I click on the shop button, it will take me to the shop function, where I can buy stuff.
    def shop():
        screen.fill((29, 98, 102))
        
        draw_text(f"CHIPS: {CHIPS}", font, TEXT_COL2, 900, 40)
        for i in range(len(SHOP_ITEMS)):
            if i == 0:
                draw_text(f"{SHOP_ITEMS[i]}", font, TEXT_COL, 1140, 600)
                pwerup_sprite.draw(screen)
        
        draw_text("know the next card", font, TEXT_COL4, 20, 500)
        draw_text("chips gamble", font, TEXT_COL4, 450, 500)
        draw_text("blue background", font, TEXT_COL4, 750, 500)

        if question_btn.draw(screen):
            paying1()
        if gamble_btn.draw(screen):
            paying2()
        if bjs_blue_btn.draw(screen):
            paying3()
        
    #This is a powerup. It should allow the user to see the next card.
    def paying1():
        global CHIPS, show_not_enough_chips, error_start_time2
        if CHIPS > 50:
            CHIPS -= PRICES[0]
            SHOP_ITEMS[0] += 1
        else:
            show_not_enough_chips = True
            error_start_time2 = pygame.time.get_ticks()

    #this is like a mystery box. Buy it for 10 chips. You can either gain lots of chips or lose lots of chips. It is sort of like a gambling game within a gambling game
    def paying2():
        global CHIPS, show_not_enough_chips, error_start_time2, result, show_chips_added_or_subtracted, error_start_time3 
        if CHIPS > 50:
            CHIPS -= PRICES[1]
            SHOP_ITEMS[1] += 1
            result = random.choice(second_item_randoms)
            show_chips_added_or_subtracted = True
            error_start_time3 = pygame.time.get_ticks()
            CHIPS += result
        else:
            show_not_enough_chips = True
            error_start_time2 = pygame.time.get_ticks()

    #cosmetic background
    def paying3():
        global CHIPS, show_not_enough_chips, error_start_time2, show_already_bought, error_start_time5
        if SHOP_ITEMS[2] == 0:
            if CHIPS >= 550:
                CHIPS -= PRICES[2]
                SHOP_ITEMS[2] += 1
            else:
                show_not_enough_chips = True
                error_start_time2 = pygame.time.get_ticks()
        else:
            show_already_bought = True
            error_start_time5 = pygame.time.get_ticks()

        
#main loop
    running = True
    while running:
        # EVENT HANDLING
        for event in pygame.event.get():
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         game_paused = True
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

        #starting screen
        if game_state == 'starting screen':
            screen.fill('seagreen') 

            draw_text(f"BlackJack!", font4, TEXT_COL2, 500, 60)

            if start_btn.draw(screen):
                game_state = 'playing'

            if instr_btn.draw(screen):
                game_state = "instructions"
            
            if shop_btn.draw(screen):
                game_state = 'shop'

            art_list = [0]

            for num in art_list:
                start_sprite = Button(num, 630, starting_img, 0.4)
                start_sprite.draw(screen)
                art_list.append(num + 30)
                if num >= 1280:
                    break

        #if game is paused, activate menu
        elif game_state == 'playing':
            screen.fill((52, 78, 91))
            if game_paused == True: #IMPORTANT IMPORTANT TMSFDOPSP

                screen.fill("seagreen")
                #check main state
                if menu_state == "main":
                    #draw pause screen buttons 
                    if resume_btn.draw(screen):
                        game_paused = False
                    if options_btn.draw(screen):
                        menu_state = "options"
                    if quit_btn.draw(screen):
                        game_state = "starting screen"
                        game_paused = False
                if menu_state == "options":
                    if change_background_btn.draw(screen):
                        menu_state = "background"
                    if audio_btn.draw(screen):
                        print("Audio Settings")
                    if back_btn.draw(screen):
                        menu_state = "main"
                #background cosmetics
                if menu_state == "background":
                    screen.fill((29, 98, 102))
                    if back_btn.draw(screen):
                        menu_state = "options"
                    draw_text("Change Background", font, TEXT_COL4, 450, 537)
                    if switch_btn.draw(screen):
                        if background == "bjs.png":
                            if SHOP_ITEMS[2] > 0:
                                background = "bjs2.png"
                            else:
                                show_not_bought = True
                                error_start_time4 = pygame.time.get_ticks()
                        elif background == "bjs2.png":
                            background = "bjs.png"
            #if game not paused, draw pause button + other functions
            else: 
                #calling Darren's code to play my game
                mainGame()
        
        #Shop
        if game_state == 'shop':
            shop()
            if back_btn.draw(screen):
                game_state = "starting screen"
        
        if game_state == "instructions":
            screen.fill("seagreen")
            draw_text(f"Blackjack is an easy game to play! Here are the instructions:", font, TEXT_COL2, 50, 100)
            draw_text("1. Enter your bet amount", font3, TEXT_COL2, 50, 200)
            draw_text("2. Choose to hit or stand. Hitting means you get another card. Standing means you don't get anything ", font3, TEXT_COL2, 50, 300)
            draw_text("3. Add your cards up. 10s, kings, queens, and jacks all count as 10s. Aces can be 11s or 1s", font3, TEXT_COL2, 50, 400)
            draw_text("4. You are trying to get a 21 total, but if you go over 21 or the dealer has more than you, you lose!", font3, TEXT_COL2, 50, 500)
            draw_text("5. Have fun!", font3, TEXT_COL2, 50, 600)
            if back_btn.draw(screen):
                game_state = "starting screen"

    #THESE CODES BELOW are from Chatgpt. They are for showing the user that there are not enough tokens and the amount of money being added/subtracted from the second item in the shop.
    #Show not enough CHIPS - ChatGPT
        if show_not_enough_chips:
            current_time2 = pygame.time.get_ticks()
            if current_time2 - error_start_time2 < ERROR_DISPLAY_DURATION2:
                draw_text("Not enough CHIPS!", font, TEXT_COL, 400, 250)
            else:
                show_error = False

    #showing amount of chips added or subtracted in the second shop function
        if show_chips_added_or_subtracted:
            current_time3 = pygame.time.get_ticks()
            if current_time3 - error_start_time3 < ERROR_DISPLAY_DURATION3:
                draw_text(f"{result-10}", font, TEXT_COL, 1017, 109)
            else:
                show_error = False

    #showing amount of chips added or subtracted in the second shop function
        if show_not_bought:
            current_time4 = pygame.time.get_ticks()
            if current_time4 - error_start_time4 < ERROR_DISPLAY_DURATION4:
                draw_text("Background not bought!", font, TEXT_COL, 450, 140)
            else:
                show_error = False

    #showing amount of chips added or subtracted in the second shop function
        if show_already_bought:
            current_time5 = pygame.time.get_ticks()
            if current_time5 - error_start_time5 < ERROR_DISPLAY_DURATION5:
                draw_text("Background already bought!", font, TEXT_COL, 450, 140)
            else:
                show_error = False

        pygame.display.flip()
        clock.tick(30)

regulus_code()

pygame.quit()
