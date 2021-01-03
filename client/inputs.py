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
    def __init__(self, length):
        self.key = keyboard.Listener(
            on_press = self.onPress,
            on_release = self.onRelease
            )
        self.key.start()
        self.index = 0
        self.selected = 0
        self.len = length

    def onPress(self, key):
        if not self.selected and self.len != 0:
            try:
                k = key.char # single-char keys
            except: 
                k = key.name # other keys
        
            if k == "up" or k == "left":
                self.index -= 1
            elif k == "down" or k == "right":
                self.index += 1
            elif k == "enter":
                self.selected = 1
                return
            
            if self.index > self.len-1:
                self.index = 0
            elif self.index < 0:
                self.index = self.len-1

    def onRelease(self, key):
        pass

    def __del__(self):
        self.key.stop()

class Reader(Listener):
    def __init__(self, output, prompt=()):
        self.prompt = prompt
        self.str = ""

        #TODO: remove the ' ' option for usernames, handle exception of pressing enter without a username, edit terminal output class to handle tuples, limit username length for scrolling 

        self.chars = [" ", "_"]
        self.chars += list(string.ascii_lowercase+string.digits)
        self.output = output
        super().__init__(len(self.chars))
    
    def getStr(self):
        return self.str
    
    def readStr(self):
        self.output.clear()
        self.output.show(tuple(self.prompt))
        time.sleep(3)
        self.output.show(self.chars[self.index])
        oldIndex = self.index
        while True:
            if oldIndex != self.index:
                self.output.clear()
                self.output.show(str(self.str+self.chars[self.index]))
                oldIndex = self.index
            if self.selected:
                if self.chars[self.index] == " ":
                    return self.str
                self.str += self.chars[self.index]
                self.index = 0
                self.selected = 0
    
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

        # If the length of the selected option is greater than the number of characters that can fit, scroll the line
        if len( self.options[self.index] ) >= chars:
            scrollIndex = 0

            while self.index == index and not self.selected:
                self.output.clear()
                toPrint = self.options.copy()
                
                for i in range(len(toPrint)):
                    if i != index:
                        toPrint[i] = " " + toPrint[i]

                toPrint[index] = self.options[index][scrollIndex:]

                toPrint[index] = ">" + toPrint[index]
                
                if index > (rows-1):
                    toPrint = toPrint[index-(rows-1):]

                self.output.show(tuple(toPrint))
                time.sleep(0.5)
                scrollIndex += 1

                if scrollIndex > len(self.options[index]):
                    scrollIndex = 0
                
        # Non-scrolling
        else:
            for i in range(len(self.options)):
                if i != self.index:
                    toPrint[i] = " " + self.options[i]

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
        time.sleep(3)

    def select(self):
        self.printPrompt()

        self.selected = 0
        self.exit = False
        self.selected = 0
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

    OUTPUT = TerminalDisplay()
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