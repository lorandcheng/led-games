"""
MQTT CLIENT STEPS
=================

SETUP USERNAME
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
5. SUB "ledGames/lobby" and "ledGames/<username>/#", add callbacks for lobby, request, and play
6. Join lobby with PUB "ledGames/lobby/status"
    message = (name, game)
    name: user updating status
    game: game user wants to play, or 0 to leave lobby
7. Choose an opponent from the lobby
8. Send the opponent a game request with PUB "ledGames/<opponent>/request"
    message = (name, request)
    name: username
    request: 1 to request or confirm, 0 to deny
9. Listen for a response on "ledGames/<username>/request"
    response = (opponent, request)
    opponent: opponent's username
    request: 1 to request or confirm, 0 to deny
10. If the request was denied, repeat from step 7, otherwise leave lobby with PUB "ledGames/lobby/status"
    message = (name, game)
    name: user updating status
    game: game user wants to play, or 0 to leave lobby

PLAY GAME
---------
Each player listens on "ledGames/<ownUsername>/play" and sends on "ledGames/<opponentsUsername>/play"

11. The player who initiated the connnection picks a random color, then sends the color assignments across
    message = [(name, color),(name, color)]
    name: one of the two usernames
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
import json

import controller

username = ""

def parseMessage(msg):
    message = str(msg.payload, "utf-8")
    parsedMessage = ""
    print(message)
    if message[0] == "[":
        parsedMessage = json.loads(message)
        for entry in parsedMessage:
            entry = parseMessage(entry)
        print(parsedMessage[0])
    else:
        parsedMessage = tuple(map(str, message.split(", ")))
    return parsedMessage

def inputName(client):
    global username
    username = controller.getName()
    client.publish("ledGames/users/status", f'{username}, 1')

def verifyName(client, userdata, msg):
    global username
    name, code = parseMessage(msg)
    if name == username:
        if code == "1":
            client.unsubscribe("ledGames/users")
            client.subscribe("ledGames/" + str(username))
            client.message_callback_add("ledGames/" + str(username), myCallback)
        else:
            print("Your username was invalid.")
            inputName(client)

def myCallback(client, userdata, msg):
    print(str(msg.payload, "utf-8"))

def lobbyCallback(client, userdata, msg):
    print(str(msg.payload, "utf-8"))

def joinLobby(client, game):
    client.subscribe("ledGames/lobby")
    client.message_callback_add("ledGames/lobby", lobbyCallback)
    print("joined lobby", username, game.name)
    client.publish("ledGames/lobby/status", f'{username}, {game.name}')

def onConnect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))
    client.subscribe("ledGames/users")
    client.message_callback_add("ledGames/users", verifyName)

def onMessage(client, userdata, msg):
    print("onMessage")
    #print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def onDisconnect(client, useradata, rc):
    print("disconnecting")

def mqttInit():   
    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage
    client.on_disconnect = onDisconnect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    return client
    

if __name__ == '__main__':
    client =  mqttInit()
    inputName(client)
        

