import time

import paho.mqtt.client as mqtt

from outputs import TerminalDisplay
from parser import parseMessage
from inputs import Reader, Menu

class mqttMessenger:
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

class UsernameGenerator(mqttMessenger):
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
            self.verified = 0
            # send username to be verified
            self.client.publish("ledGames/users/status", f'{self.username}, 1')
            # wait for a response
            while self.verified == 0:
                pass
                # usernameCallback will either set self.verified to 1 or -1
                # if self.verified == 1, then getUsername returns the verified username
                # if self.verified == -1, the outer while loop repeats
            if self.verified == -1:
                self.output.show("Username taken")
                time.sleep(1)
        return self.username

    def usernameCallback(self, client, userdata, msg):
        name, code = parseMessage(msg)
        # only take action for messages addressed to this user
        if name == self.username:
            if code == "1":
                self.verified = 1
            else:
                self.verified = -1

class Lobby(mqttMessenger):
    def __init__(self, username, game, output):
        super().__init__()
        self.output = output
        self.username = username
        self.game = game
        self.opponent = ""
        self.choseOpponent = 0 # -1 rejected, 0 waiting, 1 confirmed/accepted
        self.waiting = False

        self.client.subscribe("ledGames/lobby")
        self.client.message_callback_add("ledGames/lobby", self.lobbyCallback)
        self.client.subscribe(f"ledGames/{self.username}/requests")
        self.client.message_callback_add(f"ledGames/{self.username}/requests", self.myCallback)

        prompt = "Choose an opponent:"
        options = []
        self.menu = Menu(prompt, options, self.output)

        
    def lobby(self):
        self.client.publish("ledGames/lobby", f"{self.username}, {self.game}, 1")
        while self.menu.options == []:
            pass
        while self.choseOpponent == 0:
            self.selectOpponent()
            self.client.publish(f"ledGames/{self.opponent}/requests", f"{self.username}, 1")
            self.waiting = True
            while self.waiting:
                pass

    def myCallback(self, client, useradata, msg):
        pass
            
    
        
    def lobbyCallback(self, client, userdata, msg):
        players = parseMessage(msg)
        opponents = []
        for player in players:
            if player[1] == self.game:
                if not player[0] == self.username:
                    opponents.append(player[0])
        self.menu.updateOptions(opponents)

    def selectOpponent(self):
        self.opponent = self.menu.select()


class Game(mqttMessenger):
    def __init__(self, game, username, opponent):
        pass








if __name__ == "__main__":
    """
    DEMO USERNAME_GENERATOR CODE
    """
    OUTPUT = TerminalDisplay()
    usernameGenerator = UsernameGenerator(OUTPUT)
    username = usernameGenerator.getUsername()
    print(f"You chose the username: {username}")
    time.sleep(3)