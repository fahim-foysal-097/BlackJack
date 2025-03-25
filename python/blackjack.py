from random import shuffle

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11} # Ace should be 1/11

class Card:

    def __init__(self, suit, rank):
        
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def val(self):
        value = self.value
        return value
    

class Deck:
    
    def __init__(self):
        
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                card_created = Card(suit, rank)
                self.all_cards.append(card_created)

    def shuffle(self):

        shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop(-1)



class Player:

    def __init__(self, balance):   
        self.balance = balance

    def add_balance(self, amount):
        self.balance += amount

    def remove_balance(self, amount):
        self.balance -= amount



def place_bet(balance):

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
    
    while True:
        decision = input("Hit or Stay : ")
        if decision not in ["Hit", "hit", "h", "Stay", "stay", "s"]:
            print("Sorry! Invalid input")
        else:
            if decision in ["Hit", "hit", "h"]:
                return 1
            elif decision in ["Stay", "stay", "s"]:
                return 0
            
def keep_playing():
    
    while True:
        decision = input("Do you want to continue playing? (Y/N) : ")
        if decision not in ["Yes", "yes", "Y", "y", "No", "no", "N", "n"]:
            print("Sorry! Invalid input")
        else:
            if decision in ["Yes", "yes", "Y", "y"]:
                return True
            elif decision in ["No", "no", "N", "n"]:
                return False
            

def show_p_hand(p_hand):

    print(f"\nYour Cards")
    print("--------------------")
    for card in p_hand:
        print(card)
    print(f"Cards value : {card_sum(p_hand)}")
    print("\n")

def show_dealer_hand(dealer_hand):

    print(f"\nDealer Cards")
    print("----------------------")
    print(f"*******")
    for i in range( (len(dealer_hand))-1 ):
        print(dealer_hand[i+1])
    print("\n")

def show_dealer_full_hand(dealer_hand):

    print(f"\nDealer All Cards")
    print("--------------------")
    for card in dealer_hand:
        print(card)
    print(f"Cards value : {card_sum(dealer_hand)}")
    print("\n")


def card_sum(cards):

    total = 0
    aces = 0
    for card in cards:
        if card.rank == "Ace":
            aces += 1
        total += card.val()
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def blackjack_check(cards):

    if card_sum(cards) == 21:
        return True
    else:
        return False

def tie_check(cards_1, cards_2):

    if card_sum(cards_1) == card_sum(cards_2):
        return True
    else:
        return False
    
def bust_check(cards):

    if card_sum(cards) > 21:
        return True
    else:
        return False
    
    
def player_close_to_21(p_hand, dealer_hand):

    if card_sum(p_hand) > card_sum(dealer_hand):
        return True
    else:
        return False
    

def init_check(p, p_hand, dealer_hand, bet):
    
    if blackjack_check(p_hand):
        if tie_check(p_hand, dealer_hand) == True:
            print("BLACKJACK! It's a push - bet returned")
            p.add_balance(bet)
            return True
        print("BLACKJACK! You win {1.5 * bet}")
        p.add_balance((bet + (bet * 1.5)))
        return True
    else:
        return False

def hit_stay(p_hand,deck):

    while True:
        decision = p_decision()
        if decision == 1:  # Hit
            p_hand.append(deck.deal_one())
            print(f"Your draw : {p_hand[-1]}")
            print(f"Cards value : {card_sum(p_hand)}")
            if bust_check(p_hand) == True:
                break
            else:
                continue
        else:
            break

def dealer_hit_stay(dealer_hand,deck):

    while True:
        if card_sum(dealer_hand) < 16: 
                dealer_hand.append(deck.deal_one())
                print(f"Dealer draws : {dealer_hand[-1]}, Cards value : {card_sum(dealer_hand)}\n")
                if bust_check(dealer_hand) == True:
                    break
                else:
                    continue
        else:
            break






def main():

    deck = Deck()
    deck.shuffle()
    init_balance = 1000
    p = Player(init_balance)


    game_on = True
    round = 1

    while game_on:

        print("\n"*2)
        print(f"====== Round {round} ======\n")
        print(f"Bank Balance : {p.balance}\n")

        bet = place_bet(p.balance)
        p.remove_balance(bet)  # Remove bet from balance

        p_hand = []
        dealer_hand = []

        if len(deck.all_cards) == 10:  # Reshuffle the deck if it's close to empty
            deck = Deck()
            deck.shuffle()

        for _ in range(2):
            p_hand.append(deck.deal_one())
            dealer_hand.append(deck.deal_one())

        show_p_hand(p_hand)
        show_dealer_hand(dealer_hand)


        while True:
            #initial check
            if init_check(p, p_hand, dealer_hand, bet) == True: #blackjack (+tie)
                if keep_playing() == False:
                    game_on = False
                    return (round, p.balance)
                else:
                    round += 1
                    break
            
            # Player Turn - Hit/Stay
            hit_stay(p_hand, deck)
            show_p_hand(p_hand)
            if bust_check(p_hand) == True: # Player Bust
                print(f"You Bust! You lose {bet}")
                if keep_playing() == False:
                    game_on = False
                    return (round, p.balance)
                else:
                    round += 1
                    break
            

            #Player didnt bust - Dealer Turn

            show_dealer_full_hand(dealer_hand)

            dealer_hit_stay(dealer_hand, deck)
            show_dealer_full_hand(dealer_hand)
            if bust_check(dealer_hand) == True: # Dealer Bust case
                p.add_balance(2*bet)
                print(f"Dealer Bust! You win {bet}")
                if keep_playing() == False:
                    return (round, p.balance)
                else:
                    round += 1
                    break
            elif tie_check(p_hand, dealer_hand) == True: # Tie case
                print("PUSH! Bet returned")
                p.add_balance(bet)
                if keep_playing() == False:
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
                if keep_playing() == False:
                    return (round, p.balance)
                else:
                    round += 1
                    break
            else:
                print("Dealer Wins")
                if keep_playing() == False:
                    return (round, p.balance)
                else:
                    round += 1
                    break





if __name__ == "__main__":
    rounds, balance = main()

    print("\n"*2)
    print(f"Rounds played : {rounds}")
    print(f"Final Balance : {balance}")
