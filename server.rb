# server code
class SERVER
	require "socket"
	require "thread"
	
	address = "localhost"
	port = 2626
	server = TCPServer.open(address, port)
	
	connection_queue = Queue.new
	
	thread_pool = (0...4).map do
		Thread.new do
			while client = connection_queue.pop(false)
				puts "con"
				while line = client.gets
					case line
					when /HELO .*/
						client.puts("HELO text\nIP: " + address + "\nPort: #{port}\nStudentID: \n")
						client.puts("END\n")
					when /KILL_SERVICE/
						exit
					else
						client.puts("Invalid command: " + line)
					end
				end
			end
		end
	end
	loop do
		connection_queue.push(server.accept)
	end
end 