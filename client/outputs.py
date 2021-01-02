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
        self.font.LoadFont("rpi-rgb-led-matrix/fonts/4x6.bdf")
        self.textColor = graphics.Color(100, 100, 100)

        self.canvas = self.matrix.CreateFrameCanvas()
    
    def clear(self):
        self.matrix.Clear()
        self.canvas.Clear()

    def show(self, info):
        # first attempt at code that will print multiple lines, could be rerwitten to be easier
        if type(info) == tuple:
            index = 10 # First line in which text can be placed on matrix
            LENGTH = 10 # random constant depending on which font is chosen

            for elem in info:
                if len(elem) > 8:
                    pos = self.canvas.width

                    while True:
                        self.canvas.Clear()
                        length = graphics.DrawText(self.canvas, self.font, pos, index, self.textColor, elem)
                        pos -= 1
                        if (pos + length < 0):
                            pos = self.canvas.width

                        time.sleep(0.05)
                        self.canvas = self.matrix.SwapOnVSync(self.canvas)

                    length = graphics.DrawText(self.canvas, self.font, 0, index, self.textColor, elem) # print what you can after it scrolls
                    
                else:
                    graphics.DrawText(self.canvas, self.font, 0, index, self.textColor, elem)
                    self.canvas = self.matrix.SwapOnVSync(self.canvas)

                index += LENGTH # move to next line on matrix


        if type(info) == str:
            if len(info) > 8:
                pos = self.canvas.width
                while True:
                    self.canvas.Clear()
                    length = graphics.DrawText(self.canvas, self.font, pos, 10, self.textColor, info)
                    pos -= 1
                    if (pos + length < 0):
                        pos = self.canvas.width

                    time.sleep(0.05)
                    self.canvas = self.matrix.SwapOnVSync(self.canvas)
            else:
                graphics.DrawText(self.canvas, self.font, 0, 10, self.textColor, info)
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
    output = "Username"
    display = LedDisplay()
    display.show(output)
    time.sleep(20)
