#  Copyright © 2015 Brodie Herrick
#  [This program is licensed under the GPL version 3 or later.]
#  Please see the file COPYING in the source
#  distribution of this software for license terms.

import socket, sys, random, getpass

PORT = 6283
VER = '0.2'


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
            new_node = Node()
            new_node.name = name
            new_node.host = host
            new_node.next = self.head
            self.head = new_node

        def display_all(self):
            current = self.head
            if current is None:
                print('************************\n',
                      'you have not added any nodes')
            while current:
                print('************************\n',
                      'name:', current.name, '\n'
                                             'host:', current.host, '\n')
                current = current.next

        def delete_node(self, name):
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
            current = self.head
            found = False
            while current and found is False:
                if current.name == name:
                    found = True
                else:
                    current = current.next
            if current is None:
                return
            else:
                return current.host

    # init data
    slist = List()

    print('welcome to taunet')
    sys.stdout.write('please enter your username: '); sys.stdout.flush()
    userid = sys.stdin.readline().rstrip()
    key = getpass.getpass('what is the passphrase for your network? ')

    menu(slist, userid, key)


def menu(slist, userid, key):
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
            slist.insert(name.rstrip(), host.rstrip())
        elif int(choice) == 2:
            sys.stdout.write('which person would you like to send a message to? '); sys.stdout.flush()
            name = sys.stdin.readline().rstrip('\n')
            host = slist.get_node(name)
            send_msg(host, name, userid, key)
        elif int(choice) == 3:
            sys.stdout.write('which host would you like to delete (please enter name)? '); sys.stdout.flush()
            slist.delete_node(sys.stdin.readline().rstrip('\n'))
        elif int(choice) == 4:
            slist.display_all()
        elif int(choice) == 5:
            sys.exit()
        else:
            print('input not understood, try again')


def send_msg(host, name, userid, key):
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

    print("connected to %s\'s node\nenter \"/quit\" when done" % name)
    sys.stdout.write('[%s] ' % userid); sys.stdout.flush()

    try:
        while 1:
            # compose and send message
            msg = sys.stdin.readline()
            if msg == '/quit\n':
                srv.close()
                return
            else:
                srv.send(encipher(('version: %s\r\nfrom: %s\r\nto: %s\r\n'
                                   % (VER, userid, name) + msg), key).encode('utf-8'))
                sys.stdout.write('[%s] ' % userid); sys.stdout.flush()
    except:
        print('connection to peer lost')
        return


def encipher(message, key, iv=''):
    # Given a plaintext string and key, return an enciphered string
    while len(iv) < 10:
        iv += chr(random.randrange(256))
    ciphertext = arcfour(map(ord, message), bytes(key + iv, 'utf-8'))
    return iv + ''.join(map(chr, ciphertext))


def arcfour(keystream, key, n=20):
    # Perform the RC4 algorithm on a given input list of bytes with a
    # key given as a list of bytes, and return the output as a list of bytes.
    i, j, state = 0, 0, list(range(256))
    for k in range(n):
        for i in range(256):
            j = (j + state[i] + key[i % len(key)]) % 256
            state[i], state[j] = state[j], state[i]
    i, j, output = 0, 0, []
    for byte in keystream:
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        n = (state[i] + state[j]) % 256
        output.append(byte ^ state[n])
    return output


if __name__ == "__main__":
    sys.exit(client())
