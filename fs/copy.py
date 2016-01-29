from socket import *
import thread
import os
import sys 
import collections
import random
import time 
import os.path


class Copy:
    
    def __init__(self, isPrimary, port):
        self.buf = 1024
        self.host = "localhost"
        self.primary = isPrimary
        self.other_replicas = {8003}
        self.port = int(port)
        self.first = True
        self.PORT_ds = 8000
		self.HOST_ds = "localhost"
    
    # If the file exists, read its contents, otherwise return an error
    def readFile(self, filename, client):
        words = filename.split("/")
        print words[2]
        if os.path.isfile(words[2]):
            f = open(words[2], 'r')
            filedata = f.read()
            print "DATA: " + filedata 
            client.send(filedata+"\n")
        else:
            client.send("ERROR: file doesn't exist\n")
            print "ERROR: file doesn't exist"
    
    # Write to the the file, if it doesnt exist its created      
    def writeFile(self, data):
        lines = data.splitlines()
        print lines
        filename = lines[0].split("/")[2]
        filedata = lines[1][6:]
        file = open(filename, 'w')
        file.write(filedata)
        if self.primary:
            print "REP: "+lines[0].split(" ")[1]
            self.updateReplicas(lines[0].split(" ")[1], filedata)
    
    # After a write has happend, sends a write command to all other replicas    
    def updateReplicas(self, filename, filedata):
        msg = 'WRITE: ' + filename + '\nDATA: ' + filedata
        print msg
        s = socket(AF_INET, SOCK_STREAM)
        for port in self.other_replicas:
            print port
            s.connect((self.host, port))
            s.send(msg)
    
    # If recovering from a crash, send this to the directory server        
    def alertDirectoryServer(self, address):
		s = socket(AF_INET, SOCK_STREAM)
		s.connect((self.HOST_ds, self.PORT_ds))
		message = "ALIVE: " + address
		s.send(message)
        s.close()
    
    # Handler for incoming messages    
    def handler(self, client,addr):
        data = client.recv(self.buf)
        if data[:4] == 'HELO':
            client.send(str(data) +"IP:52.16.255.69\nPort: " + str(port) +"\nStudentID: aa3e68899f9a879f8408b5af0bec24991f35aa22398b70458a8239e15bb29b93\n")
        if data[:12] == "KILL_SERVICE":
            os._exit(0)
        if data[:4] == 'READ':
            self.readFile(data[6:], client)
        if data[:5] == 'WRITE':
            self.writeFile(data)
        if data[:11] == 'SET_PRIMARY':
            self.primary = True
        client.close()
        
    def listen(self):
        address = (self.host, self.port)
        server = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind(address)
        server.listen(5)
        while 1:
            if self.primary:
                print 'Primary copy waiting for connection...'
            else:
                print 'Copy waiting for connection...'
            client, addr = server.accept()
            print '...connected from:', addr
            thread.start_new_thread(self.handler, (client, addr))
    
if __name__=='__main__':
    if sys.argv[2] == 'true':
        copy = Copy(True, sys.argv[1])
    else:
        copy = Copy(False, sys.argv[1]) 
    copy.listen()
    
    