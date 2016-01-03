# This is a very basic implementation of a Kerberos authentication server.
# Currently it only provides encryption between the client and the directory server,
# although could be extended quiet easily into other servers.

from socket import *
import thread
import os
import sys 
import collections
import random
import crypto
buf = 1024
host = "localhost"
port = 8010#int(sys.argv[1])

# {username:password}
passwords = {"conor":"password", "john":"1234"}
ds_pass = "imthedirectoryserver"
ds_ID = "dirserv"

# LOGIN: username
# *encrypted username*	
def loginRequest(data, client):
    lines = data.splitlines()
    message = lines[1]
    userid = lines[0][7:].strip()
    decrypted = crypto.decrypt(passwords[userid], message.strip())
    if userid == decrypted:
        sessionKey = crypto.genSessionKey()
        ticket = crypto.encrypt(ds_pass, sessionKey)
        token = crypto.encrypt(passwords[userid], sessionKey)
        message = token + "\n" + ticket
    else: 
        message = "ERROR: invalid login"
        print message
    client.send(message)	
	

def handler(client,addr):
    data = client.recv(buf)
    if data[:4] == 'HELO':
        client.send(str(data) +"IP:52.16.255.69\nPort: " + str(port) +"\nStudentID: aa3e68899f9a879f8408b5af0bec24991f35aa22398b70458a8239e15bb29b93\n")
    if data[:12] == "KILL_SERVICE":
        os._exit(0)
    if data[:5] == 'LOGIN':
        loginRequest(data, client)
    print "close"
    client.close()
    
if __name__=='__main__':
    address = (host, port)
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(5)
    while 1:
        print 'Authentication Server: waiting for connection...'
        client, addr = server.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (client, addr))