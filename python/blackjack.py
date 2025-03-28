"""Blackjack"""

from random import shuffle

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:

    def __init__(self, suit, rank):
        
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def val(self):
        """Returns the value of the card"""
        value = self.value
        return value
    

class Deck:
    
    def __init__(self):
        
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        """Shuffles the deck"""

        print("\nShuffling Deck")
        shuffle(self.all_cards)

    def deal_one(self):
        """Deals one card from the deck and reshuffles if the deck is empty"""

        if len(self.all_cards) == 0: 
            print("Deck is empty")
            print("Reshuffling")
            self.__init__()
        return self.all_cards.pop(-1)



class Player:

    def __init__(self, balance):   
        self.balance = balance

    def add_balance(self, amount):
        self.balance += amount

    def remove_balance(self, amount):
        self.balance -= amount


def print_rules():
    print("""
    Simplified Blackjack Rules
    --------------------------
    1. The game is played with a standard 52-card deck.
    2. Players place a bet before receiving their cards.
    3. Each player is dealt two cards, and the dealer gets two cards (one face up, one face down).
    4. The goal is to get as close to 21 as possible without exceeding it.
    5. Card values:
       - Number cards (2-10) are worth their face value.
       - Face cards (J, Q, K) are worth 10 points.
       - Aces (A) can be worth 1 or 11, whichever benefits the player.
    6. Players can choose to:
       - 'Hit' to receive another card.
       - 'Stay' to keep their current hand.
    7. If a player's total exceeds 21, they "bust" and lose the bet.
    8. The dealer must hit if their hand is 16 or less and stay if it is 17 or more.
    9. If neither the player nor the dealer busts, the higher hand wins.
   10. If both the player and dealer have the same total, it's a push (tie), and the bet is returned.
    
   GOAL : Reach 3000 before the game ends.""")



def place_bet(balance):
    """User Input - Returns bet amount"""

    while True:
        try:
            bet = int(input("Place your bet : "))
            if bet > balance:
                print("Out of balance")
            elif bet < 25:
                print("Invalid bet : bet must be at least 25")
            else:
                print("")
                return bet
        except ValueError:
            print("Sorry! Invalid input")

def p_decision():
    """User Input - Returns 1 for hit and 0 for stay"""
    
    while True:
        decision = input("Hit or Stay : ")
        if decision not in ["Hit", "hit", "h", "Stay", "stay", "s"]:
            print("Sorry! Invalid input")
        else:
            if decision in ["Hit", "hit", "h"]:
                return 1
            if decision in ["Stay", "stay", "s"]:
                return 0
            
def replay():
    """User Input for replaying - Returns True for yes and False for no"""
    
    while True:
        decision = input("Do you want to continue playing? (Y/N) : ")
        if decision not in ["Yes", "yes", "Y", "y", "No", "no", "N", "n"]:
            print("Sorry! Invalid input")
        else:
            if decision in ["Yes", "yes", "Y", "y"]:
                return True
            if decision in ["No", "no", "N", "n"]:
                return False
            

def show_p_hand(p_hand):
    """Prints the player's hand"""

    print("\nYour Cards")
    print("--------------------")
    for card in p_hand:
        print(card)
    print(f"Cards value : {card_sum(p_hand)}")
    print("\n")

def show_dealer_hand(dealer_hand):
    """Prints the dealer's hand without the first card"""

    print("\nDealer Cards")
    print("----------------------")
    print("*******")     # First card is hidden
    for i in range( (len(dealer_hand))-1 ):
        print(f"{dealer_hand[i+1]} -- {dealer_hand[i+1].val()}")     # Prints only the second card
    print("\n")

def show_dealer_full_hand(dealer_hand):
    """Prints the dealer's hand"""

    print("\nDealer All Cards")
    print("--------------------")
    for card in dealer_hand:
        print(card)
    print(f"Cards value : {card_sum(dealer_hand)}")
    print("\n")


def card_sum(cards):
    """Returns the sum of the cards in the hand (including aces)"""

    total = 0
    aces = 0
    for card in cards:
        if card.rank == "Ace":
            aces += 1
        total += card.val()
    while total > 21 and aces > 0:
        total -= 10 # Convert Ace from 11 to 1
        aces -= 1
    return total

def blackjack(cards):
    """Returns True if the hand is a blackjack"""

    if card_sum(cards) == 21:
        return True
    else:
        return False

def tie(cards_1, cards_2):
    """Returns True if it's a tie"""

    if card_sum(cards_1) == card_sum(cards_2):
        return True
    else:
        return False
    
def bust(cards):
    """Returns True if the hand is bust"""

    if card_sum(cards) > 21:
        return True
    else:
        return False
    
    
def player_close_to_21(p_hand, dealer_hand):
    """Returns True if the player is close to 21"""

    if card_sum(p_hand) > card_sum(dealer_hand):
        return True
    else:
        return False
    

