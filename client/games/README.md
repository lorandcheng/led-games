# Game module API

In order to seamlessly fit into the rest of the application, the game modules must be designed to meet the following template:

```

class <GameName>:
    def __init__(self, output):
        self.output = output
        self.color = -1 # color is used to decide who starts 1 starts, -1 goes second
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
        one turn of the game, return value must be compatible as an input to parseData()
        """

    def printBoard(self, board):
        """
        define the visualization for each output
        """
        self.output.clear()
        if type(self.output).__name__ == "TerminalDisplay":
            pass
        elif type(self.output).__name__ == "LedDisplay":
            colors = {}
        else:
            print("Unsupported output")
            raise ValueError
    
    def winner(self):
        """
        return true if game is over and player won
        """

```