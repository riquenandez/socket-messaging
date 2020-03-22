import socket
import pickle

HEADERSIZE = 10

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('localhost', 1234))

#maintain connection
while True:
    #buffer through message
    full_msg = b''
    new_msg = True
    while True:
        msg = clientSocket.recv(16)
        if new_msg:
            print("new msg len:", msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        print(f'full message length: {msglen}')

        full_msg += msg

        print(len(full_msg))

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            print(pickle.loads(full_msg[HEADERSIZE:]))
            new_msg = True
            full_msg = b''
