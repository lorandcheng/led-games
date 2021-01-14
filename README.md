# LED Games
Contributors: Baran Cinbis, Lorand Cheng, and Evan Hashemi

https://docs.google.com/document/d/1WUN66qfwrXprSUxHzGAIiJu6dU_1FVBbShIlPxwt1o8/edit?usp=sharing

## Summary
This repository contains the source code for an LED matrix version of some traditional board games. Using an LED matrix, a controller, and a raspberry pi, players can connect to other players online and choose from a selection of games to play. The code is easily extendable to add other game modules. All source code in this repo with the exception of the LED matrix library have been written from scratch by the contributors listed. Our goal with this project has been to apply what we have learned in our distributed and embedded systems courses.

### Games
- Checkers
- Battleship

### Hardware
- Raspberry pi
- Adafruit 32x32 5mm pitch LED matrix
- Custom hardware controller (future)

### External Libraries Used
- paho-mqtt
- rpi-rgb-led-matrix library by HZeller https://github.com/hzeller/rpi-rgb-led-matrix
