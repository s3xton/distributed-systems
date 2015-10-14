class CLIENT
	require "socket"
	s = TCPSocket.open("localhost", 2623)
	s.puts("HELO text\n")
	while line = s.gets
		if line == "END\n"
			break
		else
			puts line
		end
	end
	s.close()
end
