import os
import sys
import time

if sys.platform == "linux" or sys.platform == "linux2":
    # Add paths to matrix python modules
    sys.path.append('rpi-rgb-led-matrix/bindings/python/rgbmatrix')
    sys.path.append('rpi-rgb-led-matrix/bindings/python/samples')

    from samplebase import SampleBase
    from rgbmatrix import graphics, RGBMatrixOptions, RGBMatrix

class TerminalDisplay:
    def __init__(self):
        pass

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show(self, info):
        print(info)

class LedDisplay:
    def __init__(self):
        # Configuration for the matrix
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 32
        options.chain_length = 1
        options.parallel = 1
        options.gpio_slowdown = 5
        options.hardware_mapping = 'adafruit-hat' 

        # Configuration for the matrix
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 32
        options.chain_length = 1
        options.parallel = 1
        options.gpio_slowdown = 5
        options.hardware_mapping = 'adafruit-hat' 

        # Enter in the hardware configurations
        self.matrix = RGBMatrix(options = options)

        # Specifications for Font style of text
        self.font = graphics.Font()
        self.font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")

        self.canvas = self.matrix.CreateFrameCanvas()
    
    def clear(self):
        self.matrix.Clear()

    def show(self, info):
        for r in range(self.matrix.height):
            for c in range(self.matrix.width):
                R, G, B = info[r][c]
                self.canvas.SetPixel(r, c, R, G, B)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)


if __name__ == "__main__":


    colors = {
                "red": (255, 0, 0),
                "black": (0, 0, 0),
                "white": (255, 255, 255)
            }

    output = []
    for r in range(32):
        output.append([])
        for c in range(32):
            if ((r % 8 < 4) and (c % 8 < 4)) or ((r % 8 > 4) and (c % 8 > 4)):
                output[r].append(colors['red'])
            else:
                output[r].append(colors['black'])







    display = LedDisplay()
    display.show(output)
    time.sleep(20)