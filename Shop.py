# import pygame
# import button

# #images
# exit_img = pygame.image.load("button_sprites/quit.png").convert_alpha()

# #instances
# exit_btn = button(60, 80, exit_img, 1)

#[gold, powerups, tokens]
STATS = [100, 0, 0]
#[powerup price, token price]
PRICES = [5, 10]
ITEMS = ['powerup', 'token']

shopping = True

def shop():
    while shopping:
        for i in range(len(ITEMS)):
            print(f"{i + 1}. {ITEMS[i]} - {PRICES[i]} tokens")
        item = int(input('what item would you like to get? (1. Powerup, 2. Token, 3. Quit): ' ))
        if item == 3: 
            break
        buying = item_price(item)
        Gold = STATS[0]
        Powerups = STATS[1]
        Tokens = STATS[2]
        print(f"Gold: {Gold}\nPowerups: {Powerups}\nTokens: {Tokens}")
    
    Gold = STATS[0]
    Powerups = STATS[1]
    Tokens = STATS[2]
    print(f"Gold: {Gold}\nPowerups: {Powerups}\nTokens: {Tokens}")
   
def item_price(item):
    if item == 1:
        if STATS[0] > 50:
            STATS[0] -= PRICES[0]
            STATS[1] += 1
        else: 
            print("not enough gold!")
    elif item == 2:
        if STATS[0] > 50:
            STATS[0] -= PRICES[1]
            STATS[2] += 1
        else:
            print("not enough gold!")
    else:
        print("invalid")

shop()
