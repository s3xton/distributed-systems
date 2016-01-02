from socket import *
import thread
import os
import sys 
import collections
import random
buf = 1024
host = "localhost"
port = 8000#int(sys.argv[1])

replicas = {0:"8000", 1:"8001", 2:"8002" }

def getReadPort(data, client):
    words = data[3:].split("/")
    print words[1]
    

def handler(client,addr):
    while 1:
        data = client.recv(buf)
        if not data: break
        if data[:4] == 'HELO':
            client.send(str(data) +"IP:52.16.255.69\nPort: " + str(port) +"\nStudentID: aa3e68899f9a879f8408b5af0bec24991f35aa22398b70458a8239e15bb29b93\n")
        if data[:12] == "KILL_SERVICE":
            os._exit(0)
        if data[:4] == 'READ':
            getReadAddress(data, client)
    
if __name__=='__main__':
    address = (host, port)
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(5)
    while 1:
        print 'waiting for connection...'
        client, addr = server.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (client, addr))