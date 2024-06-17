import random
import os
import sys
import pygame
import json
import pickle
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()

pygame.init()
#GREEN CODE: does not work, or work on it later

WIDTH = 1280
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

#game variables
game_state = 'starting screen'
game_paused = False
menu_state = 'main'
sound = True
background = "bjs.png"
#shop variables
SHOP_ITEMS = [0, 0, 0]
PRICES = [20, 10, 500]
second_item_randoms = [5, 5, 5, 10, 10, 100, -10, -10, -5, -5, 0, 0, 0]
result = 0
CHIPS = 100

# Constants
WIDTH, HEIGHT = 1280, 700
CARD_WIDTH, CARD_HEIGHT = 120, 180  
BLACKJACK = 21
DEALER_STAND = 17
FONT_SIZE = 32

def save_game_state():
    game_state_data = {
        'CHIPS': CHIPS,
        'background': 'background.png',  # Replace with actual background state if dynamic
        'sound': sound,
        'SHOP_ITEMS': SHOP_ITEMS
    }
    with open('game_state.json', 'w') as f:
        json.dump(game_state_data, f)

def load_game_state():
    global CHIPS, sound, SHOP_ITEMS
    try:
        with open('game_state.json', 'r') as f:
            game_state_data = json.load(f)
            CHIPS = game_state_data.get('CHIPS', CHIPS)
            sound = game_state_data.get('sound', sound)
            SHOP_ITEMS = game_state_data.get('SHOP_ITEMS', SHOP_ITEMS)
    except FileNotFoundError:
        pass

load_game_state()

