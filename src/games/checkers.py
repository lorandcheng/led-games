# Standard library imports
import copy
import os
import random 
import sys
# Third party imports

# Other file imports
#from main.py import receive callback, send function

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

        self.color = random.choice([-1, 1])
        self.redCounter = 12
        self.blackCounter = 12
        

    def selectLocation(self, locations):
        '''
        Summary: prompts user to cycle through given locations and select one. 'a' and 'd' to cycle through, 'e' to select

        Args:
            locations (list of tuples): list of locations to cycle through  

        Return: 
            selection (tuple): coordinates of selected location  
        '''
        tempBoard = copy.deepcopy(self.BOARD)
        length  = len(locations)
        inp = ""
        index = 0
        row, column = locations[index]
        for r,c in locations:
            tempBoard[r][c] = "*"
        tempBoard[row][column] = "X"
        self.printBoard(tempBoard)
        while inp != "e":
            inp = input()
            if inp == 'a':
                index -= 1
            elif inp == 'd':
                index += 1
            elif inp == 'e':
                pass
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
        tempBoard = copy.deepcopy(self.BOARD) 
        tempBoard[row][column] = "X"
        self.printBoard(tempBoard)
        return selection

    def canJump(self, location):
        
        row, col = location
        locs= []
        a = -1*self.color
        b = 1
        c = -1
        d = self.color
        checks = [(a,b),(a,c)]
        self.printBoard(self.BOARD)
        if abs(self.BOARD[row][col]) == 2:
            checks.append((d,b))
            checks.append((d,c))

        for r,k in checks:
            if self.isOnBoard(row + r, col + k): #is the piece you might jump over on baord
                if self.BOARD[row + r][col + k]*self.color < 0: # is piece opposing piece
                    if self.isOnBoard(row + 2*r,col + 2*k): # is landing spot on board
                        if self.BOARD[row + 2*r][col+ 2*k]*self.color == 0: # is landing spot empty
                            locs.append((row + 2*r,col + 2*k))
        if len(locs) == 0:
            return 0
        return locs


        

    def findPieces(self):
        '''
        Summary: finds all available pieces to move

        Return: 
            locations (list of tuples): coordinates of available pieces
        '''
        val = self.color
        locations = []
        for r in range(8):
            for c in range(8):
                if val * self.BOARD[r][c] > 0:
                    if self.canJump((r,c)):
                        locations.append((r,c))

        if len(locations):
            return locations

        for r in range(8):
            for c in range(8):
                if val * self.BOARD[r][c] > 0:
                    # TODO if findMoves((r,c)) != 0:
                    if self.findMoves((r,c)):
                        locations.append((r,c))
        return locations

    def isOnBoard(self, row, col):
        if not(0 <= row <= 7):
            return False
        if not(0 <= col <= 7):
            return False
        return True

    def isEmpty(self, row, col):
        if self.BOARD[row][col] == 0:
            return True
        return False

    def findMoves(self, location):
        '''
        Summary: finds all possible moves, jumping or non-jumping, for a given piece

        Args:
            pieceLocation (tuple): coordinates of the piece to move

        Returns:
            locs (list of tuples): coordinates of possible moves
            -1: if there are no possible moves for the given piece
        '''
        row, col = location
        locs = []

        if self.isOnBoard(row-self.color,col+1) and self.isEmpty(row-self.color,col+1):
            locs.append((row-self.color,col+1))

        if self.isOnBoard(row-self.color,col-1) and self.isEmpty(row-self.color,col-1):
            locs.append((row-self.color,col-1))
        
        if abs(self.BOARD[row][col]) == 2:
            if self.isOnBoard(row+self.color,col+1) and self.isEmpty(row+self.color,col+1):
                locs.append((row+self.color,col+1))

            if self.isOnBoard(row+self.color,col-1) and self.isEmpty(row+self.color,col-1):
                locs.append((row+self.color,col-1))
            
        if len(locs) == 0:
            return 0
        else:
            return locs

    def makeMove(self, location, final): #TODO add make king
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
        pass

    def makeKing(self, location):
        '''
        Summary: promotes piece to a King

        Args:
            location (tuple): coordinates of piece to promote
        '''
        row,col = location
        self.BOARD[row][col] *= 2

    def gameOver(self, winner):
        '''
        Summary: actions at the end of the game

        Args:
            winner (boolean): true if this player won
        '''
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
        print(str(self.color) + " Black: " + str(self.blackCounter) + " Red: " + str(self.redCounter) )
    


    def main(self):
        self.printBoard(self.BOARD)
        while self.redCounter > 0 and self.blackCounter > 0:
            pieces = self.findPieces()
            pieceLocation = self.selectLocation(pieces)
            
            hasJumped = 0
            hasMoved = 0
            
            while True:
                possibleMoves = self.canJump(pieceLocation)
                if hasJumped == 0:
                    if not possibleMoves:
                        possibleMoves = self.findMoves(pieceLocation)
                        hasMoved = 1
                        hasJumped = 0
                    else:
                        hasJumped = 1
                if possibleMoves == 0:
                    break
                moveLocation = self.selectLocation(possibleMoves)
                self.makeMove(pieceLocation, moveLocation)
                pieceLocation = moveLocation
                if hasMoved:
                    break

            self.color *= -1
            print("switch turns")
            
        if self.color == 1 and self.blackCounter > 0:
            self.gameOver(True)
        elif self.color == -1 and self.redCounter > 0:
            self.gameOver(True)
        else:
            self.gameOver(False)

if __name__ == '__main__':
    '''
    FOR TESTING PURPOSES ONLY. USE main.py FOR ACTUAL RUNTIME
    '''
    game = Checkers()
    game.main()