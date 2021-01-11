from games import battleship
from outputs import TerminalDisplay, LedDisplay

if __name__ == "__main__":

    # output = TerminalDisplay()
    # game = battleship.Battleship(output)
    # game.setup()

    message = "[[1, 1, 1, 1, 1, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] [[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]], [[1, 0], [1, 1], [1, 2], [1, 3]], [[2, 0], [2, 1], [2, 2]], [[3, 0], [3, 1], [3, 2]], [[4, 0], [4, 1]]]"
    if len(message) > 10:
            message = message[2:len(message)-3]
            board, coords = message.split("]] [[[")

            oBOARD = [
                [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]
            ]
            rows = board.split("], [")
            j = 0
            for element in rows:
                vals = element.split(", ")
                
                for i in range(10):
                    oBOARD[j][i] = int(vals[i])
                j+=1
            print("BOARD:", oBOARD)
            print("board elem:", oBOARD[0][0])

            ships = coords.split("]], [[")
            oCoords = []
            for ship in ships:
                shipCoords = []
                elems = ship.split("], [")
                for elem in elems:
                    r,c = elem.split(", ")
                    shipCoords.append([int(r),int(c)])
                oCoords.append(shipCoords)

            print("COORDS:", oCoords)
            print("coords elem:", oCoords[0][0])







