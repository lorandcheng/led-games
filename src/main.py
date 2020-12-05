# Standard library imports
import time
import os
# Third party imports

# Module imports
from games import battleship, checkers
from mqtt import mqttInit
import controller

GAMES = [
    ('Checkers', checkers.Checkers()), 
    ('Battleship', battleship.Battleship())
]

def selectGame():
    index = 0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Use 'a' and 'd' to cycle, 'e' to select")
        print('Choose a game:')
        for i in range(len(GAMES)):
            if i == index:
                print('* ' + GAMES[i][0])
            else:
                print('  ' + GAMES[i][0])
        inp = controller.getInput()
        try:
            index += inp
        except TypeError:
            break
        if index > len(GAMES)-1:
            index = 0
        elif index < 0:
            index = len(GAMES)-1
    return index
        

def gameInit():
    selection = selectGame()
    game = GAMES[selection][1]
    game.main()

def main():
    mqttInit()
    # gameInit()
    



if __name__ == '__main__':
    main()