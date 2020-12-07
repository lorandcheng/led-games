# Standard library imports
import copy
import os
import random 
import sys
# Third party imports

# Other file imports
#sys.path.append("~\led-games\client\src\controller.py")
import controller

class Checkers():
    def __init__(self):
        '''
        Summary: Initializes attributes

        Attributes:
            self.name: the name of the game
            self.BOARD: the gameboard
            self.color: the color of this player
            self.redCounter: score of red player
            self.blackCounter: score of black player
        '''
        self.name = 'Checkers'
        # Codes: -2 red king, -1 red,  0 empty,  1 black, 2 black king
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
        # self.BOARD = [
        #     [ 0,  0,  0, -1,  0, -1,  0, -1], 
        #     [-1,  0,  1,  0, -1,  0, -1,  0], 
        #     [ 0, -1,  0, -1,  0,  0,  0, -1], 
        #     [ 0,  0, -1,  0, -1,  0,  0,  0], 
        #     [ 0,  0,  0,  2,  0,  0,  0,  0], 
        #     [ 1,  0, -1,  0, -1,  0,  1,  0], 
        #     [ 0,  0,  0,  1,  0,  0,  0,  1], 
        #     [ 1,  0,  1,  0,  1,  0,  1,  0], 
        # ]
        self.color = 1
        self.redCounter = 12
        self.blackCounter = 12
        self.busy = 1
        self.done = 0

    def isOnBoard(self, row, col):
        if not(0 <= row <= 7):
            return False
        if not(0 <= col <= 7):
            return False
        return True

    def findPieces(self):
        '''
        Summary: finds all available pieces to move

        Return: 
            locations (list of tuples): coordinates of available pieces
        '''
        val = self.color
        locs = []
        for r in range(8):
            for c in range(8):
                if val * self.BOARD[r][c] > 0:
                    if self.findJumps((r,c)):
                        locs.append((r,c))

        if len(locs):
            return locs

        for r in range(8):
            for c in range(8):
                if val * self.BOARD[r][c] > 0:
                    if self.findMoves((r,c)):
                        locs.append((r,c))
        return locs

    def findMoves(self, location):
        '''
        Summary: finds all possible moves 1 square away (non-jumping) for a given piece

        Args:
            location (tuple): coordinates of piece to check

        Returns:
            locs (list of tuples): if there are any moves available, returns coordinates of possible moves
            0: returns zero if there are no possible moves
        '''

        row, col = location
        locs = []
        # if the piece is a king, check four diagonals, otherwise check only two in front
        if abs(self.BOARD[row][col]) == 2:
            checks = [
                (-1 * self.color, -1),
                (-1 * self.color,  1),
                ( 1 * self.color, -1),
                ( 1 * self.color,  1)
            ]
        else:
            checks = [
                (-1 * self.color, -1),
                (-1 * self.color,  1),
            ]

        # for each of the diagonals to check, verify:
        #   - 1 square away is on the board
        #   - 1 square away is empty
        for r,c in checks:
            if (self.isOnBoard(row + r, col + c)
            and self.BOARD[row + r][col + c] == 0):
                locs.append((row + r, col + c))
            
        return 0 if len(locs) == 0 else locs

    def findJumps(self, location):
        '''
        Summary: checks to see if there are any jump moves for a given piece

        Args:
            location (tuple): coordinates of piece to check

        Returns:
            locs (list of tuples): if there are any jump moves available, returns coordinates of possible moves
            0: returns zero if there are no possible moves
        '''

        row, col = location
        locs= []
        # if the piece is a king, check four diagonals, otherwise check only two in front
        if abs(self.BOARD[row][col]) == 2:
            checks = [
                (-1 * self.color, -1),
                (-1 * self.color,  1),
                ( 1 * self.color, -1),
                ( 1 * self.color,  1)
            ]
        else:
            checks = [
                (-1 * self.color, -1),
                (-1 * self.color,  1),
            ]

        # for each of the diagonals to check, verify:
        #   - 1 square away is on the board
        #   - 1 square away contains opponent
        #   - 2 squares away is on the board
        #   - 2 squares away is empty
        # then add to locs any that pass all four
        for r,c in checks:
            if (
                self.isOnBoard(row + r, col + c)
            and self.BOARD[row + r][col + c] * self.color < 0
            and self.isOnBoard(row + 2 * r, col + 2 * c)
            and self.BOARD[row + 2 * r][col + 2 * c] * self.color == 0
            ): 
                locs.append((row + 2 * r, col + 2 * c))

        return 0 if len(locs) == 0 else locs

    def selectLocation(self, locations):
        '''
        Summary: prompts user to cycle through given locations and select one. 'a' and 'd' to cycle through, 'e' to select

        Args:
            locations (list of tuples): list of locations to cycle through  

        Return: 
            (row, col) (tuple): coordinates of selected location  
        '''

        # copy board for display, initialize variables
        tempBoard = copy.deepcopy(self.BOARD)
        inp = ""
        index = 0
        #print(locations)
        row, col = locations[index]

        # print first view
        for r,c in locations:
            tempBoard[r][c] = "*"
        tempBoard[row][col] = "X"
        self.printBoard(tempBoard)

        # allow user to loop through inputs and select location
        while True:
            inp = controller.getInput()
            try:
                index += inp
            except TypeError:
                break
            if index > len(locations)-1:
                index = 0
            elif index < 0:
                index = len(locations)-1
            row, col = locations[index]
            # refresh view
            for r,c in locations:
                tempBoard[r][c] = "*"
            tempBoard[row][col] = "X"
            self.printBoard(tempBoard)

        # display final selection
        tempBoard = copy.deepcopy(self.BOARD) 
        tempBoard[row][col] = "X"
        self.printBoard(tempBoard)
        # return selected coordinates
        return (row, col)

    def makeMove(self, location, final):
        '''
        Summary: makes a single move or hop, updates board and counters

        Args:
            location (tuple): initial location
            final (tuple): final location
        '''
        rowI, colI = location # initial row, col
        rowF, colF = final # final row, col
        piece = self.BOARD[rowI][colI]
        if (abs(rowI - rowF)) > 1: # if a piece was hopped, remove piece and decrement counter
            self.BOARD[int((rowI+rowF)/2)][int((colI+colF)/2)] = 0
            if self.color == 1:
                self.redCounter -= 1
            else:
                self.blackCounter -= 1
        
        if rowF == 0 and piece == 1:
            piece = 2
        elif rowF == 7 and piece == -1:
            piece = -2

        # update board
        self.BOARD[final[0]][final[1]] = piece
        self.BOARD[location[0]][location[1]] = 0

            
    def endTurn(self):
        '''
        Summary: actions at the end of the turn
        '''
        print("ending turn")
        self.busy = 0


    def gameOver(self, winner):
        '''
        Summary: actions at the end of the game

        Args:
            winner (boolean): true if this player won
        '''
        self.printBoard(self.BOARD)
        print("GAME OVER")
        if winner:
            print("YOU WON")
        else:
            print("YOU LOST")

    def printBoard(self, board):
        '''
        Summary: prints the given board

        Args:
            board (2D list): the board stored in a 2D array
        '''
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
        print("Black: " + str(self.blackCounter) + " Red: " + str(self.redCounter) )
        if self.color == -1:
            print("\nRED's turn to move")
        else:
            print("\nBLACK's turn to move")
        print("Use 'a' and 'd' to cycle, 'e' to select")

    def main(self):
        '''
        Summary: play a game of checkers
        '''
        # print initial setup
        # self.printBoard(self.BOARD)
        # play game until someone loses all pieces
        while self.redCounter > 0 and self.blackCounter > 0 and self.busy == 1:
            # select piece to move
            pieces = self.findPieces()
            pieceLocation = self.selectLocation(pieces)
            # make move(s)
            possibleJumps = self.findJumps(pieceLocation)
            if possibleJumps:
                while possibleJumps:
                    moveLocation = self.selectLocation(possibleJumps)
                    self.makeMove(pieceLocation, moveLocation)
                    pieceLocation = moveLocation
                    possibleJumps = self.findJumps(pieceLocation)
            else:
                possibleMoves = self.findMoves(pieceLocation)
                moveLocation = self.selectLocation(possibleMoves)
                self.makeMove(pieceLocation, moveLocation)
            
            # switch colors
            self.endTurn()

            # switch back to your turn
            
        # Fix this: determine who won the game and set self.done = 1 when games is voer

        # if self.color == 1 and self.blackCounter > 0:
        #     self.gameOver(True)
        # elif self.color == -1 and self.redCounter > 0:
        #     self.gameOver(True)
        # else:
        #     self.gameOver(False)
        # self.done = 1



if __name__ == '__main__':
    '''
    FOR TESTING PURPOSES ONLY. USE main.py FOR ACTUAL RUNTIME:
    python3 -m main
    '''

    # comment out import controller at the top of the file
    import sys
    sys.path.append('..')
    import controller
    game = Checkers()
    game.main()