# main.py

# Evan Gaus, Alex Reed

# Define a class to represent the game state
# Player One Left = P1L
# Player One Right = P1R
# Player Two Left = P2L
# Player Two Right = P2R
# Who's turn it is = turn (1 or 2)
class GameState:
    def __init__(self, player1Left, player1Right, player2Left, player2Right, turn) -> None:
        # Initialize the game state
        self.player1Left = player1Left
        self.player1Right = player1Right
        self.player2Left = player2Left
        self.player2Right = player2Right
        self.turn = turn

    def __repr__(self) -> str:
        # Return a string representation of the game state
        return f"GS: P1({self.player1Left}, {self.player1Right}) P2({self.player2Left}, {self.player2Right}) T:{self.turn}"
        # return f"GS: [{self.player1Left}, {self.player1Right}, {self.player2Left}, {self.player2Right}, {self.turn}]"
        # return f"GameState(player1Left={self.player1Left}, player1Right={self.player1Right}, player2Left={self.player2Left}, player2Right={self.player2Right}, turn={self.turn})"
    
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
def isTerminal(gameState):
    # Check if the state is a terminal state
    if gameState.player1Left == 0 and gameState.player1Right == 0:
        return -1
    elif gameState.player2Left == 0 and gameState.player2Right == 0:
        return 1
    else:
        return 0
    

# NOTE: All of this code was written assuming that for player 1, the hand 1,3 is different from 3,1
# Function to get the possible next states for the default rules (get possible next moves)
def getPossibleNextStatesForDefaultRules(currentState):

    # Define a variable to hold the next states
    nextStates = []

    # If it's a terminal state, return an empty list
    if isTerminal(currentState) != 0:
        return nextStates

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
                newVal = 0

            # Make the new state
            if currentState.turn == 1:
                # Player 1 attacking
                if index == 0:
                    # Attacking player 2's left hand
                    newState = GameState(currentState.player1Left, currentState.player1Right, newVal, currentState.player2Right, nextTurn)
                else:
                    # Attacking player 2's right hand
                    newState = GameState(currentState.player1Left, currentState.player1Right, currentState.player2Left, newVal, nextTurn)
            else:
                # Player 2 attacking
                if index == 0:
                    # Attacking player 1's left hand
                    newState = GameState(newVal, currentState.player1Right, currentState.player2Left, currentState.player2Right, nextTurn)
                else:
                    # Attacking player 1's right hand
                    newState = GameState(currentState.player1Left, newVal, currentState.player2Left, currentState.player2Right, nextTurn)
            
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
                newState = GameState(1, 1, currentState.player2Left, currentState.player2Right, nextTurn)
            else:
                newState = GameState(currentState.player1Left, currentState.player1Right, 1, 1, nextTurn)
            # Add the new state
            nextStates.append(newState)
        elif nonzero == 3:
            # 2 and 1 division
            if currentState.turn == 1:
                newState1 = GameState(2, 1, currentState.player2Left, currentState.player2Right, nextTurn)
                newState2 = GameState(1, 2, currentState.player2Left, currentState.player2Right, nextTurn)
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 2, 1, nextTurn)
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 1, 2, nextTurn)
            # Add the new states
            nextStates.append(newState1)
            nextStates.append(newState2)
        elif nonzero == 4:
            # 3 and 1 division
            if currentState.turn == 1:
                newState1 = GameState(3, 1, currentState.player2Left, currentState.player2Right, nextTurn)
                newState2 = GameState(1, 3, currentState.player2Left, currentState.player2Right, nextTurn)
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 3, 1, nextTurn)
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 1, 3, nextTurn)
            # Add the new states
            nextStates.append(newState1)
            nextStates.append(newState2)
            # 2 and 2 division
            if currentState.turn == 1:
                newState = GameState(2, 2, currentState.player2Left, currentState.player2Right, nextTurn)
            else:
                newState = GameState(currentState.player1Left, currentState.player1Right, 2, 2, nextTurn)

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
                newState = GameState(2, 2, currentState.player2Left, currentState.player2Right, nextTurn)
            else:
                newState = GameState(currentState.player1Left, currentState.player1Right, 2, 2, nextTurn)
            # Add the new state
            nextStates.append(newState)
        elif left == 2:
            # 22 --> 31
            # 22 --> 13
            if currentState.turn == 1:
                newState1 = GameState(3, 1, currentState.player2Left, currentState.player2Right, nextTurn)
                newState2 = GameState(1, 3, currentState.player2Left, currentState.player2Right, nextTurn)
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 3, 1, nextTurn)
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 1, 3, nextTurn)
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
                newState1 = GameState(2, 3, currentState.player2Left, currentState.player2Right, nextTurn)
                newState2 = GameState(3, 2, currentState.player2Left, currentState.player2Right, nextTurn)
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 2, 3, nextTurn)
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 3, 2, nextTurn)
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
                newState1 = GameState(1, 4, currentState.player2Left, currentState.player2Right, nextTurn)
                newState2 = GameState(4, 1, currentState.player2Left, currentState.player2Right, nextTurn)
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 1, 4, nextTurn)
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 4, 1, nextTurn)
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
                newState = GameState(3, 3, currentState.player2Left, currentState.player2Right, nextTurn)
            else:
                newState = GameState(currentState.player1Left, currentState.player1Right, 3, 3, nextTurn)
            # Add the new state
            nextStates.append(newState)
        elif left == 3:
            # 33 --> 24
            # 33 --> 42
            if currentState.turn == 1:
                newState1 = GameState(2, 4, currentState.player2Left, currentState.player2Right, nextTurn)
                newState2 = GameState(4, 2, currentState.player2Left, currentState.player2Right, nextTurn)
            else:
                newState1 = GameState(currentState.player1Left, currentState.player1Right, 2, 4, nextTurn)
                newState2 = GameState(currentState.player1Left, currentState.player1Right, 4, 2, nextTurn)
            # Add the new states
            nextStates.append(newState1)
            nextStates.append(newState2)


    # ---> SUICIDES --- --- ---
    # If right and left are nonzero, they can be combined to either hand
    # if left != 0 and right != 0 and total < 5:
    #     if currentState.turn == 1:
    #         newState1 = GameState(0, total, currentState.player2Left, currentState.player2Right, nextTurn)
    #         newState2 = GameState(total, 0, currentState.player2Left, currentState.player2Right, nextTurn)
    #     else:
    #         newState1 = GameState(currentState.player1Left, currentState.player1Right, 0, total, nextTurn)
    #         newState2 = GameState(currentState.player1Left, currentState.player1Right, total, 0, nextTurn)
    #     # Add the new states
    #     nextStates.append(newState1)
    #     nextStates.append(newState2)
        

    # After all that, return the list of next states
    return nextStates


