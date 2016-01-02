class CHATSERVER
	require "socket"
	require "thread"
	require "room"
	require "user"
	
	address = "localhost"
	port = 2623
	server = TCPServer.open(address, port)
	
	rooms = Hash.new
	rooms[global] = room.new("gadmin", Hash.new, "Global Room", "Room for everyone")
	
	# Queue is thread-safe so if multiples threads access it at the same time it will
	# maintain consistency
	connection_queue = Queue.new
	
	# Create 20 threads which are constantly trying to pull from the queue.
	# If there is nothing in the queue, the thread will wait until there is.
	thread_pool = (0...20).map do
		Thread.new do
			while client = connection_queue.pop(false)
				puts "con"
				line = client.gets
				case line
				when /HELO .*/
					client.puts("HELO text\nIP: " + address + "\nPort: #{port}\nStudentID: \n")
				
				when /JOIN_CHATROOM: .*/
					# Get relevant information
					roomName = line[13, line.length-3]
					puts roomName
					
					clientIP = client.gets
					clientIP = clientIP[11,clientIP.length-3]
					puts clientIP
					
					port = client.gets
					port = port[5, port.length-3]
					puts port
					
					clientName = client.gets
					clientName = clientName[13, clientName.length-3]
					
					# Join the chatroom
					
					
					
				when /KILL_SERVICE/
					exit
				else
					client.puts("Invalid command: " + line)
				end
				puts "done"
			end
		end
	end
	# Main control loops pushes new connections to the queue
	loop do
		connection_queue.push(server.accept)
	end
	
	def joinRoom(roomName, clientName)
end