# Load card images - CHATGPT
card_images = {}
suits = ['H', 'D', 'C', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

for suit in suits:
    for rank in ranks:
        image_path = os.path.join('images', f'{suit}{rank}.png')
        card_images[f'{suit}{rank}'] = pygame.transform.scale(pygame.image.load(image_path), (CARD_WIDTH, CARD_HEIGHT))

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
    
#drawing text - Coding With Russ
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#loading sound - Darren's code
def soundLoad(name):    
    fullName = os.path.join('sounds', name)
    try: sound = pygame.mixer.Sound(fullName)
    except pygame.error as message:
        print('Cannot load sound:'), name
        raise SystemExit and message
    return sound

#playing sound - Darren's code
def playClick():
    clickSound = soundLoad("click2.wav")
    clickSound.play()

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
mute_img = pygame.image.load('button_sprites/mute.png').convert_alpha()
unmute_img = pygame.image.load('button_sprites/unmute.png').convert_alpha()

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
mute_btn = Button(535, 300, mute_img, 1)
unmute_btn = Button(535, 400, unmute_img, 1)

#sprite instances
question_btn = Button(75, 200, question_img, 0.5)
gamble_btn = Button(450, 250, mystery_img, 0.5)
bjs_blue_btn = Button(785, 250, bjs_blue_img, 1)
pwerup_sprite = Button(1100, 500, question_img, 0.2)
switch_btn = Button(450, 200, switch_img, 2)

# Load button images
hit_image = pygame.image.load(os.path.join('images', 'hit.png'))
stand_image = pygame.image.load(os.path.join('images', 'stand.png'))
restart_image = pygame.image.load(os.path.join('images', 'restart.png'))
pause_image = pygame.image.load(os.path.join('images', 'pause.png'))
up_image = pygame.image.load(os.path.join('images', 'up.png'))
down_image = pygame.image.load(os.path.join('images', 'down.png'))
    
# Create buttons
hit_button = Button(WIDTH - 300, HEIGHT // 2 - 200, hit_image, 1.5)  # 3 times bigger
stand_button = Button(WIDTH - 300, HEIGHT // 2 - 150, stand_image, 1.5)  # 3 times bigger
restart_button = Button(WIDTH - 400, HEIGHT // 2 + 150, restart_image, 1.0)  # Original size
pause_button = Button(WIDTH - 400, HEIGHT // 2 + 250, pause_image, 1.0)  # Original size
up_button = Button(990, 335, up_image, 1.0)  # Original size
down_button = Button(1140, 335, down_image, 1.0)  # Original size

#I put all my code in a function to simplify everything
def regulus_code():
    global CHIPS, game_paused, game_state, menu_state, SHOP_ITEMS, PRICES, second_item_randoms, show_not_enough_chips, show_chips_added_or_subtracted, error_start_time2, error_start_time3, ERROR_DISPLAY_DURATION2, ERROR_DISPLAY_DURATION3, result, background, show_not_bought, error_start_time4, ERROR_DISPLAY_DURATION4, show_already_bought, error_start_time5, ERROR_DISPLAY_DURATION5, sound, font, font2, font3, font4, TEXT_COL, TEXT_COL2, TEXT_COL3, TEXT_COL4, player_hand, dealer_hand, in_play, player_stands, outcome, bet

    WIDTH = 1280
    HEIGHT = 700
    SIZE = (WIDTH, HEIGHT)

    screen = pygame.display.set_mode(SIZE)
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    # Shop function, when I click on the shop button, it will take me to the shop function, where I can buy stuff.
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
            if sound == True:
                playClick()
            paying1()
        if gamble_btn.draw(screen):
            if sound == True:
                playClick()
            paying2()
        if bjs_blue_btn.draw(screen):
            if sound == True:
                playClick()
            paying3()
        
    #This is a powerup. It should allow the user to see the next card.
    def paying1():
        global CHIPS, show_not_enough_chips, error_start_time2
        if CHIPS > 50:
            CHIPS -= PRICES[0]
            SHOP_ITEMS[0] += 1
            save_game_state()
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
            save_game_state()
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
                save_game_state()
            else:
                show_not_enough_chips = True
                error_start_time2 = pygame.time.get_ticks()
        else:
            show_already_bought = True
            error_start_time5 = pygame.time.get_ticks()

    def during_game():
        global background, game_paused, WIDTH, HEIGHT, SIZE, SHOP_ITEMS, font, TEXT_COL, CHIPS
        if background == "bjs.png":
            screen.fill('seagreen')
        if background == "bjs2.png":
            screen.fill((94, 254, 255))
        draw_text(f"{SHOP_ITEMS[0]}", font, TEXT_COL, 1140, 600)
        if pwerup_sprite.draw(screen):
            if sound == True:
                playClick()
            if SHOP_ITEMS[0] > 0:
                SHOP_ITEMS[0] -= 1
                save_game_state()
    
#ACTUAL GAME FUNCTIONS - CHATGPT
    # Function to calculate the value of a hand
    def calculate_hand_value(hand):
        value = 0
        aces = 0
        for card in hand:
            rank = card[1:]
            if rank in ['J', 'Q', 'K']:
                value += 10
            elif rank == 'A':
                value += 11
                aces += 1
            else:
                value += int(rank)
        
        while value > BLACKJACK and aces:
            value -= 10
            aces -= 1

        return value

    # Function to draw the hands
    def draw_hand(hand, x, y):
        for i, card in enumerate(hand):
            screen.blit(card_images[card], (x + i * (CARD_WIDTH + 10), y))

    # Function to reset the game state
    def reset_game():
        global player_hand, dealer_hand, in_play, player_stands, outcome, bet
        player_hand = [random.choice(suits) + random.choice(ranks), random.choice(suits) + random.choice(ranks)]
        dealer_hand = [random.choice(suits) + random.choice(ranks), random.choice(suits) + random.choice(ranks)]
        in_play = True
        player_stands = False
        outcome = ""
        bet = 10  # Initial bet amount
#GAME FUNCTIONS FINISHED
        
#main loop
    running = True
    while running:

        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

        #starting screen
        if game_state == 'starting screen':
            screen.fill('seagreen') 

            draw_text(f"BlackJack!", font4, TEXT_COL2, 500, 60)

            if start_btn.draw(screen):
                if sound == True:
                    playClick()
                game_state = 'playing'


            if instr_btn.draw(screen):
                if sound == True:
                    playClick()
                game_state = "instructions"
            
            if shop_btn.draw(screen):
                if sound == True:
                    playClick()
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
            #Pause function, in-game menu. When I click pause button, I will get into the pause menu.
            if game_paused == True: #IMPORTANT IMPORTANT
                screen.fill("seagreen")
                #check main state
                if menu_state == "main":
                    #draw pause screen buttons 
                    if resume_btn.draw(screen):
                        if sound == True:
                            playClick()   
                        game_paused = False
                    if options_btn.draw(screen):
                        if sound == True:
                            playClick()   
                        menu_state = "options"
                    if quit_btn.draw(screen):
                        if sound == True:
                            playClick()   
                        game_state = "starting screen"
                        game_paused = False
                #takes me to the second page in the menu options
                if menu_state == "options":
                    if change_background_btn.draw(screen):
                        if sound == True:
                            playClick()   
                        menu_state = "background"
                    if audio_btn.draw(screen):
                        if sound == True:
                            playClick()   
                        menu_state = "audio"
                    if back_btn.draw(screen):
                        if sound == True:
                            playClick()   
                        menu_state = "main"
                #background cosmetics
                if menu_state == "background":
                    screen.fill((29, 98, 102))
                    if back_btn.draw(screen):
                        if sound == True:
                            playClick()   
                        menu_state = "options"
                    draw_text("Change Background", font, TEXT_COL4, 450, 537)
                    if switch_btn.draw(screen):
                        if sound == True:
                            playClick()   
                        if background == "bjs.png":
                            if SHOP_ITEMS[2] > 0:
                                background = "bjs2.png"
                                save_game_state()
                            else:
                                show_not_bought = True 
                                error_start_time4 = pygame.time.get_ticks()
                        elif background == "bjs2.png":
                            background = "bjs.png"
                            save_game_state()
                #audio options
                if menu_state == "audio":
                    screen.fill((29, 98, 102))
                    if back_btn.draw(screen):
                        if sound == True:
                            playClick()   
                        menu_state = "options"
                    if sound == True:
                        if mute_btn.draw(screen):
                            if sound == True:
                                playClick()   
                            sound = False
                            save_game_state()
                    if sound == False:
                        if unmute_btn.draw(screen):
                            playClick()
                            sound = True
                            save_game_state()

            else: 
                during_game()
                # Main game loop
                def main(): #CHAT GPT, but Regulus added the powerup button, the ability for it to close properly, the pause button, and a few other small things
                    global CHIPS, player_hand, dealer_hand, in_play, player_stands, outcome, bet, game_paused, running, game_state

                    run = True
                    clock = pygame.time.Clock()
                    
                    # Reset game state
                    reset_game()
                    while run:
                        if background == "bjs.png":
                            screen.fill('seagreen')
                        if background == "bjs2.png":
                            screen.fill((94, 254, 255))
                        draw_text(f"{SHOP_ITEMS[0]}", font, TEXT_COL, 1140, 600)
                        if pwerup_sprite.draw(screen):
                            if sound == True:
                                playClick()   
                            if SHOP_ITEMS[0] > 0:
                                SHOP_ITEMS[0] -= 1
                                save_game_state()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                run = False
                                pygame.quit()
                
                        # Draw hands
                        draw_hand(player_hand, 50, HEIGHT - CARD_HEIGHT - 20)
                        draw_hand(dealer_hand if player_stands else dealer_hand[:1], 50, 50)  # Adjusted dealer hand text position

                        # Calculate hand values
                        player_value = calculate_hand_value(player_hand)
                        dealer_value = calculate_hand_value(dealer_hand)

                        # Draw values
                        draw_text(f'Player: {player_value}', font, TEXT_COL4, 50, HEIGHT - CARD_HEIGHT - 90)
                        draw_text(f'Dealer: {dealer_value if player_stands else "?"}', font, TEXT_COL4, 50, CARD_HEIGHT + 70)  # Adjusted position
                        draw_text(f'Chips: {CHIPS}', font, TEXT_COL2, WIDTH - 300, 20)
                        draw_text(f'Bet: {bet}', font, TEXT_COL2, WIDTH - 300, 60)

                        # Check button clicks
                        if hit_button.draw(screen) and in_play and not player_stands:
                            if sound == True:
                                playClick()   
                            player_hand.append(random.choice(suits) + random.choice(ranks))
                        if stand_button.draw(screen) and in_play:
                            if sound == True:
                                playClick() 
                            player_stands = True
                        if restart_button.draw(screen):
                            if sound == True:
                                playClick() 
                            if CHIPS <= 0:
                                CHIPS = 10  # Reset chips on game over
                                
                            main()  # Reset the game state
                        if pause_button.draw(screen):
                            if sound == True:
                                playClick() 
                            game_paused = True
                            break
                        if up_button.draw(screen):
                            if sound == True:
                                playClick() 
                            if bet < CHIPS:
                                bet += 10  # Increase the bet by 10
                        if down_button.draw(screen):
                            if sound == True:
                                playClick() 
                            if bet > 10:
                                bet -= 10  # Decrease the bet by 10

                        if player_value > BLACKJACK and in_play:
                            outcome = "Player busts! Dealer wins."
                            CHIPS -= bet
                            save_game_state()
                            in_play = False
                        elif player_value == BLACKJACK and in_play:
                            outcome = "Blackjack! Player wins."
                            CHIPS += bet
                            save_game_state()
                            in_play = False

                        if player_stands and in_play:
                            while dealer_value < DEALER_STAND:
                                dealer_hand.append(random.choice(suits) + random.choice(ranks))
                                dealer_value = calculate_hand_value(dealer_hand)

                            if dealer_value > BLACKJACK:
                                outcome = "Dealer busts! Player wins."
                                CHIPS += bet
                                save_game_state()
                            elif dealer_value >= player_value:
                                outcome = "Dealer wins."
                                CHIPS -= bet
                                save_game_state()
                            else:
                                outcome = "Player wins."
                                CHIPS += bet
                                save_game_state()
                            in_play = False

                        if outcome:
                            draw_text(outcome, font, TEXT_COL4, WIDTH // 2 - 100, HEIGHT // 2 - 50)
                        
                        if CHIPS <= 0:
                            draw_text('Restart for 10 more chips!', font, TEXT_COL4, WIDTH // 2 - 100, HEIGHT // 2)

                        pygame.display.flip()
                        clock.tick(30)
                    
                main()
        
        #Shop
        if game_state == 'shop':
            shop()
            if back_btn.draw(screen):
                if sound == True:
                    playClick() 
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
