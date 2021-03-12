from tttplayer import Player
from tttboard import Board
import random
import numpy as np

class Novice(Player):
    '''Always moves randomly'''

    def __init__(self, piece):
        self.piece = piece

    def name(self):
        '''Return name'''
        return "Novice"
    
    def play(self, board):
        '''Move randomly, always.'''
        while True:
            try:
                board.play(random.randint(0, 2), random.randint(0, 2))
                return
            except:
                pass

class Intermediate(Player):
    '''Like Novice, but reacts to potential wins or losses.'''

    def __init__(self, piece):
        self.piece = piece
        self.pot = -1

    def name(self):
        '''Return name'''
        return "Intermediate"
    
    def play(self, board):
        '''React to potential wins or losses, if there are none play randomly.'''
        self.evalPot(board)
        if self.pot != -1:
            # React
            r, c = self.reactionPlay(board)
            board.play(r, c)
        else:
            # Random
            while True:
                try:
                    board.play(random.randint(0, 2), random.randint(0, 2))
                    return
                except:
                    pass

    def evalPot(self, board):
        '''Evaluate potentials, checks the board for potential win or lose
        situations and sets pot to react to them.'''
        self.pot = board.checkPotWin(self.piece)
        if self.pot == -1:
            self.pot = board.checkPotLoss(self.piece)

    def reactionPlay(self, board):
        '''Returns reaction move tuple, which is a move to either win or block a loss.'''
        # checks which cell of the line is free and chooses it
        if self.pot == 0:
            if board.getCell(0, 0) == ' ':
                return 0, 0
            elif board.getCell(0, 1) == ' ':
                return 0, 1
            else:
                return 0, 2
        elif self.pot == 1:
            if board.getCell(1, 0) == ' ':
                return 1, 0
            elif board.getCell(1, 1) == ' ':
                return 1, 1
            else:
                return 1, 2
        elif self.pot == 2:
            if board.getCell(2, 0) == ' ':
                return 2, 0
            elif board.getCell(2, 1) == ' ':
                return 2, 1
            else:
                return 2, 2
        elif self.pot == 3:
            if board.getCell(0, 0) == ' ':
                return 0, 0
            elif board.getCell(1, 0) == ' ':
                return 1, 0
            else:
                return 2, 0
        elif self.pot == 4:
            if board.getCell(0, 1) == ' ':
                return 0, 1
            elif board.getCell(1, 1) == ' ':
                return 1, 1
            else:
                return 2, 1
        elif self.pot == 5:
            if board.getCell(0, 2) == ' ':
                return 0, 2
            elif board.getCell(1, 2) == ' ':
                return 1, 2
            else:
                return 2, 2
        elif self.pot == 6:
            if board.getCell(0, 0) == ' ':
                return 0, 0
            elif board.getCell(1, 1) == ' ':
                return 1, 1
            else:
                return 2, 2
        elif self.pot == 7:
            if board.getCell(0, 2) == ' ':
                return 0, 2
            elif board.getCell(1, 1) == ' ':
                return 1, 1
            else:
                return 2, 0

    def setPot(self, pot):
        '''Sets pot to the configuration that will result in the end of the game,
        0-8 if there is one, -1 if not.'''
        self.pot = pot

class Experienced(Intermediate):
    '''Like Intermediate, but knows the safe first moves.'''

    def __init__(self, piece):
        self.piece = piece
    
    def name(self):
        '''Return name'''
        return "Experienced"
    
    def play(self, board):
        '''Go for safe first move, or play like Experienced'''
        if board.numPlays <= 1:
            # First move
            r, c = self.safeFirstPlay(board)
            board.play(r, c)
        else:
            # Subsequent moves are played exactly like Intermediate
            self.evalPot(board)
            if self.pot != -1:
                # React
                r, c = self.reactionPlay(board)
                board.play(r, c)
            else:
                # Random
                while True:
                    try:
                        board.play(random.randint(0, 2), random.randint(0, 2))
                        return
                    except:
                        pass

    def safeFirstPlay(self, board):
        '''Returns a safe move tuple for the first move of the player'''
        possibilities = []

        if self.piece == 'X':
            # Player 1
            # Play corners or center
            possibilities.extend([(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)])
        else:
            # Player 2
            if board.getCell(1, 1) == ' ':
                # Player 1 did not play center, play center
                possibilities = [(1, 1)]
            else:
                # Player 1 played center, play corner
                possibilities.extend([(0, 0), (0, 2), (2, 0), (2, 2)])

        # randomly select from possibilities
        return possibilities[random.randrange(len(possibilities))]

class Expert(Player):
    '''Looks into all possible games to determine best move.'''

    def __init__(self, piece):
        self.piece = piece
    
    def name(self):
        '''Return name'''
        return "Expert"
    
    def play(self, board):
        '''Use minimax to determine best move.'''
        maxScore = -np.inf
        maxR = -1
        maxC = -1
        for i in range(3):
            for j in range(3):
                b = board.dupe()
                try:
                    b.play(i, j)
                except:
                    continue
                score = self.minimaxAB(b, -np.inf, np.inf, False)
                if score > maxScore:
                    maxScore = score
                    maxR, maxC = i, j
        board.play(maxR, maxC)
    
    def minimaxAB(self, board, alpha, beta, maximizingPlayer):
        '''Minimax with alpha beta pruning. Returns max score
        possible for a given player.

        board is a Board object, move is a tuple (r, c), alpha is maximizing
        score, beta is minimizing score, and maximizingPlayer is a bool'''

        # Base case
        # Score is 1 for win, 0 for tie, -1 for loss
        winner = board.checkWinner()
        if winner != ' ':
            if winner == self.piece:
                return 2
            elif winner == '-':
                return 1
            else:
                return 0
        # else continue

        moves = []
        boards = []

        if maximizingPlayer:
            maxEval = -np.inf

            for r in range(3):
                for c in range(3):
                    if board.getCell(r, c) == ' ':
                        # if a move is possible register it and create a duplicate board to manipulate
                        moves.append((r, c))
                        boards.append(board.dupe())
            for i in range(len(moves)):
                # create child
                boards[i].play(moves[i][0], moves[i][1])
                # evaluate move
                evaluation = self.minimaxAB(boards[i], alpha, beta, False)
                # compare to current best (high score) move
                maxEval = max(maxEval, evaluation)
                # update alpha
                alpha = max(alpha, maxEval)
                # prune
                if beta <= alpha:
                    break
            return maxEval
            
        else:
            minEval = np.inf

            for r in range(3):
                for c in range(3):
                    if board.getCell(r, c) == ' ':
                        # if a move is possible register it and create a duplicate board to manipulate
                        moves.append((r, c))
                        boards.append(board.dupe())
            for i in range(len(moves)):
                # create child
                boards[i].play(moves[i][0], moves[i][1])
                # evaluate move
                evaluation = self.minimaxAB(boards[i], alpha, beta, True)
                 # compare to current best (low score) move
                minEval = min(minEval, evaluation)
                # update beta
                beta = min(beta, minEval)
                # prune
                if beta <= alpha:
                    break
            return minEval