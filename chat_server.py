import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

#create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#allows socket to reuse addreess
#SO_ - socket optioin
#SOL_ - socker option level
#sets REUSEADDRE (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#bind to IP and Port
server_socket.bind((IP, PORT))

#listen for new connections
server_socket.listen()

# List of sockets for select.select()
socket_list = [server_socket]

#list of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')


#Handle message receving
def receive_message(client_socket):
    try:
        #get message header, contains messafe length
        message_header = client_socket.recv(HEADER_LENGTH)

        #handle situation where no data is received, means client closed connection
        if not len(message_header):
            return False

        #convert header to int value length
        message_length = int(message_header.decode('utf-8').strip())

        #return message data object
        return {
            'header': message_header,
            'data': client_socket.recv(message_length)
        }

    except:
        #something went wrong like empty message or client exited abruptly
        return False


while True:
    #select takaes in rlist, wlist, and xlist
    #returns sockets that are ready
    read_sockets, _, exception_sockets = select.select(socket_list, [],
                                                       socket_list)

    #iterate over read socket list
    for notified_socket in read_sockets:
        #check for and handle new connections
        if notified_socket == server_socket:
            #get unique client socket and adress
            client_socket, client_address = server_socket.accept()
            #store client username
            user = receive_message(client_socket)
            if user is False:
                continue
            #append new client to socket list
            socket_list.append(client_socket)

            #save clients username
            clients[client_socket] = user
            print('Accepted new connection from {}:{}, username: {}'.format(
                *client_address, user['data'].decode('utf-8')))
        #if notified socket is not a server, then it is a message
        else:
            message = receive_message(notified_socket)

            #make sure a message exists before reading
            if message is False:
                print('Closed connection from: {}'.format(
                    clients[notified_socket]['data'].decode('utf-8')))
                socket_list.remove(notified_socket)
                del clients[notified_socket]

                continue
            user = clients[notified_socket]
            print(
                f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}"
            )

            #iterate over connected clinets and broadcast message
            for client_socket in clients:
                #do not send to sender
                if client_socket != notified_socket:
                    #send user and message data with headers
                    client_socket.send(user['header'] + user['data'] +
                                       message['header'] + message['data'])

            #handle error sockets
            for notified_socket in exception_sockets:
                #remove from list
                socket_list.remove(notified_socket)
                #remove from our list of users
                del clients[notified_socket]