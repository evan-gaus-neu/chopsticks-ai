# model.py

# Evan Gaus, Alex Reed --> Model.py contains all the necessary code for the chopsticks game
# NOTE: All of this code was written assuming that for player 1, the hand 1,3 is different from 3,1

# Import
import random

# VALUES
arbitraryHighValue = 1000
player1Val = 1
player2Val = -1
drawVal = 0.1
depthLimitVal = 0.2

analyticsDepthLimit = 10
playDepthLimit = 9

monteCarloSimulations = 5000

player1Str = 'PLAYER1'
player2Str = 'PLAYER2'
drawStr = 'DRAW'
contStr = 'CONTINUE'

minimaxStr = 'MINIMAX'
expectimaxStr = 'EXPECTIMAX'
monteCarloStr = 'MONTECARLO'


# CLASSES

# Define a class to represent the game state
# Player One Left
# Player One Right
# Player Two Left
# Player Two Right
# Who's turn it is (1 or 2)
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
    
    def __eq__(self, __value: object) -> bool:
        # Return True if the game states are equal
        if not isinstance(__value, GameState):
            return NotImplemented
        
        return (self.player1Left == __value.player1Left and 
                self.player1Right == __value.player1Right and 
                self.player2Left == __value.player2Left and 
                self.player2Right == __value.player2Right and 
                self.turn == __value.turn)


# FUNCTIONS

# Checks if the game is truly in a terminal state, to end the playback
def stateIsTerminal(gameState):
    # Return true if the game is in a truly terminal state (not loops)
    if gameState.player1Left == 0 and gameState.player1Right == 0:
        return True
    elif gameState.player2Left == 0 and gameState.player2Right == 0:
        return True
    else:
        return False

# Returns a string to represent the status of the game (ie including loops)
def getStatusStr(gameState):
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

# Gets the possible next states for the current state of the game
# Allows you to specifiy whether or not to allow suicides (default is True)
# Allows you to specify whether or not to allow rollover (default is True)
# Allows you to specify whether or not to allow looping (default is True) (Looping necessary (TRUE) for playing, not for analytics)
def getPossibleNextStates(currentState, allowSuicides=True, allowRollover=True, allowLooping=True):

    # Define a variable to hold the next states
    nextStates = []

    # Check the status of the game
    status = getStatusStr(currentState)
    if status == player1Str or status == player2Str:
        return nextStates # The game is truly over
    if status == drawStr and not allowLooping:
        return nextStates # The game is over if we don't allow looping
    # If it's contStr, we can continue

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
                if allowRollover:
                    # This is the rollover way:
                    newVal = newVal - 5
                else:
                    # This is the cutoff way:
                    newVal = 0

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

    # Check if suicides are allowed
    if allowSuicides:
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

# Minimax function to search possible states
def minimax(currentState, depth, allowSuicides=True, allowRollover=True, allowLooping=True):

    # Get the status at the current state
    status = getStatusStr(currentState)
    if status == player1Str:
        return player1Val
    elif status == player2Str:
        return player2Val
    elif status == drawStr:
        return drawVal

    # Check if we've reached the depth limit
    if allowLooping:
        # Use play depth limit
        if depth >= playDepthLimit:
            return depthLimitVal
    else:
        # Use analytics depth limit
        if depth >= analyticsDepthLimit:
            return depthLimitVal
    
    # If it's player 1's turn, we're maximizing
    if currentState.turn == 1:
        bestScore = -arbitraryHighValue
        for nextState in getPossibleNextStates(currentState, allowSuicides, allowRollover, allowLooping):
            score = minimax(nextState, depth + 1, allowSuicides, allowRollover, allowLooping)
            bestScore = max(score, bestScore)
        return bestScore
    else: # It's player 2's turn, so minimizing
        bestScore = arbitraryHighValue
        for nextState in getPossibleNextStates(currentState, allowSuicides, allowRollover, allowLooping):
            score = minimax(nextState, depth + 1, allowSuicides, allowRollover, allowLooping)
            bestScore = min(score, bestScore)
        return bestScore

# Expectimax function to search possible states
def expectimax(currentState, depth, allowSuicides=True, allowRollover=True, allowLooping=True):

    # Get the status at the current state
    status = getStatusStr(currentState)
    if status == player1Str:
        return player1Val
    elif status == player2Str:
        return player2Val
    elif status == drawStr:
        return drawVal

    # Check if we've reached the depth limit
    if allowLooping:
        # Use play depth limit
        if depth >= playDepthLimit:
            return depthLimitVal
    else:
        # Use analytics depth limit
        if depth >= analyticsDepthLimit:
            return depthLimitVal
    
    # If it's player 1's turn, we're maximizing
    if currentState.turn == 1:
        totalScore = 0
        for nextState in getPossibleNextStates(currentState, allowSuicides, allowRollover, allowLooping):
            score = expectimax(nextState, depth + 1, allowSuicides, allowRollover, allowLooping)
            totalScore += score
        numOfNextStates = len(getPossibleNextStates(currentState, allowSuicides, allowRollover, allowLooping))
        if numOfNextStates != 0:
            return totalScore / numOfNextStates
        else:
            return 0
    else: # It's plater 2's turn, so minimizing
        totalScore = 0
        for nextState in getPossibleNextStates(currentState, allowSuicides, allowRollover, allowLooping):
            score = expectimax(nextState, depth + 1, allowSuicides, allowRollover, allowLooping)
            totalScore += score
        numOfNextStates = len(getPossibleNextStates(currentState, allowSuicides, allowRollover, allowLooping))
        if numOfNextStates != 0:
            return totalScore / numOfNextStates
        else:
            return 0

