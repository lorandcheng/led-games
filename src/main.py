# Standard library imports
import time

# Third party imports
import paho.mqtt.client as mqtt

# Module imports
from games import battleship, checkers

def onConnect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))

def onMessage(client, userdata, msg):
        pass
    # callback functions here

def main():
    # mqtt stuff
    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    game = checkers.Checkers()
    game.main()



if __name__ == '__main__':
    main()