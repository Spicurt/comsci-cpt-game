import random 

card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades'] 
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'] 
deck = [(card, category) for category in card_categories for card in cards_list]
chips = 1000
bet = 0

def card_value(card): 
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        if (dealer_card + 11) <= 21: 
            return 11
        else:
            return 1
    else:
        return int(card[0])

def game_start(): 
    global chips
    global bet
    random.shuffle(deck) 
    player_card = [deck.pop(), deck.pop()] 
    dealer_card = [deck.pop(), deck.pop()]
    while True: 
        player_score = sum(card_value(card) for card in player_card) 
        dealer_score = sum(card_value(card) for card in dealer_card) 
        print("Cards Player Has:", player_card) 
        print("Score Of The Player:", player_score) 
        print("\n") 
        choice = input('Hit or stand (H/S): ').lower() 
        if choice == "h": 
            new_card = deck.pop() 
            player_card.append(new_card) 
        elif choice == "s": 
            break
        else: 
            print("Invalid choice. Please try again.") 
            continue

    while dealer_score < 17: 
        new_card = deck.pop() 
        dealer_card.append(new_card) 
        dealer_score += card_value(new_card) 

    print("Cards Dealer Has:", dealer_card) 
    print("Score Of The Dealer:", dealer_score) 
    print("\n") 
    
    if dealer_score > 21: 
        print("Cards Dealer Has:", dealer_card) 
        print("Score Of The Dealer:", dealer_score) 
        print("Cards Player Has:", player_card) 
        print("Score Of The Player:", player_score) 
        print("Player wins (Dealer Loss Because Dealer Score is exceeding 21)")
        chips += bet*2 
        bet = 0
    elif player_score > 21: 
        print("Cards Dealer Has:", dealer_card) 
        print("Score Of The Dealer:", dealer_score) 
        print("Cards Player Has:", player_card) 
        print("Score Of The Player:", player_score) 
        print("Dealer wins (Player Loss Because Player Score is exceeding 21)") 
    elif player_score > dealer_score: 
        print("Cards Dealer Has:", dealer_card) 
        print("Score Of The Dealer:", dealer_score) 
        print("Cards Player Has:", player_card) 
        print("Score Of The Player:", player_score) 
        print("Player wins (Player Has High Score than Dealer)")
        chips += bet*2 
        bet = 0 
    elif dealer_score > player_score: 
        print("Cards Dealer Has:", dealer_card) 
        print("Score Of The Dealer:", dealer_score) 
        print("Cards Player Has:", player_card) 
        print("Score Of The Player:", player_score) 
        print("Dealer wins (Dealer Has High Score than Player)")
        bet = 0
    else: 
        print("Cards Dealer Has:", dealer_card) 
        print("Score Of The Dealer:", dealer_score) 
        print("Cards Player Has:", player_card) 
        print("Score Of The Player:", player_score) 
        print("It's a tie.")

while True:
    play = input("Do you want to play Blackjack? Y/N")
    if play == "y" or play == "Y":
        print("You have " + str(chips) + " chips in total")
        bet = int(input("Enter your bet amount: "))
        if bet <= chips: 
            game_start()
        else:
            print("You don't have enough chips.")
    elif play == "n" or play == "N":
         print("Okay, bye!")
         break
    else:
         print("That's not an option!")
