import socket

HEADERSIZE = 10

#create socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind socket to localhost:1235
serverSocket.bind(('localhost', 1235))
#max number of ques available
serverSocket.listen(5)

#server main loop
while True:
    #accept connections from outside
    (clientsocket, address) = serverSocket.accept()
    print(f'connection from {address} has been establihed')

    #produces the length of message with 10 characters before the message
    msg = "Hellow World from the server"
    msg = f'{len(msg):<{HEADERSIZE}}' + msg

    #send message
    clientsocket.send(bytes(msg, "utf-8"))
    clientsocket.close()