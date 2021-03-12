def getInt(msg):
    '''Get integer from stdin.'''
    while True:
        try:
            integer = int(input(msg))
            return integer
        except:
            print("Please enter an integer")

class Player:
    def __init__(self, piece):
        self.piece = piece

    def name(self):
        '''Return name'''
        return "Human"
    
    def play(self, board):
        '''Reads an input from console and plays accordingly.

board is a Board object.'''
        while True:
            try:
                r = getInt(" Row (1-3): ")
                c = getInt(" Column (1-3): ")
                board.play(r - 1, c - 1)
                return
            except Exception as e:
                print(str(e))