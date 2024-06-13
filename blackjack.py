import random
import os
import sys
import pygame
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 480))
clock = pygame.time.Clock()

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
        
def soundLoad(name):    
    fullName = os.path.join('sounds', name)
    try: sound = pygame.mixer.Sound(fullName)
    except pygame.error as message:
        print('Cannot load sound:'), name
        raise SystemExit and message
    return sound

def display(font, sentence):
    
    displayFont = pygame.font.Font.render(font, sentence, 1, (255,255,255), (0,0,0)) 
    return displayFont

def playClick():
    clickSound = soundLoad("click2.wav")
    clickSound.play()

#Main game functions
def mainGame():
    
    def gameOver():

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
        
    def blackJack(deck, deadDeck, playerHand, dealerHand, funds, bet, cards, cardSprite):

        textFont = pygame.font.Font(None, 28)

        playerValue = checkValue(playerHand)
        dealerValue = checkValue(dealerHand)
        
        if playerValue == 21 and dealerValue == 21:
            displayFont = display(textFont, "Blackjack! The dealer also has blackjack, so it's a push!")
            deck, playerHand, dealerHand, deadDeck, funds, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, funds, 0, bet, cards, cardSprite)
                
        elif playerValue == 21 and dealerValue != 21:
            # Dealer loses
            displayFont = display(textFont, "Blackjack! You won $%.2f." %(bet*1.5))
            deck, playerHand, dealerHand, deadDeck, funds, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, funds, bet, 0, cards, cardSprite)
            
        elif dealerValue == 21 and playerValue != 21:
            # Player loses, money is lost, and new hand will be dealt
            deck, playerHand, dealerHand, deadDeck, funds, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, funds, 0, bet, cards, cardSprite)
            displayFont = display(textFont, "Dealer has blackjack! You lose $%.2f." %(bet))
            
        return displayFont, playerHand, dealerHand, deadDeck, funds, roundEnd

    def bust(deck, playerHand, dealerHand, deadDeck, funds, moneyGained, moneyLost, cards, cardSprite):
        
        font = pygame.font.Font(None, 28)
        displayFont = display(font, "You bust! You lost $%.2f." %(moneyLost))
        
        deck, playerHand, dealerHand, deadDeck, funds, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, funds, moneyGained, moneyLost, cards, cardSprite)
        
        return deck, playerHand, dealerHand, deadDeck, funds, roundEnd, displayFont

    def endRound(deck, playerHand, dealerHand, deadDeck, funds, moneyGained, moneyLost, cards, cardSprite):
    
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

        funds += moneyGained
        funds -= moneyLost
        
        textFont = pygame.font.Font(None, 28)
        
        if funds <= 0:
            gameOver()  
        
        roundEnd = 1

        return deck, playerHand, dealerHand, deadDeck, funds, roundEnd 
        
    def compareHands(deck, deadDeck, playerHand, dealerHand, funds, bet, cards, cardSprite):
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
            deck, playerHand, dealerHand, deadDeck, funds, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, funds, bet, 0, cards, cardSprite)
            displayFont = display(textFont, "You won $%.2f." %(bet))
        elif playerValue == dealerValue and playerValue <= 21:
            deck, playerHand, dealerHand, deadDeck, funds, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, funds, 0, 0, cards, cardSprite)
            displayFont = display(textFont, "It's a push!")
        elif dealerValue > 21 and playerValue <= 21:
            deck, playerHand, dealerHand, deadDeck, funds, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, funds, bet, 0, cards, cardSprite)
            displayFont = display(textFont, "Dealer busts! You won $%.2f." %(bet))
        else:
            deck, playerHand, dealerHand, deadDeck, funds, roundEnd = endRound(deck, playerHand, dealerHand, deadDeck, funds, 0, bet, cards, cardSprite)
            displayFont = display(textFont, "Dealer wins! You lost $%.2f." %(bet))
            
        return deck, deadDeck, roundEnd, funds, displayFont

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
                    playClick()
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
            
        def update(self, mX, mY, deck, deadDeck, playerHand, dealerHand, cards, pCardPos, roundEnd, cardSprite, funds, bet, displayFont):            
            if roundEnd == 0: self.image, self.rect = imageLoad("stand.png", 0)
            else: self.image, self.rect = imageLoad("stand-grey.png", 0)
            
            self.position = (735, 365)
            self.rect.center = self.position
            
            if self.rect.collidepoint(mX, mY) == 1:
                if roundEnd == 0: 
                    playClick()
                    deck, deadDeck, roundEnd, funds, displayFont = compareHands(deck, deadDeck, playerHand, dealerHand, funds, bet, cards, cardSprite)
                
            return deck, deadDeck, roundEnd, funds, playerHand, deadDeck, pCardPos, displayFont 
            
    class doubleButton(pygame.sprite.Sprite):
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("double-grey.png", 0)
            self.position = (735, 330)
            
        def update(self, mX, mY,   deck, deadDeck, playerHand, dealerHand, playerCards, cards, pCardPos, roundEnd, cardSprite, funds, bet, displayFont):            
            if roundEnd == 0 and funds >= bet * 2 and len(playerHand) == 2: self.image, self.rect = imageLoad("double.png", 0)
            else: self.image, self.rect = imageLoad("double-grey.png", 0)
                
            self.position = (735, 330)
            self.rect.center = self.position
                
            if self.rect.collidepoint(mX, mY) == 1:
                if roundEnd == 0 and funds >= bet * 2 and len(playerHand) == 2: 
                    bet = bet * 2
                    
                    playClick()
                    deck, deadDeck, playerHand = hit(deck, deadDeck, playerHand)

                    currentCard = len(playerHand) - 1
                    card = cardSprite(playerHand[currentCard], pCardPos)
                    playerCards.add(card)
                    pCardPos = (pCardPos[0] - 80, pCardPos[1])
        
                    deck, deadDeck, roundEnd, funds, displayFont = compareHands(deck, deadDeck, playerHand, dealerHand, funds, bet, cards, cardSprite)
                    
                    bet = bet / 2

            return deck, deadDeck, roundEnd, funds, playerHand, deadDeck, pCardPos, displayFont, bet

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
                    playClick()
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
            
        def update(self, mX, mY, bet, funds, click, roundEnd):
            if roundEnd == 1: self.image, self.rect = imageLoad("up.png", 0)
            else: self.image, self.rect = imageLoad("up-grey.png", 0)
            
            self.position = (710, 255)
            self.rect.center = self.position
            
            if self.rect.collidepoint(mX, mY) == 1 and click == 1 and roundEnd == 1:
                playClick()
                    
                if bet < funds:
                    bet += 5.0                
                    if bet % 5 != 0:
                        while bet % 5 != 0:
                            bet -= 1

                click = 0
            
            return bet, click
            
    class betButtonDown(pygame.sprite.Sprite):
        
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
                playClick()
                if bet > 5:
                    bet -= 5.0
                    if bet % 5 != 0:
                        while bet % 5 != 0:
                            bet += 1
                    
                click = 0
            
            return bet, click
         
    #Initializing
    textFont = pygame.font.Font(None, 28)

    background, backgroundRect = imageLoad("bjs.png", 0)
    
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

    funds = 100.00
    bet = 10.00
    handsPlayed = 0    
    firstTime = 1
    roundEnd = 1
    while 1:
    
        screen.blit(background, backgroundRect)
        
        if bet > funds:
            bet = funds
        
        if roundEnd == 1 and firstTime == 1:
            displayFont = display(textFont, "Click on the arrows to declare your bet, then deal to start the game.")
            firstTime = 0
            
        screen.blit(displayFont, (10,444))
        fundsFont = pygame.font.Font.render(textFont, "Funds: $%.2f" %(funds), 1, (255,255,255), (0,0,0))
        screen.blit(fundsFont, (663,205))
        betFont = pygame.font.Font.render(textFont, "Bet: $%.2f" %(bet), 1, (255,255,255), (0,0,0))
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
                displayFont, playerHand, dealerHand, deadDeck, funds, roundEnd = blackJack(deck, deadDeck, playerHand, dealerHand, funds,  bet, cards, cardSprite)
                
            if dealerValue == 21 and len(dealerHand) == 2:
                displayFont, playerHand, dealerHand, deadDeck, funds, roundEnd = blackJack(deck, deadDeck, playerHand, dealerHand, funds,  bet, cards, cardSprite)

            if playerValue > 21:
                deck, playerHand, dealerHand, deadDeck, funds, roundEnd, displayFont = bust(deck, playerHand, dealerHand, deadDeck, funds, 0, bet, cards, cardSprite)
         
        deck, deadDeck, playerHand, dealerHand, dCardPos, pCardPos, roundEnd, displayFont, click, handsPlayed = dealButton.update(mX, mY, deck, deadDeck, roundEnd, cardSprite, cards, playerHand, dealerHand, dCardPos, pCardPos, displayFont, playerCards, click, handsPlayed)   
        deck, deadDeck, playerHand, pCardPos, click = hitButton.update(mX, mY, deck, deadDeck, playerHand, playerCards, pCardPos, roundEnd, cardSprite, click)
        deck, deadDeck, roundEnd, funds, playerHand, deadDeck, pCardPos,  displayFont  = standButton.update(mX, mY,   deck, deadDeck, playerHand, dealerHand, cards, pCardPos, roundEnd, cardSprite, funds, bet, displayFont)
        deck, deadDeck, roundEnd, funds, playerHand, deadDeck, pCardPos, displayFont, bet  = doubleButton.update(mX, mY,   deck, deadDeck, playerHand, dealerHand, playerCards, cards, pCardPos, roundEnd, cardSprite, funds, bet, displayFont)
        bet, click = bbU.update(mX, mY, bet, funds, click, roundEnd)
        bet, click = bbD.update(mX, mY, bet, click, roundEnd)
        buttons.draw(screen)
         
        if len(cards) != 0:
            playerCards.update()
            playerCards.draw(screen)
            cards.update()
            cards.draw(screen)

        pygame.display.flip()

#Main game:
if __name__ == "__main__":
    mainGame()
