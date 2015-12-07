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
            if current is None:
                print('************************\n',
                      'there are no servers available, you should add some!')
            while current:
                print('************************\n',
                      'name:', current.name, '\n'
                      ' host:', current.host, '\n')
                current = current.next

        def delete_node(self, name):
            # search for and remove node, if found
            # otherwise, display error
            current = self.head
            prev = None
            found = False
            while current and found is False:
                if current.name == name:
                    found = True
                else:
                    prev = current
                    current = current.next
            if current is None:
                print('name not found')
                return
            if prev is None:
                self.head = current.next
            else:
                prev.next = current.next
            print('node deleted')

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
                print('hostname not found')
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
              '5) quit \n'
              '************************\n')
        choice = sys.stdin.readline()
        if int(choice) == 1:
            print('************************')
            sys.stdout.write('please enter the person\'s name: '); sys.stdout.flush()
            name = sys.stdin.readline()
            sys.stdout.write('please enter the host\'s address: '); sys.stdout.flush()
            host = sys.stdin.readline()
            slist.insert(name.rstrip('\n'), host.rstrip('\n'))
        elif int(choice) == 2:
            sys.stdout.write('which person would you like to send a message to? '); sys.stdout.flush()
            name = slist.get_node(sys.stdin.readline().rstrip('\n'))
            send_msg(name, slist)
        elif int(choice) == 3:
            sys.stdout.write('which host would you like to delete (please enter name)? '); sys.stdout.flush()
            slist.delete_node(sys.stdin.readline().rstrip('\n'))
        elif int(choice) == 4:
            slist.display_all()
        elif int(choice) == 5:
            sys.exit()
        else:
            print('input not understood, try again')


def send_msg(host, slist):
    # setup client
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.settimeout(None)

    # connect to host
    try:
        srv.connect((host, PORT))
    except:
        print('\n************************\n'
              'unable to connect\n'
              '************************\n')
        return

    print("connected to remote host. you can start sending messages\nenter \"/quit\" when done")
    sys.stdout.write('[Me] '); sys.stdout.flush()

    try:
        while 1:
            socket_list = [sys.stdin, srv]

            # get the list of readable sockets
            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], 0)

            '''for sock in ready_to_read:
                if sock == srv:
                    # message from server
                    data = sock.recv(4096)
                    if not data:
                        print('\ndisconnected from chat server')
                        return
                    else:
                        sys.stdout.write(data)
                        sys.stdout.write('[Me] '); sys.stdout.flush()

                else:'''
            # compose and send message
            msg = sys.stdin.readline()
            if msg == '/quit\n':
                srv.close()
                return
            else:
                srv.send(encrypt(msg).encode('utf-8'))
                print('message sent: %s' % msg)
                sys.stdout.write('[Me] '); sys.stdout.flush()
    except:
        print('connection to peer lost')
        return


def encrypt(msg):
    # do encryption
    return msg


if __name__ == "__main__":
    sys.exit(client())
