from socket import *
import thread
import os
import sys 
import collections
import random
buf = 1024
host = "localhost"
port = 8001#int(sys.argv[1])

locks = collections.defaultdict(dict) #[address:[filename:locked]]

def acquireLock(data, client):
    words = data.split(" ")
    address = words[1]
    filename = words[2].strip()
    if not filename in locks[address].keys():
        locks[address][filename] = False
    print locks    
    while locks[address][filename]:
        time.sleep(1)
    locks[address][filename] = True
    print "lock"
    client.send("LOCK\n")
    
def releaseLock(data):
    words = data.split(" ")
    address = words[1].strip()
    filename = words[2].strip()
    
    locks[address][filename] = False  
    print locks 
    
def handler(client,addr):
    data = client.recv(buf)
    if data[:4] == 'HELO':
        client.send(str(data) +"IP:52.16.255.69\nPort: " + str(port) +"\nStudentID: aa3e68899f9a879f8408b5af0bec24991f35aa22398b70458a8239e15bb29b93\n")
    if data[:12] == "KILL_SERVICE":
        os._exit(0)
    if data[:4] == 'LOCK':
        acquireLock(data[5:], client)
    if data[:4] == 'FREE':
        releaseLock(data[5:])
    print "close"
    client.close()
            
    
if __name__=='__main__':
    address = (host, port)
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(5)
    while 1:
        print 'Lock Server: waiting for connection...'
        client, addr = server.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (client, addr))