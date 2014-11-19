from Telegram import Telegram
from ModuleType import ModuleType
from Elster import Elster

import socket
import select

CANSERVER_IP = '192.168.5.11'
CANSERVER_PORT = 5524
BUFFER_SIZE = 32

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((CANSERVER_IP, CANSERVER_PORT))

el = Elster()
rt = Telegram()
st = Telegram()

scan_modules = [0x0c, 0x06, 0x03, 0x09, 0x0a]
scan_module_idx = 0
scan_busaddr_max = 15
scan_busaddr = 0

state = 0
timeout = 0

#devices = [(0,0), (12, 1), (6, 1),(3, 0),(9, 0)]
devices = []
#devices = [(12, 1)]
device_idx = 0

variable_idx = 0
variable_max = 0x10000

fo = open("scanout.inc","w")

data = ""
print "connected?" 
while True:
	rtr = select.select([s], [], [], 0.75)[0]

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

			if state < 3:
				# save every seen device in discovery
				if dev not in devices:
					print "New device found: ", ModuleType.to_string(rt.from_type), ":", rt.from_addr
					devices.append(dev)

				if rt.from_type == scan_modules[scan_module_idx] and rt.from_addr == scan_busaddr:
					state = 2
			elif state >= 3:
				# print response in scanner mode
				canid = (rt.from_type << 7) + rt.from_addr
				var_data = rt.value
				if rt.is_response(st):
					print "%03x: %s = %s" % (canid, el.var_name(rt.tgr_number), el.get_value(rt))
					sline = "  { 0x%03x, 0x%04x, 0x%04x}," % (canid, rt.tgr_number, var_data)
					if var_data != 0x8000:
						fo.write(sline + '\n')


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
				# we are done, exit discovery, print and then start scanning
				state = 5
				continue

		state = 0
	elif state == 3:
		if variable_idx == variable_max:
			#last variable read, advance device
			device_idx += 1
			if device_idx >= len(devices):
				# we are done, wait some time for answers to arrive
				timeout = 0
				state = 4

		
		dev = devices[device_idx]
		st.to_type = dev[0]
		st.to_addr = dev[1]
		st.tgr_type = 1
		st.tgr_number = variable_idx

		print str(st)
		s.send(str(st) + '\n')

		variable_idx += 1
		
		if variable_idx > 0x200:
			while el.var_exists(variable_idx) == False:
				variable_idx += 1
		elif variable_idx == 250:
			variable_idx = 251

	elif state == 4:
		timeout += 1
		if timeout == 3:
			s.close()
			break

	elif state == 5:
		print "Devices discovered:"
		for dev in devices:
			print dev
		state = 3

	else:
		# send space, keepalive for server (gets dropped anyways)
		s.send(' ')

	
fo.close()
