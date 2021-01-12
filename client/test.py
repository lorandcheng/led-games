from games import battleship, checkers
from outputs import TerminalDisplay, LedDisplay
import copy
from inputs import Menu, Reader, Listener

class LocalGame:
    def __init__(self, game, output):
        self.output = output
        self.player1 = game        
        self.player2 = copy.deepcopy(game)
        self.player1.color = 1

    def playLocal(self):
        lst = Listener(1)
        if self.player1.needSetup():
            # Player 1 setup
            self.output.clear()
            self.output.show(('Player 1','Setup'))
            lst.selected = False
            while not lst.selected:
                pass
            data = str(self.player1.setup())
            self.player2.parseData(data)

            # Player 2 setup
            self.output.clear()
            self.output.show(('Player 2','Setup'))
            lst.selected = False
            while not lst.selected:
                pass
            data = str(self.player2.setup())
            self.player1.parseData(data)

        while not self.player2.done:
            # Player 1 turn
            self.output.clear()
            self.output.show(('Player 1','Turn'))
            lst.selected = False
            while not lst.selected:
                pass
            turn = str(self.player1.playTurn())
            self.player2.parseData(turn)

            # End if player 1 won
            if self.player1.done:
                break

            # Player 2 turn    
            self.output.clear()
            self.output.show(('Player 2','Turn'))
            lst.selected = False
            while not lst.selected:
                pass
            turn = str(self.player2.playTurn())
            self.player1.parseData(turn)

        # Print winner
        self.output.clear()
        if self.player1.winner():
            self.output.show(('Player 1', 'Won!'))
        else:
            self.output.show(('Player 2', 'Won!'))
        lst.selected = False
        while not lst.selected:
            pass

if __name__ == "__main__":
   
    output = TerminalDisplay()
    game = checkers.Checkers(output)

    
    # game.setup()
    LIAF = LocalGame(game, output)
    
    LIAF.playLocal()