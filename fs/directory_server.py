from socket import *
import thread
import os
import sys 
import collections
import random
buf = 1024
host = "localhost"
port = 8000#int(sys.argv[1])

directories = {"user":{0:8002, 1:8003}, "docs": {0:8004, 1:8005}}

def getAddress(direct, client, write):
    words = direct.split("/")
    print words[1]
    if directories.has_key(words[1]):
        if write:
            client.send(str(directories[words[1]][0]) + "\n")
        else:
            client.send(str(directories[words[1]][random.randrange(0,1,1)]) + "\n")
    else:
        client.send("ERROR: No such directory")

def handler(client,addr):
    data = client.recv(buf)
    if data[:4] == 'HELO':
        client.send(str(data) +"IP:52.16.255.69\nPort: " + str(port) +"\nStudentID: aa3e68899f9a879f8408b5af0bec24991f35aa22398b70458a8239e15bb29b93\n")
    if data[:12] == "KILL_SERVICE":
        os._exit(0)
    if data[:4] == 'READ':
        getAddress(data[6:], client, False)
    if data[:4] == 'OPEN':
        getAddress(data[6:], client, True)
    print "close"
    client.close()
    
if __name__=='__main__':
    address = (host, port)
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(5)
    while 1:
        print 'Directory Server: waiting for connection...'
        client, addr = server.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (client, addr))