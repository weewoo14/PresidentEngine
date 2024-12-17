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
    print(
        "You currently have:", " ".join(sorted(cardDeck, key=lambda x: cardValues[x]))
    )
    if len(gamePile):
        print(f"The top of the pile is {gameAmount}x{gamePile[-1]}")
    else:
        print("Pile is blank")
    return input("How many? "), input("What will you play? ").upper()
