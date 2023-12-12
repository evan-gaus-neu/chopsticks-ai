# analytics.py

# Imports
import model

# Evan Gaus, Alex Reed --> Run this file to run the analytics of the different algorithms
# NOTE: The way we analyze the draws, they're never going to be successfully found via our algorithms
# (We're jumping in the game halfway through at the specificed "draw" state, so it's not going to have a whole history to check for a loop)
# We kept the analytics to show that (for minimax), it doesn't find any wins or losses, as is expected


# Set useMinimax to false to use expectimax
# Function to validate our minimax algorithm using data from the paper
def validate(validationPath, outputPath, searchAlgo=model.minimaxStr):

    print("\nBeginning validation...\n")

    # Set the search algorithm
    if searchAlgo == model.minimaxStr:
        searchFunc = model.minimax
    elif searchAlgo == model.expectimaxStr:
        searchFunc = model.expectimax
    elif searchAlgo == model.monteCarloStr:
        searchFunc = model.monteCarlo
    else:
        print("ERROR: Invalid search algorithm, defaulting to minimax")
        searchFunc = model.minimax

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
            testState = model.GameState(int(line[0]), int(line[1]), int(line[3]), int(line[4]), 1)
            score = searchFunc(testState, 0, True, True, False)
            
            # Add the tuple to the list
            tupleList.append((line, score))

    # Export the results
    print("\n === === === === === RESULTS === === === === ===")
    with open(outputPath, 'w') as file:
        for item in tupleList:
            file.write(str(item[1]) + "\n")
            print(f"For State: {item[0]}   -->   {item[1]}")
    print("")
    print(f"Key:   {model.player1Val} = Player 1 wins,   {model.player2Val} = Player 2 wins,   {model.drawVal} = Draw (ie loop state),   {model.depthLimitVal} = Depth Limit Reached")
    print("\n")


# Function to analyze the results of the validation
def analyze(resultsPath, searchAlgo=model.minimaxStr):

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

            if searchAlgo == model.minimaxStr:
                if line == '1':
                    winCount += 1
                elif line == '-1':
                    loseCount += 1
                elif line == str(model.drawVal):
                    drawCount += 1
                elif line == str(model.depthLimitVal):
                    depthLimitCount += 1
                else:
                    errCount += 1
            else:
                # Other algo
                lineAsNum = float(line)
                if lineAsNum >= 0:
                    winCount += 1
                else:
                    loseCount += 1

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


# Function to run the validation   
def runValidation(searchType):
    print("Validate: winning")
    validate('data/winning.txt', searchType + '-results/winning-results.txt', searchType)
    print("Validate: losing")
    validate('data/losing.txt', searchType + '-results/losing-results.txt', searchType)
    print("Validate: draws")
    validate('data/draw.txt', searchType + '-results/draw-results.txt', searchType)


# Function to run the analytics
def runAnalytics():
    listOfSearchTypes = [model.minimaxStr, model.expectimaxStr, model.monteCarloStr]
    for searchType in listOfSearchTypes:
        print(f"\n--- --- --- --- --- {searchType} --- --- --- --- ---")
        print(f"\nAnalyze: winning")
        winCount, loseCount, drawCount, depthLimitCount, errCount, totalCount = analyze(searchType + '-results/winning-results.txt', searchType)
        print(f"--> Accuracy: {winCount / totalCount}")
        print(f"\nAnalyze: losing")
        winCount, loseCount, drawCount, depthLimitCount, errCount, totalCount = analyze(searchType + '-results/losing-results.txt', searchType)
        print(f"--> Accuracy: {loseCount / totalCount}")
        print(f"\nAnalyze: draw")
        winCount, loseCount, drawCount, depthLimitCount, errCount, totalCount = analyze(searchType + '-results/draw-results.txt', searchType)
        print(f"--> Accuracy: {drawCount / totalCount}")
        print("")


# MAIN RUN CODE

print("\nWelcome to Chopsticks Analytics!\n")
print("Validation takes a while (about 7 minutes, depending on the algorithm). You can instead skip validation and just run analytics")
validationInput = input("Would you like to re-validate (Takes 7 min) (y/n)?\n")

if validationInput == 'y' or validationInput == 'Y':
    # Run validation
    print("\nWould you like to validate with:\n(0) Minimax\n(1) Expectimax\n(2) Monte Carlo\n")
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

    print("Now Running Validation...")
    runValidation(searchType)
elif validationInput == 'n' or validationInput == 'N':
    # Skip validation
    print("\nSkipping validation...\n")
else:
    # Skip validation
    print("\nInvalid input, defaulting to no re-validation\n")

# Run the analytics
print("Now Running Analytics...")
runAnalytics()