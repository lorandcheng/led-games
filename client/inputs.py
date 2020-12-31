import string
import time

from pynput import keyboard

from outputs import TerminalDisplay

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


class Reader(Listener):
    def __init__(self, output, prompt=""):
        self.prompt = prompt
        self.str = ""
        self.chars = [" ", "_"]
        self.chars += list(string.ascii_lowercase+string.digits)
        self.output = output
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
    
    def __del__(self):
        self.key.stop()


class Menu(Listener):
    def __init__(self, output, prompt="", options=[], indexing=False):
        self.output = output
        self.prompt = prompt
        self.options = options
        self.indexing = indexing
        self.exit = False
        super().__init__(len(options))

    def updateOptions(self, newOptions):
        self.options = newOptions
        self.len = len(newOptions)

    def _printOptions(self):
        self.output.clear()
        self.output.show(self.prompt)
        for i in range(len(self.options)):
            if i == self.index:
                self.output.show('* ' + self.options[i])
            else:
                self.output.show('  ' + self.options[i])

    def select(self):
        self.selected = 0
        self.exit = False
        self.selected = 0
        self._printOptions()
        oldIndex = self.index
        while True:
            if self.exit:
                return 0
            if oldIndex != self.index:
                self._printOptions()
                oldIndex = self.index
            if self.selected:
                try:
                    if self.indexing:
                        return (self.index, self.options[self.index])
                    else:
                        return self.options[self.index]
                except:
                    self.output.show("List was updated since your selection")

    def exitMenu(self):
        self.exit = True

    def __del__(self):
        self.key.stop()

if __name__ == '__main__':
    from outputs import TerminalDisplay

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
    # prompt = "Enter a name"
    # reader = Reader(prompt, OUTPUT)
    # print("Starting reader")
    # reader.readStr()
    # print("You entered:", reader.getStr())

    """
    DEMO MENU CODE
    """
    prompt = "Choose an option"
    options = ["option 1", "option 2", "option 3", "option 4", "option 5"]
    menu = Menu(OUTPUT, prompt, options, indexing=True)
    index, selection = menu.select()
    print("You chose:", selection, "at index", index)
    del menu