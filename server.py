# Copyright © 2015 Brodie Herrick
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

import sys
import socket
import select

HOST = ''
SERVER_LIST = []
PORT = 13475
RECV_BUFFER = 4096


def server():
    # Create socket and parse which it a IPv4 and a TCP input
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Parse it the socket layer and the last parameter says it all
    srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind HOST and PORT
    srv_sock.bind((HOST, PORT))

    srv_sock.listen(5)

    # pass socket to readable socket connection list
    SERVER_LIST.append(srv_sock)

    # print check point
    print("Starting server connection listening on PORT: ", str(PORT))

    while 1:
        # Create to variables to handle information
        ready_to_read, ready_to_write, in_error = select.select(SERVER_LIST, [], [], 0)

        # for each socket in the incoming read
        for sock in ready_to_read:
            # new connection request received
            if sock == srv_sock:
                sockfd, addr = srv_sock.accept()
                SERVER_LIST.append(sockfd)

                print("Client: (%s, %s) " % addr)
                broadcast(srv_sock, sockfd, "[%s:%s] entered our chatting room\n" % addr)

            # A already known connection knocks on the door
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # Is there anything in the socket
                        broadcast(srv_sock, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                    else:
                        # The socket is broken remove it
                        if sock in SERVER_LIST:
                            SERVER_LIST.remove(sock)

                        broadcast(srv_sock, sock, "Client (%s, %s) is offline\n" % addr)

                except:
                    broadcast(srv_sock, sock, "Client (%s, %s) is offline\n" % addr)
                    continue
    # Always close connection when done using it
    srv_sock.close()


# The broadcast method is to tell all the clients the incoming messages
def broadcast(ser_socket, sock, message):
    for socket in SERVER_LIST:
        if socket != sock and socket != sock:
            try:
                socket.send(message)
            except:
                # Broken socket connection
                socket.close()
                # Remove it
                if socket in SERVER_LIST:
                    SERVER_LIST.remove(socket)


if __name__ == "__main__":
    sys.exit(server())
