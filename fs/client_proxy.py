import socket
import sys
import signal
import threading
import crypto

class ClientProxy: 
	#
	# This class handles all interaction with the file system.
	# To write to files, users must first open them. Opening them 
	# grants the client a lock. I did this to maintain total ordering
	# in the file system and all clients the ability to work on a value
	# without it being changed. Closing the file releases the lock.
	#
	def __init__(self):
		self.file_address = ""
		self.PORT_ds = 8000
		self.HOST_ds = "localhost"
		self.PORT_ls = 8001
		self.HOST_ls = "localhost"
		self.PORT_as = 8010
		self.HOST_as = "localhost"
		self.lock = ""
		self.sessionKey = ""
		self.ticket = ""
		self.loggedIn = False
		# Timer which closes a file after 10 seconds if the user doesn't
		
		signal.signal(signal.SIGALRM, self.signal_handler)
		signal.alarm(10)   # Ten seconds
	
	def signal_handler(self, signum, frame):
		raise Exception("Timed out!")
	
	def formMessage(self, message):
		new_m = crypto.encrypt(self.sessionKey, message) + "\n" + self.ticket
		return new_m
		
	def openFile(self, filename):
		if self.loggedIn:
			# Get the address of the file from the directory server
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.HOST_ds, self.PORT_ds))
			message = "OPEN: " + filename
			s.send(self.formMessage(message))
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
			s2.send(message)
			string = ""
			data = s2.recv(2048)
			while len(data):
				string = string + data
				data = s2.recv(2048)
			print string
			print "lock aquired\n"
			self.lock = filename
			self.t = threading.Timer(10.0, self.closeFile, [self.lock])
			self.t.start()
			s2.close()
		else:
			print "ERROR: you must log in first"
			
	def writeFile(self, filename, data):
		if self.loggedIn:
			if self.lock == filename:
				# write to the file location no the primary copy
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect(("localhost", int(self.file_address)))
				msg = "WRITE: " + filename + "\nDATA: " + data
				s.send(msg)
				s.close()
			else: 
				print "ERROR: You must first open the file to write to it"
		else:
			print "ERROR: you must log in first"
	
	def closeFile(self, filename):
		if self.loggedIn:
			self.t.cancel()
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.HOST_ls, self.PORT_ls))
			message = "FREE: " + self.file_address + " " + filename
			s.send(message)
			self.file_address = ""
			self.lock = ""
			print message
			s.close()
		else:
			print "ERROR: you must log in first"
	
	def alertDirectoryServer(self, address):
		if self.loggedIn:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.HOST_ds, self.PORT_ds))
			message = "CRASH: " + address
			s.send(self.formMessage(message))
			s.close()
		else:
			print "ERROR: you must log in first"
		
	def readFile(self, filename):
		if self.loggedIn:
			# Get the address of the file
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.HOST_ds, self.PORT_ds))
			message = "READ: " + filename
			s.send(self.formMessage(message))
			data = s.recv(2048)
			print "file address: " + data
			s.close()
			
			# read the file from the correct address
			s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s2.connect((self.HOST_ds, int(data)))
			s2.send(message)
			string = ""
			
			# Waits for 10 seconds for response from server, if none coming
			# alert directory server to slave failure and retry with new address
			try:
				data = s2.recv(2048)
				while len(data):
					string = string + data
					data = s2.recv(2048)
				print "File data:" + string
				s2.close()
			except Exception, msg:
				print "Timed out, retrying with new copy"
				self.alertDirectoryServer(data)
				string = self.readFile(filename)
				s2.close()
			
			return string
		else:
			print "ERROR: you must log in first"
	
	def login(self, username, password):
		encrypted = crypto.encrypt(password, username)
		message = "LOGIN: " + username + "\n" + encrypted
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.HOST_as, self.PORT_as))
		s.send(message)
		data = s.recv(2048)
		lines = data.splitlines()
		self.sessionKey = crypto.decrypt(password, lines[0])
		self.ticket = lines[1]
		self.loggedIn = True
	


#### TESTS ####
cp = ClientProxy()
#cp.readFile("/user/tb.txt")
cp.login("conor", "password")
cp.openFile("/user/tb.txt")
cp.writeFile("/user/tb.txt", "Helllll")
cp.closeFile("/user/tb.txt")
#writeFile("/user/hello.text", "nothing")
