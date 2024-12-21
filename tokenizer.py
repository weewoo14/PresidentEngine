import tokenize


def getTokenCount(fileName):
    with open(fileName + ".py", "rb") as f:
        tokens = tokenize.tokenize(f.readline)
        tokenCount = 0
        for token in tokens:
            if token.type == 3:  # is string, count every character
                tokenCount += len(token.string)
            if not token.type in [
                61,
                4,
                5,
                6,
                0,
            ]:  # is not a comment, indent, dedent, newline, or end of file
                tokenCount += 1

    return tokenCount
