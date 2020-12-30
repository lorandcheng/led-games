# Standard library imports
import copy
import sys
# Third party imports

# Other file imports
sys.path.append('..')
import inputs

class Checkers:
    """
    Summary: Checkers game module
    """
    def __init__(self, output):
        """
        Summary: Initializes attributes

        Attributes:
            self.name: the name of the game  
            self.output: output to write to  
            self.BOARD: the gameboard  
            self.color: the color of this player  
            self.redCounter: score of red player  
            self.blackCounter: score of black player  
            self.done: whether the game is over
        """
        self.name = 'Checkers'
        self.output = output
        
        # Gameboard codes: -2 red king, -1 red,  0 empty,  1 black, 2 black king

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

        # End of game test board

        # self.BOARD = [
        #     [-2,  0,  0,  0,  0,  0,  0,  0], 
        #     [ 0,  0,  0,  0,  0,  0,  0,  0], 
        #     [ 0,  0,  0,  0,  0,  0,  0,  2], 
        #     [ 0,  0,  0, -1,  0,  0,  0,  0], 
        #     [ 0,  0,  0,  0,  1,  0,  0,  0], 
        #     [ 0,  0,  0,  0,  0,  0,  0,  0], 
        #     [ 0,  1,  0,  0,  0,  0,  0,  0], 
        #     [ 0,  0,  0,  0,  0,  0,  0,  0], 
        # ]

        self.color = -1
        self.redCounter = 12
        self.blackCounter = 12
        self.updateScores()
        self.done = False


    def updateScores(self):
        """
        Summary: Updates scores based on pieces in self.BOARD
        """
        self.redCounter = 0
        self.blackCounter = 0
        for r in range(8):
            for c in range(8):
                if self.BOARD[r][c] > 0:
                    self.blackCounter += 1
                elif self.BOARD[r][c] < 0:
                    self.redCounter += 1


    def parseData(self, data):
        """
        Summary: Processes string game board into array format
        """
        message = str(data.payload, 'utf-8')
        message = message[2:len(message)-2]

        rows = message.split("], [")
        j = 0
        for element in rows:
            vals = element.split(", ")
            
            for i in range(8):
                self.BOARD[j][i] = int(vals[i])
            j+=1


    def isOnBoard(self, row, col):
        """
        Summary: checks if a given coordinate is on the board
        
        Returns: True or False
        """
        if not(0 <= row <= 7):
            return False
        if not(0 <= col <= 7):
            return False
        return True


    def findPieces(self):
        """
        Summary: finds all available pieces to move

        Return: 
            locations (list of tuples): coordinates of available pieces
        """
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
        """
        Summary: finds all possible moves 1 square away (non-jumping) for a given piece

        Args:
            location (tuple): coordinates of piece to check

        Returns:
            locs (list of tuples): if there are any moves available, returns coordinates of possible moves
            0: returns zero if there are no possible moves
        """

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
        """
        Summary: checks to see if there are any jump moves for a given piece

        Args:
            location (tuple): coordinates of piece to check

        Returns:
            locs (list of tuples): if there are any jump moves available, returns coordinates of possible moves
            0: returns zero if there are no possible moves
        """

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
        """
        Summary: prompts user to cycle through given locations and select one. Arrow keys to cycle through, enter to select

        Args:
            locations (list of tuples): list of locations to cycle through  

        Return: 
            (row, col) (tuple): coordinates of selected location  
        """

        # copy board for display, initialize listener
        tempBoard = copy.deepcopy(self.BOARD)
        listener = inputs.Listener(len(locations))
        oldIndex = listener.index
        row, col = locations[oldIndex]

        # print first view
        for r,c in locations:
            tempBoard[r][c] = "*"
        tempBoard[row][col] = "X"
        self.printBoard(tempBoard)

        # allow user to loop through inputs and select location
        while True:
            if oldIndex != listener.index:
                # refresh view
                row, col = locations[listener.index]
                for r,c in locations:
                    tempBoard[r][c] = "*"
                tempBoard[row][col] = "X"
                self.printBoard(tempBoard)
                oldIndex = listener.index
            if listener.selected:
                break

        # display final selection
        tempBoard = copy.deepcopy(self.BOARD) 
        tempBoard[row][col] = "X"
        self.printBoard(tempBoard)
        # return selected coordinates
        return (row, col)


    def makeMove(self, location, final):
        """
        Summary: makes a single move or hop, updates board and counters

        Args:
            location (tuple): initial location
            final (tuple): final location
        """
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
        self.printBoard(self.BOARD)


    def printBoard(self, board):
        """
        Summary: prints the given board

        Args:
            board (2D list): the board stored in a 2D array
        """
        self.output.clear()

        if type(self.output).__name__ == "TerminalDisplay":
            output = "\n"
            output += "+---+---+---+---+---+---+---+---+\n"
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
                output += f"{row}\n+---+---+---+---+---+---+---+---+\n"
            scores = "Black: " + str(self.blackCounter) + " Red: " + str(self.redCounter)
            output += scores

        elif type(self.output).__name__ == "LedDisplay":
            colors = {
                
                "black": (0, 0, 0),
                "grey": (100, 100, 100),
                "red": (255, 0, 0),
                "orange": (255, 255, 0),
                "blue": (0, 0, 255),
                "purple": (255, 0, 255),
                "green": (0, 255, 0)

            }

            output = []
            for r in range(32):
                output.append([])
                for c in range(32):
                    if ((r % 8 < 4) and (c % 8 < 4)) or ((r % 8 >= 4) and (c % 8 >= 4)):
                        output[r].append(colors["grey"])
                    else:
                        output[r].append(colors["black"])

            for r in range(8):
                for c in range(8):
                    if board[r][c] and board[r][c] != "*":
                        if board[r][c] == "X":
                            pixels = [ 
                            (r*4,c*4),  (r*4,c*4+1), (r*4,c*4+2), (r*4,c*4+3), 
                            (r*4+1,c*4), (r*4+1,c*4+3),
                            (r*4+2,c*4), (r*4+2,c*4+3),
                            (r*4+3,c*4),  (r*4+3,c*4+1), (r*4+3,c*4+2), (r*4+3,c*4+3), 
                            ]
                            
                            for row, column in pixels:
                                output[column][row] = colors["green"]
                        
                        pixels = [ 
                        (r*4+1, c*4+1), 
                        (r*4+1, c*4+2),
                        (r*4+2, c*4+1),
                        (r*4+2, c*4+2),
                        ]

                        diagonal = [
                        (r*4+1, c*4+2),
                        (r*4+2, c*4+1)
                        ]

                        if board[r][c] > 0:
                            for row, column in pixels:
                                output[column][row] = colors["red"]
                            if board[r][c] == 2:
                                for row, column in diagonal:
                                    output[column][row] = colors["orange"]
                        else:
                            for row, column in pixels:
                                output[column][row] = colors["blue"]
                            if board[r][c] == -2:
                                for row, column in diagonal:
                                    output[column][row] = colors["purple"]

        else:
            print("Unsupported output")
            raise ValueError

        self.output.show(output)


    def winner(self):
        """
        Summary: returns true if you are the winner
        """
        if self.color == 1 and self.blackCounter != 0 and self.done:
            return True
        elif self.color == -1 and self.redCounter != 0 and self.done:
            return True
        else:
            return False


    def playTurn(self):
        """
        Summary: plays a turn of checkers

        Return:
            self.BOARD: updated board after turn
        """
        self.updateScores()
        # print initial setup
        self.printBoard(self.BOARD)
        
        if self.blackCounter == 0 or self.redCounter == 0:
            self.done = True
        else:
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

        if self.blackCounter == 0 or self.redCounter == 0:
            self.done = True
        self.output.show("ending turn")

        return self.BOARD