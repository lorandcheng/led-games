import os
import paho.mqtt.client as mqtt

USERS = []
LOBBY = []


def parseMessage(msg):
    message = str(msg.payload, "utf-8")
    parsedMessage = tuple(map(str, message.split(", ")))
    return parsedMessage


def users(client, userdata, msg):
    """
    Summary: handles username list (add and remove), and validation
    
    Arguments:
        client: mqtt client
        userdata: unused
        msg:(name, action)
            name: username
            action: 1(add), 0(remove)
    """
    name, action = parseMessage(msg)
    a = int(action)
    if a:
        if name in USERS:
            client.publish("ledGames/users", f'{name}, 0')
            print("\nuser tried to join with existing username:", name)
        else:
            client.publish("ledGames/users", f'{name}, 1')
            USERS.append(name)
            print("\nuser added:", name)
            print("users:", USERS)
    elif a == 0:
        try:
            USERS.remove(name)
            print("\nuser removed:", name)
            print("users:", USERS)
        except:
            print("\ntried to remove non-existent user")


def lobby(client, userdata, msg):
    """
    Summary: handles lobby list (add and remove)

    Arguments:
        client: mqtt client
        userdata: unused
        msg:(name, game, action)
            name: username
            game: game to join lobby with
            action: 1(add), 0(remove)
    """
    name, game, action = parseMessage(msg)
    a = int(action)
    if a == 1:
        LOBBY.append((name, game))
        client.publish("ledGames/lobby", str(LOBBY))
        print("\n" + name, "entered lobby to play", game)
        print("lobby:", LOBBY)
    elif a == 0:
        for entry in LOBBY:
            if entry[0] == name:
                print("\nuser removed from lobby:", name)
                LOBBY.remove(entry)


def onConnect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))

    client.subscribe("ledGames/users/status")
    client.subscribe("ledGames/lobby/status")

    client.message_callback_add("ledGames/users/status", users)
    client.message_callback_add("ledGames/lobby/status", lobby)
    

def onMessage(client, userdata, msg):
    print("onMessage")  


if __name__ == '__main__':
    """
    MQTT SERVER
    ===========
    1. Start server:
        - SUB "ledGames/users/status"
        - SUB "ledGames/lobby/status"
    2. Listen for incoming user connections on "ledGames/users/status"
        - when a new user connects, add them to USERS list
        - reject already used usernames
        - remove users who leave
    3. Listen for incoming lobby connections on "ledGames/lobby/status"
        - when a new user joins the lobby, send out an updated lobby list
        - remove users from lobby

    """
    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Starting mqtt server...")
    client.loop_forever()
