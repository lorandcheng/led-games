"""
MQTT CLIENT STEPS
=================

SETUP self.username
--------------
1. SUB "ledGames/users"
2. Generate a self.username
3. Check self.username against existing self.usernames by PUB "ledGames/user/status" 
    message = (name, code)
    name: generated self.username
    code: 1 to add, 0 to remove self.username
4. Listen for a response on "ledGames/users"
    response = (name, code)
    name: self.username that the response is for
    code: 1 for sucess, 0 for failure (self.username taken or other failure)

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
    name: self.username
    request: 1 to request or confirm, 0 to deny
9. Listen for a response on "ledGames/<self.username>/request"
    response = (opponent, request)
    opponent: opponent's self.username
    request: 1 to request or confirm, 0 to deny
10. If the request was denied, repeat from step 7, otherwise leave lobby with PUB "ledGames/lobby/status"
    message = (name, game)
    name: user updating status
    game: game user wants to play, or 0 to leave lobby

PLAY GAME
---------
Each player listens on "ledGames/<ownself.username>/play" and sends on "ledGames/<opponentsself.username>/play"

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


import paho.mqtt.client as mqtt
import time
import os
from pynput import keyboard

import controller

class mqttClient:
    def __init__(self):
        self.username = ""
        self.unverified = ""
        self.players = []
        self.game = 0
        self.client = mqtt.Client()
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.on_disconnect = self.onDisconnect
        self.client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
        self.client.loop_start()
        self.key = keyboard.Listener(on_press = self.onPress)
        self.index = 0
        self.selected = 0
        self.requested = 0

    def onPress(self, key):
        try: 
            k = key.char # single-char keys
        except: 
            k = key.name # other keys
    
        if k == "a":
            self.index -=1
            print("a")
        elif k == "d":
            self.index +=1
            print("d")
        elif k == "e":
            self.selected = 1

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
        self.unverified = controller.getName()
        client.publish("ledGames/users/status", f'{self.unverified}, 1')

    def verifyName(self, client, userdata, msg):
        name, code = self.parseMessage(msg)
        if name == self.unverified:
            if code == "1":
                client.unsubscribe("ledGames/users")
                self.username = self.unverified
                client.subscribe(f"ledGames/{self.username}/requests")
                client.message_callback_add(f"ledGames/{self.username}/requests", self.myCallback)
            else:
                print("Your username was invalid.")
                self.inputName(client)
        

    def myCallback(self, client, userdata, msg):
        self.requested = 1
        request = self.parseMessage(msg)
        print(request[1])
        print(type(request[1]))
        if str(request[1]) == "1":
            # add to controller later
            inp = input(f"accept match request from {request[0]}?  Type y/n")
            if inp == "y":
                client.publish(f"ledGames/{request[0]}/requests", f"{self.username}, 2")
            elif inp == "n":
                client.publish(f"ledGames/{request[0]}/requests", f"{self.username}, 0")
                self.requested = 0
                self.chooseOpponent(self.players)

        elif str(request[1]) == "2":
            print("match confirmed")
        elif str(request[1]) == "0":
            self.requested = 0
            print("george bush did pizzagate")
            self.chooseOpponent(self.players)




    def lobbyCallback(self, client, userdata, msg):
        """
        Exception case: what if a new user joins while you are doing something like choosing an opponent, etc.
        """
        self.players = self.parseMessage(msg)
        

    def joinLobby(self, client, game):
        client.subscribe("ledGames/lobby")
        client.message_callback_add("ledGames/lobby", self.lobbyCallback)
        self.game = game
        print("joined lobby", self.username, game.name)
        client.publish("ledGames/lobby/status", f'{self.username}, {game.name}')

    def chooseOpponent(self, players):
        self.key.start()
        self.index = 0
        oldIndex = 0
        available = []
        for player in players:
            if player[1] == self.game.name:
                if not player[0] == self.username:
                    available.append(player[0])

        while True:
            if self.requested == 1:
                break
            elif not oldIndex == self.index:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Use 'a' and 'd' to cycle, 'e' to select")
                print('Choose an opponent:')

                
                if self.index > len(available)-1:
                    self.index = 0
                elif self.index < 0:
                    self.index = len(available)-1

                for i in range(len(available)):
                    if i == self.index:
                        print('* ' + available[i])
                    else:
                        print('  ' + available[i])
                
                if self.selected == 1:
                    self.selected = 0
                    break
                oldIndex = self.index
        return available[self.index]


    def onConnect(self, client, userdata, flags, rc):
        print("Connection returned " + str(rc))
        client.subscribe("ledGames/users")
        client.message_callback_add("ledGames/users", self.verifyName)

    def onMessage(self, client, userdata, msg):
        print("onMessage")
        #print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

    def onDisconnect(self, client, useradata, rc):
        print("disconnecting")
        

