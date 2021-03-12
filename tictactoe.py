# TODO
##   finish game logic
##   pretty ui up
##  exception handling
#   sophisticated ai
##       novice
##       intermediate
##       experienced
#       expert
#           minimax avoids losing but favors ties over wins
#           makes bad moves if opponent makes a mistake and does not capitalize
##   put players and ai into seperate classes, and
##    allow selection of any player or ai for both players 1 and 2
##   pit ai against ai
##   make running multiple AvA games and recording scores possible

import os
clear = lambda: os.system("cls")
from tttboard import Board
from tttplayer import *
from tttai import Novice
from tttai import Intermediate
from tttai import Experienced
from tttai import Expert

board = Board()
n_plays = 0
turn = 0

# 0,0  0,1  0,2
# 1,0  1,1  1,2
# 2,0  2,1  2,2

#  X | O | X
# ---+---+---
#  O | X | O
# ---+---+---
#  X | O | X

def printBoard(gameNumber, turn = None):
    global players
    if gameNumber != 0:
        print("Game {}".format(gameNumber))
    if turn == None:
        print("{} is {}, {} is {}".format('X', players[0].name(), 'O', players[1].name()))
    else:
        print("{} is {}, {} is {}".format('X', players[0].name(), 'O', players[1].name()))
        print("Turn: {}".format(turn))
    board.printBoard()

# Setup
aiConstructors = [ Novice, Intermediate, Experienced, Expert ] 
players = []
humanPlaying = False

# Set player 1
clear()
while True:
    try:
        p1 = getInt(" Choose player 1: 1 is human, 2 is computer: ")
        if p1 == 1:
            players.append(Player('X'))
            humanPlaying = True
        elif p1 == 2:
            while True:
                try:
                    p1 = getInt(" Choose computer skill level: 0 is Novice, 1 is Intermediate, 2 is Experienced, 3 is Expert: ")
                    if p1 < 0 or p1 > len(aiConstructors) - 1:
                        raise Exception("Please choose from one of the options.")
                    else:
                        players.append(aiConstructors[p1]('X'))
                        break
                except Exception as e:
                    print(str(e))
        else:
            raise Exception("Please choose from one of the options.")
        break
    except Exception as e:
        print(str(e))

# Set player 2
clear()
while True:
    try:
        p2 = getInt(" Choose player 2: 1 is human, 2 is computer: ")
        if p2 == 1:
            players.append(Player('O'))
            humanPlaying = True
        elif p2 == 2:
            while True:
                try:
                    p2 = getInt(" Choose computer skill level: 0 is Novice, 1 is Intermediate, 2 is Experienced, 3 is Expert: ")
                    if p2 < 0 or p2 > len(aiConstructors) - 1:
                        raise Exception("Please choose from one of the options.")
                    else:
                        players.append(aiConstructors[p2]('O'))
                        break
                except Exception as e:
                    print(str(e))
        break
    except Exception as e:
        print(str(e))

# Set number of games
clear()
while True:
    try:
        numGames = getInt(" Number of games (0 quits): ")
        if numGames < 0:
            raise Exception("Please enter a positive number")
        else:
            break
    except Exception as e:
        print(str(e))

# If no human players are present give option to omit printing the board
drawBoard = True
if not humanPlaying:
    while True:
        try:
            a = input(" No human players, do you want to skip drawing the board? (Y/n): ")
            if a != 'Y' and a != 'n':
                raise Exception("Please choose from one of the options.")
            else:
                if a == 'Y':
                    drawBoard = False
                else:
                    drawBoard = True
                break
        except Exception as e:
            print(str(e))

# Stats initialization
numXWins = 0
numOWins = 0
numTies = 0

# Gameloop
clear()
for game in range(numGames):
    while True:
        clear()
        if drawBoard:
            printBoard(game + 1, board.turn)
        else:
            print("Game {} of {}".format(game, numGames))

        # Move
        players[board.turn == 'O'].play(board)
        
        # Check for end of game
        if board.isGameOver():
            if drawBoard:
                clear()
                printBoard(game + 1)
            winner = board.checkWinner()
            if winner == 'X':
                if drawBoard:
                    print("Player 1 wins!")
                numXWins += 1
            elif winner == 'O':
                if drawBoard:
                    print("Player 2 wins!")
                numOWins += 1
            else:
                if drawBoard:
                    print("Draw!")
                numTies += 1
            if humanPlaying:
                if game < numGames - 1:
                    input("\nEnter to continue to next game...")
                else:
                    input ("\nEnter to continue to stats...")
            board.reset()
            break

# Stats display
if numGames > 0:
    clear()
    print("Games: {}".format(numGames))
    print("Player 1 ({}) wins: {}, %.2f%%".format(players[0].name(), numXWins) % ((numXWins/numGames)*100))
    print("Player 2 ({}) wins: {}, %.2f%%".format(players[1].name(), numOWins) % ((numOWins/numGames)*100))
    print("Ties: {}, %.2f%%\n".format(numTies) % ((numTies/numGames)*100))