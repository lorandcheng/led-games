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
        self.textColor = graphics.Color(255, 255, 0)

        self.canvas = self.matrix.CreateFrameCanvas()
    
    def clear(self):
        self.matrix.Clear()
        self.canvas.Clear()

    def show(self, info):
        if type(info) == str:
            print("Displaying string:", info)
            if len(info) > 4:
                pos = self.canvas.width
                while True:
                    self.canvas.Clear()
                    len = graphics.DrawText(self.canvas, font, pos, 10, textColor, my_text)
                    pos -= 1
                    if (pos + len < 0):
                        pos = self.canvas.width

                    time.sleep(0.05)
                    self.canvas = self.matrix.SwapOnVSync(self.canvas)
            

        elif type(info) == list:
            for r in range(self.matrix.height):
                for c in range(self.matrix.width):
                    R, G, B = info[r][c]
                    self.canvas.SetPixel(r, c, R, G, B)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)

        else:
            print("Invalid input: must be a string or a list")
            raise ValueError


if __name__ == "__main__":
    output = "Testing strings"
    display = LedDisplay()
    display.show(output)
    time.sleep(20)