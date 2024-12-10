from time import *
from random import *
from math import *


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