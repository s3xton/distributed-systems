# Author: Conor Sexton 14/10/25
class SERVER
	require "socket"
	require "thread"
	
	address = "localhost"
	port = ARGV[0]
	server = TCPServer.open(address, port)
	
	# Queue is thread-safe so if multiples threads access it at the same time it will
	# maintain consistency
	connection_queue = Queue.new
	
	# Create 10 threads which are constantly trying to pull from the queue.
	# If there is nothing in the queue, the thread will wait until there is.
	thread_pool = (0...20).map do
		Thread.new do
			while client = connection_queue.pop(false)
				puts "con"
				line = client.gets
				case line
				when /HELO .*/
					client.puts("HELO text\nIP: " + address + "\nPort: #{port}\nStudentID: \n")
				when /KILL_SERVICE/
					exit
				else
					client.puts("Invalid command: " + line)
				end
			end
		end
	end
	# Main control loops pushes new connections to the queue
	loop do
		connection_queue.push(server.accept)
	end
end 
