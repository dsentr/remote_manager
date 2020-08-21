import socket
import sys
import threading
import cmd
from cmd import Cmd
import time
import logging

logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

class tcpserver():
    def __init__(self, address, port, listeners=5):
        self.address = address
        self.port = port
        self.listeners = listeners
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.clients = []
        self.clientsdict = {}
    
    def bind(self):
        self.s.bind((self.address, self.port))
        print('socket binded to port 3127') # make string formating here
        self.s.listen(self.listeners)
        print("socket is listening on port ", self.port)

    @property
    def port(self):
        print("listing port")
        return self._port

    @port.setter
    def port(self, value):
        print("setting port")
        if value > 65535 or value < 1:
            raise ValueError("must be between 0 and 65535")
        self._port = value
    
    def listen_loop(self):
        client_number = 0
        while True:
            self.c, self.addr = self.s.accept() #blocking call
            # add the new client connection to dictionary of connected clients 
            self.clients.append(self.addr)
            client_number += 1
            # add new item to the client list (dictionary)
            self.clientsdict[client_number] = self.addr
            # start a new thread for each connected client to avoid blocking calls
            threading.Thread(target = self.new_client(client_number, self.c, self.addr)) 

    def new_client(self, clientnum, clientsocket, addr):
        print('Got connection from ', self.addr)
        while True:
            try: 
                msg = clientsocket.recv(1024)
                print(self.addr, ' >> ', msg)
                z = "ls"
                clientsocket.sendto(z.encode('utf-8'), (addr))
            except BrokenPipeError:
                print("client connection closed")
                self.clients.pop(self.clients.index(self.addr)) # remove client from list when it disconnects
                del self.clientsdict[clientnum]
                break
            except ConnectionResetError:
                print("connection reset, client connection not open")
                break

            try:
                output=clientsocket.recv(1024)
                print(output.decode())
            except socket.error:
                print("end of output from client")
            except ConnectionResetError:
                print("client reset connection")
                clientsocket.close()
                self.clients 
                break
        clientsocket.close()

#### CLI Banner ####
def motd():
    print('''
  _____                      _         __  __                                   
 |  __ \                    | |       |  \/  |                                  
 | |__) |___ _ __ ___   ___ | |_ ___  | \  / | __ _ _ __   __ _  __ _  ___ _ __ 
 |  _  // _ \ '_ ` _ \ / _ \| __/ _ \ | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
 | | \ \  __/ | | | | | (_) | ||  __/ | |  | | (_| | | | | (_| | (_| |  __/ |   
 |_|  \_\___|_| |_| |_|\___/ \__\___| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
                                                                 __/ |          
                                                                |___/                  

Type help for command list
''')   

### start of CMD ###

class MyPrompt(Cmd):
    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit

    def do_list_clients(self, args):
        """List connected clients."""
        if len(server.clientsdict) == 0:
            print("There are no clients currently connected.")
        else:
            print("Connected Client List:")
            for key, value in server.clientsdict.items():
                print("Client ", key, " ", value)

    def do_send_command(self, args: str): 
        # function annotation performs no type check at runtime.
        # CMD module only accepts one argument as string, so multiple arguments must be split
        """send a command to a client."""
        intversion = int(args)
        client_tuple = server.clientsdict[intversion]
        user_input = input("Enter a command: ")
        try:
            server.c.sendto(user_input.encode('utf-8'), client_tuple)
            logging.info("sending command '%s' to client", user_input)
            output=server.c.recv(1024)
            print(output.decode())
        except socket.error:
            print("end of output from client") 


if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = 'RemoteManager>> '
    server = tcpserver("0.0.0.0", 3127, 5)
    server.bind()
    # using threading instead of multi procesing because I need to share variables between threads
    t1 = threading.Thread(target = server.listen_loop)
    t1.start()
    # Start of CMD program loop
    t2 = threading.Thread(target = prompt.cmdloop(motd()))
    t2.start()

 
