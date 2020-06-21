import socket
import sys
import threading
import cmd
from cmd import Cmd
import time


class tcpserver():
    def __init__(self, address, port, listeners=5):
        self.address = address
        self.port = port
        self.listeners = listeners
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.clients = []
    
    def bind(self):
        #self.bind((self.address, self.port))
        self.s.bind((self.address, self.port))
        print('socket binded to port 3127') # make string formating here
        self.s.listen(self.listeners)
        print("socket is listening")
    
    def listen_loop(self):
        while True:
            self.c, self.addr = self.s.accept()
            print('Got connection from ', self.addr)
            self.clients.append(self.addr) 
            print(self.clients)
            self.test1 = "now its 2 test"
            self.z = 'ls'
            # allows me to send to specific client or address
            self.c.sendto(self.z.encode(), (self.addr))  
            try:
                output=self.c.recv(1024)
                print(output.decode())
            except socket.error:
                print("end of output from client")
            # pass 
            return self.clients
            self.c.close()

### start of CMD ###

class MyPrompt(Cmd):

    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print("Hello, %s" % name)

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit

    def do_list_clients(self, args):
        """List connected clients."""
        print(server.clients)

    def do_send_command(self, client_command):
        """send a command to a client."""
        server.c.sendto(client_command.encode(), (server.addr))
        try:
            output=server.c.recv(1024)
            print(output.decode())
        except socket.error:
            print("end of output from client")

if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = '> '
    server = tcpserver("0.0.0.0", 3127, 5)
    server.bind()
    # using threading instead of multi procesing because I need to share variables between threads
    t1 = threading.Thread(target = server.listen_loop)
    t1.start()
    time.sleep(4)
    print(server.clients)
    time.sleep(5)
    print(server.c)

    t2 = Process(target = prompt.cmdloop('Starting prompt...'))
    t2.start()
    

 
