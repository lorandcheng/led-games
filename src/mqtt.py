import paho.mqtt.client as mqtt


def onConnect(client, userdata, flags, rc):
    #print("Connection returned " + str(rc))
    pass
    # client.subscribe("")

def onMessage(client, userdata, msg):
    pass
    # callback functions here

def mqttInit():
    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()