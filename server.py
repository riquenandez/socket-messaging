import socket
import pickle
import time

HEADERSIZE = 10

#create socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind socket to localhost:1235
serverSocket.bind(('localhost', 1234))
#max number of ques available
serverSocket.listen(5)

#server main loop
while True:
    #accept connections from outside
    (clientsocket, address) = serverSocket.accept()
    print(f'connection from {address} has been establihed')

    #produces the length of message with 10 characters before the message
    d = {1: "hi", 2: "there"}
    msg = pickle.dumps(d)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg
    print(msg)

    #send message
    clientsocket.send(msg)
