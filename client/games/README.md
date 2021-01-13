# Game module API

In order to seamlessly fit into the rest of the application, the game modules must be designed to meet the following template:

class Game:
    def __init__(self, output):
        self.output = output
        self.color = # default
        self.BOARD = # gameboard data
        self.done = False
        # only if setup is required before players take turns playing
        self.setupDone = False 
        """
        other inits
        """

    def needSetup(self):
        """
        return True if game needs setup. also set self.setupDone flag at some point (in parseData perhaps)
        """

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
