# telnet program example
import socket, select, string, sys


class Main:

    def __init__(self, host, port, username):
        # if (len(sys.argv) < 4):
        #     print('Usage : python telnet.py hostname port username')
        #
        #     sys.exit()

        self.host = host
        self.port = port
        self.username = username

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)

        self.message_list = []


    def prompt(self):
        sys.stdout.write('<You> ')
        sys.stdout.flush()

    def get_messages(self):
        return self.message_list

    def set_username(self, username):
        self.username = username


    # main function
    def main_loop(self):

        # connect to remote host
        try:
            self.s.connect((self.host, self.port))
        except:
            print('Unable to connect')
            sys.exit()

        print('Connected to remote host. Start sending messages')
        self.prompt()

        while 1:
            socket_list = [sys.stdin, self.s]

            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

            for sock in read_sockets:
                # incoming message from remote server
                if sock == self.s:
                    data = sock.recv(4096)
                    # if not data:
                    #     print('\nDisconnected from chat server')
                    #     sys.exit()
                    if data:
                        # print data
                        sys.stdout.write(data.decode())
                        self.prompt()


                # user entered a message
                else:
                    msg = sys.stdin.readline()
                    msg += "///" + self.username
                    self.s.send(msg.encode())
                    self.prompt()

Main = Main("0.0.0.0", 5000, "HPringles")
Main.main_loop()