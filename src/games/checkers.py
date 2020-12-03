
class Checkers():
    def __init__(self):
        # -1 red,  0 empty,  1 black
        BOARD = [
            [ 0, -1,  0, -1,  0, -1,  0, -1], 
            [-1,  0, -1,  0, -1,  0, -1,  0], 
            [ 0, -1,  0, -1,  0, -1,  0, -1], 
            [ 0,  0,  0,  0,  0,  0,  0,  0], 
            [ 0,  0,  0,  0,  0,  0,  0,  0], 
            [ 1,  0,  1,  0,  1,  0,  1,  0], 
            [ 0,  1,  0,  1,  0,  1,  0,  1], 
            [ 1,  0,  1,  0,  1,  0,  1,  0], 
        ]
        self.color = 1 # TODO change to random assignment
        self.redCounter = 12
        self.blackCounter = 12

    def selectLocation(self):
        #select location with mouse
        pass

    def findMoves(self, location):
        # return coordinates of possible final moves
        pass

    def makeMove(self, location, final):
        # update board to move piece and remove any hopped pieces
        # call findMoves again
        pass

    def endTurn(self):
        # send info to opponent
        pass

    def makeKing(self, location):
        pass

    def gameOver(self, winner):
        # send final message to end game
        pass

    def printBoard(self):
        for r in range(8):
            for c in range(8):
                print()
    