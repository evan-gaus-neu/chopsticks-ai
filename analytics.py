# analytics.py

# Evan Gaus, Alex Reed

# Helpful values
arbitraryHighValue = 1000
depthLimit = 8
player1Str = 'PLAYER1'
player2Str = 'PLAYER2'
drawStr = 'DRAW'
contStr = 'CONTINUE'
drawVal = 0.1
depthLimitVal = 0.2
# rolloverByDefault = True

# Define a class to represent the game state
# Player One Left = P1L
# Player One Right = P1R
# Player Two Left = P2L
# Player Two Right = P2R
# Who's turn it is = turn (1 or 2)
class GameState:
    def __init__(self, player1Left, player1Right, player2Left, player2Right, turn, previousStates=None) -> None:
        # Initialize the game state
        self.player1Left = player1Left
        self.player1Right = player1Right
        self.player2Left = player2Left
        self.player2Right = player2Right
        self.turn = turn

        if previousStates is None:
            previousStates = []
        self.previousStates = previousStates

    def __repr__(self) -> str:
        # Return a string representation of the game state
        return f"GS: P1({self.player1Left}, {self.player1Right}) P2({self.player2Left}, {self.player2Right}) T:{self.turn}"
        # return f"GS: [{self.player1Left}, {self.player1Right}, {self.player2Left}, {self.player2Right}, {self.turn}]"
        # return f"GameState(player1Left={self.player1Left}, player1Right={self.player1Right}, player2Left={self.player2Left}, player2Right={self.player2Right}, turn={self.turn})"
    
    # QQQ This was never updated after adding previous states
    def __eq__(self, __value: object) -> bool:
        # Return True if the game states are equal
        if not isinstance(__value, GameState):
            return NotImplemented
        
        return (self.player1Left == __value.player1Left and 
                self.player1Right == __value.player1Right and 
                self.player2Left == __value.player2Left and 
                self.player2Right == __value.player2Right and 
                self.turn == __value.turn)
    

# QQQ Might have to come back to this, because we might need to make 0 for a tie instead of it not being over yet
# Define a function to check if a game state is a terminal state
def isTerminalPlay(gameState):
    # Return true if the game is in a truly terminal state (not loops)
    if gameState.player1Left == 0 and gameState.player1Right == 0:
        return True
    elif gameState.player2Left == 0 and gameState.player2Right == 0:
        return True
    else:
        return False
    # Check if the state is a terminal state
    # if gameState.player1Left == 0 and gameState.player1Right == 0:
    #     return -1
    # elif gameState.player2Left == 0 and gameState.player2Right == 0:
    #     return 1
    # else:
    #     return 0
    
def isTerminal2(gameState):
    # Check if the game is over
    if gameState.player1Left == 0 and gameState.player1Right == 0:
        return player2Str
    elif gameState.player2Left == 0 and gameState.player2Right == 0:
        return player1Str
    # Check if the state is in any of the previous states
    elif gameState in gameState.previousStates:
        return drawStr
    else:
        return contStr
    

