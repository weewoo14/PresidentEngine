from time import *
from random import *
from math import *
from tokenizer import getTokenCount
import sys


### IMPORTING THE BOT STRATEGIES ###
botName1 = "manual"
botName2 = "manual"

botStrat1 = __import__(botName1)
botStrat2 = __import__(botName2)
####################################

# Options
games = 1  # How many games to simulate
verbose = True  # Print every move, or just print the result of each game (cheating will always be printed)

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


@timeout(seconds=5)
def strat1Move(cardDeck, gamePile, gameAmount, oppCardDeckLen):
    return botStrat1.getMove(cardDeck, gamePile, gameAmount, oppCardDeckLen)


@timeout(seconds=5)
def strat2Move(cardDeck, gamePile, gameAmount, oppCardDeckLen):
    return botStrat2.getMove(cardDeck, gamePile, gameAmount, oppCardDeckLen)


print(f"Bot 1 has {getTokenCount(botName1)}/5000 tokens")
print(f"Bot 2 has {getTokenCount(botName2)}/5000 tokens")


def unimportantPrint(thing):
    if verbose:
        print(thing)


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
        sys.exit()

    playerAmount = int(playerAmount)

    if playerAmount == 0:
        unimportantPrint(f"Player {currentPlayer} skipped their turn")
        return

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
            unimportantPrint(f"The pile now looks like this: {' '.join(gamePile)}")

            gamePile.append(playerCard)
            currentTurn += 1

            if currentPlayer == 1:
                for card in range(playerAmount):

                    try:
                        cardDeck1.remove(playerCard)

                    except:
                        print(
                            "Player 1 has cheated! They don't have enough of that card!"
                        )
                        sys.exit()

            else:
                for card in range(playerAmount):

                    try:
                        cardDeck2.remove(playerCard)
                    except:
                        print(
                            "Player 2 has cheated! They don't have enough of that card!"
                        )
                        sys.exit()

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
            sys.exit()

    else:
        print(f"Player {currentPlayer} has cheated! not enough cards")
        sys.exit()


coinflip = floor(random() * 2)
unimportantPrint("player", coinflip + 1, "begins")
while len(cardDeck1) > 0 and len(cardDeck2) > 0:
    if currentTurn % 2 == coinflip:
        placeMove(1)

    else:
        placeMove(2)

if len(cardDeck1) == 0:
    print("Player 1 wins!")

else:
    print("Player 2 wins!")
