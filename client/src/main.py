# Standard library imports
import time
import os
# Third party imports

# Module imports
from games import battleship, checkers
from mqtt import mqttInit, inputName, joinLobby
import controller

GAMES = [
    checkers.Checkers(),
    battleship.Battleship()
]

def selectGame():
    index = 0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Use 'a' and 'd' to cycle, 'e' to select")
        print('Choose a game:')
        for i in range(len(GAMES)):
            if i == index:
                print('* ' + GAMES[i].name)
            else:
                print('  ' + GAMES[i].name)
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
    game = GAMES[selection]
    return game

def main():
<<<<<<< HEAD:src/main.py
    mqttInit()
    # gameInit()
    
=======
    client = mqttInit()
    game = gameInit()
    inputName(client)
    joinLobby(client, game)

>>>>>>> 70f471a1d534b9cd4c284a808443270eb2f61ff0:client/src/main.py



if __name__ == '__main__':
    main()