# NOTE: All of this code was written assuming that for player 1, the hand 1,3 is different from 3,1
# Function to get the possible next states for the default rules (get possible next moves)
def getPossibleNextStatesForDefaultRules(currentState, rollover=True):

    # Define a variable to hold the next states
    nextStates = []

    # If it's a terminal state # 2
    terminal = isTerminal2(currentState)
    if terminal == player1Str or terminal == player2Str or terminal == drawStr:
        return nextStates
    # If it's contStr, we can continue

    # # If it's a terminal state, return an empty list
    # if isTerminal(currentState) != 0:
    #     return nextStates

    # Gotta switch the turn
    if currentState.turn == 1:
        nextTurn = 2
    else:
        nextTurn = 1

    # ---> ATTACKS --- --- ---
    # Set the attack and defense values
    if currentState.turn == 1:
        attack = (currentState.player1Left, currentState.player1Right)
        defense = (currentState.player2Left, currentState.player2Right)
    else:
        attack = (currentState.player2Left, currentState.player2Right)
        defense = (currentState.player1Left, currentState.player1Right)

    # If the attack values are the same, remove one of them
    if attack[0] == attack[1]:
        attack = (attack[0],)

    for attVal in attack:
        # If the hand is empty, we can't attack with it
        if attVal == 0:
            continue

        for index, defVal in enumerate(defense):
            # If a hand is empty, we can't attack it
            if defVal == 0:
                continue

            # Do the attack
            newVal = attVal + defVal
            if newVal >= 5:
                if rollover:
                    # This is the rollover way:
                    newVal = newVal - 5
                else:
                    # This is the cutoff way:
                    newVal = 0
                # # QQQ This is the rollover way:
                # newVal = newVal - 5
                # # This is the cutoff way:
                # # newVal = 0

            # Make the new state
            if currentState.turn == 1:
                # Player 1 attacking
                if index == 0:
                    # Attacking player 2's left hand
                    newState = GameState(currentState.player1Left, currentState.player1Right, newVal, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
                else:
                    # Attacking player 2's right hand
                    newState = GameState(currentState.player1Left, currentState.player1Right, currentState.player2Left, newVal, nextTurn, currentState.previousStates + [currentState])
            else:
                # Player 2 attacking
                if index == 0:
                    # Attacking player 1's left hand
                    newState = GameState(newVal, currentState.player1Right, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
                else:
                    # Attacking player 1's right hand
                    newState = GameState(currentState.player1Left, newVal, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            
            # Add the new state to the list of next states
            nextStates.append(newState)



    # DIVISIONS AND TRANSFERS
     # Set the left and right values
    if currentState.turn == 1:
        left = currentState.player1Left
        right = currentState.player1Right
    else:
        left = currentState.player2Left
        right = currentState.player2Right

    # ---> DIVISIONS --- --- ---
    # If one of the hands is zero, get the other hand
    nonzero = -1
    if left == 0:
        nonzero = right
    elif right == 0:
        nonzero = left

    # If 1 hand is zero, and the other is not, we can divide
    if nonzero != -1:
        # Switch on the right hand
        if nonzero == 2:
            # 1 and 1 dvision
            if currentState.turn == 1:
                newState = GameState(1, 1, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            else:
                newState = GameState(currentState.player1Left, currentState.player1Right, 1, 1, nextTurn, currentState.previousStates + [currentState])
            # Add the new state
            nextStates.append(newState)
        elif nonzero == 3:
            # 2 and 1 division
            if currentState.turn == 1:
                newState1 = GameState(2, 1, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(1, 2, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 2, 1, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 1, 2, nextTurn, currentState.previousStates + [currentState])
            # Add the new states
            nextStates.append(newState1)
            nextStates.append(newState2)
        elif nonzero == 4:
            # 3 and 1 division
            if currentState.turn == 1:
                newState1 = GameState(3, 1, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(1, 3, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 3, 1, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 1, 3, nextTurn, currentState.previousStates + [currentState])
            # Add the new states
            nextStates.append(newState1)
            nextStates.append(newState2)
            # 2 and 2 division
            if currentState.turn == 1:
                newState = GameState(2, 2, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            else:
                newState = GameState(currentState.player1Left, currentState.player1Right, 2, 2, nextTurn, currentState.previousStates + [currentState])
            # Add the new state
            nextStates.append(newState)

    # ---> TRANSFERS --- --- ---
    # If sum of hands is 4, 5 or 6, we can transfer
    total = left + right

    if total == 4:
        # Sum is 4, we have 4 transfers
        # 13 --> 22
        # 31 --> 22
        # 22 --> 31
        # 22 --> 13
        if left == 1 or left == 3:
            # 13 --> 22
            # 31 --> 22
            if currentState.turn == 1:
                newState = GameState(2, 2, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            else:
                newState = GameState(currentState.player1Left, currentState.player1Right, 2, 2, nextTurn, currentState.previousStates + [currentState])
            # Add the new state
            nextStates.append(newState)
        elif left == 2:
            # 22 --> 31
            # 22 --> 13
            if currentState.turn == 1:
                newState1 = GameState(3, 1, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(1, 3, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 3, 1, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 1, 3, nextTurn, currentState.previousStates + [currentState])
            # Add the new states
            nextStates.append(newState1)
            nextStates.append(newState2)
    elif total == 5:
        # Sum is 5, we have 8 transfers
        # 14 --> 23
        # 14 --> 32
        # 41 --> 23
        # 41 --> 32

        # 23 --> 14
        # 23 --> 41
        # 32 --> 14
        # 32 --> 41
        if left == 1 or left == 4:
            # 14 --> 23
            # 14 --> 32
            # or
            # 41 --> 23
            # 41 --> 32
            if currentState.turn == 1:
                newState1 = GameState(2, 3, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(3, 2, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 2, 3, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 3, 2, nextTurn, currentState.previousStates + [currentState])
            # Add the new states
            nextStates.append(newState1)
            nextStates.append(newState2)
        elif left == 2 or left == 3:
            # 23 --> 14
            # 23 --> 41
            # or
            # 32 --> 14
            # 32 --> 41
            if currentState.turn == 1:
                newState1 = GameState(1, 4, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(4, 1, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 1, 4, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 4, 1, nextTurn, currentState.previousStates + [currentState])
            # Add the new states
            nextStates.append(newState1)
            nextStates.append(newState2)
    elif total == 6:
        # If the sum is 6, we have 4 transfers
        # 24 --> 33
        # 42 --> 33
        # 33 --> 24
        # 33 --> 42
        if left == 2 or left == 4:
            # 24 --> 33
            # 42 --> 33
            if currentState.turn == 1:
                newState = GameState(3, 3, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            else:
                newState = GameState(currentState.player1Left, currentState.player1Right, 3, 3, nextTurn, currentState.previousStates + [currentState])
            # Add the new state
            nextStates.append(newState)
        elif left == 3:
            # 33 --> 24
            # 33 --> 42
            if currentState.turn == 1:
                newState1 = GameState(2, 4, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(4, 2, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 2, 4, nextTurn, currentState.previousStates + [currentState])
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 4, 2, nextTurn, currentState.previousStates + [currentState])
            # Add the new states
            nextStates.append(newState1)
            nextStates.append(newState2)


    # ---> SUICIDES --- --- ---
    # If right and left are nonzero, they can be combined to either hand
    if left != 0 and right != 0 and total < 5:
        if currentState.turn == 1:
            newState1 = GameState(0, total, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
            newState2 = GameState(total, 0, currentState.player2Left, currentState.player2Right, nextTurn, currentState.previousStates + [currentState])
        else:
            newState1 = GameState(currentState.player1Left, currentState.player1Right, 0, total, nextTurn, currentState.previousStates + [currentState])
            newState2 = GameState(currentState.player1Left, currentState.player1Right, total, 0, nextTurn, currentState.previousStates + [currentState])
        # Add the new states
        nextStates.append(newState1)
        nextStates.append(newState2)
        

    # After all that, return the list of next states
    return nextStates



def minimax(currentState, depth):

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
        for nextState in getPossibleNextStatesForDefaultRules(currentState):
            score = minimax(nextState, depth + 1)
            bestScore = max(score, bestScore)
        return bestScore
    else: # It's plater 2's turn, so minimizing
        bestScore = arbitraryHighValue
        for nextState in getPossibleNextStatesForDefaultRules(currentState):
            score = minimax(nextState, depth + 1)
            bestScore = min(score, bestScore)
        return bestScore


def findThePolicy(currentState):
    bestScore = -arbitraryHighValue
    bestNextState = None

    for nextState in getPossibleNextStatesForDefaultRules(currentState):
        score = minimax(nextState, 0)
        if score > bestScore:
            bestScore = score
            bestNextState = nextState
    return bestNextState

def assessPossibleMoves(currentState):

    print("Running assessment...")

    listOfNextMoveTuples = []

    for nextState in getPossibleNextStatesForDefaultRules(currentState):
        score = minimax(nextState, 0)
        listOfNextMoveTuples.append((nextState, score))
    
    # Print the assessment
    print("=== === === === === MARK === === === === ===")
    print(f"CURRENT State: {currentState}")
    print(f"Number of Possible Moves: {len(listOfNextMoveTuples)}")
    print("")
    for item in listOfNextMoveTuples:
        print(f"For State: {item[0]}   -->   {item[1]}")
    print("")
    print(f"Key:   1 = Player 1 wins,   -1 = Player 2 wins,   {drawVal} = Draw (ie loop state),   {depthLimitVal} = Depth Limit Reached")
    print("\n")
    return listOfNextMoveTuples


def validate(validationPath, outputPath):
    # Function to validate using the paper
    print("\nBeginning validation...\n")

    tupleList = []

    lineCount = 0

    # Open the file
    with open(validationPath, 'r') as file:
        for line in file:
            # Print the current line
            lineCount += 1
            print(f"---> Testing line {lineCount}")

            # Strip the line
            line = line.strip()

            # Now test the game state
            testState = GameState(int(line[0]), int(line[1]), int(line[3]), int(line[4]), 1)
            score = minimax(testState, 0)

            # Add the tuple to the list
            tupleList.append((line, score))

    # Export the results
    print("\n === === === === === RESULTS === === === === ===")
    with open(outputPath, 'w') as file:
        for item in tupleList:
            file.write(str(item[1]) + "\n")
            print(f"For State: {item[0]}   -->   {item[1]}")
    print("")
    print(f"Key:   1 = Player 1 wins,   -1 = Player 2 wins,   {drawVal} = Draw (ie loop state),   {depthLimitVal} = Depth Limit Reached")
    print("\n")

def analyze(resultsPath):

    # Initialize the counts
    winCount = 0
    loseCount = 0
    drawCount = 0
    depthLimitCount = 0
    errCount = 0

    # Open the file of the results
    with open(resultsPath, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '1':
                winCount += 1
            elif line == '-1':
                loseCount += 1
            elif line == str(drawVal):
                drawCount += 1
            elif line == str(depthLimitVal):
                depthLimitCount += 1
            else:
                errCount += 1

    # Print the results
    print(f"For File: {resultsPath}")
    print(f"Win Count: {winCount}")
    print(f"Lose Count: {loseCount}")
    print(f"Draw Count: {drawCount}")
    print(f"Depth Limit Count: {depthLimitCount}")
    print(f"Error Count: {errCount}")
    totalCount = winCount + loseCount + drawCount + depthLimitCount + errCount
    print(f"Total Count: {totalCount}")
    return winCount, loseCount, drawCount, depthLimitCount, errCount, totalCount

            
def run():
    print("Validate: winning")
    validate('winning.txt', 'results/winning-results.txt')
    print("Validate: losing")
    validate('losing.txt', 'results/losing-results.txt')
    print("Validate: draws")
    # Change the draw value then run draws
    depthLimitVal = 0.01
    validate('draw.txt', 'results/draw-results.txt')

    print("\nAnalyze: winning")
    winCount, loseCount, drawCount, depthLimitCount, errCount, totalCount = analyze('results/winning-results.txt')
    print(f"Accuracy: {winCount / totalCount}")
    print("\nAnalyze: losing")
    winCount, loseCount, drawCount, depthLimitCount, errCount, totalCount = analyze('results/losing-results.txt')
    print(f"Accuracy: {loseCount / totalCount}")
    print("\nAnalyze: draw")
    winCount, loseCount, drawCount, depthLimitCount, errCount, totalCount = analyze('results/draw-results.txt')
    print(f"Accuracy: {drawCount / totalCount}")


# # Current State: GS: P1(0, 4) P2(3, 3) T:1
# testState = GameState(0, 4, 3, 3, 1)
# # assessPossibleMoves(testState)
# # print(getPossibleNextStatesForDefaultRules(testState))

# print(f"Current State: {testState}")

# for item in getPossibleNextStatesForDefaultRules(testState):
#     print(item)




# QQQ The draws are never going to work (because of the nature of how we find a draw, we're jumping in the game halfway through so it's not going to have a whole history to check for a loop)

run()

# Testing:
# testState = GameState(0, 3, 0, 4, 1)
# assessPossibleMoves(testState)


# print("Validate: winning")
# validate('winning.txt', 'results/winning-results.txt')
# print("Validate: losing")
# validate('losing.txt', 'results/losing-results.txt')
# print("Validate: draws")
# validate('draw.txt', 'results/draw-results.txt')

# print("\nAnalyze: winning")
# winCount, loseCount, drawCount, depthLimitCount, errCount, totalCount = analyze('results/winning-results.txt')
# print(f"Accuracy: {winCount / totalCount}")
# print("\nAnalyze: losing")
# winCount, loseCount, drawCount, depthLimitCount, errCount, totalCount = analyze('results/losing-results.txt')
# print(f"Accuracy: {loseCount / totalCount}")
# print("\nAnalyze: draw")
# winCount, loseCount, drawCount, depthLimitCount, errCount, totalCount = analyze('results/draw-results.txt')
# print(f"Accuracy: {drawCount / totalCount}")








# testState1 = GameState(0, 1, 0, 4, 1)
# testState2 = GameState(0, 1, 1, 4, 1)
# testState3 = GameState(0, 2, 0, 1, 1)
# testState4 = GameState(0, 2, 0, 3, 1)
# testState5 = GameState(0, 2, 0, 4, 1)
# assessPossibleMoves(testState1)
# assessPossibleMoves(testState2)
# assessPossibleMoves(testState3)
# assessPossibleMoves(testState4)
# assessPossibleMoves(testState5)

# print("=== === === === === START === === === === ===")
# # DEFINE THE CURRENT STATE
# testState = GameState(1, 1, 1, 1, 1)

# # TESTING
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")

# # print("POLICY:")
# # print(findThePolicy(testState))

# print("ASSESSING POSSIBLE MOVES:")
# assessment = assessPossibleMoves(testState)
# for item in assessment:
#     print(f"FOR STATE: {item[0]}   -->   {item[1]}")

# print("\n")

# print("=== === === === === ROUND 2 === === === === ===")
# # DEFINE THE CURRENT STATE
# testState = possible[0]
# # testState = GameState(0, 2, 0, 1, 2)

# # TESTING
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")

# # print("POLICY:")
# # print(findThePolicy(testState))

# print("ASSESSING POSSIBLE MOVES:")
# assessment = assessPossibleMoves(testState)
# for item in assessment:
#     print(f"FOR STATE: {item[0]} --> {item[1]}")

# print("\n")


# print("=== === === === === ROUND 3 === === === === ===")
# # DEFINE THE CURRENT STATE
# testState = possible[1]
# # testState = GameState(0, 2, 0, 1, 2)

# # TESTING
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")

# # print("POLICY:")
# # print(findThePolicy(testState))

# print("ASSESSING POSSIBLE MOVES:")
# assessment = assessPossibleMoves(testState)
# for item in assessment:
#     print(f"FOR STATE: {item[0]} --> {item[1]}")

# print("\n")

# print("=== === === === === ROUND 4 === === === === ===")
# # DEFINE THE CURRENT STATE
# testState = possible[1]
# # testState = GameState(0, 2, 0, 1, 2)

# # TESTING
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")

# # print("POLICY:")
# # print(findThePolicy(testState))

# print("ASSESSING POSSIBLE MOVES:")
# assessment = assessPossibleMoves(testState)
# for item in assessment:
#     print(f"FOR STATE: {item[0]} --> {item[1]}")

# print("\n")

# print("=== === === === === ROUND 5 === === === === ===")
# # DEFINE THE CURRENT STATE
# testState = possible[1]
# # testState = GameState(0, 2, 0, 1, 2)

# # TESTING
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")

# # print("POLICY:")
# # print(findThePolicy(testState))

# print("ASSESSING POSSIBLE MOVES:")
# assessment = assessPossibleMoves(testState)
# for item in assessment:
#     print(f"FOR STATE: {item[0]} --> {item[1]}")

# print("\n")










# # TESTING THE NEXT STATES
# print("Testing next states:")
# print("=== === === === === ROUND 1 === === === === ===")
# testState = GameState(1, 1, 1, 1, 1)
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")
# print(possible)
# print("\n")

# print("=== === === === === ROUND 2 === === === === ===")
# testState = possible[0]
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")
# print(possible)
# print("\n")

# print("=== === === === === ROUND 3 === === === === ===")
# testState = possible[0]
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")
# print(possible)
# print("\n")

# print("=== === === === === ROUND 4 === === === === ===")
# testState = possible[0]
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")
# print(possible)
# print("\n")

# print("=== === === === === ROUND 5 === === === === ===")
# testState = possible[0]
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")
# print(possible)
# print("\n")

# print("=== === === === === ROUND 6 === === === === ===")
# testState = possible[0]
# possible = getPossibleNextStatesForDefaultRules(testState)
# print(f"CURRENT: {testState}")
# print(f"Length: {len(possible)}")
# print("")
# for state in possible:
#     print(state)
# print("")
# print(possible)
# print("\n")