message = "[[0, -1, 0, -1, 0, -1, 0, -1], [-1, 0, -1, 0, -1, 0, -1, 0], [0, -1, 0, -1, 0, -1, 0, -1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0]]"
#print(message)

message = message[2:len(message)-2]
#print(message)

board = [[0] * 8] * 8
#print(board)

rows = message.split("], [")
#print(rows)
j = 0
for element in rows:
    vals = element.split(", ")
    
    for i in range(8):
        board[j][i] = int(vals[i])
    j+=1

print(board)
print(type(board))