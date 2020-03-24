import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

#set recv method to not block
client_socket.setblocking(False)

#first message is username info
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

#main client loop - accepts new messages from client
while True:
    #input message from user
    message = input(f'{my_username} > ')

    #check for message before sending
    if message:

        #encode msg to bytes
        message = message.encode('utf-8')

        #prepare header and encode to bytes
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')

        #send
        client_socket.send(message_header + message)

    try:
        #message receiving loop
        while True:

            username_header = client_socket.recv(HEADER_LENGTH)

            #If no data is reeived, then server closed connection gracefully
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            #get username
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            #get message
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode(('utf-8'))

            print(f'{username} > {message}')

    except IOError as e:
        #check for EAGAIN & EWOULDBLOCK errors
        #these errors mean there was no data received
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        #nothing was received
        continue

    except Exception as e:
        #Any other exception - actual error
        print('Reading error: '.format(str(e)))
        sys.exit()
