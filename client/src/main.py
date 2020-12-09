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
    listener = controller.Listener(len(GAMES))
    oldIndex = listener.index
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Choose a game:')
    for i in range(len(GAMES)):
        if i == listener.index:
            print('* ' + GAMES[i].name)
        else:
            print('  ' + GAMES[i].name)
    while True:
        if oldIndex != listener.index:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Choose a game:')
            for i in range(len(GAMES)):
                if i == listener.index:
                    print('* ' + GAMES[i].name)
                else:
                    print('  ' + GAMES[i].name)
            oldIndex = listener.index
            print(listener.selected)
        if listener.selected:
            break
    return GAMES[listener.index]
        
def gameInit(): 
    return selectGame()

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
    client.chooseOpponent()
    #print(f"ledGames/{opponent}/requests")
    client.client.publish(f"ledGames/{client.opponent}/requests", f"{client.username}, 1")
    while not client.start:
        pass
    while not game.done:
        if client.initiator == 1:
            game.busy = 1
            game.color = 1
            game.main()
            print("sending your turn")
            client.client.publish(f"ledGames/{client.opponent}/play", f"{game.BOARD}")
            # print(str(game.busy))
            client.initiator = 0
           

        while game.busy == 0:
            if len(client.boardStr) > 0:
                game.busy = 1

                print(client.boardStr)
                game.beginTurn(client.boardStr)
                client.boardStr = ""
            else:
                pass
        
        game.main()
        print("sending your turn")
        print(client.opponent)
        client.client.publish(f"ledGames/{client.opponent}/play", f"{game.BOARD}")
    
    while True:
        pass

if __name__ == '__main__':
    main()