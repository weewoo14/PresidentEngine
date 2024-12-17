# just plays the lowest thing it can possibly play

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
}  # too lazy to figure out circular commit issues


def getMove(cardDeck, gamePile, gameAmount, oppCardDeckLen):
    sortedDeck = sorted(cardDeck, key=lambda x: cardValues[x])

    if gameAmount == -1:  # the pile is empty and we play the lowest card we can
        amount = 0
        for card in sortedDeck:
            if card == sortedDeck[0]:
                amount += 1
        return amount, sortedDeck[0]

    toPlay = None
    currentAmount = 0
    lookingAt = ""
    for card in sortedDeck:
        if card == lookingAt:
            currentAmount += 1
        else:
            currentAmount = 1
            lookingAt = card
        if currentAmount == gameAmount and cardValues[card] >= cardValues[gamePile[-1]]:
            toPlay = card
            break
    return gameAmount if toPlay != None else 0, toPlay
