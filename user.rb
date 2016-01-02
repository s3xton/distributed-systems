class USER
	
	def initialize(id, pass, ipAddr)
		@username = id
		@password = pass
		@ip = ipAddr
		@rooms = Hash.new
	end
	
	def getUsername
		return @username
	end
	
	def getIP
		return @ip
	end
	
	def setIP(newIP)
		@ip = newIP
	end
	
	def getRooms
		return @rooms
	end
	
	def addTo(newRoom)
		@rooms[newRoom.getID] = newRoom
	end
	
	def removeFrom(oldRoom)
		@rooms.delete(oldRoom.getID)
	end
	
	def checkPassword(pass)
		if @password == pass
			return true
		else
			return false
		end
	end
	
	
end