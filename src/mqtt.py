import paho.mqtt.client as mqtt
import time

name = ""

def parseMessage(message):
    parsedMessage = tuple(map(str, message.split(", ")))
    return parsedMessage

def inputName(client):
    global name
    name = input("Enter your name: ")
    client.publish("ledGames/users/status", name)

def verifyName(client, userdata, msg):
    global name
    response = str(msg.payload, "utf-8")

    eyeD, ack = parseMessage(response)

    if eyeD == name:

        if ack == "1":
            client.unsubscribe("ledGames/users")
            client.subscribe("ledGames/lobby")
            client.subscribe("ledGames/" + str(eyeD) )
            return
        else:
            print("Your username was invalid.")
            inputName(client)


def onConnect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))
    client.subscribe("ledGames/users")
    client.message_callback_add("ledGames/users", verifyName)
    inputName(client)



def onMessage(client, userdata, msg):
    print("onMessage")
    #print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def mqttInit():   
    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    while True:
        time.sleep(3)

if __name__ == '__main__':
    mqttInit()
    
