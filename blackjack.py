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

#System functions (music, images, animations)
def imageLoad(name, card):

    if card == 1:
        fullname = os.path.join("images/cards/", name)
    else: 
        fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit and message
    image = image.convert()
    
    return image, image.get_rect()
        
# def soundLoad(name):    
#     fullName = os.path.join('sounds', name)
#     try: sound = pygame.mixer.Sound(fullName)
#     except pygame.error as message:
#         print('Cannot load sound:'), name
#         raise SystemExit and message
#     return sound

def display(font, sentence):
    
    displayFont = pygame.font.Font.render(font, sentence, 1, (255,255,255), (0,0,0)) 
    return displayFont

# def playClick():
#     clickSound = soundLoad("click2.wav")
#     clickSound.play()

#Main game functions
def mainGame():

    global background, game_paused
    WIDTH = 800
    HEIGHT = 480
    SIZE = (WIDTH, HEIGHT)

    screen = pygame.display.set_mode(SIZE)
    global CHIPS, game_paused, game_state
    def gameOver():
        global CHIPS, game_paused, game_state
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()

            screen.fill((0,0,0))
            
            oFont = pygame.font.Font(None, 50)
            displayFont = pygame.font.Font.render(oFont, "Game over! You're outta cash!", 1, (255,255,255), (0,0,0)) 
            screen.blit(displayFont, (125, 220))
            
            pygame.display.flip()
            
    #Deck functions (Hit, stand, winning, losing, regulus is cruisin)
    def shuffle(deck):

        n = len(deck) - 1
        while n > 0:
            k = random.randint(0, n)
            deck[k], deck[n] = deck[n], deck[k]
            n -= 1

        return deck        
                        
    def createDeck():
        deck = ['sj', 'sq', 'sk', 'sa', 'hj', 'hq', 'hk', 'ha', 'cj', 'cq', 'ck', 'ca', 'dj', 'dq', 'dk', 'da']
        values = range(2,11)
        for x in values:
            spades = "s" + str(x)
            hearts = "h" + str(x)
            clubs = "c" + str(x)
            diamonds = "d" + str(x)
            deck.append(spades)
            deck.append(hearts)
            deck.append(clubs)
            deck.append(diamonds)
        return deck

    def returnFromDead(deck, deadDeck):

        for card in deadDeck:
            deck.append(card)
        del deadDeck[:]
        deck = shuffle(deck)

        return deck, deadDeck
        
    def deckDeal(deck, deadDeck):

        deck = shuffle(deck)
        dealerHand, playerHand = [], []

        cardsToDeal = 4

        while cardsToDeal > 0:
            if len(deck) == 0:  
                deck, deadDeck = returnFromDead(deck, deadDeck)

            if cardsToDeal % 2 == 0: playerHand.append(deck[0])
            else: dealerHand.append(deck[0])
            
            del deck[0]
            cardsToDeal -= 1
            
        return deck, deadDeck, playerHand, dealerHand

    def hit(deck, deadDeck, hand):

        if len(deck) == 0:
            deck, deadDeck = returnFromDead(deck, deadDeck)

        hand.append(deck[0])
        del deck[0]

        return deck, deadDeck, hand

    def checkValue(hand):

        totalValue = 0

        for card in hand:
            value = card[1:]

            if value == 'j' or value == 'q' or value == 'k': value = 10
            elif value == 'a': value = 11
            else: value = int(value)

            totalValue += value
            

        if totalValue > 21:
            for card in hand:
                if card[1] == 'a': totalValue -= 10
                if totalValue <= 21:
                    break
                else:
                    continue

        return totalValue
        
    def blackJack(deck, deadDeck, playerHand, dealerHand, CHIPS, bet, cards, cardSprite):

        textFont = pygame.font.Font(None, 28)

        playerValue = checkValue(playerHand)
        dealerValue = checkValue(dealerHand)
        
        if playerValue == 21 and dealerValue == 21:
            displayFont = display(textFont, "Blackjack! The dealer also has blackjack, so it's a push!")
            deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, CHIPS, 0, bet, cards, cardSprite)
                
        elif playerValue == 21 and dealerValue != 21:
            # Dealer loses
            displayFont = display(textFont, "Blackjack! You won $%.2f." %(bet*1.5))
            deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, CHIPS, bet, 0, cards, cardSprite)
            
        elif dealerValue == 21 and playerValue != 21:
            # Player loses, money is lost, and new hand will be dealt
            deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, CHIPS, 0, bet, cards, cardSprite)
            displayFont = display(textFont, "Dealer has blackjack! You lose $%.2f." %(bet))
            
        return displayFont, playerHand, dealerHand, deadDeck, CHIPS, roundEnd

    def bust(deck, playerHand, dealerHand, deadDeck, CHIPS, moneyGained, moneyLost, cards, cardSprite):
        
        font = pygame.font.Font(None, 28)
        displayFont = display(font, "You bust! You lost $%.2f." %(moneyLost))
        
        deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, CHIPS, moneyGained, moneyLost, cards, cardSprite)
        
        return deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd, displayFont

    def endRound(deck, playerHand, dealerHand, deadDeck, CHIPS, moneyGained, moneyLost, cards, cardSprite):
    
        if len(playerHand) == 2 and "a" in playerHand[0] or "a" in playerHand[1]:
            moneyGained += (moneyGained/2.0)
            
        cards.empty()
        
        dCardPos = (50, 70)
                   
        for x in dealerHand:
            card = cardSprite(x, dCardPos)
            dCardPos = (dCardPos[0] + 80, dCardPos [1])
            cards.add(card)

        for card in playerHand:
            deadDeck.append(card)
        for card in dealerHand:
            deadDeck.append(card)

        del playerHand[:]
        del dealerHand[:]

        CHIPS += moneyGained
        CHIPS -= moneyLost
        
        textFont = pygame.font.Font(None, 28)
        
        if CHIPS <= 0:
            gameOver()  
        
        roundEnd = 1

        return deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd 
        
    def compareHands(deck, deadDeck, playerHand, dealerHand, CHIPS, bet, cards, cardSprite):
        textFont = pygame.font.Font(None, 28)
        moneyGained = 0
        moneyLost = 0

        dealerValue = checkValue(dealerHand)
        playerValue = checkValue(playerHand)
            
        while 1:
            if dealerValue < 17:
                deck, deadDeck, dealerHand = hit(deck, deadDeck, dealerHand)
                dealerValue = checkValue(dealerHand)
            else:   
                break
            
        if playerValue > dealerValue and playerValue <= 21:
            moneyGained = bet
            deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, CHIPS, bet, 0, cards, cardSprite)
            displayFont = display(textFont, "You won $%.2f." %(bet))
        elif playerValue == dealerValue and playerValue <= 21:
            deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, CHIPS, 0, 0, cards, cardSprite)
            displayFont = display(textFont, "It's a push!")
        elif dealerValue > 21 and playerValue <= 21:
            deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, CHIPS, bet, 0, cards, cardSprite)
            displayFont = display(textFont, "Dealer busts! You won $%.2f." %(bet))
        else:
            deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, CHIPS, 0, bet, cards, cardSprite)
            displayFont = display(textFont, "Dealer wins! You lost $%.2f." %(bet))
            
        return deck, deadDeck, roundEnd, CHIPS, displayFont

    #Sprite maker baker candy taker
    class cardSprite(pygame.sprite.Sprite):
        
        def __init__(self, card, position):
            pygame.sprite.Sprite.__init__(self)
            cardImage = card + ".png"
            self.image, self.rect = imageLoad(cardImage, 1)
            self.position = position
        def update(self):
            self.rect.center = self.position
            
    class hitButton(pygame.sprite.Sprite):        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("hit-grey.png", 0)
            self.position = (735, 400)
            
        def update(self, mX, mY, deck, deadDeck, playerHand, cards, pCardPos, roundEnd, cardSprite, click):
            
            if roundEnd == 0: self.image, self.rect = imageLoad("hit.png", 0)
            else: self.image, self.rect = imageLoad("hit-grey.png", 0)
            
            self.position = (735, 400)
            self.rect.center = self.position
            
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                if roundEnd == 0: 
                    # playClick()
                    deck, deadDeck, playerHand = hit(deck, deadDeck, playerHand)

                    currentCard = len(playerHand) - 1
                    card = cardSprite(playerHand[currentCard], pCardPos)
                    cards.add(card)
                    pCardPos = (pCardPos[0] - 80, pCardPos[1])
                
                    click = 0
                
            return deck, deadDeck, playerHand, pCardPos, click
            
    class standButton(pygame.sprite.Sprite):
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("stand-grey.png", 0)
            self.position = (735, 365)
            
        def update(self, mX, mY, deck, deadDeck, playerHand, dealerHand, cards, pCardPos, roundEnd, cardSprite, CHIPS, bet, displayFont):            
            if roundEnd == 0: self.image, self.rect = imageLoad("stand.png", 0)
            else: self.image, self.rect = imageLoad("stand-grey.png", 0)
            
            self.position = (735, 365)
            self.rect.center = self.position
            
            if self.rect.collidepoint(mX, mY) == 1:
                if roundEnd == 0: 
                    # playClick()
                    deck, deadDeck, roundEnd, CHIPS, displayFont = compareHands(deck, deadDeck, playerHand, dealerHand, CHIPS, bet, cards, cardSprite)
                
            return deck, deadDeck, roundEnd, CHIPS, playerHand, deadDeck, pCardPos, displayFont 

    class doubleButton(pygame.sprite.Sprite):
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("double-grey.png", 0)
            self.position = (735, 330)
            
        def update(self, mX, mY,   deck, deadDeck, playerHand, dealerHand, playerCards, cards, pCardPos, roundEnd, cardSprite, CHIPS, bet, displayFont):            
            if roundEnd == 0 and CHIPS >= bet * 2 and len(playerHand) == 2: self.image, self.rect = imageLoad("double.png", 0)
            else: self.image, self.rect = imageLoad("double-grey.png", 0)
                
            self.position = (735, 330)
            self.rect.center = self.position
                
            if self.rect.collidepoint(mX, mY) == 1:
                if roundEnd == 0 and CHIPS >= bet * 2 and len(playerHand) == 2: 
                    bet = bet * 2
                    
                    # playClick()
                    deck, deadDeck, playerHand = hit(deck, deadDeck, playerHand)

                    currentCard = len(playerHand) - 1
                    card = cardSprite(playerHand[currentCard], pCardPos)
                    playerCards.add(card)
                    pCardPos = (pCardPos[0] - 80, pCardPos[1])
        
                    deck, deadDeck, roundEnd, CHIPS, displayFont = compareHands(deck, deadDeck, playerHand, dealerHand, CHIPS, bet, cards, cardSprite)
                    
                    bet = bet / 2

            return deck, deadDeck, roundEnd, CHIPS, playerHand, deadDeck, pCardPos, displayFont, bet

    class dealButton(pygame.sprite.Sprite):
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("deal.png", 0)
            self.position = (735, 450)

        def update(self, mX, mY, deck, deadDeck, roundEnd, cardSprite, cards, playerHand, dealerHand, dCardPos, pCardPos, displayFont, playerCards, click, handsPlayed):
        
            textFont = pygame.font.Font(None, 28)
            
            if roundEnd == 1: self.image, self.rect = imageLoad("deal.png", 0)
            else: self.image, self.rect = imageLoad("deal-grey.png", 0)
            
            self.position = (735, 450)
            self.rect.center = self.position
            
                
            if self.rect.collidepoint(mX, mY) == 1:
                if roundEnd == 1 and click == 1:
                    # playClick()
                    displayFont = display(textFont, "")
                    
                    cards.empty()
                    playerCards.empty()
                    
                    deck, deadDeck, playerHand, dealerHand = deckDeal(deck, deadDeck)

                    dCardPos = (50, 70)
                    pCardPos = (540,370)

                    for x in playerHand:
                        card = cardSprite(x, pCardPos)
                        pCardPos = (pCardPos[0] - 80, pCardPos [1])
                        playerCards.add(card)
                    
                    faceDownCard = cardSprite("back", dCardPos)
                    dCardPos = (dCardPos[0] + 80, dCardPos[1])
                    cards.add(faceDownCard)

                    card = cardSprite(dealerHand [0], dCardPos)
                    cards.add(card)
                    roundEnd = 0
                    click = 0
                    handsPlayed += 1
                    
            return deck, deadDeck, playerHand, dealerHand, dCardPos, pCardPos, roundEnd, displayFont, click, handsPlayed
            
            
    class betButtonUp(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("up.png", 0)
            self.position = (710, 255)
            
        def update(self, mX, mY, bet, CHIPS, click, roundEnd):
            if roundEnd == 1: self.image, self.rect = imageLoad("up.png", 0)
            else: self.image, self.rect = imageLoad("up-grey.png", 0)
            
            self.position = (710, 255)
            self.rect.center = self.position
            
            if self.rect.collidepoint(mX, mY) == 1 and click == 1 and roundEnd == 1:
                # playClick()
                if bet < CHIPS:
                    bet += 5.0                
                    if bet % 5 != 0:
                        while bet % 5 != 0:
                            bet -= 1

                click = 0
            
            return bet, click
            
    class betButtonDown(pygame.sprite.Sprite):
        global background
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("down.png", 0)
            self.position = (710, 255)
            
        def update(self, mX, mY, bet, click, roundEnd):  
            if roundEnd == 1: self.image, self.rect = imageLoad("down.png", 0)
            else: self.image, self.rect = imageLoad("down-grey.png", 0)
        
            self.position = (760, 255)
            self.rect.center = self.position
            
            if self.rect.collidepoint(mX, mY) == 1 and click == 1 and roundEnd == 1:
                # playClick()
                if bet > 5:
                    bet -= 5.0
                    if bet % 5 != 0:
                        while bet % 5 != 0:
                            bet += 1
                    
                click = 0
            
            return bet, click
         
    #Initializing
    textFont = pygame.font.Font(None, 28)

    background, backgroundRect = imageLoad(f"{background}", 0)
    
    cards = pygame.sprite.Group()
    playerCards = pygame.sprite.Group()
    
    cards = pygame.sprite.Group()
    playerCards = pygame.sprite.Group()

    bbU = betButtonUp()
    bbD = betButtonDown()
    standButton = standButton()
    dealButton = dealButton()
    hitButton = hitButton()
    doubleButton = doubleButton()
    
    buttons = pygame.sprite.Group(bbU, bbD, hitButton, standButton, dealButton, doubleButton)

    deck = createDeck()
    deadDeck = []

    playerHand, dealerHand, dCardPos, pCardPos = [],[],(),()
    mX, mY = 0, 0
    click = 0

    bet = 10
    handsPlayed = 0    
    firstTime = 1
    roundEnd = 1
    while 1:
    
        screen.blit(background, backgroundRect)
        
        if bet > CHIPS:
            bet = CHIPS
        
        if roundEnd == 1 and firstTime == 1:
            displayFont = display(textFont, "Click on the arrows to declare your bet, then deal to start the game.")
            firstTime = 0
            
        screen.blit(displayFont, (10,444))
        CHIPSFont = pygame.font.Font.render(textFont, "chips: %.2f" %(CHIPS), 1, (255,255,255), (0,0,0))
        screen.blit(CHIPSFont, (663,205))
        betFont = pygame.font.Font.render(textFont, "Bet: %.2f" %(bet), 1, (255,255,255), (0,0,0))
        screen.blit(betFont, (680,285))
        hpFont = pygame.font.Font.render(textFont, "Round: %i " %(handsPlayed), 1, (255,255,255), (0,0,0))
        screen.blit(hpFont, (663, 180))

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mX, mY = pygame.mouse.get_pos()
                    click = 1
            elif event.type == MOUSEBUTTONUP:
                mX, mY = 0, 0
                click = 0
            
        if roundEnd == 0:
            playerValue = checkValue(playerHand)
            dealerValue = checkValue(dealerHand)
    
            if playerValue == 21 and len(playerHand) == 2:
                displayFont, playerHand, dealerHand, deadDeck, CHIPS, roundEnd = blackJack(deck, deadDeck, playerHand, dealerHand, CHIPS,  bet, cards, cardSprite)
                
            if dealerValue == 21 and len(dealerHand) == 2:
                displayFont, playerHand, dealerHand, deadDeck, CHIPS, roundEnd = blackJack(deck, deadDeck, playerHand, dealerHand, CHIPS,  bet, cards, cardSprite)

            if playerValue > 21:
                deck, playerHand, dealerHand, deadDeck, CHIPS, roundEnd, displayFont = bust(deck, playerHand, dealerHand, deadDeck, CHIPS, 0, bet, cards, cardSprite)
         
        deck, deadDeck, playerHand, dealerHand, dCardPos, pCardPos, roundEnd, displayFont, click, handsPlayed = dealButton.update(mX, mY, deck, deadDeck, roundEnd, cardSprite, cards, playerHand, dealerHand, dCardPos, pCardPos, displayFont, playerCards, click, handsPlayed)   
        deck, deadDeck, playerHand, pCardPos, click = hitButton.update(mX, mY, deck, deadDeck, playerHand, playerCards, pCardPos, roundEnd, cardSprite, click)
        deck, deadDeck, roundEnd, CHIPS, playerHand, deadDeck, pCardPos,  displayFont  = standButton.update(mX, mY,   deck, deadDeck, playerHand, dealerHand, cards, pCardPos, roundEnd, cardSprite, CHIPS, bet, displayFont)
        deck, deadDeck, roundEnd, CHIPS, playerHand, deadDeck, pCardPos, displayFont, bet  = doubleButton.update(mX, mY,   deck, deadDeck, playerHand, dealerHand, playerCards, cards, pCardPos, roundEnd, cardSprite, CHIPS, bet, displayFont)
        bet, click = bbU.update(mX, mY, bet, CHIPS, click, roundEnd)
        bet, click = bbD.update(mX, mY, bet, click, roundEnd)
        buttons.draw(screen)
         
        if len(cards) != 0:
            playerCards.update()
            playerCards.draw(screen)
            cards.update()
            cards.draw(screen)
        
        pygame.display.flip()
    pygame.display.flip()


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
