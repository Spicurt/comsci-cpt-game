import pygame, random, sys
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)
card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades'] 
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'] 
deck = [(card, category) for category in card_categories for card in cards_list]
chips = 1000
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
    global high_score
    global chips
    global bet
    random.shuffle(deck) 
    dealer_card = [deck.pop(), deck.pop()]
    player_card = [deck.pop(), deck.pop()] 
    text = font.render("game_text", True, green, blue)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT// 2)
    player_score = card_value(player_card)
    dealer_score = card_value(dealer_card)
    text = font.render("Cards Player Has: " + str(player_card) + " Score Of The Player: " + str(player_score), True, green, blue)
    if player_score > 21:
        text = font.render("You have exceeded 21. Press 1 to continue", True, green, blue)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("works")
        elif player_score == 21:
            print("works")
        elif dealer_score > 21:
            text = font.render("The dealer has exceeded 21. Press 1 to continue", True, green, blue)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("works")
        else:
            text = font.render("Hit or Stand? H/S", True, green, blue) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    new_card = deck.pop() 
                    player_card.append(new_card) 
                elif event.key == pygame.K_s: 
                    print('works')
                else: 
                    game_text = "Invalid choice. Please try again."
    if player_score > 21:
        text = font.render("You have exceeded 21. Press 1 to continue", True, green, blue)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("works")
        elif player_score == 21:
            print("works")
        elif dealer_score > 21:
            text = font.render("The dealer has exceeded 21. Press 1 to continue", True, green, blue)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("works")              

    while dealer_score < 17: 
        new_card = deck.pop() 
        dealer_card.append(new_card) 
        dealer_score = card_value(dealer_card)
        pygame.display.flip()
        clock.tick(30)
    game_text ="Cards Dealer Has:", dealer_card
    game_text ="Score Of The Dealer:", dealer_score
    
    if dealer_score > 21 and player_score > 21: 
        game_text = "Cards Dealer Has:", dealer_card
        game_text = "Score Of The Dealer:", dealer_score
        game_text = "Cards Player Has:", player_card
        game_text = "Score Of The Player:", player_score
        game_text = "It's a tie."
    elif dealer_score > 21: 
        game_text = "Cards Dealer Has:", dealer_card
        game_text = "Score Of The Dealer:", dealer_score 
        game_text = "Cards Player Has:", player_card
        game_text = "Score Of The Player:", player_score
        game_text = "Player wins (Dealer Loss Because Dealer Score is exceeding 21)"
        chips += bet*2
        bet = 0
        if chips >= high_score:
            high_score = chips
    elif player_score > 21: 
        game_text = "Cards Dealer Has:", dealer_card
        game_text = "Score Of The Dealer:", dealer_score
        game_text = "Cards Player Has:", player_card 
        game_text = "Score Of The Player:", player_score 
        game_text = "Dealer wins (Player Loss Because Player Score is exceeding 21)"
        bet = 0
    elif player_score > dealer_score: 
        game_text = "Cards Dealer Has:", dealer_card
        game_text = "Score Of The Dealer:", dealer_score 
        game_text = "Cards Player Has:", player_card
        game_text = "Score Of The Player:", player_score
        game_text = "Player wins (Player Has High Score than Dealer)"
        chips += bet*2
        bet = 0 
        if chips >= high_score:
            high_score = chips
    elif dealer_score > player_score: 
        game_text = "Cards Dealer Has:", dealer_card
        game_text = "Score Of The Dealer:", dealer_score
        game_text = "Cards Player Has:", player_card
        game_text = "Score Of The Player:", player_score 
        game_text = "Dealer wins (Dealer Has High Score than Player)"
        bet = 0
    else: 
        game_text = "Cards Dealer Has:", dealer_card
        game_text = "Score Of The Dealer:", dealer_score
        game_text = "Cards Player Has:", player_card
        game_text = "Score Of The Player:", player_score
        game_text = "It's a tie."


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

#define font
font = pygame.font.SysFont("arialblack", 40)
#define color
TEXT_COL = (255, 255, 255)

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
quit_img = pygame.image.load("button_sprites/exit.png").convert_alpha()
video_img = pygame.image.load('button_sprites/video.png').convert_alpha()
audio_img = pygame.image.load('button_sprites/audio.png').convert_alpha() #red
keys_img = pygame.image.load('button_sprites/keys.png').convert_alpha() #green
back_img = pygame.image.load('button_sprites/back.png').convert_alpha() #red
pause_img = pygame.image.load("button_sprites/pause.png").convert_alpha() 
start_img = pygame.image.load('button_sprites/new.png').convert_alpha() #red
instr_img = pygame.image.load('button_sprites/instr.png').convert_alpha()
shop_img = pygame.image.load('button_sprites/shop.png').convert_alpha()

#Button instances
resume_btn = Button(60, 80, resume_img, 1)
options_btn = Button(60, 220, options_img, 1)
quit_btn = Button(60, 370, quit_img, 1)
video_btn = Button(400, 75, video_img, 1)
audio_btn = Button(400, 200, audio_img, 1)
keys_btn = Button(400, 325, keys_img, 1)
back_btn = Button(1, 1, back_img, 0.8)
pause_btn = Button(1, 1, pause_img, 0.8)
start_btn = Button(200, 45, start_img, 1)
instr_btn = Button(190, 195, instr_img, 1)
shop_btn = Button(240, 345, shop_img, 1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

# #display time for text
# display_time = 0

running = True
while running:
    text = font.render("game_text", True, green, blue)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT// 2)
    # EVENT HANDLING
    for event in pygame.event.get():
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         game_paused = True
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    #display_time += 1

    # DRAWING
    screen.fill((52, 78, 91))

    # if display_time >= 100:
    #     game_paused = True

    #if game is paused, activate menu - partly Coding With Russ partly Regulus
    if game_state == 'playing':
        if game_paused == True: #IMPORTANT
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
        else:
            display_surface.blit(text, textRect)
            game_start()
            if pause_btn.draw(screen):
                game_paused = True
    elif game_state == 'starting screen':
        screen.fill('seagreen') 

        if start_btn.draw(screen):
            game_state = 'playing'

        if instr_btn.draw(screen):
            print("Instr")
        
        if shop_btn.draw(screen):
            print("Shop")
            #menu_state = 'shop'


    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
