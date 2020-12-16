import time

import paho.mqtt.client as mqtt

from outputs import TerminalDisplay
from parser import parseMessage
from inputs import Reader

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

if __name__ == "__main__":
    """
    DEMO USERNAME_GENERATOR CODE
    """
    OUTPUT = TerminalDisplay()
    usernameGenerator = UsernameGenerator(OUTPUT)
    username = usernameGenerator.getUsername()
    print(f"You chose the username: {username}")
    time.sleep(3)