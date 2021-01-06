
class Battleship:
    def __init__(self, output):
        self.name = 'Battleship'
        self.output = output
        self.color = # default
        self.BOARD = # gameboard data
        self.oBOARD = # opponent's board
        self.done = False
        """
        other inits
        """




    def boardSetUp(self):
        carrier = [[0,0],[0,1],[0,2],[0,3],[0,4]]
        battle = [[0,0],[0,1],[0,2],[0,3]]
        cruiser = [[0,0],[0,1],[0,2]]
        sub = [[0,0],[0,1],[0,2]]
        destroy = [[0,0],[0,1]]

        

    def parseData(self, data):
        """
        parse the data returned from playTurn after it has been sent as a string
        """

    def playTurn(self):
        """
        one turn of the game
        """

    def printBoard(self, board):
        """
        define the visualization for each output
        """
    
    def winner(self):
        """
        return true if game is over and player won
        """