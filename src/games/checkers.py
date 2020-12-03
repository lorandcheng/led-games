
class Checkers():
    def __init__(self):
        # -1 red,  0 empty,  1 black
        self.BOARD = [
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
        rowI, colI = location
        rowF, colF = final

        if (abs(rowI - rowF)) > 1:
            self.BOARD[(rowI+rowF)/2][(colI+colF)/2] = 0
            if self.BOARD[rowI][colI] == 1:
                self.redCounter -= 1
            else:
                self.blackCounter -= 1

        self.BOARD[final[0]][final[1]] = self.color
        self.BOARD[location[0]][location[1]] = 0

            
    def endTurn(self):
        # send info to opponent
        pass

    def makeKing(self, location):
        pass

    def gameOver(self, winner):
        # send final message to end game
        pass

    def printBoard(self):
        print('+---+---+---+---+---+---+---+---+')
        for r in range(8):
            row = '|'
            for c in range(8):
                if self.BOARD[r][c] == 2:
                    row += ' B |'
                elif self.BOARD[r][c] == -2:
                    row += ' R |'
                elif self.BOARD[r][c] == 1:
                    row += ' b |'
                elif self.BOARD[r][c] == -1:
                    row += ' r |'
                else:
                    row += '   |'
            print(row)
            print('+---+---+---+---+---+---+---+---+')
    
    def main(self):
        self.printBoard()
        while self.redCounter > 0 and self.blackCounter > 0:
            pieces = self.findPieces()
            pieceLocation = self.selectLocation(pieces)
            possibleMoves = self.findMoves(pieceLocation)
            moveLocation = self.selectLocation(possibleMoves)






if __name__ == '__main__':
    game = Checkers()
    game.main()