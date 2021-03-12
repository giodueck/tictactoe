import copy

class Board:
    def __init__(self):
        self.reset()

    def dupe(self):
        '''Returns a duplicate board objective.'''
        return copy.deepcopy(self)
    
    def setBoard(self, board):
        '''Makes the contents of the Board object be the same as the given board's'''
        pass

    def reset(self):
        '''Initializes (or reinitializes) the board.'''
        self.grid = [ [' ',' ',' '], [' ',' ',' '], [' ',' ',' '] ]
        self.prevTurn = None
        self.turn = 'X'
        self.numPlays = 0

    def printBoard(self):
        print(" {} | {} | {}".format(self.grid[0][0], self.grid[0][1], self.grid[0][2]))
        print("---+---+---")
        print(" {} | {} | {}".format(self.grid[1][0], self.grid[1][1], self.grid[1][2]))
        print("---+---+---")
        print(" {} | {} | {}".format(self.grid[2][0], self.grid[2][1], self.grid[2][2]))
    
    def getCell(self, r, c):
        '''Returns what is held in self.grid[r][c].'''
        return self.grid[r][c]

    def play(self, r, c):
        '''Executes a play for the next player at position (r, c),
        and advances the turn'''
        if r >= 0 and r < 3 and c >= 0 and c < 3:
            if self.grid[r][c] == ' ':
                self.grid[r][c] = self.turn
                self.prevTurn = self.turn
                if self.prevTurn == 'X':
                    self.turn = 'O'
                else:
                    self.turn = 'X'
                self.numPlays += 1
            else:
                raise Exception("Already marked position")
        else:
            raise Exception("Invalid position")
    
    def checkWinner(self):
        '''Evaluates the current state of the board and returns the winner,
        which is either 'X', 'O', or '-' or ' ', in case of tie or unfinished game.'''
        # horizontals:
        if self.grid[0][0] == self.grid[0][1] == self.grid[0][2] and self.grid[0][0] != ' ':
            return self.grid[0][0]
        if self.grid[1][0] == self.grid[1][1] == self.grid[1][2] and self.grid[1][0] != ' ':
            return self.grid[1][0]
        if self.grid[2][0] == self.grid[2][1] == self.grid[2][2] and self.grid[2][0] != ' ':
            return self.grid[2][0]
        
        # verticals
        if self.grid[0][0] == self.grid[1][0] == self.grid[2][0] and self.grid[0][0] != ' ':
            return self.grid[0][0]
        if self.grid[0][1] == self.grid[1][1] == self.grid[2][1] and self.grid[0][1] != ' ':
            return self.grid[0][1]
        if self.grid[0][2] == self.grid[1][2] == self.grid[2][2] and self.grid[0][2] != ' ':
            return self.grid[0][2]

        # diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[0][0] != ' ':
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and self.grid[0][2] != ' ':
            return self.grid[0][2]
        
        # game not over
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == ' ':
                    return ' '
        
        # tie
        return '-'

    def isGameOver(self):
        '''True if the game is over.'''
        return self.checkWinner() != ' '

    def checkPotWin(self, piece):
        '''Check for potential win configurations for the given piece, returns -1 if none, 0-8 if there is one'''
        # checks cell by cell, and every configuration which includes that cell
        # and ignores cells/configurations already tested False
        # checking 5 cells already provides a cell in every configuration
        # 0 0
            # h top
        if self.grid[0][0][0] == self.grid[0][1][0] and self.grid[0][2][0] == ' ' and self.grid[0][0][0] == piece and self.grid[0][2][0] != piece \
        or self.grid[0][0][0] == self.grid[0][2][0] and self.grid[0][1][0] == ' ' and self.grid[0][0][0] == piece and self.grid[0][1][0] != piece \
        or self.grid[0][1][0] == self.grid[0][2][0] and self.grid[0][0][0] == ' ' and self.grid[0][1][0] == piece and self.grid[0][0][0] != piece:
            return 0
            # v left
        if self.grid[0][0][0] == self.grid[1][0][0] and self.grid[2][0][0] == ' ' and self.grid[0][0][0] == piece and self.grid[2][0][0] != piece \
        or self.grid[0][0][0] == self.grid[2][0][0] and self.grid[1][0][0] == ' ' and self.grid[0][0][0] == piece and self.grid[1][0][0] != piece \
        or self.grid[1][0][0] == self.grid[2][0][0] and self.grid[0][0][0] == ' ' and self.grid[1][0][0] == piece and self.grid[0][0][0] != piece:
            return 3
            # diag
        if self.grid[0][0][0] == self.grid[1][1][0] and self.grid[2][2][0] == ' ' and self.grid[0][0][0] == piece and self.grid[2][2][0] != piece \
        or self.grid[0][0][0] == self.grid[2][2][0] and self.grid[1][1][0] == ' ' and self.grid[0][0][0] == piece and self.grid[1][1][0] != piece \
        or self.grid[1][1][0] == self.grid[2][2][0] and self.grid[0][0][0] == ' ' and self.grid[1][1][0] == piece and self.grid[0][0][0] != piece:
            return 6
        # 0 1
            # v middle
        if self.grid[0][1][0] == self.grid[1][1][0] and self.grid[2][1][0] == ' ' and self.grid[0][1][0] == piece and self.grid[2][1][0] != piece \
        or self.grid[0][1][0] == self.grid[2][1][0] and self.grid[1][1][0] == ' ' and self.grid[0][1][0] == piece and self.grid[1][1][0] != piece \
        or self.grid[1][1][0] == self.grid[2][1][0] and self.grid[0][1][0] == ' ' and self.grid[1][1][0] == piece and self.grid[0][1][0] != piece:
            return 4
        # 0 2
            # v right
        if self.grid[0][2][0] == self.grid[1][2][0] and self.grid[2][2][0] == ' ' and self.grid[0][2][0] == piece and self.grid[2][2][0] != piece \
        or self.grid[0][2][0] == self.grid[2][2][0] and self.grid[1][2][0] == ' ' and self.grid[0][2][0] == piece and self.grid[1][2][0] != piece \
        or self.grid[1][2][0] == self.grid[2][2][0] and self.grid[0][2][0] == ' ' and self.grid[1][2][0] == piece and self.grid[0][2][0] != piece:
            return 5
            # anti diag
        if self.grid[0][2][0] == self.grid[1][1][0] and self.grid[2][0][0] == ' ' and self.grid[0][2][0] == piece and self.grid[2][0][0] != piece \
        or self.grid[0][2][0] == self.grid[2][0][0] and self.grid[1][1][0] == ' ' and self.grid[0][2][0] == piece and self.grid[1][1][0] != piece \
        or self.grid[1][1][0] == self.grid[2][0][0] and self.grid[0][2][0] == ' ' and self.grid[1][1][0] == piece and self.grid[0][2][0] != piece:
            return 7
        # 1 0
            # h middle
        if self.grid[1][0][0] == self.grid[1][1][0] and self.grid[1][2][0] == ' ' and self.grid[1][0][0] == piece and self.grid[1][2][0] != piece \
        or self.grid[1][0][0] == self.grid[1][2][0] and self.grid[1][1][0] == ' ' and self.grid[1][0][0] == piece and self.grid[1][1][0] != piece \
        or self.grid[1][1][0] == self.grid[1][2][0] and self.grid[1][0][0] == ' ' and self.grid[1][1][0] == piece and self.grid[1][0][0] != piece:
            return 1
        # 2 0
            # h bottom
        if self.grid[2][0][0] == self.grid[2][1][0] and self.grid[2][2][0] == ' ' and self.grid[2][0][0] == piece and self.grid[2][2][0] != piece \
        or self.grid[2][0][0] == self.grid[2][2][0] and self.grid[2][1][0] == ' ' and self.grid[2][0][0] == piece and self.grid[2][1][0] != piece \
        or self.grid[2][1][0] == self.grid[2][2][0] and self.grid[2][0][0] == ' ' and self.grid[2][1][0] == piece and self.grid[2][0][0] != piece:
            return 2

        # none found
        return -1

    def checkPotLoss(self, piece):
        '''Check for potential lose conditions for the given piece, returns -1 if none, 0-8 if there is one'''
        # checks cell by cell, and every configuration which includes that cell
        # and ignores cells/configurations already tested False
        # checking 5 cells already provides a cell in every configuration
        # 0 0
            # h top
        if self.grid[0][0][0] == self.grid[0][1][0] and self.grid[0][0][0] != ' ' and self.grid[0][0][0] != piece and self.grid[0][2][0] != piece \
        or self.grid[0][0][0] == self.grid[0][2][0] and self.grid[0][0][0] != ' ' and self.grid[0][0][0] != piece and self.grid[0][1][0] != piece \
        or self.grid[0][1][0] == self.grid[0][2][0] and self.grid[0][1][0] != ' ' and self.grid[0][1][0] != piece and self.grid[0][0][0] != piece:
            return 0
            # v left
        if self.grid[0][0][0] == self.grid[1][0][0] and self.grid[0][0][0] != ' ' and self.grid[0][0][0] != piece and self.grid[2][0][0] != piece \
        or self.grid[0][0][0] == self.grid[2][0][0] and self.grid[0][0][0] != ' ' and self.grid[0][0][0] != piece and self.grid[1][0][0] != piece \
        or self.grid[1][0][0] == self.grid[2][0][0] and self.grid[1][0][0] != ' ' and self.grid[1][0][0] != piece and self.grid[0][0][0] != piece:
            return 3
            # diag
        if self.grid[0][0][0] == self.grid[1][1][0] and self.grid[0][0][0] != ' ' and self.grid[0][0][0] != piece and self.grid[2][2][0] != piece \
        or self.grid[0][0][0] == self.grid[2][2][0] and self.grid[0][0][0] != ' ' and self.grid[0][0][0] != piece and self.grid[1][1][0] != piece \
        or self.grid[1][1][0] == self.grid[2][2][0] and self.grid[1][1][0] != ' ' and self.grid[1][1][0] != piece and self.grid[0][0][0] != piece:
            return 6
        # 0 1
            # v middle
        if self.grid[0][1][0] == self.grid[1][1][0] and self.grid[0][1][0] != ' ' and self.grid[0][1][0] != piece and self.grid[2][1][0] != piece \
        or self.grid[0][1][0] == self.grid[2][1][0] and self.grid[0][1][0] != ' ' and self.grid[0][1][0] != piece and self.grid[1][1][0] != piece \
        or self.grid[1][1][0] == self.grid[2][1][0] and self.grid[1][1][0] != ' ' and self.grid[1][1][0] != piece and self.grid[0][1][0] != piece:
            return 4
        # 0 2
            # v right
        if self.grid[0][2][0] == self.grid[1][2][0] and self.grid[0][2][0] != ' ' and self.grid[0][2][0] != piece and self.grid[2][2][0] != piece \
        or self.grid[0][2][0] == self.grid[2][2][0] and self.grid[0][2][0] != ' ' and self.grid[0][2][0] != piece and self.grid[1][2][0] != piece \
        or self.grid[1][2][0] == self.grid[2][2][0] and self.grid[1][2][0] != ' ' and self.grid[1][2][0] != piece and self.grid[0][2][0] != piece:
            return 5
            # anti diag
        if self.grid[0][2][0] == self.grid[1][1][0] and self.grid[0][2][0] != ' ' and self.grid[0][2][0] != piece and self.grid[2][0][0] != piece \
        or self.grid[0][2][0] == self.grid[2][0][0] and self.grid[0][2][0] != ' ' and self.grid[0][2][0] != piece and self.grid[1][1][0] != piece \
        or self.grid[1][1][0] == self.grid[2][0][0] and self.grid[1][1][0] != ' ' and self.grid[1][1][0] != piece and self.grid[0][2][0] != piece:
            return 7
        # 1 0
            # h middle
        if self.grid[1][0][0] == self.grid[1][1][0] and self.grid[1][0][0] != ' ' and self.grid[1][0][0] != piece and self.grid[1][2][0] != piece \
        or self.grid[1][0][0] == self.grid[1][2][0] and self.grid[1][0][0] != ' ' and self.grid[1][0][0] != piece and self.grid[1][1][0] != piece \
        or self.grid[1][1][0] == self.grid[1][2][0] and self.grid[1][1][0] != ' ' and self.grid[1][1][0] != piece and self.grid[1][0][0] != piece:
            return 1
        # 2 0
            # h bottom
        if self.grid[2][0][0] == self.grid[2][1][0] and self.grid[2][0][0] != ' ' and self.grid[2][0][0] != piece and self.grid[2][2][0] != piece \
        or self.grid[2][0][0] == self.grid[2][2][0] and self.grid[2][0][0] != ' ' and self.grid[2][0][0] != piece and self.grid[2][1][0] != piece \
        or self.grid[2][1][0] == self.grid[2][2][0] and self.grid[2][1][0] != ' ' and self.grid[2][1][0] != piece and self.grid[2][0][0] != piece:
            return 2

        # none found
        return -1