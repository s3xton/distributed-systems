import socket
import sys

PORT = 8000
HOST = "localhost"

message = "JOIN_CHATROOM: [chatroom name]\nCLIENT_IP: [IP Address of client if UDP | 0 if TCP]\nPORT: [port number of client if UDP | 0 if TCP]\nCLIENT_NAME: [string Handle to identifier client user]"


# Open socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Send get request to server
s.send(message)

# Receive response from server
data = s.recv(2048)
string = ""

while len(data):
	string = string + data
	data = s.recv(2048)
s.close()

# Print the response
print(string)

sys.exit(0)
	