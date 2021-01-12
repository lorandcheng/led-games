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
            while not lst.selected:
                pass
            data = str(self.player1.setup())
            lst.selected = False
            self.player2.parseData(data)

            # Player 2 setup
            self.output.clear()
            self.output.show(('Player 2','Setup'))
            while not lst.selected:
                pass
            data = str(self.player2.setup())
            lst.selected = False
            self.player1.parseData(data)

        while (not self.player1.done) and (not self.player2.done):
            self.output.clear()
            self.output.show(('Player 1','Turn'))
            while not lst.selected:
                pass
            turn = str(self.player1.playTurn())
            lst.selected = False
            self.player2.parseData(turn)

            self.output.clear()
            self.output.show(('Player 2','Turn'))
            while not lst.selected:
                pass
            turn = str(self.player2.playTurn())
            lst.selected = False
            self.player1.parseData(turn)
        print('ending')
        
        self.ouput.clear()
        if self.player1.winner():
            self.output.show(('Player 1', 'Won!'))
            
        else:
            self.output.show(('Player 2', 'Won!'))
        
        
        while not lst.selected:
                pass

if __name__ == "__main__":
   
    output = TerminalDisplay()
    game = checkers.Checkers(output)

    
    # game.setup()
    LIAF = LocalGame(game, output)
    
    LIAF.playLocal()