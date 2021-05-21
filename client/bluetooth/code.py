
import digitalio
import analogio
import board
import time
from adafruit_ble import *
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

## Joystick Stuff ###############################################

# Set the pin number
buttonJ = digitalio.DigitalInOut(board.D6)
# Input/output
buttonJ.direction = digitalio.Direction.INPUT
# Pullup resistor
buttonJ.pull = digitalio.Pull.UP

x = analogio.AnalogIn(board.A4)
y = analogio.AnalogIn(board.A0)

MIN = 0
MAX = 2**16
THRESHOLD = 3000

## Clue Buttons Stuff ###############################################

buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonB = digitalio.DigitalInOut(board.BUTTON_B)

buttonA.pull = digitalio.Pull.UP
buttonB.pull = digitalio.Pull.UP


## BLE Stuff ######################################################
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)



#ble.start_advertising(advertisement)

while True:
  ble.start_advertising(advertisement)
  print("Waiting to connect")
  while not ble.connected:
    pass
  print("Connected")
  while ble.connected:
  	#s = input("Eval: ")
    #uart_service.write(s.encode("utf-8"))
    #uart_service.write(b'\n')
    #print(uart_service.readline().decode("utf-8"))

    

    # Access the pin values with .value tag!

    #print("Button value: " + button.value)
    #print(x.value)
    #print(y.value)
    message = "none"
    # Access the pin values with .value tag!
    #print("\n\n\nJOYSTICK STATUS")
    # Button
    

    #message = ""
    # x-direction
    if x.value in range(MIN, MIN + THRESHOLD):
  	  print("Left")
  	  message = "Left"
  	  while x.value in range(MIN, MIN + THRESHOLD):
  	  	pass
    elif x.value in range(MAX - THRESHOLD, MAX):
      print("Right")
      message = "Right"
      while x.value in range(MAX - THRESHOLD, MAX):
  	  	pass

    # y-direction
    elif y.value in range(MIN, MIN + THRESHOLD):
      print("Up")
      message = "Up"
      while y.value in range(MIN, MIN + THRESHOLD):
      	pass
    elif y.value in range(MAX - THRESHOLD, MAX):
      print("Down")
      message = "Down"
      while y.value in range(MAX - THRESHOLD, MAX):
      	pass
    elif buttonJ.value == 0:
      print("J")
      message = "J"
      while buttonJ.value == 0:
  	  	pass
    elif buttonA.value == 0:
  	  print("A")
  	  message = "A"
  	  while buttonA.value == 0:
  	  	pass

    elif buttonB.value == 0:
  	  print("B")
  	  message = "B"
  	  while buttonB.value == 0:
  	  	pass
    else:
  	  message = "None"

    if message != "None":
      uart.write((message+"\n").encode("utf-8"))

  '''
  ble.start_advertising(advertisement)
  while not ble.connected:
  	pass
  '''
  