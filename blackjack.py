import random
from sys import stdout
from time import sleep


def play() -> None:

    global player_cards
    global computer_cards

    global player_score
    global computer_score

    computer_wins = player_wins = False

    # Handle cards and compute score
    print("Handling cards...")
    player_cards, computer_cards = get_cards(2), get_cards(2)
    player_score, computer_score = get_score(player_cards), get_score(computer_cards)

    print_cards_and_score(hide_computers_card=True, to_sleep=True)

    # Check if blackjack ocurred
    if computer_score == 21: computer_wins = True
    if player_score == 21: player_wins = True

    if computer_wins or player_wins:
        clear_last_lines(3)
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

                # Clear last cards and scores and print new ones
                clear_last_lines(4)
                print_cards_and_score(hide_computers_card=True)
            else:
                # Clear our question
                clear_last_lines(1)
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

                clear_last_lines(4)
                print_cards_and_score()
                print("Computer draws a card...")

            sleep(1)
            clear_last_lines(1)

        if (computer_score < player_score <= 21) or (computer_score > 21 and player_score <= 21):
            player_wins = True
        elif (player_score < computer_score <= 21) or (player_score > 21 and computer_score <= 21):
            computer_wins = True

        if len(computer_cards) == 2:
            # That means the computer hasn't drawn any cards, thus the score on screen wasn't
            # updated and the user still doesn't know what's the computer's second
            # card. So, let's clear the last scores/cards and print the new ones
            clear_last_lines(4)
            print_cards_and_score()

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


# Prints each player's cards and scores
def print_cards_and_score(hide_computers_card=False, to_sleep=False) -> None:

    # Setting hide_computers_card to True will only print the first
    # computer's card in the deck and will not take it into account
    # when computing its score

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


# Clears `num_of_lines` lines from console
def clear_last_lines(num_of_lines: int) -> None:
    for i in range(num_of_lines):
        # Move cursor back to previous line
        stdout.write('\x1b[1A')

        # Clear line
        stdout.write('\x1b[2K')


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

print("W E L C O M E  T O  B L A C K J A C K !\n")

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
            print("--------------------------------------------------")
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(1)
