# Copyright © 2015 Brodie Herrick
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

import sys
import socket
import select

HOST = ''
SERVER_LIST = []
PORT = 6283
RECV_BUFFER = 4096


def server():
    # set up server
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.bind((HOST, PORT))
    srv_socket.listen(5)

    # pass socket to readable socket connection list
    SERVER_LIST.append(srv_socket)

    # print check point
    print("Starting server connection listening on PORT:", str(PORT))

    while 1:
        # get list of sockets for incoming info
        ready_to_read, ready_to_write, in_error = select.select(SERVER_LIST, [], [], 0)

        # for each socket in the incoming read
        for sock in ready_to_read:
            # new connection request received
            if sock == srv_socket:
                sockfd, addr = srv_socket.accept()
                SERVER_LIST.append(sockfd)
                print('sockfd: (%s, %s) ' % sockfd)
                print('client: (%s, %s) ' % addr)

            # A already known connection knocks on the door
            else:
                try:
                    msg = sock.recv(RECV_BUFFER)
                    if msg:
                        # check for contents, and display if present
                        print('[{}]'.format(sock.getpeername()) + decrypt(msg))
                    else:
                        # socket is broken, remove it
                        if sock in SERVER_LIST:
                            SERVER_LIST.remove(sock)

                except:
                    continue
    # Always close connection when done using it
    srv_socket.close()


def decrypt(msg):
    # do decryption
    return msg


if __name__ == "__main__":
    sys.exit(server())
