from games import battleship
from outputs import TerminalDisplay, LedDisplay

if __name__ == "__main__":

    output = TerminalDisplay()
    game = battleship.Battleship(output)
    game.playTurn()