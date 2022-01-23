import random
from sys import stdout
from os import system, name
from time import sleep


def play() -> None:
    computer_wins = False
    player_wins = False

    sleep(0.1)
    print("Handling cards...")
    computer_cards = get_cards(2)
    computer_score = get_score(computer_cards)
    if computer_score == 21:
        computer_wins = True

    player_cards = get_cards(2)
    player_score = get_score(player_cards)
    if player_score == 21:
        player_wins = True

    sleep(1)
    print(f"Computer's cards: [{computer_cards[0]}, ?]"
          f"-- Score: {CARDS[computer_cards[0]]}")
    sleep(1)
    print(f"Your cards:       [{player_cards[0]}, {player_cards[1]}]"
          f"-- Score: {get_score(player_cards)}\n")

    if not (computer_wins or player_wins):

        # player draws cards
        while player_score < 21:
            answer = input("Wanna buy a card? (Y/n): ")
            if answer.lower() == "y" or answer == "":
                player_cards.append(get_cards(1)[0])
                player_score = get_score(player_cards)
                clear_last_lines(3)
                print(f"Your cards:       [{', '.join(player_cards)}] "
                      f"-- Score: {get_score(player_cards)}\n")
            else:
                clear_last_lines(1)
                break

        if (player_score <= 21) and (computer_score < player_score):
            print("Computer is thinking...")
            while computer_score < player_score:
                sleep(COMPUTER_TIME)
                computer_cards.append(get_cards(1)[0])
                computer_score = get_score(computer_cards)

                clear_last_lines(4)
                print(f"Computer's cards: [{', '.join(computer_cards)}] "
                      f"-- Score: {get_score(computer_cards)}")
                print(f"Your cards:       [{', '.join(player_cards)}] "
                      f"-- Score: {player_score}\n")
                print("Computer draws a card...")

            sleep(1)
            clear_last_lines(1)

        if (computer_score < player_score <= 21) or \
           (computer_score > 21 and player_score <= 21):

            player_wins = True
        elif (player_score < computer_score <= 21) or \
             (player_score > 21 and computer_score <= 21):

            computer_wins = True

        if len(computer_cards) == 2:
            """ that means the computer didn't drawn any cards and the user still
            doesn't know what's its second car, so let's show it """
            clear_last_lines(3)
            print(f"Computer's cards: [{', '.join(computer_cards)}] "
                  f"-- Score: {get_score(computer_cards)}")
            print(f"Your cards:       [{', '.join(player_cards)}] "
                  f"-- Score: {player_score}\n")

    else:
        clear_last_lines(3)
        print(f"Computer's cards: [{', '.join(computer_cards)}] -- "
              f"Score: {get_score(computer_cards)}")
        print(f"Your cards:       [{', '.join(player_cards)}] -- "
              f"Score: {player_score}\n")
        print("B L A C K J A C K !")

    if player_wins:
        print("YOU WIN!")
    elif computer_wins:
        print("YOU LOSE!")
    else:
        print("IT'S A DRAW!")


def get_cards(num_of_cards: int) -> list:
    return random.choices(list(CARDS.keys()), k=num_of_cards)


def get_score(user_cards: list) -> int:

    result = 0

    if "A" in user_cards:  # ace card...
        is_there_ace = True
    else:
        is_there_ace = False

    if is_there_ace:
        for i in user_cards:
            if i != "A":
                result += CARDS[i]
        for i in range(user_cards.count("A")):
            if result + 11 <= 21:
                result += 11
            else:
                result += 1
    else:
        for i in user_cards:
            result += CARDS[i]

    return result


def clear_last_lines(num_of_lines: int) -> None:
    for i in range(num_of_lines):
        # move cursor back to previous line
        stdout.write('\x1b[1A')

        # clear line
        stdout.write('\x1b[2K')


CARDS = {
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": "1 or 11"
}
for x, y in enumerate(range(1, 11)):
    CARDS[str(x+1)] = y

# time computer takes to "think"
COMPUTER_TIME = 1.5

system('cls' if name == 'nt' else 'clear')
print("W E L C O M E  T O  B L A C K J A C K !\n")

while True:
    play()
    answer = input("Play again? (Y/n): ")
    if not (answer.lower() == "y" or answer == ''):
        break
    print("--------------------------------------------------")
