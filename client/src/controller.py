def getInput():
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
            pass
        else:
            raise ValueError('Invalid input')

if __name__ == '__main__':
    while True:
        getInput()