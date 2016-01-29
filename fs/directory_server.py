from socket import *
import thread
import os
import sys 
import collections
import random
import crypto
buf = 1024
host = "localhost"
port = 8000#int(sys.argv[1])

ds_pass = "imthedirectoryserver"
ds_ID = "dirserv"

# All directories and their current status (to handle downed servers)
directories = {"user":{0:8002, 1:8003}, "docs": {0:8004, 1:8005}}
status = {8002:True, 8003:True, 8004:True, 8005:True}

# Returns an address of a copy for the client to access.
# If they are writing give them the primary, if theyre reading give
# them a random slave/primary.
def getAddress(direct, client, write):
    words = direct.split("/")
    print words[1]
    if directories.has_key(words[1]):
        if write:
            client.send(str(directories[words[1]][0]) + "\n")
        else:
            numCopy = len(directories[words[1]])
            index = random.randrange(0,numCopy,1)
            while not status[directories[words[1]][index]]:
                index = random.randrange(0,numCopy,1)
            client.send(str(directories[words[1]][index]) + "\n")
    else:
        client.send("ERROR: No such directory")

# If a server is said to be down, mark its status as false
def removeServer(address):
    status[address] = False
    print "Removed: " + str(address)
    
def reviveServer(address):
    status[address] = True
    print "Revived: " + str(address)

# Handles incoming messages
def handler(client,addr):
    data = client.recv(buf)
    lines = data.splitlines()
    print lines
    sessionKey = crypto.decrypt(ds_pass, lines[1])
    msg = crypto.decrypt(sessionKey, lines[0])
    print msg
    if msg[:4] == 'HELO':
        client.send(str(msg) +"IP:52.16.255.69\nPort: " + str(port) +"\nStudentID: aa3e68899f9a879f8408b5af0bec24991f35aa22398b70458a8239e15bb29b93\n")
    if msg[:12] == "KILL_SERVICE":
        os._exit(0)
    if msg[:4] == 'READ':
        getAddress(msg[6:], client, False)
    if msg[:4] == 'OPEN':
        getAddress(msg[6:], client, True)
    if msg[:5] == 'CRASH':
        removeServer(int(msg[7:]))
    if msg[:5] == 'ALIVE':
        reviveServer(int(msg[7:]))
   
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