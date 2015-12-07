#  Copyright © 2015 Brodie Herrick
#  [This program is licensed under the GPL version 3 or later.]
#  Please see the file COPYING in the source
#  distribution of this software for license terms.

import select
import socket
import sys

PORT = 6283


def client():
    class Node(object):
        # structure of server information
        def __init__(self):
            self.name = None
            self.host = None
            self.next = None

    class List(object):
        # list of servers
        def __init__(self):
            self.head = None

        def insert(self, name, host):
            # init new node
            new_node = Node()

            # set node data
            new_node.name = name
            new_node.host = host

            # insert node into list
            new_node.next = self.head
            self.head = new_node

        def display_all(self):
            current = self.head
            while current:
                print('name:', current.name, '\nhost: ', current.host)
                current = current.next

        def delete_node(self, name):
            # search for and remove node, if found
            # otherwise, display error
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
            # search for node and return it
            # otherwise, display error
            current = self.head
            found = False
            while current and found is False:
                if current.name == name:
                    found = True
                else:
                    current = current.next
            if current is None:
                raise ValueError('hostname not found')
            else:
                return current.host

    # init data
    slist = List()

    print('welcome to taunet')
    menu(slist)


def menu(slist):
    while 1:
        print('\n************************\n'
              'please select an option:\n'
              '1) add taunet node\n'
              '2) send message\n'
              '3) delete node\n'
              '4) display all nodes\n'
              '5) quit ')
        choice = sys.stdin.readline()
        if int(choice) == 1:
            sys.stdout.write('please enter the person\'s name: '); sys.stdout.flush()
            name = sys.stdin.readline()
            sys.stdout.write('please enter the host\'s address: '); sys.stdout.flush()
            host = sys.stdin.readline()
            slist.insert(name, host.rstrip('\n'))
            menu(slist)
        elif int(choice) == 2:
            sys.stdout.write('which person would you like to send a message to? '); sys.stdout.flush()
            host = slist.get_node(sys.stdin.readline())
            send_msg(host, slist)
        elif int(choice) == 3:
            sys.stdout.write('which host would you like to delete (please enter name)? ')
            slist.delete_node(sys.stdin.readline())
        elif int(choice) == 4:
            slist.display_all()
        elif int(choice) == 5:
            sys.exit()
        else:
            print('input not understood, try again')


def send_msg(host, slist):
    # set connection type
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set socket timeout
    srv.settimeout(2)

    # for testing
    print('%s:%d' % (host, PORT))

    # connect to host
    try:
        srv.connect((host, PORT))
    except:
        print('\n****************\n'
              'unable to connect\n'
              '****************\n')
        menu(slist)

    print("connected to remote host. you can start sending messages\nenter \"/quit\" when done")
    sys.stdout.write('[Me] '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, srv]

        # get the list of readable sockets
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], 0)

        for sock in ready_to_read:
            if sock == srv:
                # message from server
                data = sock.recv(4096)
                if not data:
                    print('\ndisconnected from chat server')
                    menu(slist)
                else:
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()

            else:
                # User has entered a message
                msg = sys.stdin.readline()
                if msg == '/quit':
                    menu(slist)
                else:
                    srv.send(encrypt(msg).encode('utf-8'))
                    print('message sent')
                    sys.stdout.write('[Me] '); sys.stdout.flush()


def encrypt(msg):
    # do encryption
    return msg


if __name__ == "__main__":
    sys.exit(client())
