import atexit
import random
import sys
import time

import paho.mqtt.client as mqtt

from games import battleship, checkers
from inputs import Menu, Reader
from outputs import TerminalDisplay, LedDisplay
from parsersM import parseMessage


def selectGame(games):
    prompt = ("Choose", "a game")
    options = [game.name for game in games]
    menu = Menu(OUTPUT, prompt, options, indexing=True)
    index,_ = menu.select()
    return games[index]

def setMode():
    prompt = ("Choose", "a mode")
    options = ['local', 'online']
    menu = Menu(OUTPUT, prompt, options)
    result = menu.select()
    return result
    

class mqttClient:
    """
    Summary: Bare-bones mqtt client class
    """
    def __init__(self):   
        self.client = mqtt.Client()
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.on_disconnect = self.onDisconnect
        self.client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
        self.client.loop_start()

    def onConnect(self, client, userdata, flags, rc):
        print("Connection returned " + str(rc))

    def onMessage(self, client, userdata, msg):
        print("onMessage")

    def onDisconnect(self, client, useradata, rc):
        print("disconnecting")

class UsernameGenerator(mqttClient):
    """
    Summary: Prompts user to enter a username until it is approved by the server
    """
    def __init__(self, output):
        super().__init__()
        self.output = output
        self.username = ""
        self.verified = 0 # -1 rejected, 0 unverified, 1 verified
        self.client.subscribe("ledGames/users")
        self.client.message_callback_add("ledGames/users", self.usernameCallback)

    def getUsername(self):
        # loop until username is verified
        while self.verified != 1:
             # create reader
            prompt = ("Enter", "a name")
            reader = Reader(self.output, prompt)
            # get username input
            self.username = reader.readStr()
            # send username to be verified
            self.client.publish("ledGames/users/status", f'{self.username}, 1')
            # wait for a response
            self.verified = 0
            while self.verified == 0:
                pass
                # usernameCallback will either set self.verified to 1 or -1
                # if self.verified == 1, then getUsername returns the verified username
                # if self.verified == -1, the outer while loop repeats
            if self.verified == -1:
                self.output.show(("Username", "taken"))
                time.sleep(2)

        return self.username

    def usernameCallback(self, client, userdata, msg):
        name, code = parseMessage(msg)
        # only take action for messages addressed to this user
        if name == self.username:
            if code == "1":
                self.verified = 1
            else:
                self.verified = -1

    def __del__(self):
        self.client.disconnect()

class Lobby(mqttClient):
    """
    Summary: Class to handle matchmaking and opponent selection
    """
    def __init__(self, username, game, output):
        super().__init__()
        self.output = output
        self.output.clear()
        self.username = username
        self.game = game
        self.selected = "" # name of user that I selected
        self.requester = "" # name of user that sent me a request
        self.opponentResponse = 0 # -1 rejected, 0 waiting, 1 accepted
        self.color = 1

        self.client.subscribe("ledGames/lobby")
        self.client.message_callback_add("ledGames/lobby", self.lobbyCallback)
        self.client.subscribe(f"ledGames/{self.username}/requests")
        self.client.message_callback_add(f"ledGames/{self.username}/requests", self.myCallback)

        self.menu = Menu(self.output, ("Choose", "an", "opponent:"))


        
    def lobby(self):
        # join lobby
        self.client.publish("ledGames/lobby/status", f"{self.username}, {self.game}, 1")

        # wait until lobby is received and other players are present
        if self.menu.options == []:
            self.output.show(("Waiting", "for", "players"))
            while self.menu.options == []:
                pass

        # choose an opponent
        while True:
            self.selected = ""
            self.selected = self.menu.select()
            # if menu was exited because an opponent sent me a request, process the request
            if self.selected == 0:
                menu = Menu(self.output, ("Accept", "game", "with", f"{self.requester}?"), ["y", "n"])
                selection = menu.select()
                # if the request is accepted, send accept message and finalize opponent
                if selection == "y":
                    # choose a random color and map to 1 and -1
                    self.color = random.choice([0, 1])
                    if self.color == 0:
                        self.color = -1
                    # send username, accepting code, and opponent's color
                    self.client.publish(f"ledGames/{self.requester}/requests", f"{self.username}, 1, {self.color*-1}")
                    self.selected = self.requester
                    print("accepting opponent")
                    break
                    
                # if the request is denied, send deny message and return to choosing an opponent
                else:
                    print("denying opponent", self.requester)
                    self.client.publish(f"ledGames/{self.requester}/requests", f"{self.username}, -1")
                    self.requester = ""

            # otherwise, send a request to the selected opponent
            else:
                self.client.publish(f"ledGames/{self.selected}/requests", f"{self.username}, 0") 
                self.opponentResponse = 0
                self.output.clear()
                self.output.show(('Waiting', 'for', 'response'))
                # wait for response
                while self.opponentResponse == 0:
                    pass
                # if opponent accepted, finalize
                if self.opponentResponse == 1:
                    break

                # if opponent rejected, return to choosing an opponent
                else:
                    pass
        
        # leave lobby
        self.client.publish(f"ledGames/lobby/status", f"{self.username}, , 0")

        return self.selected, self.color



    def myCallback(self, client, useradata, msg):
        if len(parseMessage(msg)) == 3:
            opponent, code, color = parseMessage(msg)
            self.color = color
        else:
            opponent, code = parseMessage(msg)

        code = int(code)
        if code == 0:
            # exit selection menu if opponent sent me a request
            self.requester = opponent
            self.menu.exitMenu()
        else:
            # -1 if opponent rejected, 1 if opponent confirmed my request
            self.opponentResponse = code
            print("recieved response " + str(code))
        


    def lobbyCallback(self, client, userdata, msg):
        """
        Topic: "ledGames/lobby"

        Summary: updates the list of potential opponents whenever a new user joins the lobby
        """

        players = parseMessage(msg)
        opponents = []
        for player in players:
            if player[1] == self.game:
                if not player[0] == self.username:
                    opponents.append(player[0])
        self.menu.updateOptions(opponents)
        
    def __del__(self):
        self.client.disconnect()