# Monte Carlo function to search possible states
def monteCarlo(currentState, depth, allowSuicides=True, allowRollover=True, allowLooping=True):
    
    # Get the status at the current state
    status = getStatusStr(currentState)
    if status == player1Str:
        return player1Val
    elif status == player2Str:
        return player2Val
    elif status == drawStr:
        return drawVal
    

    # If it's player 1's turn, we're maximizing
    if currentState.turn == 1:
        # Define variables
        bestNextState = None
        bestWinRate = -float('inf')

        # Loop through next states
        for nextState in getPossibleNextStates(currentState, allowSuicides, allowRollover, allowLooping):
            # Define wins
            wins = 0.0

            for _ in range(monteCarloSimulations):
                # Simulate random game returns the outcome of the game
                wins += simulateRandomGame(nextState, depth, allowSuicides, allowRollover, allowLooping)

            # Get the win rate for this state
            winRate = wins / monteCarloSimulations

            if winRate > bestWinRate:
                bestWinRate = winRate
                bestNextState = nextState
        return bestWinRate
    else: # It's plater 2's turn, so minimizing
        # Define variables
        worstNextState = None
        worstWinRate = float('inf')

        # Loop through next states
        for nextState in getPossibleNextStates(currentState, allowSuicides, allowRollover, allowLooping):
            # Define wins
            wins = 0.0

            for _ in range(monteCarloSimulations):
                # Simulate random game returns the outcome of the game
                wins += simulateRandomGame(nextState, depth, allowSuicides, allowRollover, allowLooping)

            # Get the win rate for this state
            winRate = wins / monteCarloSimulations

            if winRate < worstWinRate:
                worstWinRate = winRate
                worstNextState = nextState
        return worstWinRate
    

# Monte Carlo Helper --> Simulates a random game for {DEPTH LIMIT} steps from the given state, return the outcome
def simulateRandomGame(currentState, depth, allowSuicides, allowRollover, allowLooping):

    # Get the status at the current state
    status = getStatusStr(currentState)
    if status == player1Str:
        return player1Val
    elif status == player2Str:
        return player2Val
    elif status == drawStr:
        return drawVal

    # Check if we've reached the depth limit
    if allowLooping:
        # Use play depth limit
        if depth >= playDepthLimit:
            return depthLimitVal
    else:
        # Use analytics depth limit
        if depth >= analyticsDepthLimit:
            return depthLimitVal

    # Get the next states
    nextStates = getPossibleNextStates(currentState, allowSuicides, allowRollover, allowLooping)

    # Make sure there are next states
    if len(nextStates) == 0:
        return 0

    # Choose a random next state
    randomNextState = random.choice(nextStates)

    # Call the function recursively
    return simulateRandomGame(randomNextState, depth + 1, allowSuicides, allowRollover, allowLooping)


# Function to assess the possible next moves using specified search algorithm (default is minimax)
def assessPossibleMoves(currentState, searchAlgo=minimaxStr, allowSuicides=True, allowRollover=True, allowLooping=True):

    # Set the search algorithm
    if searchAlgo == minimaxStr:
        searchFunc = minimax
    elif searchAlgo == expectimaxStr:
        searchFunc = expectimax
    elif searchAlgo == monteCarloStr:
        searchFunc = monteCarlo
    else:
        print("ERROR: Invalid search algorithm, defaulting to minimax")
        searchFunc = minimax

    print("Running assessment...")

    listOfNextMoveTuples = []

    for nextState in getPossibleNextStates(currentState, allowSuicides, allowRollover, allowLooping):
        score = searchFunc(nextState, 0, allowSuicides, allowRollover, allowLooping)
        listOfNextMoveTuples.append((nextState, score))
    
    # Print the assessment
    print(f"Number of Possible Moves: {len(listOfNextMoveTuples)}:")
    for index, item in enumerate(listOfNextMoveTuples):
        print(f"{index}: {item[0]}   -->   {item[1]}")
    print("")
    print(f"Key:   {player1Val} = Player 1 wins,   {player2Val} = Player 2 wins,   {drawVal} = Draw (ie loop state),   {depthLimitVal} = Depth Limit Reached")
    return listOfNextMoveTuples