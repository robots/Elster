from Telegram import Telegram
from ModuleType import ModuleType

import socket
import select

CANSERVER_IP = '192.168.5.11'
CANSERVER_PORT = 5524
BUFFER_SIZE = 32

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((CANSERVER_IP, CANSERVER_PORT))

rt = Telegram()
st = Telegram()

scan_modules = [0x0c, 0x06, 0x03, 0x09, 0x0a]
scan_module_idx = 0
scan_busaddr_max = 15
scan_busaddr = 0

state = 0
timeout = 0

devices = []

data = ""
print "connected?" 
while True:
	rtr = select.select([s], [], [], 0.1)[0]

	#received something ?
	if len(rtr) > 0:
		data = data + s.recv(BUFFER_SIZE)
		if len(data) == 0:
			continue

		if '\n' not in data:
			continue
		
		frame, data = data.split('\n', 1)
		print frame
		if len(frame) >= 24:
			rt.from_data(frame)

			dev = (rt.from_type, rt.from_addr)
			# save every seen device
			if dev not in devices:
				print "New device found: ", ModuleType.to_string(rt.from_type), ":", rt.from_addr
				devices.append(dev)

			if rt.from_type == scan_modules[scan_module_idx] and rt.from_addr == scan_busaddr:
				state = 2


	if state == 0:
#		st.from_addr = 0
#		st.from_type = 0x0d
		st.to_addr = scan_busaddr
		st.to_type = scan_modules[scan_module_idx]
		st.tgr_type = 1
		st.tgr_number = 0x0b
	
		print str(st)
#		break
		s.send(str(st) + '\n')

		state = 1
		timeout = 0
	elif state == 1:
		timeout = timeout + 1
		if timeout == 2:
			# timeout, advance to next device
			state = 2
	elif state == 2:
		scan_busaddr += 1
		if scan_busaddr > scan_busaddr_max:
			scan_busaddr = 0
			scan_module_idx += 1

			if scan_module_idx >= len(scan_modules):
				# we are done, exit
				s.close()
				break

		state = 0
	else:
		# send space, keepalive for server (gets dropped anyways)
		s.send(' ')

	

print "Devices discovered:"
for dev in devices:
	canid = (dev[0] << 7) + dev[1]
	print "Canid: 0x%03x type: 0x%02x addr: 0x02x" % (canid, dev[0], dev[1])
