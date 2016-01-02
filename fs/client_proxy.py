import socket
import sys
	
class ClientProxy: 
	
	PORT_ds = 8000
	HOST_ds = "localhost"
	PORT_ls = 8001
	HOST_ls = "localhost"
	lock = ""
	file_address = ""
	
	def __init__(self):
		self.file_address = ""
		self.PORT_ds = 8000
		self.HOST_ds = "localhost"
		self.PORT_ls = 8001
		self.HOST_ls = "localhost"
		self.lock = ""
	
	def openFile(self, filename):
		# Get the address of the file from the directory server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.HOST_ds, self.PORT_ds))
		message = "OPEN: " + filename
		s.send(message)
		data = s.recv(2048)
		string = ""
		while len(data):
			string = string + data
			data = s.recv(2048)
		self.file_address = string.strip()
		print self.file_address
		s.close()
		
		# Get a lock on the file from the lock server
		s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s2.connect((self.HOST_ls, self.PORT_ls))
		message = "LOCK: " + self.file_address.strip() + " " + filename + "\n"
		print "message - " + message
		s2.send(message)
		string = ""
		data = s2.recv(2048)
		while len(data):
			string = string + data
			data = s2.recv(2048)
		print string
		print "lock aquired\n"
		self.lock = filename
		s2.close()
			
	def writeFile(self, filename, data):
		if self.lock == filename:
			# write to the file location no the primary copy
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(("localhost", int(self.file_address)))
			msg = "WRITE: " + filename + "\nDATA: " + data
			s.send(msg)
			s.close()
		else: 
			print "ERROR: You must first open the file to write to it"
	
	def closeFile(self, filename):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.HOST_ls, self.PORT_ls))
		message = "FREE: " + self.file_address + " " + filename
		s.send(message)
		self.file_address = ""
		self.lock = ""
		print "file closed"
		s.close()
		
	def readFile(self, filename):
		# Get the address of the file
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.HOST_ds, self.PORT_ds))
		message = "READ: " + filename
		s.send(message)
		data = s.recv(2048)
		print "file address: " + data + "\n"
		s.close()
		
		# read the file from the correct address
		s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s2.connect((self.HOST_ds, int(data)))
		s2.send(message)
		string = ""
		data = s2.recv(2048)
		while len(data):
				string = string + data
				data = s2.recv(2048)
		print "File data:" + string
		s2.close()
		return string

#### TESTS ####
cp = ClientProxy()
cp.openFile("/user/test.txt")
cp.writeFile("/user/test.txt", "Fuck you")
cp.closeFile("/user/test.txt")
#writeFile("/user/hello.text", "nothing")