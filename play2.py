# play.py

# Evan Gaus, Alex Reed --> Run this file to play chopsticks against the AI

# Imports
import model


# MAIN CODE TO RUN THE GAME

# Get Search Algorithm
print("\nWelcome to Chopsticks!\n")
print("Would you like to play with:\n(0) Minimax\n(1) Expectimax\n(2) Monte Carlo\n")
startInput = input()

if startInput == '0':
    searchType = model.minimaxStr
elif startInput == '1':
    searchType = model.expectimaxStr
elif startInput == '2':
    searchType = model.monteCarloStr
else:
    searchType = model.minimaxStr
    print("\nInvalid input, defaulting to minimax\n")

# Get the suicides option
suicidesInput = input("\nWould you like to play with suicides (y/n)?\n")
if suicidesInput == 'y' or suicidesInput == 'Y':
    suicides = True
elif suicidesInput == 'n' or suicidesInput == 'N':
    suicides = False
else:
    suicides = True
    print("\nInvalid input, defaulting to allow suicides\n")

# Get the rollover option
rolloverInput = input("\nWould you like to play with rollover (y/n)?\n")
if rolloverInput == 'y' or rolloverInput == 'Y':
    rollover = True
elif rolloverInput == 'n' or rolloverInput == 'N':
    rollover = False
else:
    rollover = False
    print("\nInvalid input, defaulting to no rollover\n")

# Set start state
currentGameState = model.GameState(1, 1, 1, 1, 1)

# Begin loop
while not model.stateIsTerminal(currentGameState):

    # PLAYER TURN
    print("===========================================")
    print("It's your turn now!")
    print(f"Current State: {currentGameState}\n")

    # Assess the possible moves
    model.assessPossibleMoves(currentGameState, searchType, suicides, rollover, True)
    print("\nWhich move do you want to make (type only the index number of the move you wish to make):")
    userInput = input()

    # User inputted a number
    userInputIndex = int(userInput)
    print(f"You made move: {userInputIndex}")

    # Update state:
    currentGameState = model.getPossibleNextStates(currentGameState, suicides, rollover, True)[userInputIndex]

    # Check if the game is over
    if model.stateIsTerminal(currentGameState):
        print("")
        break


    # COMPUTER TURN
    # Assess the possible moves:
    print("\nIt's the computer's turn now:")
    print(f"New Current State: {currentGameState}\n")

    possibleMoves = model.assessPossibleMoves(currentGameState, searchType, suicides, rollover, True)

    # Find the lowest scoring move
    minScore = model.arbitraryHighValue
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

# Check who won
status = model.getStatusStr(currentGameState)
if status == model.player1Str:
    print("Congrats, you won!\n")
elif status == model.player2Str:
    print("Sorry, you lost!\n")

# Print the final state
print(f"Final State of the game: {currentGameState}\n\n") 