class OnlineGame(mqttClient):
    """
    Summary: Class to handle game modules and gameplay
    """
    def __init__(self, game, username, opponent, color, output):
        self.game = game
        self.username = username
        self.opponent = opponent
        self.game.color = int(color)
        self.output = output
        self.turn = False

        super().__init__()
        self.client.subscribe(f"ledGames/{self.username}/play")
        self.client.message_callback_add(f"ledGames/{self.username}/play", self.receiveTurn)

    def playOnline(self):
        """
        Summary: main gameplay
        """
        if game.needSetup():
            data = game.setup()
            self.sendData(data)
            while not game.setupDone:
                pass
            self.turn = False
        # play first turn if you start
        if self.game.color == 1:
            data = self.game.playTurn()
            self.sendData(data)
        else:
            self.game.printBoard(self.game.BOARD)

        while not self.game.done:
            # wait for opponent to play and receive game info (in callback)
            while self.turn == False:
                pass

            # play your turn
            data = self.game.playTurn()

            # send game info
            self.sendData(data)
            self.turn = False
        self.output.clear()
        print("done with game")
        if self.game.winner():
            self.output.show(("game", "over", "you won"))
        else:
            self.output.show(("game", "over", "you lost"))
        time.sleep(3)


    def sendData(self, data):
        """
        Summary: sends game data to opponent after each turn
        """
        self.client.publish(f"ledGames/{self.opponent}/play", str(data))

    def receiveTurn(self, client, userdata, msg):
        """
        Summary: callback to receive game data from opponent
        """
        if not self.game.done:
            msg = str(msg.payload, 'utf-8')
            self.game.parseData(msg)
            self.turn = True


class LocalGame:
    def __init__(self, game, output):
        self.player1 = game.__init__(output)
        self.player2 = game.__init__(output)
        self.player2.color = 234
        print(self.player2.color)
        print(self.player2.color)

def leave(username):
    """
    Summary: cleanup function on program exit, removes username from server list
    """
    print("exiting program")
    client = mqtt.Client()
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    info = client.publish("ledGames/users/status", f"{username}, 0")
    info.wait_for_publish()
    info = client.publish("ledGames/lobby/status", f"{username}, , 0")
    info.wait_for_publish()
    time.sleep(5)

if __name__ == "__main__":
    # set output to LED matrix if on the raspberry pi, otherwise use terminal display
    if sys.platform == "linux" or sys.platform == "linux2":
        OUTPUT = LedDisplay()
    else:
        OUTPUT = TerminalDisplay()

    # initialize game classes
    GAMES = [
        checkers.Checkers(OUTPUT),
        battleship.Battleship(OUTPUT)
    ]

    mode = setMode()

    if mode == 'local':

    else:
        # prompt user to enter a valid username
        usernameGenerator = UsernameGenerator(OUTPUT)
        USERNAME = usernameGenerator.getUsername()

        # register the cleanup function to remove user from server list
        atexit.register(leave, USERNAME)

        while True:
            # prompt user to select a game, then initialize the game module
            game = selectGame(GAMES)
            game.__init__(OUTPUT)

            # join the lobby with username and game, select an opponent and assign colors
            lobby = Lobby(USERNAME, game.name, OUTPUT)
            opponent, color = lobby.lobby()
            del lobby
            print(f"You started a match with {opponent}")
            print(f"Your color is {color}")

            # main gameplay
            gameplay = OnlineGame(game, USERNAME, opponent, color, OUTPUT)
            gameplay.playOnline()
            del gameplay

            # prompt user to play again or exit program
            menu = Menu(OUTPUT, ("Do you", "want to", "keep", "playing?"), ["y", "n"])
            selection = menu.select()
            if selection == "n":
                break

