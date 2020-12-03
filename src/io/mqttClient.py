import paho.mqtt.client as mqtt

class mqttClient:
    def __init__(self):
        client = mqtt.Client()
        client.on_connect = self.onConnect
        client.on_message = self.onMessage
        client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
        client.loop_start()

    def onConnect(client, userdata, flags, rc):
        pass

    def onMessage(self):
        pass