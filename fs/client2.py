import socket
import sys

PORT_ds = 8000
HOST_ds = "localhost"
PORT_ls = 8001
HOST_ls = "localhost"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lock = ""
file_address = ""

def openFile(filename):
	# Get the address of the file from the directory server
	s.connect((HOST_ds, PORT_ds))
	message = "OPEN: " + filename
	socket.send(message)
	data = s.recv(2048)
	string = ""
	while len(data):
		string = string + data
		data = s.recv(2048)
	file_address = string
	
	# Get a lock on the file from the lock server
	socket.connect((HOST_ls, PORT_ls))
	message = "LOCK: " + string + " " + filename
	socket.send(message)
	data = s.recv(2048)
	string = ""
	while string != "LOCK"
		while len(data):
			string = string + data
			data = s.recv(2048)
	print "lock aquired\n"
	lock = filename
		
def writeFile(filename, data):
	if lock == filename:
		# write to the file location no the primary copy
		socket.connect((file_address, 8000))
		msg = "WRITE: " + filename + " " + data
		socket.send(msg)
	else: 
		print "ERROR: You must first open the file to write to it"

def closeFile(filename):
	socket.connect((HOST_ls, PORT_ls))
	message = "FREE: " + file_address + " " + filename
	socket.send(message)
	file_address = ""
	lock = ""
