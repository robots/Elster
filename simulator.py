from Telegram import Telegram
from ModuleType import ModuleType

from ElsterDevice import ElsterDevice

import time
import socket
import select

CANSERVER_IP = '192.168.5.11'
CANSERVER_PORT = 5524
BUFFER_SIZE = 32

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((CANSERVER_IP, CANSERVER_PORT))

ed = ElsterDevice()

rt = Telegram()
st = Telegram()

data = ""
print "connected?" 

s.send(str(ed.create_init_tgr()) + '\n')

while True:
	rtr = select.select([s], [], [], 1)[0]

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

#			print ts, repr(rt)
			sndtgr = ed.process_tgr(rt)
			if not sndtgr == False:
				s.send(str(sndtgr) + '\n')



	# send space, keepalive for server (gets dropped anyways)
	sndtgr = ed.periodic()
	if sndtgr == False:
		s.send(' ')
	else:
		s.send(str(sndtgr) + '\n')


