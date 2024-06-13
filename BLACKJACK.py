import pygame, random
from pygame.locals import *

pygame.init()

card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades'] 
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'] 
deck = [(card, category) for category in card_categories for card in cards_list]
CHIPS = 1000
high_score = 1000
bet = 0
white = (255, 0, 255)
green = (255, 255, 0)
blue = (0, 255, 255)
game_text = ""
X = 400
Y = 400
display_surface = pygame.display.set_mode((X, Y))

def card_value(hand):
    sum = 0
    aces = 0
    for i in hand:
        if i[0] == "Ace":
            sum += 11
            aces += 1
        elif i[0] in ["Jack", "Queen", "King"]:
            sum += 10
        else:
            sum += int(i[0])
    for num in range(aces):
        if sum > 21:
            sum -= 10
    return sum

def game_start():
    print("")

#GREEN CODE: does not work, or work on it later

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

#game variables
game_state = 'starting screen'
game_paused = False
menu_state = 'main'
game_phase = "Dealing"
#powerup 1, powerup 2
SHOP_ITEMS = [0, 0]
PRICES = [5, 10]

#define font
font = pygame.font.SysFont("arialblack", 40)
font2 = pygame.font.SysFont("arvo", 13)
#define color
TEXT_COL = (255, 255, 255)
TEXT_COL3 = ("gray0")
TEXT_COL2 = ("darkgoldenrod1")

#Text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

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
video_img = pygame.image.load('button_sprites/video.png').convert_alpha()
audio_img = pygame.image.load('button_sprites/audio.png').convert_alpha() #red
keys_img = pygame.image.load('button_sprites/keys.png').convert_alpha() #green
back_img = pygame.image.load('button_sprites/back.png').convert_alpha() #red
pause_img = pygame.image.load("button_sprites/pause.png").convert_alpha() 
start_img = pygame.image.load('button_sprites/new.png').convert_alpha() #red
instr_img = pygame.image.load('button_sprites/instr.png').convert_alpha()
shop_img = pygame.image.load('button_sprites/shop.png').convert_alpha()

#sprites
question_img = pygame.image.load("button_sprites/question_card.png").convert_alpha()

#Button instances
resume_btn = Button(200, 80, resume_img, 1)
options_btn = Button(200, 220, options_img, 1)
quit_btn = Button(200, 370, quit_img, 1)
video_btn = Button(WIDTH -300, 75, video_img, 1)
audio_btn = Button(WIDTH -300, 200, audio_img, 1)
keys_btn = Button(WIDTH -300, 325, keys_img, 1)
back_btn = Button(20, 20, back_img, 0.8)
pause_btn = Button(20, 20, pause_img, 0.8)
start_btn = Button(500, 120, start_img, 1)
instr_btn = Button(492, 300, instr_img, 1)
shop_btn = Button(535, 480, shop_img, 1)

#sprite instances
question_btn = Button(200, 200, question_img, 0.5)
pwerup_sprite = Button(1100, 500, question_img, 0.2)

# Display time for text - Chat GPT
show_error = False
error_start_time = 0
ERROR_DISPLAY_DURATION = 2000  # 2 seconds

# Display time for text 2 - Regulus
show_error2 = False
error_start_time2 = 0
ERROR_DISPLAY_DURATION2 = 2000  # 2 seconds

# Shop function - Regulus
def shop():
    screen.fill("lightblue")
    draw_text(f"{CHIPS}", font, TEXT_COL2, 1100, 40)
    draw_text("Chips:", font, TEXT_COL2, 900, 40)
    for i in range(len(SHOP_ITEMS)):
        if i == 0:
            draw_text(f"{SHOP_ITEMS[i]}", font, TEXT_COL, 1140, 600)
            pwerup_sprite.draw(screen)

        if i == 1:
            draw_text(f"{SHOP_ITEMS[i]}", font, TEXT_COL, 930, 600)
    
    if question_btn.draw(screen):
        paying1()

