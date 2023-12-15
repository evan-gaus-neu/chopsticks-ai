# cs-4100-final

Evan Gaus, Alex Reed - Final project for CS 4100

## Playing Chopsticks

To play the game against the AI, run the file `play.py`

When you run `play.py`, you'll be prompted to answer a couple questions about how you want to play. The first is which search algorithm you want the computer to use. The next is about the variations of the game you would like to play, choosing to allow suicides or rollover.

The game then begins - you are player 1, and the computer is player 2. The state of the game will be printed as follows:

```
Current State: GS: P1(1, 1) P2(1, 1) T:1
```

`P1(1, 1)` represents player one's (your) hands, with a 1 on each hand. `P2(1, 1)` represents player two's (the computer) hands. `T:1` denotes that it's player one's turn.

Listed below that will be the following:

```
Number of Possible Moves: 4:
0: GS: P1(1, 1) P2(2, 1) T:2   -->   0.2
1: GS: P1(1, 1) P2(1, 2) T:2   -->   0.2
2: GS: P1(0, 2) P2(1, 1) T:2   -->   0.1
3: GS: P1(2, 0) P2(1, 1) T:2   -->   0.1

Key:   1 = Player 1 wins,   -1 = Player 2 wins,   0.1 = Draw (ie loop state),   0.2 = Depth Limit Reached

Which move do you want to make (type only the index number of the move you wish to make):
```

This represents all your possible moves when it's your turn. The list of game states provided shows the possible next game states, and the number following the arrow represents the search algorithm's assessment of each move, according to the key provided.

To make your move, type the index of the move you wish to make. Then it will be the computer's turn. The computer is faced with a similar state, it will print out its possible moves and the assessment, and then choose whichever most benefits itself. It will then loop back to your turn, until either one of you wins the game, at which point a message will be printed!

## Running the Analysis

To analyze the accuracy of the AI, run the file `analytics.py`

When you run `analytics.py`, you will be prompted whether you want to re run the validation step (which can around 10 minutes depending on the search algorithm and your machine).

If you choose to re-validate by submitting `y`, you will be asked which search algorithm you'd like to validate. Depending on your choice, the program will then run the analysis from each of the positions identified in the study, winning, losing, then draw states. The output will be saved in the results folder according to which search algortihm was chosen. Analytics on the results will then be run.

For ease of use, the data has already been validated, and the outputs have been saved into text files in their respective folders.

You can skip the revalidation phase, and only analyze the results by submitting `n`. This will run analysis on the output of each search algorithm from the various positions, measuring the accuracy of each algorithm for the 3 different types of states.