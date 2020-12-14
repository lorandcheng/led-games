
# def getInput():
#     while True:
#         try:
#             inp = input()
#             if inp == 'a':
#                 return -1
#             elif inp == 'd':
#                 return 1
#             elif inp == 'e':
#                 return 'select'
#             else:
#                 raise ValueError

#         except ValueError:
#             if input('Invalid input. Do you want to continue? y/n\n') == 'y':
#                 print('Enter a new input:')
#                 continue
#             else:
#                 raise ValueError('Invalid input')
#         break

# def getName():
#     name = input("Enter your name: ")
#     return name

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

if __name__ == '__main__':
    """
    DEMO CODE
    """
    listener = Listener(10)
    print("Starting keyboard listener")
    oldIndex = listener.index
    while True:
        if oldIndex != listener.index:
            print("\nUpdating menu")
            print("Index value:", listener.index)
            oldIndex = listener.index
        if listener.selected:
            break
    print("A selection has been made at index", listener.index)