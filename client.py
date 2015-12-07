#  Copyright © 2015 Brodie Herrick
#  [This program is licensed under the GPL version 3 or later.]
#  Please see the file COPYING in the source
#  distribution of this software for license terms.

import select
import socket
import sys


def client():
    class Node(object):
        # structure of server information
        def __init__(self):
            self.hostname = None
            self.host = None
            self.port = None
            self.next = None

    class List(object):
        # list of servers
        def __init__(self):
            self.head = None

        def insert(self):
            new_node = Node()

            # get node data
            sys.stdout.write('please enter the hosts display name: ')
            new_node.hostname = sys.stdin.readline()
            sys.stdout.write('please enter the hosts address: ')
            new_node.host = sys.stdin.readline()
            sys.stdout.write('please enter the hosts port: ')
            new_node.port = sys.stdin.readline()
            new_node.next = None

            new_node.next = self.head
            self.head = new_node

        def display_all(self):
            current = self.head
            while current:
                print('Hostname:', current.hostname, '\nHost: ',
                      current.host, '\nPort:', current.port)
                current = current.next

        def delete_node(self, name):
            current = self.head
            prev = None
            found = False
            while current and found is False:
                if current.hostname == name:
                    found = True
                else:
                    prev = current
                    current = current.next
            if current is None:
                raise ValueError('hostname not found')
            if prev is None:
                self.head = current.next
            else:
                prev.next = current.next

        def get_node(self, name):
            current = self.head
            found = False
            while current and found is False:
                if current.hostname == name:
                    found = True
                else:
                    current = current.next
            if current is None:
                raise ValueError('hostname not found')
            else:
                return current

    # set connection type
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set socket timeout
    s.settimeout(2)

    # init data
    slist = List()
    host = ''
    port = 0

    print('welcome to taunet')

    while 1:
        print('please select an option:\n'
              '1) add taunet node\n'
              '2) send message\n'
              '3) delete node\n'
              '4) display all nodes\n'
              '5) quit ')
        choice = sys.stdin.readline()
        if int(choice) == 1:
            slist.insert()
        elif int(choice) == 2:
            sys.stdout.write('which host would you like to send a message to? ')
            hostname = sys.stdin.readline()
            node = slist.get_node(hostname)
            host = node.host
            port = node.port
        elif int(choice) == 3:
            sys.stdout.write('which host would you like to delete (please enter hostname)? ')
            hostname = sys.stdin.readline()
            slist.delete_node(hostname)
        elif int(choice) == 4:
            slist.display_all()
        elif int(choice) == 5:
            sys.exit()
        else:
            print('input not understood, try again')

    # connect to host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')

    print("Connected to remote host. You can start sending messages")
    sys.stdout.write('[Me] '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list of readable sockets
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], 0)

        for sock in ready_to_read:
            if sock == s:
                # Message from server
                data = sock.recv(4096)
                print('reading from server')
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    print('got data from server')
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] ')

            else:
                # User has entered a message
                msg = sys.stdin.readline()
                print('message entered: {}'.format(msg))
                s.send(msg.encode('utf-8'))
                print('message sent')
                sys.stdout.write('[Me] ')

if __name__ == "__main__":
    sys.exit(client())
