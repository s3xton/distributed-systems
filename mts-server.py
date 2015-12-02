from socket import *
import thread
import os

buf = 1024
host = ""
port = 443

def handler(client,addr):
    while 1:
        data = client.recv(buf)
        if not data: break
        if data[:4] == 'HELO':
            client.send(str(data) +"IP:52.16.255.69\nPort: " + str(port) +"\nStudentID: 12311449\n")
        if data[:12] == "KILL_SERVICE":
            os._exit(0)
    
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
