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
        if not self.selected:
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

import string
import time
from output import terminalDisplay
class Reader(Listener):
    def __init__(self, prompt):
        self.prompt = prompt
        self.str = ""
        self.chars = [" ", "_"]
        self.chars += list(string.ascii_lowercase+string.digits)
        self.output = terminalDisplay()
        super().__init__(len(self.chars))
    
    def getStr(self):
        return self.str
    
    def readStr(self):
        self.output.clear()
        self.output.show(self.prompt)
        self.output.show(self.chars[self.index])
        oldIndex = self.index
        while True:
            if oldIndex != self.index:
                self.output.clear()
                self.output.show(self.prompt)
                self.output.show(self.str+self.chars[self.index])
                oldIndex = self.index
            if self.selected:
                if self.chars[self.index] == " ":
                    return self.str
                self.str += self.chars[self.index]
                self.index = 0
                self.selected = 0

class Menu(Listener):
    def __init__(self, prompt, options, indexing=False):
        self.output = terminalDisplay()
        self.prompt = prompt
        self.options = options
        self.indexing = indexing
        super().__init__(len(options))

    def _printOptions(self):
        self.output.clear()
        self.output.show(self.prompt)
        for i in range(len(self.options)):
            if i == self.index:
                self.output.show('* ' + self.options[i])
            else:
                self.output.show('  ' + self.options[i])

    def select(self):
        self._printOptions()
        oldIndex = self.index
        while True:
            if oldIndex != self.index:
                self._printOptions()
                oldIndex = self.index
            if self.selected:
                if self.indexing:
                    return (self.index, self.options[self.index])
                else:
                    return self.options[self.index]

if __name__ == '__main__':
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
    # prompt = "Enter a name"
    # reader = Reader(prompt)
    # print("Starting reader")
    # reader.readStr()
    # print("You entered:", reader.getStr())

    """
    DEMO MENU CODE
    """
    prompt = "Choose an option"
    options = ["option 1", "option 2", "option 3", "option 4", "option 5"]
    menu = Menu(prompt, options, indexing=True)
    index, selection = menu.select()
    print("You chose:", selection, "at index", index)
    del menu