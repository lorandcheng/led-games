import paho.mqtt.client as mqtt

USERS = []
LOBBY = []

def parseMessage(msg):
    message = str(msg.payload, "utf-8")
    parsedMessage = tuple(map(str, message.split(", ")))
    return parsedMessage

def userStatus(client, userdata, msg):
    '''
    msg: (name, action) name = username, action = 1(add)/0(remove)
    '''
    name, action = parseMessage(msg)
    if action:
        if name in USERS:
            client.publish("ledGames/users", str((name, 0)))
        else:
            client.publish("ledGames/users", str((name, 1)))
            USERS.append(name)
            print("user added: " + name)
    else:
        try:
            USERS.remove(name)
            print("user removed: " + name)
        except:
            pass


def onConnect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))
    client.subscribe("ledGames/users/status")
    client.subscribe("ledGames/lobby/status")

    client.message_callback_add("ledGames/users/status", userStatus)
    

def onMessage(client, userdata, msg):
    print("onMessage")

def mqttInit():   
    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()


if __name__ == '__main__:
    mqttInit()