def paying1():
    global CHIPS, show_error, error_start_time
    if CHIPS > 50:
        CHIPS -= PRICES[0]
        SHOP_ITEMS[0] += 1
    else:
        show_error = True
        error_start_time = pygame.time.get_ticks()
        #Put this with other button
        # show_error2 = True
        # error_start_time2 = pygame.time.get_ticks()

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

    #starting screen - Regulus
    if game_state == 'starting screen':
        screen.fill('seagreen') 

        if start_btn.draw(screen):
            game_state = 'playing'

        if instr_btn.draw(screen):
            game_state = "instructions"
        
        if shop_btn.draw(screen):
            game_state = 'shop'

    #if game is paused, activate menu - Regulus
    elif game_state == 'playing': #- Regulus
        screen.fill((52, 78, 91))
        if game_paused == True: #IMPORTANT IMPORTANT TMSFDOPSP
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
                if video_btn.draw(screen):
                    print("Video Settings")
                if audio_btn.draw(screen):
                    print("Audio Settings")
                if keys_btn.draw(screen):
                    print("Change Key Bindings")
                if back_btn.draw(screen):
                    menu_state = "main"

        #if game not paused, draw pause button + other functions - Regulus PUT GAME HERE, PLAY HERE
        else: #- Regulus
            if pause_btn.draw(screen):
                game_paused = True
            random.shuffle(deck)
            pygame.event.clear()
            event = pygame.event.wait()
            if game_phase == "Dealing":
                dealer_card = [deck.pop(), deck.pop()]
                player_card = [deck.pop(), deck.pop()] 
                draw_text("Dealing Cards...", font, TEXT_COL, 400, 300)

                player_score = 0
                dealer_score = 0
                game_phase == "Interval"
            elif game_phase == "Interval":
                player_score = card_value(player_card)
                dealer_score = card_value(dealer_card)
                draw_text(f"Cards Player Has: {str(player_card)} Score Of The Player: {str(player_score)}", font, TEXT_COL, 500, 500)
                if player_score > 21:
                    draw_text("You have exceeded 21. Press 1 to continue", font, TEXT_COL, 400, 300)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            print("works")
                            game_phase == "End"
                elif player_score == 21:
                    game_phase == "End"
                elif dealer_score > 21:
                    draw_text("The dealer has exceeded 21. Press 1 to continue", font, TEXT_COL, 400, 300)

                    game_phase == "End"
            elif game_phase == "Action":
                for event in pygame.event.get():
                        if dealer_score < 17:
                            new_card = deck.pop() 
                            dealer_card.append(new_card) 
                            dealer_score = card_value(dealer_card)
                        else:
                            break
                draw_text("Hit or Stand? H/S", font, TEXT_COL, 400, 300) 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        new_card = deck.pop() 
                        player_card.append(new_card) 
                    elif event.key == pygame.K_s: 
                        print('works')
                        game_phase == "End"
                    else: 
                            draw_text("Invalid choice. Please try again.", font, TEXT_COL, 400, 300)            
            elif game_phase == "End":   
                game_text ="Cards Dealer Has:", dealer_card
                draw_text(game_text, font, TEXT_COL, 400, 300)
                game_text ="Score Of The Dealer:", dealer_score
                draw_text(game_text, font, TEXT_COL, 400, 300)
                if dealer_score > 21 and player_score > 21: 
                    game_text = "Cards Dealer Has:", dealer_card
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Score Of The Dealer:", dealer_score
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Cards Player Has:", player_card
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Score Of The Player:", player_score
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "It's a tie."
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_phase == "Interval"
                elif dealer_score > 21: 
                    game_text = "Cards Dealer Has:", dealer_card
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Score Of The Dealer:", dealer_score
                    draw_text(game_text, font, TEXT_COL, 400, 300) 
                    game_text = "Cards Player Has:", player_card
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Score Of The Player:", player_score
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    draw_text("Player wins (Dealer Loss Because Dealer Score is exceeding 21)", font, TEXT_COL, 400, 300)
                    CHIPS += bet*2
                    bet = 0
                    if CHIPS >= high_score:
                        high_score = CHIPS
                        game_phase == "Interval"
                    else:
                        game_phase == "Interval"
                elif player_score > 21: 
                    game_text = "Cards Dealer Has:", dealer_card
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Score Of The Dealer:", dealer_score
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Cards Player Has:", player_card 
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Score Of The Player:", player_score
                    draw_text(game_text, font, TEXT_COL, 400, 300) 
                    draw_text("Dealer wins (Player Loss Because Player Score is exceeding 21)", font, TEXT_COL, 400, 300)
                    bet = 0
                    game_phase == "Interval"
                elif player_score > dealer_score: 
                    game_text = "Cards Dealer Has:", dealer_card
                    draw_text(game_text, font, TEXT_COL, 400, 300) 
                    game_text = "Score Of The Dealer:", dealer_score 
                    draw_text(game_text, font, TEXT_COL, 400, 300) 
                    game_text = "Cards Player Has:", player_card
                    draw_text(game_text, font, TEXT_COL, 400, 300) 
                    game_text = "Score Of The Player:", player_score
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    draw_text("Player wins (Player Has High Score than Dealer)", font, TEXT_COL, 400, 300) 
                    CHIPS += bet*2
                    bet = 0 
                    if CHIPS >= high_score:
                        high_score = CHIPS
                        game_phase == "Interval"
                    else:
                        game_phase == "Interval"
                elif dealer_score > player_score: 
                    game_text = "Cards Dealer Has:", dealer_card
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Score Of The Dealer:", dealer_score
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Cards Player Has:", player_card
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Score Of The Player:", player_score
                    draw_text(game_text, font, TEXT_COL, 400, 300) 
                    draw_text("Dealer wins (Dealer Has High Score than Player)", font, TEXT_COL, 400, 300)
                    bet = 0
                    game_phase == "Interval"
                else: 
                    game_text = "Cards Dealer Has:", dealer_card
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Score Of The Dealer:", dealer_score
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Cards Player Has:", player_card
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    game_text = "Score Of The Player:", player_score
                    draw_text(game_text, font, TEXT_COL, 400, 300)
                    draw_text("It's a tie.", font, TEXT_COL, 400, 300)
                    game_phase == "Interval"

    if game_state == 'shop':
        shop()
        if back_btn.draw(screen):
            game_state = "starting screen"
    
    if game_state == "instructions":
        screen.fill("lightpink")
        if back_btn.draw(screen):
            game_state = "starting screen"

    #Show error - chatgpt
    if show_error:
        current_time = pygame.time.get_ticks()
        if current_time - error_start_time < ERROR_DISPLAY_DURATION:
            draw_text("Not enough CHIPS!", font, TEXT_COL, 160, 250)
        else:
            show_error = False

#Show error 2 - Regulus
    if show_error2:
        current_time2 = pygame.time.get_ticks()
        if current_time2 - error_start_time2 < ERROR_DISPLAY_DURATION2:
            draw_text("Not enough CHIPS!", font, TEXT_COL, 400, 250)
        else:
            show_error = False

    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
