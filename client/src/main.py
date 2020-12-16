# Standard library imports
import time
# Third party imports

# Module imports
from games import battleship, checkers
from mqttClient import mqttClient
from mqtt import UsernameGenerator
import inputs
import outputs

OUTPUT = outputs.TerminalDisplay()

GAMES = [
    checkers.Checkers(),
    battleship.Battleship()
]

USERNAME = ""

def selectGame(games):
    prompt = "Choose a game:"
    options = [game.name for game in games]
    menu = inputs.Menu(prompt, options, OUTPUT, indexing=True)
    index,_ = menu.select()
    return games[index]
        
def gameInit(): 
    return selectGame(GAMES)

def userInit():
    generator = UsernameGenerator(OUTPUT)
    return generator.getUsername()

def main():
    USERNAME = userInit()
    client = mqttClient()
    client.inputName(client.client)
    while not client.verified:
        pass
    OUTPUT.show("Username verified")
    time.sleep(1)

    while True:
        client.reset()
        game = selectGame(GAMES)
        game.__init__()
        #enter match-making lobby
        client.joinLobby(client.client, game)
        while client.lobby == []:
            pass
        #choose opponent from lobby, then wait for acceptance of request
        opponent = 0
        while not opponent:
            opponents = client.findOpponents(client.lobby)
            opponent = client.selectOpponent(opponents)
            if opponent != 0:
                break
            else:
                while client.requested:
                    pass
        OUTPUT.show(f"SELECTED OPPONENT {opponent}")
        OUTPUT.show("Sending match request...")
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
                print("entered while loop")
                if len(client.boardStr) > 0:
                    print("received board")
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
        client.opponent = ""
        client.start = 0
        client.lobby = []
        prompt = "Would you like to play again? y/n"
        options = ["y", "n"]
        menu = inputs.Menu(prompt, options, OUTPUT)
        selection = menu.select()
        del menu
        if selection == 'y':
            print("returning to lobby")
        else:
            info = client.client.publish("ledGames/users/status", f'{client.username}, 0')
            info.wait_for_publish()
            #time.sleep(2)
            break

if __name__ == '__main__':
    main()