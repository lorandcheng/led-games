import copy
import sys
import time
# Other file imports
sys.path.append('..')
import inputs
class Battleship:
    def __init__(self, output):
        self.name = 'Battleship'
        self.output = output
        self.color = -1

        # empty:0, ship:1, hit:2, invalid:-1, miss:-2
        self.BOARD = [
            [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
            [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
            [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
            [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
            [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
            [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
            [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
            [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
            [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
            [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]
        ]
        self.done = False
        """
        other inits
        """
        self.oBOARD = copy.deepcopy(self.BOARD)
        self.setupDone = False
        self.myShips = 0
        self.oShips = 0
        self.countShips()

    def needSetup(self):
        return True

    def isEmpty(self, ship):
        for r,c in ship:
            if self.BOARD[r][c] == 1:
                return False
        return True

    def invalid(self, ship):
        for r,c in ship:
            if not (0<=r<=9) or not (0<=c<=9):
                return True
        return False

    def fixRotate(self, ship):
        while ship[-1][0] > 9:
            for elem in ship:
                elem[0] -= 1
        while ship[-1][1] > 9:
            for elem in ship:
                elem[1] -= 1
        
    def placeShip(self, ship):
        tempBoard = copy.deepcopy(self.BOARD)
        if self.isEmpty(ship):
            for r,c in ship:
                tempBoard[r][c] = 1
        else:
            for r,c in ship:
                tempBoard[r][c] = -1
        # print initial view
        self.printBoard(tempBoard)

        listener = inputs.Listener()
        done = False
        while not done:
            while not listener.selected:
                if listener.rChange or listener.cChange:
                    oldShip = copy.deepcopy(ship)
                    for elem in ship:
                        elem[0] += listener.rChange
                        elem[1] += listener.cChange
                    listener.resetChanges()
                    if self.invalid(ship):
                        ship = oldShip
                    else:
                        tempBoard = copy.deepcopy(self.BOARD)
                        if self.isEmpty(ship):
                            for r,c in ship:
                                tempBoard[r][c] = 1
                        else:
                            for r,c in ship:
                                tempBoard[r][c] = -1
                        self.printBoard(tempBoard)
                if listener.rotate:
                    listener.resetRotate()
                    pivot = copy.copy(ship[0])
                    for elem in ship:
                        elem[0] -= pivot[0]
                        elem[1] -= pivot[1]
                        r = elem[0]
                        c = elem[1]
                        elem[0] = c
                        elem[1] = r
                        elem[0] += pivot[0]
                        elem[1] += pivot[1]
                    if self.invalid(ship):
                        self.fixRotate(ship)
                    tempBoard = copy.deepcopy(self.BOARD)
                    if self.isEmpty(ship):
                        for r,c in ship:
                            tempBoard[r][c] = 1
                    else:
                        for r,c in ship:
                            tempBoard[r][c] = -1
                    self.printBoard(tempBoard)

            if self.isEmpty(ship):
                done = True
            else:
                listener.selected = False

        self.BOARD = tempBoard


    def setup(self):
        shipSizes = [2]# [5,4,3,3,2]
        for size in shipSizes:
            ship = []
            for i in range(size):
                ship.append([0,i])
            self.placeShip(ship)
        
        return self.BOARD
        

    def parseData(self, data):
        """
        parse the data returned from playTurn after it has been sent as a string
        """
        message = str(data.payload, 'utf-8')
        if len(message) > 10:
            message = message[2:len(message)-2]

            rows = message.split("], [")
            j = 0
            for element in rows:
                vals = element.split(", ")
                
                for i in range(10):
                    self.oBOARD[j][i] = int(vals[i])
                j+=1
            self.setupDone = True
        else:
            message = message[1:len(message)-1]
            coords = message.split(", ")
            self.showTurn(coords)

    def showTurn(self, coords):
        """
        animate opponent's turn
        """
        tempBoard = copy.deepcopy(self.BOARD)
        r = int(coords[0])
        c = int(coords[1])
        if tempBoard[r][c] == 1:
            tempBoard[r][c] = 2
        elif tempBoard[r][c] == 0:
            tempBoard[r][c] = -2
        
        self.printBoard(self.BOARD)
        time.sleep(0.3)
        self.printBoard(tempBoard)
        time.sleep(0.3)
        self.printBoard(self.BOARD)
        time.sleep(0.3)
        self.printBoard(tempBoard)
        time.sleep(0.3)
        self.printBoard(self.BOARD)
        time.sleep(0.3)
        self.printBoard(tempBoard)

        self.BOARD = tempBoard


    def hideShips(self):
        tempBoard = copy.deepcopy(self.oBOARD)
        for r in range(10):
            for c in range(10):
                if tempBoard[r][c] == 1:
                    tempBoard[r][c] = 0
        return tempBoard

    def selectLoc(self):
        row = 0
        col = 0
        tempBoard = self.hideShips()
        tempBoard[row][col] = str(tempBoard[row][col]) + "X"
        self.printBoard(tempBoard)
        listener = inputs.Listener()
        done = False
        while not done:
            while not listener.selected:
                if listener.rChange or listener.cChange:
                    r = listener.rChange
                    c = listener.cChange
                    listener.resetChanges()

                    if (0<=(row+r)<=9) and (0<=(col+c)<=9):
                        row += r
                        col += c
                        tempBoard = self.hideShips()
                        tempBoard[row][col] = str(tempBoard[row][col]) + "X"
                        self.printBoard(tempBoard)

            if int(tempBoard[row][col][:-1]) == 0:
                done = True
            else: 
                listener.selected = False

        return row, col

    def countShips(self):
        self.myShips = 0
        self.oShips = 0
        for r in range(10):
            for c in range(10):
                if self.BOARD[r][c] == 1:
                    self.myShips += 1
                if self.oBOARD[r][c] == 1:
                    self.oShips += 1

    
    def playTurn(self):
        """
        one turn of the game
        """
        self.countShips()
        if self.myShips:
            row, col = self.selectLoc()
            if self.oBOARD[row][col] == 1:
                self.oBOARD[row][col] = 2
                print("hit at", row, col)
            elif self.oBOARD[row][col] == 0:
                self.oBOARD[row][col] = -2
                print("missed at", row, col)
            time.sleep(3)
            self.printBoard(self.hideShips())
            self.countShips()
        else:
            self.done = True
            return 0
        if self.oShips == 0:
            self.done = True

        return row, col

    def printBoard(self, board):
        """
        define the visualization for each output
        """
        self.output.clear()
        if type(self.output).__name__ == "TerminalDisplay":
            output = "\n"
            output += "+---+---+---+---+---+---+---+---+---+---+\n"
            for r in range(10):
                row = '|'
                for c in range(10):
                    if board[r][c] == 2:
                        row += ' X |'
                    elif board[r][c] == -2:
                        row += ' . |'
                    elif board[r][c] == 1:
                        row += ' S |'
                    elif board[r][c] == -1:
                        row += ' ! |'
                    elif str(board[r][c])[-1] == 'X':
                        row += ' @ |'
                    else:
                        row += '~~~|'
                output += f"{row}\n+---+---+---+---+---+---+---+---+---+---+\n"

        elif type(self.output).__name__ == "LedDisplay":
            colors = {
                "black": (0, 0, 0),
                "grey": (80, 80, 80),
                "red": (230, 0, 0),
                "white": (150, 150, 150),
                "blue": (0, 0, 100),
                "blue green": (0, 50, 100),
                "green": (0, 200, 0),
                "dark green": (0, 100, 0)
            }

            output = []
            for r in range(32):
                output.append([])
                for c in range(32):

                    if r == 0 or r == 31 or c == 0 or c == 31:
                        output[r].append(colors["blue green"])
                    elif r%2 == 0 and c%2 == 0:
                        output[r].append(colors["black"])
                    else:
                        output[r].append(colors["blue"])

            for r in range(10):
                for c in range(10):
                    if board[r][c]:
                        if type(board[r][c]) == str:
                            pixels = [ 
                            (r*3+1,c*3+1),  (r*3+1,c*3+2), (r*3+1,c*3+3),  
                            (r*3+2,c*3+1),  (r*3+2,c*3+3),
                            (r*3+3,c*3+1),  (r*3+3,c*3+2), (r*3+3,c*3+3), 
                            ]

                            for row, column in pixels:
                                if str(board[r][c])[-1] == "X":
                                    output[column][row] = colors["green"]

                        elif board[r][c] == 1 or board[r][c] == 2:
                            pixels = [ 
                            (r*3+1,c*3+1),  (r*3+1,c*3+2), (r*3+1,c*3+3),  
                            (r*3+2,c*3+1),  (r*3+2,c*3+2), (r*3+2,c*3+3),
                            (r*3+3,c*3+1),  (r*3+3,c*3+2), (r*3+3,c*3+3), 
                            ]

                            for row, column in pixels:
                                output[column][row] = colors["grey"]

                            if board[r][c] == 2:
                                pixels = [ 
                                (r*3+1,c*3+1), (r*3+1,c*3+3),  
                                (r*3+2,c*3+2),
                                (r*3+3,c*3+1), (r*3+3,c*3+3), 
                                ]

                                for row, column in pixels:
                                    output[column][row] = colors["red"]

                        elif board[r][c] == -1:
                            pixels = [ 
                            (r*3+1,c*3+1),  (r*3+1,c*3+2), (r*3+1,c*3+3),  
                            (r*3+2,c*3+1),  (r*3+2,c*3+2), (r*3+2,c*3+3),
                            (r*3+3,c*3+1),  (r*3+3,c*3+2), (r*3+3,c*3+3), 
                            ]

                            for row, column in pixels:
                                output[column][row] = colors["red"]

                        elif board[r][c] == -2:
                            pixels = [(r*3+2,c*3+2)]
                            for row, column in pixels:
                                    output[column][row] = colors["white"]

        else:
            print("Unsupported output")
            raise ValueError

        self.output.show(output)
    
    def winner(self):
        """
        return true if game is over and player won
        """
        if self.myShips:
            return True
        else:
            return False