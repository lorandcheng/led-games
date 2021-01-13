import copy
import sys
import time
# Other file imports
sys.path.append('..')
import inputs
class Battleship:
    def __init__(self, output):
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

        self.setupDone = False
        self.done = False
        """
        other inits
        """
        self.oBOARD = copy.deepcopy(self.BOARD)
        self.fleet = None
        self.oFleet = None
        self.oGuess = None

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
        return ship


    def setup(self):
        shipSizes = [5,4,3,3,2]
        coords = []
        for size in shipSizes:
            ship = []
            for i in range(size):
                ship.append([0,i])
            ship = self.placeShip(ship)
            coords.append(ship)
        self.fleet = Fleet(coords)

        self.output.show(("Waiting", "for", "opponent", "to", "set up"))
        return self.BOARD, coords
        

    def parseData(self, message):
        """
        parses the data returned from playTurn() or setup() after it has been sent as a string
        """
        # print(message)
        # parsing opponent's setup
        if len(message) > 10:
            message = message[3:len(message)-4]
            board, coords = message.split("]], [[[")
            # parse opponent's board
            rows = board.split("], [")
            j = 0
            for element in rows:
                vals = element.split(", ")
                
                for i in range(10):
                    self.oBOARD[j][i] = int(vals[i])
                j+=1
            # parse opponents's fleet coordinates
            ships = coords.split("]], [[")
            oCoords = []
            for ship in ships:
                shipCoords = []
                elems = ship.split("], [")
                for elem in elems:
                    r,c = elem.split(", ")
                    shipCoords.append([int(r),int(c)])
                oCoords.append(shipCoords)
            self.oFleet = Fleet(oCoords)

            self.setupDone = True

        # parsing opponent's turn
        else:
            message = message[1:len(message)-1]
            coords = message.split(", ")
            r = int(coords[0])
            c = int(coords[1])
            self.oGuess = (r, c)

    def animate(self, coords, board, hide=False):
        """
        animate turn and update the board
        """
        if hide:
            before = copy.deepcopy(self.hideShips(board))
            after = copy.deepcopy(self.hideShips(board))
        else:
            before = copy.deepcopy(board)
            after = copy.deepcopy(board)

        r = coords[0]
        c = coords[1]

        if hide:
            hit, sunk = self.oFleet.hit(r,c)
        else:
            hit, sunk = self.fleet.hit(r,c)

        # cosmetic detail
        if type(self.output).__name__ == "TerminalDisplay":
            before[r][c] = 0
            
        if hit:
            if sunk:
                if hide:
                    ship = self.oFleet.getShip(r,c)
                else:
                    ship = self.fleet.getShip(r,c)
                for row, col in ship:
                    board[row][col] = -1
                    after[row][col] = -1
                    # changing appearance to be all Xs underneath the flashing red
                    before[row][col] = 2
            else:
                board[r][c] = 2
                after[r][c] = 2
        elif board[r][c] == 0:
            board[r][c] = -2
            after[r][c] = -2
        
        self.printBoard(before)
        time.sleep(0.5)
        for i in range(10):
            self.printBoard(after)
            time.sleep(0.1)
            self.printBoard(before)
            time.sleep(0.1)
        self.printBoard(after)
        time.sleep(0.5)


    def hideShips(self, board):
        tempBoard = copy.deepcopy(board)
        for r in range(10):
            for c in range(10):
                if tempBoard[r][c] == 1:
                    tempBoard[r][c] = 0
        return tempBoard


    def selectLoc(self):
        row = 0
        col = 0
        tempBoard = self.hideShips(self.oBOARD)
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
                        tempBoard = self.hideShips(self.oBOARD)
                        tempBoard[row][col] = str(tempBoard[row][col]) + "X"
                        self.printBoard(tempBoard)

            if int(tempBoard[row][col][:-1]) == 0:
                done = True
            else: 
                listener.selected = False

        return row, col
    

    def playTurn(self):
        """
        one turn of the game
        """
        self.printBoard(self.hideShips(self.oBOARD))
        if self.fleet.shipCount():
            if self.oGuess:
                self.animate(self.oGuess, self.BOARD)
            row, col = self.selectLoc()
            self.animate((row, col), self.oBOARD, hide=True)
        else:
            self.done = True
            return 0
        if self.oFleet.shipCount() == 0:
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
                        row += '   |'
                output += f"{row}\n+---+---+---+---+---+---+---+---+---+---+\n"

        elif type(self.output).__name__ == "LedDisplay":
            colors = {
                "black": (0, 0, 0),
                "grey": (80, 80, 80),
                "red": (230, 0, 0),
                "white": (150, 150, 150),
                "dark blue": (0, 0, 50),
                "light blue": (50, 50, 100),
                "blue green": (0, 80, 80),
                "green": (0, 200, 0),
                "dark green": (0, 100, 0)
            }

            output = []
            for r in range(32):
                output.append([])
                for c in range(32):

                    if r == 0 or r == 31 or c == 0 or c == 31:
                        output[r].append(colors["blue green"])
                    elif (r+1)%3 == 0 and (c+1)%3 == 0:
                        output[r].append(colors["light blue"])
                    else:
                        output[r].append(colors["dark blue"])

            for r in range(10):
                for c in range(10):
                    if board[r][c]:
                        # Selected
                        if type(board[r][c]) == str:
                            pixels = [ 
                                    (r*3+1,c*3+1), (r*3+1,c*3+2), (r*3+1,c*3+3),  
                                    (r*3+2,c*3+1),                (r*3+2,c*3+3),
                                    (r*3+3,c*3+1), (r*3+3,c*3+2), (r*3+3,c*3+3)
                                ]

                            for row, column in pixels:
                                if board[r][c][-1] == "X":
                                    output[column][row] = colors["green"]
                                if board[r][c][:-1] == "2":
                                    output[c*3+2][r*3+2] = colors["red"]
                                elif board[r][c][:-1] == "-2":
                                    output[c*3+2][r*3+2] = colors["white"]
                        # Ship
                        elif board[r][c] == 1: 
                            pixels = [ 
                                    (r*3+1,c*3+1), (r*3+1,c*3+2), (r*3+1,c*3+3),  
                                    (r*3+2,c*3+1), (r*3+2,c*3+2), (r*3+2,c*3+3),
                                    (r*3+3,c*3+1), (r*3+3,c*3+2), (r*3+3,c*3+3)
                                ]

                            for row, column in pixels:
                                output[column][row] = colors["grey"]

                        # Invalid
                        elif board[r][c] == -1:
                            pixels = [ 
                                    (r*3+1,c*3+1), (r*3+1,c*3+2), (r*3+1,c*3+3),  
                                    (r*3+2,c*3+1), (r*3+2,c*3+2), (r*3+2,c*3+3),
                                    (r*3+3,c*3+1), (r*3+3,c*3+2), (r*3+3,c*3+3)
                                ]

                            for row, column in pixels:
                                output[column][row] = colors["red"]

                        # Hit
                        elif board[r][c] == 2:
                            pixels = [ 
                                    (r*3+1,c*3+1),                (r*3+1,c*3+3),  
                                                   (r*3+2,c*3+2),
                                    (r*3+3,c*3+1),                (r*3+3,c*3+3)
                                ]

                            for row, column in pixels:
                                output[column][row] = colors["red"]
                            
                            pixels = [ 
                                                   (r*3+1,c*3+2),  
                                    (r*3+2,c*3+1),                (r*3+2,c*3+3),
                                                   (r*3+3,c*3+2)
                                ]
                            
                            for row, column in pixels:
                                output[column][row] = colors["black"]

                        # Miss
                        elif board[r][c] == -2:
                            pixels = [ 
                                    (r*3+1,c*3+1),                (r*3+1,c*3+3),  
                                                   (r*3+2,c*3+2),
                                    (r*3+3,c*3+1),                (r*3+3,c*3+3)
                                ]

                            for row, column in pixels:
                                output[column][row] = colors["white"]
                            
                            pixels = [ 
                                                   (r*3+1,c*3+2),  
                                    (r*3+2,c*3+1),                (r*3+2,c*3+3),
                                                   (r*3+3,c*3+2)
                                ]
                            
                            for row, column in pixels:
                                output[column][row] = colors["black"]

        else:
            print("Unsupported output")
            raise ValueError

        self.output.show(output)
    
    def winner(self):
        """
        return true if game is over and player won
        """
        if self.fleet.shipCount():
            return True
        else:
            return False

