class CLIENT
	require "socket"
	s = TCPSocket.open("localhost", 2623)
	s.puts("HELO text\n")
	while line = s.gets
		puts line
	end
	s.close()
end
