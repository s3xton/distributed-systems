import socket
import sys

PORT = 8000
HOST = "localhost"

message = "GET /echo.php?message="
word = raw_input("Enter message to send: ")
message = message + word + " HTTP/1.0\r\n" + "\r\n"

print(message)

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
	