class CHATCLIENT
	require "socket"
	s = TCPSocket.open("localhost", 2623)
	s.puts("JOIN_CHATROOM: name1\nCLIENT_IP: 0\n")
	while line = s.gets
		puts line
	end
	s.close()
end