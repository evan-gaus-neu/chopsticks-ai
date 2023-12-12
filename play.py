# play.py
# imports
from main import GameState, isTerminal2, getPossibleNextStatesForDefaultRules, isTerminalPlay, arbitraryHighValue, player1Str, player2Str, drawStr, contStr, drawVal, depthLimitVal

depthLimit = 9

def minimaxPlay(currentState, depth):

    # Check if the current state is a terminal state
    terminal = isTerminal2(currentState)
    if terminal == player1Str:
        return 1
    elif terminal == player2Str:
        return -1
    elif terminal == drawStr:
        return drawVal

    # # Check if the current state is a terminal state
    # if isTerminal(currentState) != 0:
    #     return isTerminal(currentState)

    # Check if we've reached the depth limit
    if depth >= depthLimit:
        return depthLimitVal
    
    # If it's player 1's turn, we're maximizing
    if currentState.turn == 1:
        bestScore = -arbitraryHighValue
        for nextState in getPossibleNextStatesForDefaultRules(currentState, False):
            score = minimaxPlay(nextState, depth + 1)
            bestScore = max(score, bestScore)
        return bestScore
    else: # It's plater 2's turn, so minimizing
        bestScore = arbitraryHighValue
        for nextState in getPossibleNextStatesForDefaultRules(currentState, False):
            score = minimaxPlay(nextState, depth + 1)
            bestScore = min(score, bestScore)
        return bestScore

def assessPossibleMovesPlay(currentState):

    print("Running assessment...")

    listOfNextMoveTuples = []

    for nextState in getPossibleNextStatesForDefaultRules(currentState, False):
        score = minimaxPlay(nextState, 0)
        listOfNextMoveTuples.append((nextState, score))
    
    # Print the assessment
    # print("=== === === === === MARK === === === === ===")
    # print(f"CURRENT State: {currentState}")
    print(f"Number of Possible Moves: {len(listOfNextMoveTuples)}:")
    # print("")
    for index, item in enumerate(listOfNextMoveTuples):
        print(f"{index}: {item[0]}   -->   {item[1]}")
    print("")
    print(f"Key:   1 = Player 1 wins,   -1 = Player 2 wins,   {drawVal} = Draw (ie loop state),   {depthLimitVal} = Depth Limit Reached")
    return listOfNextMoveTuples


# Print
currentGameState = GameState(1, 1, 1, 1, 1)
while (not isTerminalPlay(currentGameState)):
    print("===========================================")
    print("It's your turn now!")
    print(f"Current State: {currentGameState}\n")

    # Assess the possible moves
    assessPossibleMovesPlay(currentGameState)
    
    
    # print("Possible Next States:")
    # nextStates = getPossibleNextStatesForDefaultRules(currentGameState, False)
    # for index, item in enumerate(nextStates):
    #     print(f"{index}: {item}")
    print("\nWhich move do you want to make (type only the index number of the move you wish to make):")

    # print(f"Possible Next States: {getPossibleNextStatesForDefaultRules(currentGameState, False)}")
    # print("Which move do you want to make")
    userInput = input()

    # User inputted a number
    userInputIndex = int(userInput)
    print(f"You made move: {userInputIndex}")

    # QQQ Check if it's out of bounds?

    # Update state:
    currentGameState = getPossibleNextStatesForDefaultRules(currentGameState, False)[int(userInput)]

    # Check if the game is over
    if isTerminalPlay(currentGameState):
        break

    # COMPUTER TURN
    # Assess the possible moves:
    print("\nIt's the computer's turn now:")
    print(f"New Current State: {currentGameState}\n")
    possibleMoves = assessPossibleMovesPlay(currentGameState)

    minScore = arbitraryHighValue
    minNewState = None
    indexOfMinNewState = 0

    for index, item in enumerate(possibleMoves):
        if item[1] < minScore:
            minScore = item[1]
            minNewState = item[0]
            indexOfMinNewState = index

    # Make the lowest scoring move
    currentGameState = minNewState
    print(f"\nComputer made move: {indexOfMinNewState}\n")

# The game is over
print("--- GAME OVER!!! ---\n")
terminal = isTerminal2(currentGameState)
if terminal == player1Str:
    print("Congrats, you won!\n")
elif terminal == player2Str:
    print("Sorry, you lost!\n")
print(f"Final State of the game: {currentGameState}\n\n")


