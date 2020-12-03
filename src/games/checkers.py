import os
import copy
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
        self.yourTurn = 1
    
    # def __copy__(self):
    #     newInstance = Checkers()
    #     newInstance.BOARD = copy.deepcopy(self.BOARD)
    #     return newInstance

    def selectLocation(self, locations):
        #select a position of tuple from list of tuples
        tempBoard = copy.deepcopy(self.BOARD)
        length  = len(locations)
        inp = ""
        index = 0
        while inp != "e":
            inp = input()
            if inp == 'a':
                index -= 1
            elif inp == 'd':
                index += 1
            else:
                print("invalid input")
            if index >= length:
                index = 0
            elif index <= -1:
                index = length-1
            row, column = locations[index]
            for r,c in locations:
                tempBoard[r][c] = "*"
            tempBoard[row][column] = "X"
            self.printBoard(tempBoard)
            selection = (row, column)
        tempBoard = copy.copy(self.BOARD) 
        tempBoard[row][column] = "X"
        self.printBoard(tempBoard)
        print(self.BOARD)
        return selection

    def findPieces(self):
        val = self.color
        location = []
        for r in range(8):
            for c in range(8):
                if val * self.BOARD[r][c] > 0:
                    location.append((r,c))
        return location

    def findMoves(self):
        # return coordinates of possible final moves
        
        pass

    def makeMove(self, location, final):
        # update board to move piece and remove any hopped pieces
        # call findMoves again
        rowI, colI = location
        rowF, colF = final

        if (abs(rowI - rowF)) > 1:
            self.BOARD[(rowI+rowF)/2][(colI+colF)/2] = 0
            if self.color == 1:
                self.redCounter -= 1
            else:
                self.blackCounter -= 1

        self.BOARD[final[0]][final[1]] = self.color
        self.BOARD[location[0]][location[1]] = 0

            
    def endTurn(self):
        # send info to opponent
        pass

    def makeKing(self, location):
        row,col = location
        self.BOARD[row][col] *= 2

    def gameOver(self, winner):
        # send final message to end game
        print("GAME OVER")
        if winner:
            print("YOU WON")
        else:
            print("YOU LOST")

    def printBoard(self, board):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n+---+---+---+---+---+---+---+---+')
        for r in range(8):
            row = '|'
            for c in range(8):
                if board[r][c] == 2:
                    row += ' B |'
                elif board[r][c] == -2:
                    row += ' R |'
                elif board[r][c] == 1:
                    row += ' b |'
                elif board[r][c] == -1:
                    row += ' r |'
                elif board[r][c] == '*':
                    row += ' * |'
                elif board[r][c] == 'X':
                    row += ' X |'
                else:
                    row += '   |'
            print(row)
            print('+---+---+---+---+---+---+---+---+')
    
    def switchColor(self):
        if self.color == 1:
            self.color = -1
        elif self.color == -1:
            self.color = 1

    def main(self):
        self.printBoard(self.BOARD)
        while self.redCounter > 0 and self.blackCounter > 0:
            pieces = self.findPieces()
            pieceLocation = self.selectLocation(pieces)
            possibleMoves = self.findMoves(pieceLocation)
            moveLocation = self.selectLocation(possibleMoves)
            self.makeMove(pieceLocation, moveLocation)
            self.switchColor()
        if self.color == 1 and self.blackCounter > 0:
            self.gameOver(True)
        elif self.color == 0 and self.redCounter > 0:
            self.gameOver(True)
        else:
            self.gameOver(False)

if __name__ == '__main__':
    game = Checkers()
    game.main()
