class ROOM

	@@no_rooms = 0
	
	def initialize(administratorID, initialUsers, title, description)
		@admin = administrator
		@users = initialUsers
		@users_last_message = Hash.new(0)
		@title = title
		@desc = description
		@msg_no = 0
		@id = @@no_rooms
		@@no_rooms += 1
	end
	
	def addUser(newUser)
		if users.has_key?(newUser.getUsername) != true
			@users[newUser.getUsername] = newUser
		end	
	end
	
	def isAdmin(userID)
		if userID == @admin
			return true
		else
			return false
		end
	end
end