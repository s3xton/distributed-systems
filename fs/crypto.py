# Just for the basis of this assignment, stupid encryption used
# more focused on correct implementation within the system
import random

def encrypt(password, message):
	return message + password

def decrypt(password, message):
	return message[:len(message)-len(password)]
	
def genSessionKey():
	return str(random.random())