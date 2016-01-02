from socket import *
import thread
import os
import sys 
import collections
buf = 1024
host = ""
port = 443
rooms = collections.defaultdict(dict) #[rooms_red : [join_id: socket]]
room_numbers = collections.defaultdict(dict)
client_numbers = collections.defaultdict(dict)

def joinChat(data, client):
    lines = str(data).splitlines()
    chat_name = lines[0][14:]
    client_name = lines[3][12:]
    
    rooms[hash(chat_name)][hash(client_name)] = client
     
    reply = "JOINED_CHATROOM: " + chat_name + "\nSERVER_IP: 52.31.145.59" + "\nPORT: " + str(port) + "\nROOM_REF: " + str(hash(chat_name)) + "\nJOIN_ID: " + str(hash(client_name))+"\n"
    client.send(reply)
    
    #room_msg = 'CHAT: ' + str(hash(chat_name)) + '\nCLIENT_NAME: ' + client_name + '\nMESSAGE: ' + client_name+ ' has joined this chatroom.\n\n'
    room_join_message = "CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {1} has joined this chatroom.\n\n".format(str(hash(chat_name)),client_name)
    #print room_join_message
    for id in rooms[hash(chat_name)].keys():
        rooms[hash(chat_name)][id].send(room_join_message)
            
def sendMessage(data):
    lines = str(data).splitlines()
    room_ref = lines[0][6:]
    join_id = lines[1][9:]
    client_name = lines[2][13:]
    msg = lines[3][9:]
    reply = "CHAT:" + room_ref + "\nCLIENT_NAME: " + client_name+ "\nMESSAGE: " + msg + "\n\n"
    #print reply
    for id in rooms[int(room_ref)].keys():
        rooms[int(room_ref)][id].send(str(reply))

def leaveChatroom(data, client, dc):
    lines = str(data).splitlines()
    room_ref = lines[0][16:]
    join_id = lines[1][9:]
    client_name = lines[2][12:]
    print "cn ---- " + client_name + "\n"
    if not dc:
        reply = "LEFT_CHATROOM: " + room_ref + "\nJOIN_ID: " + join_id +"\n"
        client.send(reply)
    
    room_leave_message = "CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {1} has left this chatroom.\n\n".format(room_ref,client_name)
    for id in rooms[int(room_ref)].keys():
        print room_leave_message
        rooms[int(room_ref)][id].send(room_leave_message)
        
    del rooms[int(room_ref)][int(join_id)]
    
def disconnect(data, client):
    lines = str(data).splitlines()
    client_name = lines[2][12:]
    #print "cn ---- " + client_name + "\n"
    for id in reversed(sorted(rooms.keys())):
        if rooms[id].has_key(hash(client_name)):
            print "d\n"
            msg = "LEAVE_CHATROOM: " + str(id) + "\nJOIN_ID: " + str(hash(client_name)) + "\nCLIENT_NAME: " + client_name+"\n"
            leaveChatroom(msg, client, True)
                
    client.close()
    
def handler(client,addr):
    chat_name = ""
    client_name = ""
    while 1:
        data = client.recv(buf)

        if data[:4] == 'HELO':
            client.send(str(data) +"IP:52.31.145.59\nPort: " + str(port) +"\nStudentID: aa3e68899f9a879f8408b5af0bec24991f35aa22398b70458a8239e15bb29b93\n")
       
        if data[:12] == "KILL_SERVICE":
            os._exit(0)
        
        if data[:5] == 'JOIN_':
            joinChat(data, client)
            
        if data[:4] == 'CHAT':
            sendMessage(data)
            
        if data[:5] == 'LEAVE':
            leaveChatroom(data, client, False)
        
        if data[:10] == 'DISCONNECT':
            print "switch_d\n"
            disconnect(data, client)
            break
        
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