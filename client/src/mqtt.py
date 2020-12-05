import paho.mqtt.client as mqtt
import time

name = ""

def parseMessage(msg):
    message = str(msg.payload, "utf-8")
    parsedMessage = tuple(map(str, message.split(", ")))
    return parsedMessage

def inputName(client):
    global name
    name = input("Enter your name: ")
    client.publish("ledGames/users/status", f'{name}, 1')

def verifyName(client, userdata, msg):
    global name
    eyeD, ack = parseMessage(msg)
    if eyeD == name:
        if ack == "1":
            client.unsubscribe("ledGames/users")
            client.subscribe("ledGames/" + str(eyeD))
        else:
            print("Your username was invalid.")
            inputName(client)

def joinLobby(client, name, game):
    client.subscribe("ledGames/lobby")
    # game = chooseGame()
    # client.publish("ledGames/lobby/status", str((name, game)))

def onConnect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))
    client.subscribe("ledGames/users")
    client.message_callback_add("ledGames/users", verifyName)



def onMessage(client, userdata, msg):
    print("onMessage")
    #print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def onDisconnect(client):
    pass

def mqttInit():   
    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage
    client.on_disconnect = onDisconnect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    inputName(client)
    return client
    

if __name__ == '__main__':
    client =  mqttInit()
    while True:
        pass
