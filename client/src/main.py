# Standard library imports
import time
import os
# Third party imports

# Module imports
from games import battleship, checkers
from mqttClient import mqttClient
import controller
import output

firstGame = 1 #flag that makes reentering lobby easier

OUTPUT = output.terminalDisplay()

GAMES = [
    checkers.Checkers(),
    battleship.Battleship()
]

def selectGame():
    listener = controller.Listener(len(GAMES))
    oldIndex = listener.index
    OUTPUT.clear()
    OUTPUT.show('Choose a game:')
    for i in range(len(GAMES)):
        if i == listener.index:
            OUTPUT.show('* ' + GAMES[i].name)
        else:
            OUTPUT.show('  ' + GAMES[i].name)
    while True:
        if oldIndex != listener.index:
            OUTPUT.clear()
            OUTPUT.show('Choose a game:')
            for i in range(len(GAMES)):
                if i == listener.index:
                    OUTPUT.show('* ' + GAMES[i].name)
                else:
                    OUTPUT.show('  ' + GAMES[i].name)
            oldIndex = listener.index
            OUTPUT.show(listener.selected)
        if listener.selected:
            break
    return GAMES[listener.index]
        
def gameInit(): 
    return selectGame()

def main():
    client = mqttClient()
    OUTPUT.clear()
    OUTPUT.show("Enter your username")
    time.sleep(2)
    client.inputName(client.client)
    while not client.verified:
        pass
    OUTPUT.show("Username verified")
    time.sleep(1)

    while True:
        game = selectGame()
        #enter match-making lobby
        client.joinLobby(client.client, game)
        while client.lobby == []:
            pass
        #choose opponent from lobby, then wait for acceptance of request
        opponents = client.findOpponents(client.lobby)
        opponent = client.selectOpponent(opponents)
        if opponent != 0:
            OUTPUT.show(f"SELECTED OPPONENT {opponent}")
            OUTPUT.show("Sending match request...")
            time.sleep(2)
            client.client.publish(f"ledGames/{client.opponent}/requests", f"{client.username}, 1")
        while not client.start:
            pass

        #loop responsible for gameplay
        while not game.done:
            #sequence for very first turn of game, only runs once
            if client.initiator == 1:
                game.busy = 1
                game.color = 1
                game.main()
                print("sending your turn")
                client.client.publish(f"ledGames/{client.opponent}/play", f"{game.BOARD}")
                client.initiator = 0
            
            #where a player waits to recieve a turn from the opponent
            while game.busy == 0:
                if len(client.boardStr) > 0:
                    game.busy = 1

                    print(client.boardStr)
                    game.beginTurn(client.boardStr) #update the game board
                    client.boardStr = ""
                else:
                    pass
            
            #players turn begins, and is sent
            game.main()
            print("sending your turn")
            print(client.opponent)
            client.client.publish(f"ledGames/{client.opponent}/play", f"{game.BOARD}")
        
        # ending sequence
        time.sleep(1)
        print("Your game with " + client.opponent + "has ended.")
        firstGame = 0
        client.opponent = ""
        client.start = 0
        client.players = []
        inp = input("Would you like to play again? y/n")
        if inp == 'y':
            print("returning to lobby")
        elif inp == 'n':
            print(inp)
            info = client.client.publish("ledGames/users/status", f'{client.username}, 0')
            info.wait_for_publish()
            #time.sleep(2)
            break
        else:
            print("please type y or n")
            inp = input("Would you like to play again? y/n")
            continue

    return

if __name__ == '__main__':
    main()