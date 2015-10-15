# Author: Conor Sexton 14/10/25
class SERVER
	require "socket"
	require "thread"
	
	address = "localhost"
	port = ARGV[0]
	server = TCPServer.open(address, port)
	student_id = "aa3e68899f9a879f8408b5af0bec24991f35aa22398b70458a8239e15bb29b93"
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
					client.puts("HELO text\nIP: " + address + "\nPort: #{port}\nStudentID: " + student_id +"\n")
				when /KILL_SERVICE/
					exit
				else
					client.puts("Invalid command: " + line)
				end
			end
			client.close
		end
	end
	# Main control loops pushes new connections to the queue
	loop do
		connection_queue.push(server.accept)
	end
	server.close
end 
