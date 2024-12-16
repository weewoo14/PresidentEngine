from time import *
from random import *
from math import *
import sys


### IMPORTING THE BOT STRATEGIES ###
botName1 = ""
botName2 = ""

botStrat1 = __import__(botName1)
botStrat2 = __import__(botName2)
####################################


# Establishing the card values
cardValues = {'3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14, '2':15, 'JOKER':16}

# Creating the total card deck by extracting the values from the 
totalCardDeck = []
for card in cardValues:
    if card == 'JOKER': # Only two jokers in a deck
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
        if cardChoice == '3':
            playerOne3 += 1
        cardDeck1.append(cardChoice)
    else:
        if cardChoice == '3':
            playerTwo3 += 1
        cardDeck2.append(cardChoice)
    
    curDeck += 1

if playerOne3 == playerTwo3:
    currentTurn = randint(0,1)

else:
    if playerOne3 > playerTwo3:
        currentTurn = 0
    
    else:
        currentTurn = 1

gamePile, gameAmount = [], -1

def placeMove(currentPlayer):
    global gamePile, gameAmount, currentTurn, cardDeck1, cardDeck2

    if currentPlayer == 1:
        playerAmount, playerCard = botStrat1.getMove(cardDeck1, gamePile, gameAmount, len(cardDeck2))
    
    else:
        playerAmount, playerCard = botStrat2.getMove(cardDeck1, gamePile, gameAmount, len(cardDeck2))

    playerAmount = int(playerAmount)

    if gameAmount == -1:
        gameAmount = playerAmount
        gamePile.append(playerCard)
    
    else:
        if playerAmount == gameAmount:
            cardValue1 = cardValues[gamePile[-1]]
            cardValue2 = cardValues[playerCard]

            if cardValue2 > cardValue1:
                print(f"Player {currentPlayer} has placed {gameAmount} {playerCard} into the pile.")
                print(f"The pile now looks like this: {' '.join(gamePile)}")

                gamePile.append(playerCard)
                currentTurn += 1

                if currentPlayer == 1:
                    for card in range(playerAmount):

                        try:
                            cardDeck1.remove(playerCard)
                        
                        except:
                            print("Player 1 has cheated! They don't have enough of that card!")
                            sys.exit()
                
                else:
                    for card in range(playerAmount):

                        try:
                            cardDeck2.remove(playerCard)
                        except:
                            print("Player 2 has cheated! They don't have enough of that card!")
                            sys.exit()
            
            elif cardValue2 == cardValue1:
                print(f"Player {currentPlayer} has burned the pile!")
                gamePile = []
                gameAmount = -1

                if currentPlayer == 1:
                    for card in range(playerAmount):
                        cardDeck1.remove(playerCard)
                
                else:
                    for card in range(playerAmount):
                        cardDeck2.remove(playerCard)
            
            else:
                print(f"Player {currentPlayer} has cheated!")
                sys.exit()
        
        elif playerAmount != gameAmount and playerCard == "JOKER":
            print(f"Player {currentPlayer} has burned the pile with a joker!")
            gamePile = []
            gameAmount = -1

            if currentPlayer == 1:
                for card in range(playerAmount):
                    cardDeck1.remove(playerCard)
            
            else:
                for card in range(playerAmount):
                    cardDeck2.remove(playerCard)

        else:
            print(f"Player {currentPlayer} has cheated!")
            sys.exit()

while len(cardDeck1) > 0 and len(cardDeck2) > 0:

    if currentTurn % 2 == 0:
        placeMove(1)

    else:
        placeMove(2)
    
if len(cardDeck1) == 0:
    print("Player 1 wins!")

else:
    print("Player 2 wins!")
