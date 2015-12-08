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
KEY = 'password'


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
                print('client: (%s, %s) ' % addr)

            # A already known connection knocks on the door
            else:
                try:
                    msg = sock.recv(RECV_BUFFER)
                    if msg:
                        # check for contents, and display if present
                        sys.stdout.write('message content: '); sys.stdout.flush()
                        print(decipher(a2b(msg), KEY))
                    else:
                        # socket is broken, remove it
                        if sock in SERVER_LIST:
                            SERVER_LIST.remove(sock)

                except:
                    continue
    # Always close connection when done using it
    srv_socket.close()


def decipher(ciphertext, key):
    print('decoding in process...')
    iv, ciphertext = ciphertext[:10], ciphertext[10:]
    message = rc4(map(ord, ciphertext), bytes(key + iv, 'utf-8'))
    return ''.join(map(chr, message))


def rc4(keystream, key, n=20):
    # Perform the RC4 algorithm on a given input list of bytes with a
    # key given as a list of bytes, and return the output as a list of bytes.
    i, j, state = 0, 0, list(range(256))
    for k in range(n):
        for i in range(256):
            j = (j + state[i] + key[i % len(key)]) % 256
            state[i], state[j] = state[j], state[i]
    i, j = 0, 0
    output = []
    for byte in keystream:
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        n = (state[i] + state[j]) % 256
        output.append(byte ^ state[n])
    return output


def a2b(text):
    # Given an "armoured" string, return a string of binary data
    return ''.join(map(chr, [int(w, 16) for w in text.split()]))


if __name__ == "__main__":
    sys.exit(server())
