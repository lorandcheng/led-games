import string
import time

from pynput import keyboard

class Listener:
    """
    Class usage:
    This class is for menu selection requiring user input. A listener object is initialized with a parameter of the menu length.
    The calling code should wait in a while loop and break when Listener.selected == 1
    In the while loop, the menu display should be updated according to the selected index Listener.index
    """
    def __init__(self, length=1):
        self.key = keyboard.Listener(
            on_press = self.onPress,
            on_release = self.onRelease
            )
        self.key.start()
        self.index = 0
        self.rChange = 0
        self.cChange = 0
        self.rotate = False
        self.selected = False
        self.len = length
        self.keypress = False
        print("listener setup done")

    def onPress(self, key):
        self.keypress = True
        if not self.selected and self.len != 0:
            index = self.index
            rChange = self.rChange
            cChange = self.cChange

            try:
                k = key.char # single-char keys
            except: 
                k = key.name # other keys
        
            if k == "up":
                index -= 1
                rChange -= 1
            elif k == "left":
                index -= 1
                cChange -= 1
            elif k == "down":
                index += 1
                rChange += 1
            elif k == "right":
                index += 1
                cChange += 1
            elif k == "shift_r" or k == "shift":
                self.rotate = True
                print("rotate")
            elif k == "enter":
                self.selected = True
            
            if index > self.len-1:
                index = 0
            elif index < 0:
                index = self.len-1

            self.index = index
            self.rChange = rChange
            self.cChange = cChange

    def resetChanges(self):
        self.rChange = 0
        self.cChange = 0

    def resetRotate(self):
        self.rotated = False

    def onRelease(self, key):
        pass

    def __del__(self):
        self.key.stop()

class Reader(Listener):
    def __init__(self, output, prompt=()):
        self.prompt = prompt
        self.str = ""

        #TODO: limit username length for scrolling ?
        
        self.chars = ["_"]
        self.chars += list(string.ascii_lowercase+string.digits)
        self.output = output
        super().__init__(len(self.chars))
    
    def getStr(self):
        return self.str
    
    def printPrompt(self):
        self.output.clear()
        if type(self.output).__name__ == "TerminalDisplay":
            toPrint = " ".join(self.prompt)

        elif type(self.output).__name__ == "LedDisplay":
            # define the number and width of rows on the display
            _, chars = self.output.getTextDimensions()
            toPrint = []
            for word in self.prompt:
                toPrint.append(word.center(chars))
            toPrint = tuple(toPrint)       
        else:
            print("Unsupported output")
            raise ValueError
        
        self.output.show(toPrint)
        self.keypress = False
        while not self.keypress:
            pass
        self.output.clear()

    def readStr(self):
        self.printPrompt()
        self.selected = False
        self.output.show(self.chars[self.index])
        oldIndex = self.index
        while True:
            if oldIndex != self.index:
                self.output.clear()
                self.output.show(str(self.str+self.chars[self.index]))
                oldIndex = self.index
            if self.selected:
                if self.chars[self.index] == "_":
                    if len(self.str) != 0:
                        return self.str
                    else:
                        self.output.clear()
                        self.output.show(("Enter", "a valid", "username"))
                else:
                    self.str += self.chars[self.index]
                    self.index = 0

                self.selected = False
    
    def __del__(self):
        self.key.stop()


class Menu(Listener):
    def __init__(self, output, prompt=(), options=[], indexing=False):
        self.output = output
        self.prompt = prompt
        self.options = options
        self.indexing = indexing
        self.exit = False
        super().__init__(len(options))

    def updateOptions(self, newOptions):
        self.options = newOptions
        self.len = len(newOptions)

    def printOptions(self):
        # define the number and width of rows on the display
        rows, chars = self.output.getTextDimensions()
        # clear the display
        self.output.clear()
        # copy the options to print
        toPrint = self.options.copy()
        # copy the index so it stays constant during this function
        index = self.index
        # indent the non-selected options with a space
        for i in range(len(toPrint)):
            if i != index:
                toPrint[i] = " " + toPrint[i]
        # If the length of the selected option is greater than the number of characters that can fit, scroll the line
        if len( toPrint[index] ) >= chars:
            scrollIndex = 0
            for i in range(chars-1):
                    toPrint[index] += " "
            original = toPrint[index]
            while self.index == index and not self.selected:
                self.output.clear()
                str = ">" + toPrint[index][scrollIndex:] + toPrint[index][:scrollIndex]
                toPrint[index] = str
                # vertical scroll
                if index > (rows-1):
                    trunc = toPrint[index-(rows-1):]
                    self.output.show(tuple(trunc))
                else:
                    self.output.show(tuple(toPrint))

                time.sleep(0.4)
                scrollIndex += 1
                if scrollIndex > len(toPrint[index]):
                    scrollIndex = 0
                toPrint[index] = original
                
        # Non-scrolling
        else:
            toPrint[self.index] = ">" + toPrint[self.index]

            if self.index > (rows-1):
                toPrint = toPrint[self.index-(rows-1):]
            self.output.show(tuple(toPrint))

    def printPrompt(self):
        self.output.clear()
        if type(self.output).__name__ == "TerminalDisplay":
            toPrint = " ".join(self.prompt)

        elif type(self.output).__name__ == "LedDisplay":
            # define the number and width of rows on the display
            _, chars = self.output.getTextDimensions()
            toPrint = []
            for word in self.prompt:
                toPrint.append(word.center(chars))
            toPrint = tuple(toPrint)       
        else:
            print("Unsupported output")
            raise ValueError
        
        self.output.show(toPrint)
        self.keypress = False
        while not self.keypress and not self.exit:
            pass
        self.output.clear()

    def select(self):
        self.printPrompt()
        self.selected = False
        oldIndex = self.index
        self.printOptions()
        while True:
            if self.exit:
                return 0
            if oldIndex != self.index:
                oldIndex = self.index
                self.printOptions()
            if self.selected:
                try:
                    if self.indexing:
                        return (self.index, self.options[self.index])
                    else:
                        return self.options[self.index]
                except:
                    print("List was updated since your selection")

    def exitMenu(self):
        self.exit = True

    def __del__(self):
        self.key.stop()

if __name__ == '__main__':
    from outputs import TerminalDisplay, LedDisplay

    OUTPUT = LedDisplay()
    """
    DEMO LISTENER CODE
    """
    # listener = Listener(10)
    # print("Starting keyboard listener")
    # oldIndex = listener.index
    # while True:
    #     if oldIndex != listener.index:
    #         print("\nUpdating menu")
    #         print("Index value:", listener.index)
    #         oldIndex = listener.index
    #     if listener.selected:
    #         break
    # print("A selection has been made at index", listener.index)

    """
    DEMO READER CODE
    """
    # prompt = ("Enter", "a name")
    # reader = Reader(OUTPUT, ("Enter", "a name"))
    # print("Starting reader")
    # reader.readStr()
    # print("You entered:", reader.getStr())

    """
    DEMO MENU CODE
    """
    prompt = ("Choose", "an", "option")
    options = ["option 1", "option 2", "option 3", "option 4", "option 5", "option option 6", "option option 7"]
    menu = Menu(OUTPUT, prompt, options, indexing=True)
    index, selection = menu.select()
    print("You chose:", selection, "at index", index)
    del menu