from time import *
from random import *
from math import *
from tokenizer import getTokenCount
import os

# get size of terminal
columns, lines = os.get_terminal_size()

### IMPORTING THE BOT STRATEGIES ###
botName1 = "basic"
botName2 = "manual"

botStrat1 = __import__(botName1)
botStrat2 = __import__(botName2)
####################################

# Options
games = 1  # How many games to simulate
verbose = True  # Print every move, or just print the result of each game (cheating will always be printed)
delay = 1  # delay between turns (s)

# wrapping the functions to add timeouts (copied from stackoverflow)
import signal
import functools


def timeout(seconds=5):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            def handle_timeout(signum, frame):
                raise TimeoutError()

            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(seconds)

            result = func(*args, **kwargs)

            signal.alarm(0)

            return result

        return wrapper

    return decorator


@timeout(seconds=60)
def strat1Move(cardDeck, gamePile, gameAmount, oppCardDeckLen):
    return botStrat1.getMove(cardDeck, gamePile, gameAmount, oppCardDeckLen)


@timeout(seconds=60)
def strat2Move(cardDeck, gamePile, gameAmount, oppCardDeckLen):
    return botStrat2.getMove(cardDeck, gamePile, gameAmount, oppCardDeckLen)


print(f"Bot 1 has {getTokenCount(botName1)}/5000 tokens")
print(f"Bot 2 has {getTokenCount(botName2)}/5000 tokens")


def unimportantPrint(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)


# Establishing the card values
cardValues = {
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
    "2": 15,
    "JOKER": 16,
}


def shuffleDeck():
    global cardDeck1, cardDeck2, currentTurn, gamePile, gameAmount
    # Creating the total card deck by extracting the values from the
    totalCardDeck = []
    for card in cardValues:
        if card == "JOKER":  # Only two jokers in a deck
            numTimes = 2
        else:
            numTimes = 4

        for numType in range(numTimes):
            totalCardDeck.append(card)

    # Distributing the cards to the bots
    cardDeck1 = []
    cardDeck2 = []

    # Keeping track of the 3's to see which bot goes first. In the event no bot goes first, coinflip
    playerOne3 = 0
    playerTwo3 = 0
    curDeck = 1
    while len(totalCardDeck) > 18:

        cardChoice = choice(totalCardDeck)
        totalCardDeck.remove(cardChoice)

        if curDeck % 2 == 1:
            if cardChoice == "3":
                playerOne3 += 1
            cardDeck1.append(cardChoice)
        else:
            if cardChoice == "3":
                playerTwo3 += 1
            cardDeck2.append(cardChoice)

        curDeck += 1

    if playerOne3 == playerTwo3:
        currentTurn = randint(0, 1)

    else:
        if playerOne3 > playerTwo3:
            currentTurn = 0

        else:
            currentTurn = 1

    gamePile, gameAmount = [], -1


def placeMove(currentPlayer):
    global gamePile, gameAmount, currentTurn, cardDeck1, cardDeck2

    unimportantPrint(f"Player {currentPlayer}'s turn")

    try:
        if currentPlayer == 1:
            playerAmount, playerCard = strat1Move(
                cardDeck1, gamePile, gameAmount, len(cardDeck1)
            )

        else:
            playerAmount, playerCard = strat2Move(
                cardDeck2, gamePile, gameAmount, len(cardDeck1)
            )

    except TimeoutError:
        print(f"Player {currentPlayer} took too long and lost")
        return 1

    playerAmount = int(playerAmount)

    # player skips their turn
    if playerAmount == 0:
        unimportantPrint(f"Player {currentPlayer} skipped their turn")
        currentTurn += 1
        gamePile = []
        gameAmount = -1
        return 0

    # was empty pile
    if gameAmount == -1:
        gameAmount = playerAmount

    if playerCard == "JOKER":
        unimportantPrint(f"Player {currentPlayer} has burned the pile with a joker!")
        gamePile = []
        gameAmount = -1

        if currentPlayer == 1:
            for card in range(playerAmount):
                cardDeck1.remove(playerCard)

        else:
            for card in range(playerAmount):
                cardDeck2.remove(playerCard)
    elif playerAmount == gameAmount:
        cardValue1 = cardValues[gamePile[-1]] if len(gamePile) else 0
        cardValue2 = cardValues[playerCard]

        if cardValue2 > cardValue1:
            unimportantPrint(
                f"Player {currentPlayer} has placed {gameAmount} {playerCard} into the pile."
            )

            gamePile.append(playerCard)
            currentTurn += 1
            unimportantPrint(f"The pile now looks like this: {' '.join(gamePile)}")

            if currentPlayer == 1:
                for card in range(playerAmount):

                    try:
                        cardDeck1.remove(playerCard)
                    except:
                        print(
                            "Player 1 has cheated! They don't have enough of that card!"
                        )
                        return 1

            else:
                for card in range(playerAmount):

                    try:
                        cardDeck2.remove(playerCard)
                    except:
                        print(
                            "Player 2 has cheated! They don't have enough of that card!"
                        )
                        return 1

        elif cardValue2 == cardValue1:
            unimportantPrint(f"Player {currentPlayer} has burned the pile!")
            gamePile = []
            gameAmount = -1

            if currentPlayer == 1:
                for card in range(playerAmount):
                    cardDeck1.remove(playerCard)

            else:
                for card in range(playerAmount):
                    cardDeck2.remove(playerCard)

        else:
            print(
                f"Player {currentPlayer} has cheated because card value less than pile card!"
            )
            return 1

    else:
        print(
            f"Player {currentPlayer} has cheated! Different number of cards than the pile!"
        )
        return 1

    return 0


def runRound():
    while len(cardDeck1) > 0 and len(cardDeck2) > 0:
        if currentTurn % 2 == 0:
            try:
                if placeMove(1):
                    return 2
            except KeyboardInterrupt:
                raise
            except:
                return 2

        else:
            try:
                if placeMove(2):
                    return 1
            except KeyboardInterrupt:
                raise
            except:
                return 1
        sleep(delay)

    if len(cardDeck1) == 0:
        return 1

    else:
        return 2


strat1Wins = 0
strat2Wins = 0

for i in range(games):
    shuffleDeck()
    res = runRound()

    if res == 1:
        strat1Wins += 1
    else:
        strat2Wins += 1

    if games > 10 and not verbose:
        strat1Avg = strat1Wins * 100 / (i + 1)
        strat2Avg = strat2Wins * 100 / (i + 1)
        print(
            f"\x1b[0J\n{i + 1}/{games} games played ({round(100 * (i + 1)/games, 2)}%)   \n{'█' * round((i+1)/games * columns)}{'▒' * round((1 - (i+1)/games) * columns)}\n{botName1} wins: {strat1Wins} ({round(strat1Avg, 2)}%)   \n{botName2} wins: {strat2Wins} ({round(strat2Avg, 2)}%)   ",
            end="\x1B[4A\r",
        )
    elif res == 1:
        print("Player 1 wins!")
    else:
        print("Player 2 wins!")
