import random
from sys import stdout
from time import sleep
import os

def play() -> None:

    global player_cards
    global computer_cards

    global player_score
    global computer_score

    computer_wins = player_wins = False

    player_cards, computer_cards = get_cards(2), get_cards(2)
    player_score, computer_score = get_score(player_cards), get_score(computer_cards)

    print_cards_and_score(hide_computers_card=True,
                          to_sleep=True,
                          message="Handling cards...")

    # Check if blackjack ocurred
    if computer_score == 21: computer_wins = True
    if player_score == 21: player_wins = True

    if computer_wins or player_wins:
        print_cards_and_score()
        print("B L A C K J A C K !")

    else:
        # Keep asking user to buy a card until either he loses the game or denies it
        while player_score < 21:

            answer = input("Wanna buy a card? (Y/n): ").lower()
            if answer in ["yes", "y", ""]:
                # Append new card to player's deck
                player_cards.append(get_cards(1))
                # Update score
                player_score = get_score(player_cards)

                print_cards_and_score(hide_computers_card=True)
            else:
                print_cards_and_score()
                break

        # If player hasn't lost and player's score is higher than computer's
        if (player_score <= 21) and (computer_score < player_score):
            print("Computer is thinking...")

            # Computer will keep buying cards until
            # his score is higher than player's
            while computer_score < player_score:
                sleep(COMPUTER_TIME)
                computer_cards.append(get_cards(1))
                computer_score = get_score(computer_cards)

                print_cards_and_score()
                print("Computer draws a card...")

            sleep(1)

        if (computer_score < player_score <= 21) or (computer_score > 21 and player_score <= 21):
            player_wins = True
        elif (player_score < computer_score <= 21) or (player_score > 21 and computer_score <= 21):
            computer_wins = True

    # Check who has won
    if player_wins == computer_wins:
        print("IT'S A DRAW!")
    elif player_wins:
        print("YOU WIN!")
    else:
        print("YOU LOSE!")


# Returns `num_of_cards` random cards
def get_cards(num_of_cards: int) -> list:
    cards = random.choices(list(CARDS.keys()), weights=CARD_WEIGHTS, k=num_of_cards)
    return cards[0] if len(cards) == 1 else cards


# Returns a score based on the deck passed in
def get_score(cards: list) -> int:
    score = 0

    # Compute value ignoring Ace cards
    for card in cards:
        if card != "A":
            score += CARDS[card]

    # Look for Ace cards and compute their value
    for card in cards:
        if card == "A":
            if score + 11 <= 21:
                score += 11
            else:
                score += 1

    return score


# Clears console and prints each player's cards and scores
def print_cards_and_score(hide_computers_card=False, to_sleep=False, message=None) -> None:

    # Setting hide_computers_card to True will only print the first
    # computer's card in the deck and will not take it into account
    # when computing its score

    os.system('cls' if os.name == 'nt' else 'clear')
    print("W E L C O M E  T O  B L A C K J A C K !\n")

    # Print message, if user passed one to the function
    if message != None:
        print(message)

    if to_sleep: sleep(1)

    if not hide_computers_card:
        print(f"Computer's cards: [{', '.join(computer_cards)}] -- "
              f"Score: {get_score(computer_cards)}")
    else:
        print(f"Computer's cards: [{computer_cards[0]}, ?] -- "
              f"Score: {CARDS[computer_cards[0]]}")

    if to_sleep: sleep(1)

    print(f"Your cards:       [{', '.join(player_cards)}] -- "
          f"Score: {player_score}\n")


# Cards and their values
CARDS = {
    # Value of Ace will be handled by `get_score`
    "A": "1 or 11",
    "J": 10,
    "Q": 10,
    "K": 10
}

# Add cards 2 to 10 and their values to CARDS
for card, value in enumerate(range(2, 11)):
    CARDS[str(card + 2)] = value

# Cards' weights from first to last in CARDS
CARD_WEIGHTS = [4/52]*4 + [36/52]*9

# Time computer takes to "think"
COMPUTER_TIME = 1.5

# Define players' decks
player_cards = computer_cards = []
player_score = computer_score = 0

if __name__ == "__main__":
    try:
        while True:
            play()

            answer = input("Play again? (Y/n): ").lower()
            if not answer in ["y", "yes", ""]:
                break

    except KeyboardInterrupt:
        print("\nExiting...")
        exit(1)
