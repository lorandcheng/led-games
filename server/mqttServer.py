"""
MQTT SERVER STEPS
=================
1. Start server:
    - SUB "ledGames/users/status"
    - SUB "ledGames/lobby/status"
2. Listen for incoming user connections on "ledGames/users/status"
    - when a new user connects, add them to USERS list
    - reject already used usernames
    - TODO remove users who leave
3. Listen for incoming lobby connections on "ledGames/lobby/status"
    - when a new user joins the lobby, send out an updated lobby list
    - TODO remove users from lobby

"""

import paho.mqtt.client as mqtt

USERS = []
LOBBY = []

def parseMessage(msg):
    message = str(msg.payload, "utf-8")
    parsedMessage = tuple(map(str, message.split(", ")))
    return parsedMessage

def users(client, userdata, msg):
    """
    msg: (name, action)
        name: username
        action: 1(add), 0(remove)
    """
    name, action = parseMessage(msg)
    if int(action):
        if name in USERS:
            print("denied")
            client.publish("ledGames/users", f'{name}, 0')
        else:
            client.publish("ledGames/users", f'{name}, 1')
            USERS.append(name)
            print("user added: " + name)
            print(USERS)
    elif int(action)==0:
        print("removing")
        try:
            USERS.remove(name)
            print("user removed: " + name)
            print(USERS)
        except:
            pass

def lobby(client, userdata, msg):
    user = parseMessage(msg)
    print(user, "entered lobby")
    LOBBY.append(user)
    print(LOBBY)
    client.publish("ledGames/lobby", str(LOBBY))

def onConnect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))
    client.subscribe("ledGames/users/status")
    client.subscribe("ledGames/lobby/status")

    client.message_callback_add("ledGames/users/status", users)
    client.message_callback_add("ledGames/lobby/status", lobby)
    

def onMessage(client, userdata, msg):
    print("onMessage")

def mqttInit():   
    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    while True:
        pass


if __name__ == '__main__':
    mqttInit()