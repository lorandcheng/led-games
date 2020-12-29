
def getInput():
    while True:
        try:
            inp = input()
            if inp == 'a':
                return -1
            elif inp == 'd':
                return 1
            elif inp == 'e':
                return 'select'
            else:
                raise ValueError

        except ValueError:
            if input('Invalid input. Do you want to continue? y/n\n') == 'y':
                print('Enter a new input:')
                continue
            else:
                raise ValueError('Invalid input')
        break

def getName():
    name = input("Enter your name: ")
    return name


if __name__ == '__main__':
    while True:
        getInput()