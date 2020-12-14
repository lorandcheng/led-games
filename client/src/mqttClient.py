"""
MQTT CLIENT STEPS
=================

SETUP username
--------------
1. SUB "ledGames/users"
2. Generate a username
3. Check username against existing usernames by PUB "ledGames/user/status" 
    message = (name, code)
    name: generated username
    code: 1 to add, 0 to remove username
4. Listen for a response on "ledGames/users"
    response = (name, code)
    name: username that the response is for
    code: 1 for sucess, 0 for failure (username taken or other failure)

JOIN LOBBY AND SELECT OPPONENT
------------------------------
5. SUB "ledGames/lobby" and "ledGames/<self.username>/#", add callbacks for lobby, request, and play
6. Join lobby with PUB "ledGames/lobby/status"
    message = (name, game)
    name: user updating status
    game: game user wants to play, or 0 to leave lobby
7. Choose an opponent from the lobby
    - identify players of the same game
8. Send the opponent a game request with PUB "ledGames/<opponent>/request"
    message = (name, request)
    name: username
    request: 1 to request or confirm, 0 to deny
9. Listen for a response on "ledGames/<self.username>/request"
    response = (opponent, request)
    opponent: opponent's username
    request: 1 to request or confirm, 0 to deny
10. If the request was denied, repeat from step 7, otherwise leave lobby with PUB "ledGames/lobby/status"
    message = (name, game)
    name: user updating status
    game: game user wants to play, or 0 to leave lobby

PLAY GAME
---------
Each player listens on "ledGames/<self.username>/play" and sends on "ledGames/<opponent.username>/play"

11. The player who initiated the connnection picks a random color, then sends the color assignments across
    message = [(name, color),(name, color)]
    name: one of the two self.usernames
    color: the corresponding color (varies by game)
        Checkers: 1 (black) or -1 (red)

12. After the first player makes a move, they send the game info
    message = (board, scores)
    board: setup of the board at the end of player's turn
    scores: scores at the end of player's turn

...

"""
import time
import os
import random
from pynput import keyboard
import paho.mqtt.client as mqtt

import controller
import output

class mqttClient:
    def __init__(self):
        self.username = ""
        self.verified = False
        self.lobby = []
        self.opponent = ""
        self.game = 0
        self.client = mqtt.Client()
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.on_disconnect = self.onDisconnect
        self.client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
        self.client.loop_start()
        self.requested = 0
        self.gameAccepted = 0
        self.start = 0
        self.boardStr = ""
        self.initiator = -1
        self.output = output.terminalDisplay()

    def parseMessage(self, msg):
        message = str(msg.payload, "utf-8")
        parsedMessage = []
        if message[0] == "[":
            message = message[2:len(message)-2]
            for entry in message.split("), ("):
                entry = entry[1:len(entry)-1]     
                parsedMessage.append(tuple(entry.split("', '")))
        else:
            parsedMessage = tuple(map(str, message.split(", ")))
        return parsedMessage

    def inputName(self, client):
        reader = controller.Reader()
        self.username = reader.readStr()
        client.publish("ledGames/users/status", f'{self.username}, 1')

    def verifyName(self, client, userdata, msg):
        name, code = self.parseMessage(msg)
        if name == self.username:
            if code == "1":
                client.unsubscribe("ledGames/users")
                self.verified = True
                client.subscribe(f"ledGames/{self.username}/requests")
                client.message_callback_add(f"ledGames/{self.username}/requests", self.myCallback)
            else:
                print("Your username was invalid.")
                self.inputName(client)
        

    def playCallback(self, client, userdata, msg):
        print("you recieved a turn")
        self.boardStr = str(msg.payload, 'utf-8')

    def myCallback(self, client, userdata, msg):
        self.requested = 1
        request = self.parseMessage(msg)

        if str(request[1]) == "1":
            inp = input(f"accept match request from {request[0]}?  Type y/n \n")
            if inp[-1] == "y":
                print("confirming request")
                # print(f"ledGames/{request[0]}/requests" + f"{self.username}, 2")
                client.publish(f"ledGames/{request[0]}/requests", f"{self.username}, 2")
                client.subscribe(f"ledGames/{self.username}/play")
                client.message_callback_add(f"ledGames/{self.username}/play", self.playCallback)
                client.publish(f"ledGames/lobby/status", f'{self.username}, , 0')
                self.start = 1
                self.initiator = 0
                self.opponent = str(request[0])
            elif inp[-1] == "n":
                print("rejecting request")
                client.publish(f"ledGames/{request[0]}/requests", f"{self.username}, 0")
                self.requested = 0
                # self.chooseOpponent()

        elif str(request[1]) == "2":
            print("match confirmed")
            client.publish(f"ledGames/lobby/status", f'{self.username}, , 0')
            self.start = 1
            self.initiator = 1
            client.subscribe(f"ledGames/{self.username}/play")
            client.message_callback_add(f"ledGames/{self.username}/play", self.playCallback)
        elif str(request[1]) == "0":
            self.requested = 0
            print("george bush did pizzagate")
            # self.chooseOpponent()

    def lobbyCallback(self, client, userdata, msg):
        """
        Exception case: what if a new user joins while you are doing something like choosing an opponent, etc.
        """
        self.lobby = self.parseMessage(msg)
        
    def joinLobby(self, client, game):
        client.subscribe("ledGames/lobby")
        client.message_callback_add("ledGames/lobby", self.lobbyCallback)
        self.game = game
        print(self.username, "joined the lobby to play", game.name)
        client.publish("ledGames/lobby/status", f'{self.username}, {game.name}, 1')

    def selectOpponent(self, players):
        """
        exception case: if there are no players to choose from?
        """
        # initialize listener
        listener = controller.Listener(len(players))
        # define printing function
        def printPlayers(self):
            self.output.clear()
            for i in range(len(players)):
                if i == listener.index:
                    self.output.show('* ' + players[i])
                else:
                    self.output.show('  ' + players[i])
        
        printPlayers(self)
        oldIndex = listener.index
        while True:
            if oldIndex != listener.index:
                printPlayers(self)
                oldIndex = listener.index
            if listener.selected:
                self.opponent = players[listener.index]
                return self.opponent
            if self.requested:
                return 0

    def findOpponents(self, players):
        opponents = []
        for player in players:
            if player[1] == self.game.name:
                if not player[0] == self.username:
                    opponents.append(player[0])
        return opponents

    def onConnect(self, client, userdata, flags, rc):
        print("Connection returned " + str(rc))
        client.subscribe("ledGames/users")
        client.message_callback_add("ledGames/users", self.verifyName)

    def onMessage(self, client, userdata, msg):
        print("onMessage")
        #print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

    def onDisconnect(self, client, useradata, rc):
        print("disconnecting")
        

