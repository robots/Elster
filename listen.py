from Telegram import Telegram
from ModuleType import ModuleType

import time
import socket
import select

CANSERVER_IP = '192.168.5.11'
CANSERVER_PORT = 5524
BUFFER_SIZE = 32

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((CANSERVER_IP, CANSERVER_PORT))

rt = Telegram()
st = Telegram()

data = ""
print "connected?" 
while True:
	rtr = select.select([s], [], [], 2)[0]

	#received something ?
	if len(rtr) > 0:
		data = data + s.recv(BUFFER_SIZE)
		if len(data) == 0:
			continue

		if '\n' not in data:
			continue
		
		frame, data = data.split('\n', 1)
#		print frame
		if len(frame) >= 24:
			ts = time.time()
			rt.from_data(frame)

			print ts, repr(rt)


	# send space, keepalive for server (gets dropped anyways)
	s.send(' ')