# Helpful values
arbitraryHighValue = 1000
depthLimit = 10

def minimax(currentState, depth):

    # Check if the current state is a terminal state
    if isTerminal(currentState) != 0:
        return isTerminal(currentState)

    # Check if we've reached the depth limit
    if depth >= depthLimit:
        return 0
    
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

    listOfNextMoveTuples = []

    for nextState in getPossibleNextStatesForDefaultRules(currentState):
        score = minimax(nextState, 0)
        listOfNextMoveTuples.append((nextState, score))
    
    return listOfNextMoveTuples


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
# print("\n")

# # print("POLICY:")
# # print(findThePolicy(testState))

# print("ASSESSING POSSIBLE MOVES:")
# assessment = assessPossibleMoves(testState)
# for item in assessment:
#     print(f"FOR STATE: {item[0]} --> {item[1]}")


# TESTING THE NEXT STATES
print("Testing next states:")
print("=== === === === === ROUND 1 === === === === ===")
testState = GameState(1, 1, 1, 1, 1)
possible = getPossibleNextStatesForDefaultRules(testState)
print(f"CURRENT: {testState}")
print(f"Length: {len(possible)}")
print("")
for state in possible:
    print(state)
print("")
print(possible)
print("\n")

print("=== === === === === ROUND 2 === === === === ===")
testState = possible[0]
possible = getPossibleNextStatesForDefaultRules(testState)
print(f"CURRENT: {testState}")
print(f"Length: {len(possible)}")
print("")
for state in possible:
    print(state)
print("")
print(possible)
print("\n")

print("=== === === === === ROUND 3 === === === === ===")
testState = possible[0]
possible = getPossibleNextStatesForDefaultRules(testState)
print(f"CURRENT: {testState}")
print(f"Length: {len(possible)}")
print("")
for state in possible:
    print(state)
print("")
print(possible)
print("\n")

print("=== === === === === ROUND 4 === === === === ===")
testState = possible[0]
possible = getPossibleNextStatesForDefaultRules(testState)
print(f"CURRENT: {testState}")
print(f"Length: {len(possible)}")
print("")
for state in possible:
    print(state)
print("")
print(possible)
print("\n")

print("=== === === === === ROUND 5 === === === === ===")
testState = possible[0]
possible = getPossibleNextStatesForDefaultRules(testState)
print(f"CURRENT: {testState}")
print(f"Length: {len(possible)}")
print("")
for state in possible:
    print(state)
print("")
print(possible)
print("\n")

print("=== === === === === ROUND 6 === === === === ===")
testState = possible[0]
possible = getPossibleNextStatesForDefaultRules(testState)
print(f"CURRENT: {testState}")
print(f"Length: {len(possible)}")
print("")
for state in possible:
    print(state)
print("")
print(possible)
print("\n")
