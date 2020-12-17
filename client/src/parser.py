def parseMessage(msg):
    message = str(msg.payload, "utf-8")
    parsedMessage = []
    if message[0] == "[":
        message = message[2:len(message)-2]
        for entry in message.split("), ("):
            entry = entry[1:len(entry)-1]     
            parsedMessage.append(tuple(entry.split("', '")))
    else:
        parsedMessage = tuple(map(str, message.split(", ")))
    return parsedMessage