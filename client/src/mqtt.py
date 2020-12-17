import time

import paho.mqtt.client as mqtt

from outputs import TerminalDisplay
from parsersM import parseMessage
from inputs import Reader, Menu

class mqttClient:
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
    def __init__(self, Output):
        super().__init__()
        self.output = Output
        self.username = ""
        self.verified = 0 # -1 rejected, 0 unverified, 1 verified
        self.client.subscribe("ledGames/users")
        self.client.message_callback_add("ledGames/users", self.usernameCallback)

    def getUsername(self):
        # loop until username is verified
        while self.verified != 1:
             # create reader
            prompt = "Enter your username:"
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
                self.output.show("Username taken")
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
    def __init__(self, username, game, output):
        super().__init__()
        self.output = output
        self.username = username
        self.game = game
        self.selected = "" # name of user that I selected
        self.requester = "" # name of user that sent me a request
        self.opponentResponse = 0 # -1 rejected, 0 waiting, 1 accepted

        self.client.subscribe("ledGames/lobby")
        self.client.message_callback_add("ledGames/lobby", self.lobbyCallback)
        self.client.subscribe(f"ledGames/{self.username}/requests")
        self.client.message_callback_add(f"ledGames/{self.username}/requests", self.myCallback)

        self.menu = Menu(self.output, "Choose an opponent:")


        
    def lobby(self):
        # join lobby
        self.client.publish("ledGames/lobby/status", f"{self.username}, {self.game}, 1")

        # wait until lobby is received and other players are present
        while self.menu.options == []:
            pass

        # choose an opponent
        while True:
            self.selected = ""
            self.selected = self.menu.select()
            print("selected:", self.selected)
            time.sleep(2)
            # if menu was exited because an opponent sent me a request, process the request
            if self.selected == 0:
                menu = Menu(self.output, f"Accept game with {self.requester}?", ["y", "n"])
                selection = menu.select()

                # if the request is accepted, send accept message and finalize opponent
                if selection == "y":
                    self.client.publish(f"ledGames/{self.requester}/requests", f"{self.username}, 1")
                    self.selected = self.requester
                    break
                    
                # if the request is denied, send deny message and return to choosing an opponent
                else:
                    self.client.publish(f"ledGames/{self.requester}/requests", f"{self.username}, -1")
                    self.requester = ""

            # otherwise, send a request to the selected opponent
            else:
                self.client.publish(f"ledGames/{self.selected}/requests", f"{self.username}, 0") 
                self.opponentResponse = 0

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

        return self.selected



    def myCallback(self, client, useradata, msg):

        opponent, code = parseMessage(msg)
        code = int(code)

        if code == 0:
            # exit selection menu if opponent sent me a request
            self.requester = opponent
            self.menu.exitMenu()
        else:
            # -1 if opponent rejected, 1 if opponent confirmed my request
            self.opponentResponse = code 
        


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

class Game(mqttClient):
    def __init__(self, game, username, opponent):
        pass








if __name__ == "__main__":
    OUTPUT = TerminalDisplay()

    """
    DEMO USERNAME_GENERATOR CODE
    """
    usernameGenerator = UsernameGenerator(OUTPUT)
    USERNAME = usernameGenerator.getUsername()
    print(f"You chose the username: {USERNAME}")
    time.sleep(2)

    """
    DEMO LOBBY CODE (do not comment out previous demo code)
    """
    GAME = "Checkers"
    lobby = Lobby(USERNAME, GAME, OUTPUT)
    lobby.lobby()


    """
    DEMO GAME CODE
    """