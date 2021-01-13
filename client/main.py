import atexit
import sys
import time

from games.battleship import Battleship
from games.checkers import Checkers
from inputs import Menu, Listener
from outputs import TerminalDisplay, LedDisplay
from mqtt import UsernameGenerator, Lobby, OnlineGame, leave

def selectGame(games):
    prompt = ("Choose", "a game")
    options = [game.__name__ for game in games]
    menu = Menu(OUTPUT, prompt, options, indexing=True)
    index,_ = menu.select()
    return games[index]

def setMode():
    prompt = ("Choose", "a mode")
    options = ["Local", "Online"]
    menu = Menu(OUTPUT, prompt, options)
    result = menu.select()
    return result

class LocalGame:
    def __init__(self, player1, player2, output):
        self.player1 = player1    
        self.player2 = player2
        self.player1.color = 1
        self.output = output

    def playLocal(self):
        lst = Listener()
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
    # set output to LED matrix if on the raspberry pi, otherwise use terminal display
    if sys.platform == "linux" or sys.platform == "linux2":
        OUTPUT = LedDisplay()
    else:
        OUTPUT = TerminalDisplay()

    # initialize game classes
    GAMES = [
        Checkers,
        Battleship
    ]

    while True:
        # prompt user to select a game
        game = selectGame(GAMES)
        # prompt user to select game mode
        mode = setMode()

        if mode == "Local":
            # initialize a game instance for each player
            player1 = game(OUTPUT)
            player2 = game(OUTPUT)
            # play a local game
            gameplay = LocalGame(player1, player2, OUTPUT)
            gameplay.playLocal()

        elif mode == "Online":
            # initialize a game instance
            player = game(OUTPUT)
            # prompt user to enter a valid username
            usernameGenerator = UsernameGenerator(OUTPUT)
            USERNAME = usernameGenerator.getUsername()

            # register the cleanup function to remove user from server list
            atexit.register(leave, USERNAME)

            # join the lobby with username and game, select an opponent and assign colors
            lobby = Lobby(USERNAME, game.__name__, OUTPUT)
            opponent, color = lobby.lobby()
            del lobby
            print(f"You started a match with {opponent}")
            print(f"Your color is {color}")

            # play online
            gameplay = OnlineGame(player, USERNAME, opponent, color, OUTPUT)
            gameplay.playOnline()
            del gameplay

        # prompt user to play again or exit program
        menu = Menu(OUTPUT, ("Do you", "want to", "keep", "playing?"), ["y", "n"])
        selection = menu.select()
        if selection == "n":
            break

