# Standard library imports
import time
import os
# Third party imports

# Module imports
from games import battleship, checkers
from mqttClient import mqttClient
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
    client = mqttClient()
    game = gameInit()
    client.inputName(client.client)
    while client.username == "":
        pass
    print("username verified")
    client.joinLobby(client.client, game)
    while client.players == []:
        pass
    opponent = client.chooseOpponent(client.players)
    #print(f"ledGames/{opponent}/requests")
    client.client.publish(f"ledGames/{opponent}/requests", f"{client.username}, 1")
    while True:
        pass

if __name__ == '__main__':
    main()