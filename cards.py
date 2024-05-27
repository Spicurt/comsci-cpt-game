from random import choice, randint

MASTER_DECK = ["sA", "hA", "cA", "dA",
               "s2", "h2", "c2", "d2",
               "s3", "h3", "c3", "d3",
               "s4", "h4", "c4", "d4",
               "s5", "h5", "c5", "d5",
               "s6", "h6", "c6", "d6",
               "s7", "h7", "c7", "d7",
               "s8", "h8", "c8", "d8",
               "s9", "h9", "c9", "d9",
               "s10", "h10", "c10", "d10",
               "sJ", "hJ", "cJ", "dJ",
               "sQ", "hQ", "cQ", "dQ",
               "sK", "hK", "cK", "dK"]


def setup(deck):
    """Sets up all game variables"""
    # Initialize all of the hands
    player_hand, deck = pick_cards(deck)
    dealer_hand, deck = pick_cards(deck)
    return deck, player_hand, dealer_hand


def pick_cards(deck):
    """Deals two random cards"""
    hand = []
    if len(deck) <= 6:
        deck = MASTER_DECK.copy()
    for card in range(0, 2):
        chosen_card = choice(deck)
        hand.append(chosen_card)
        deck.remove(chosen_card)
    return hand, deck


def print_ui(player_hand, dealer_hand, deck, game_state):
    """Prints out the display that tells the user there cards"""
    print()
    if game_state == "player_dealing":
        print("The dealer has these cards:\n_, " + ", ".join(dealer_hand[1:]))
        print()
        print("You have these cards:\n" + ", ".join(player_hand))
        print()
        print(f"There are {len(deck)} cards left in the deck")
    elif game_state == "dealer_dealing":
        print("The dealer has these cards:\n" + ", ".join(dealer_hand))
        print()
        print("You have these cards:\n" + ", ".join(player_hand))
        print()
        if have_won(player_hand, dealer_hand):
            print("You have beaten the dealer.")
        else:
            print("You have not beaten the dealer.")
    else:
        print("Something has gone wrong")
        while True:
            pass


def have_won(player_hand, dealer_hand):
    """Checks if the player has won"""
    numeric_player_hand = numeric_cards(player_hand.copy())
    player_hand_total = 0
    for card in numeric_player_hand:
        player_hand_total += card
    numeric_dealer_hand = numeric_cards(dealer_hand.copy())
    dealer_hand_total = 0
    for card in numeric_dealer_hand:
        dealer_hand_total += card
    if dealer_hand_total > 21:
        if player_hand_total > 21:
            return False
        return True
    if dealer_hand_total == 21:
        return False
    if dealer_hand_total < 21:
        if dealer_hand_total < player_hand_total <= 21:
            return True
        return False


def betting_phase(tokens):
    """Takes the users bet"""
    print(f"You have {tokens} tokens.")
    while True:
        try:
            bet = int(input("Please enter you bet: "))
            if int(bet) > 0:
                if (tokens - bet) >= 0:
                    break
                print("Do not bet more than you have.")
            else:
                print("Please enter a number greater than zero.")
        except ValueError:
            print("Please enter a number.")
    return tokens - bet, bet


def player_dealing(deck, player_hand, game_state):
    """Handles dealing to the player"""
    if not deck:
        print("As there are no more cards left, the round ends.")
        game_state = "dealer_dealing"
    else:
        while True:
            user_command = input("Would you like to hit or to stay? (H/S): ").lower()
            if user_command == "h":
                chosen_card = choice(deck)
                player_hand.append(chosen_card)
                deck.remove(chosen_card)
                break
            elif user_command == "s":
                game_state = "dealer_dealing"
                break
            else:
                print("Please only enter H for hit or S for stay.")
    return deck, player_hand, game_state


def dealer_dealing(deck, dealer_hand):
    """Handles dealing to the dealer"""
    while True:
        if not deck:
            break
        numeric_dealer_hand = numeric_cards(dealer_hand.copy())
        hand_total = 0
        for card in numeric_dealer_hand:
            hand_total += card
        if hand_total < 16:
            chosen_card = choice(deck)
            dealer_hand.append(chosen_card)
            deck.remove(chosen_card)
        elif hand_total == 16:
            if randint(0, 1):
                chosen_card = choice(deck)
                dealer_hand.append(chosen_card)
                deck.remove(chosen_card)
            else:
                break
        elif 11 in numeric_dealer_hand and hand_total > 21:
            for card_number, card in enumerate(numeric_dealer_hand):
                if card == 11:
                    numeric_dealer_hand[card_number] = 1
        else:
            break
    return deck, dealer_hand


def numeric_cards(hand):
    """Turns card letters into their number values"""
    for card_number, card in enumerate(hand):
        if card == "sJ" or card == "hJ" or card == "cJ" or card == "dJ"  or card == "sQ" or card == "hQ" or card == "cQ" or card == "dQ" or card == "sK" or card == "hK" or card == "cK" or card == "dK":
            hand[card_number] = 10
        elif card == "sA" or card == "hA" or card == "cA" or card == "dA":
            hand[card_number] = 11
        elif card == "s1" or card == "h1" or card == "c1" or card == "d1":
            hand[card_number] = 1
        elif card == "s2" or card == "h2" or card == "c2" or card == "d2":
            hand[card_number] = 2
        elif card == "s3" or card == "h3" or card == "c3" or card == "d3":
            hand[card_number] = 3
        elif card == "s4" or card == "h4" or card == "c4" or card == "d4":
            hand[card_number] = 4
        elif card == "s5" or card == "h5" or card == "c5" or card == "d5":
            hand[card_number] = 5
        elif card == "s6" or card == "h6" or card == "c6" or card == "d6":
            hand[card_number] = 6
        elif card == "s7" or card == "h7" or card == "c7" or card == "d7":
            hand[card_number] = 7
        elif card == "s8" or card == "h8" or card == "c8" or card == "d8":
            hand[card_number] = 8
        elif card == "s9" or card == "h9" or card == "c9" or card == "d9":
            hand[card_number] = 9
    hand_total = 0
    for card in hand:
        hand_total += card
    if hand_total > 21 and 11 in hand:
        for card_number, card in enumerate(hand):
            if card == 11:
                hand[card_number] = 1
    return hand


def play_again():
    """Allows user to play again or quit"""
    while True:
        play_again = input("Do you want to play again? (Y/N): ").lower()
        if play_again == "y":
            break
        elif play_again == "n":
            quit()
        print("Please only enter a Y or N")


deck = MASTER_DECK.copy()
tokens = 200

while True:
    game_state = "betting"
    playing_game = True

    deck, player_hand, dealer_hand = setup(deck)

    while playing_game:
        if game_state == "betting":
            tokens, bet = betting_phase(tokens)
            game_state = "player_dealing"
        else:
            print_ui(player_hand, dealer_hand, deck, game_state)
            deck, player_hand, game_state = player_dealing(deck, player_hand, game_state)
            if game_state == "dealer_dealing":
                deck, dealer_hand = dealer_dealing(deck, dealer_hand)
                if have_won(player_hand, dealer_hand):
                    tokens += 2 * bet
                print_ui(player_hand, dealer_hand, deck, game_state)
                playing_game = False
    if tokens:
        play_again()
    else:
        input("You have no more tokens to spend. Hit enter to quit.")
        quit()