def init_check(p, p_hand, dealer_hand, bet):
    """Returns True if the player has won initially or ties"""
    
    if blackjack(p_hand):
        if tie(p_hand, dealer_hand):
            print("BLACKJACK! It's a push - bet returned")
            p.add_balance(bet)
            return True
        print(f"BLACKJACK! You win {1.5 * bet}")
        p.add_balance((bet + (bet * 1.5)))
        return True
    else:
        return False

def hit_stay(p_hand,deck):
    """Hit or Stay"""

    while True:
        decision = p_decision()
        if decision == 1:  # Hit
            p_hand.append(deck.deal_one())
            print(f"Your draw : {p_hand[-1]}")
            print(f"Cards value : {card_sum(p_hand)}")
            if blackjack(p_hand):
                break
            elif bust(p_hand):
                break
            else:
                continue
        else:
            break

def dealer_hit_stay(dealer_hand,deck):
    """Dealer - Hit or Stay"""

    while True:
        if card_sum(dealer_hand) < 17: # Hit if hand is less than 17
            dealer_hand.append(deck.deal_one())
            print(f"Dealer draws : {dealer_hand[-1]}, Cards value : {card_sum(dealer_hand)}\n")
            if bust(dealer_hand):
                break
            else:
                continue
        else: # Stay if hand is 17 or more
            break






def main():

    print_rules()

    deck = Deck()
    deck.shuffle()
    init_balance = 1000
    p = Player(init_balance)


    game_on = True
    round = 1

    while game_on:

        if p.balance >= 3000: # Check if player reached the goal
            print("Congratulations!")
            print("You Have Reached The Goal! Well Done!")

        if p.balance < 25: # Check if player has enough money
            print("You Don't Have Enough Money! Game Over!")
            return (round, p.balance)

        print("\n"*2)
        print(f"====== Round {round} ======\n")
        print(f"Bank Balance : {p.balance}\n")

        bet = place_bet(p.balance)
        p.remove_balance(bet)  # Remove bet from balance

        p_hand = []
        dealer_hand = []

        if len(deck.all_cards) == 10:  # Reshuffle the deck if it's close to empty
            print("\nReshuffling Deck")
            deck = Deck()
            deck.shuffle()

        for _ in range(2):
            p_hand.append(deck.deal_one())
            dealer_hand.append(deck.deal_one())

        show_p_hand(p_hand)
        show_dealer_hand(dealer_hand)


        while True:
            #initial check
            if init_check(p, p_hand, dealer_hand, bet) == True: #blackjack or tie
                if not replay():
                    game_on = False
                    return (round, p.balance)
                else:
                    round += 1
                    break
            
            # Player Turn - Hit/Stay
            hit_stay(p_hand, deck)
            show_p_hand(p_hand)
            if blackjack(p_hand): # Player Blackjack
                print(f"BLACKJACK! You win {1.5 * bet}")
                p.add_balance((bet + (bet * 1.5)))
                if not replay():
                    game_on = False
                    return (round, p.balance)
                else:
                    round += 1
                    break
            elif bust(p_hand): # Player Bust
                print(f"You Bust! You lose {bet}")
                if not replay():
                    game_on = False
                    return (round, p.balance)
                else:
                    round += 1
                    break
            

            #Player didnt bust - Dealer Turn
            show_dealer_full_hand(dealer_hand)

            dealer_hit_stay(dealer_hand, deck)
            show_dealer_full_hand(dealer_hand)
            if bust(dealer_hand): # Dealer Bust case
                p.add_balance(2*bet)
                print(f"Dealer Bust! You win {bet}")
                if not replay():
                    return (round, p.balance)
                else:
                    round += 1
                    break
            elif tie(p_hand, dealer_hand): # Tie case
                print("PUSH! Bet returned")
                p.add_balance(bet)
                if not replay():
                    return (round, p.balance)
                else:
                    round += 1
                    break
            

            print(f"Your cards value : {card_sum(p_hand)}")
            print(f"Dealer cards value : {card_sum(dealer_hand)}")
            print("\n"*2)

            # none BUST case
            if player_close_to_21(p_hand, dealer_hand) == True: # Player close to 21
                print(f"You win {bet}")
                p.add_balance(2*bet)
                if not replay():
                    return (round, p.balance)
                else:
                    round += 1
                    break
            else:
                print("Dealer Wins")
                if not replay():
                    return (round, p.balance)
                else:
                    round += 1
                    break





if __name__ == "__main__":
    rounds, balance = main()

    print("\n"*2)
    print(f"Rounds played : {rounds}")
    print(f"Final Balance : {balance}")
    if balance < 1000:
        print(f"Money Lost : {1000-balance}")
    else:
        print(f"Money Won : {balance-1000}")
