# Game module API

In order to seamlessly fit into the rest of the application, the game modules must be designed to meet the following requirements:

class Game:
    def __init__(self, output):
        self.name = 'GameName'
        self.output = output
        self.color = # default
        self.BOARD = # gameboard data
        self.done = False
        """
        other inits
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