class Ship:
    def __init__(self, size, coords):
        """
        Args:
            size: length of the ship
            coords: list of coords of all the pieces of the ship
        """
        self.size = size
        self.coords = coords
        self.sunk = False
        self.hits = 0

    def hit(self, row, col):
        """
        returns:
            True: hit
            False: miss
        """
        if [row, col] in self.coords:
            self.hits += 1
            if self.hits == self.size:
                self.sunk = True
            return True
        return False

    def onShip(self, row, col):
        if [row, col] in self.coords:
            return True
        return False
    
    def isSunk(self):
        return self.sunk

    def getCoords(self):
        return self.coords

class Fleet:
    def __init__(self, coords):
        """
        coords: 2d list of coordinates of the different ships, ordered in descending size
        """
        self.coords = coords
        self.carrier = Ship(5, coords[0])
        self.battleship = Ship(4, coords[1])
        self.cruiser = Ship(3, coords[2])
        self.sub = Ship(3, coords[3])
        self.destroyer = Ship(2, coords[4])
        self.fleet = [self.carrier, self.battleship, self.cruiser, self.sub, self.destroyer]
        self.numShips = len(self.fleet)

    def hit(self, row, col):
        """
        returns: 
            True, True: hit and sunk
            True, False: hit but not sunk
            False, False: miss
        """
        for ship in self.fleet:
            if ship.hit(row, col):
                if ship.isSunk():
                    self.numShips -= 1
                    return True, True
                return True, False
        return False, False

    def shipCount(self):
        return self.numShips

    def getShip(self, row, col):
        for ship in self.fleet:
            if ship.onShip(row, col):
                return ship.getCoords()


if __name__ == "__main__":
    """
    DEMO SHIP AND FLEET CODE (have to comment out import inputs)
    """
    coords = [
        [
            [0,0], [0,1], [0,2], [0,3], [0,4]
        ],
        [
            [1,0], [1,1], [1,2], [1,3]
        ],
        [
            [2,0], [2,1], [2,2]
        ],
        [
            [3,0], [3,1], [3,2]
        ],
        [
            [4,0], [4,1]
        ]
    ]
    
    fleet = Fleet(coords)

    print("Ship count:", str(fleet.shipCount()))
    for ship in coords:
        for row, col in ship:
            hit, sunk = fleet.hit(row, col)
            print("\nGuess:", row, col)
            print("Hit?", hit)
            print("Sunk?", sunk)
    print("\nShip count:", str(fleet.shipCount()))