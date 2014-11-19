from Telegram import Telegram
from TelegramType import TelegramType
from ModuleType import ModuleType
from Elster import Elster

import urllib2

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

vzlink = "http://192.168.5.5/vz/middleware.php/data/%s.json?operation=add&value=%s"
get_value = [
	{ "dev_type": 3, "dev_id": 0, "var": "AUSSENTEMP",       "uuid": "034c1220-6525-11e4-a668-f3f4f57220d0" },
	{ "dev_type": 6, "dev_id": 1, "var": "RAUMISTTEMP",      "uuid": "0d34c4e0-6525-11e4-9c0d-11c59c4eabc4" },
	{ "dev_type": 3, "dev_id": 0, "var": "SPEICHERISTTEMP",  "uuid": "d8edb830-6524-11e4-9ab4-0bfa4c512470" },
	{ "dev_type": 3, "dev_id": 0, "var": "QUELLE_IST",       "uuid": "ce7478a0-6dba-11e4-a0fb-f10dd2556483" },
	{ "dev_type": 3, "dev_id": 0, "var": "RUECKLAUFISTTEMP", "uuid": "c5ca77a0-6524-11e4-8a86-3f0f03d5fa01" },
	{ "dev_type": 3, "dev_id": 0, "var": "WPVORLAUFIST",     "uuid": "bbe2d780-6524-11e4-919d-673aa542bf85" },
	{ "dev_type": 3, "dev_id": 0, "var": "HEISSGAS_TEMP",    "uuid": "ea828320-6524-11e4-995a-5bfbbfc4c365" },
]
get_value_idx = 0

state = 0
timeout = 0

#devices = [(0,0), (12, 1), (6, 1),(3, 0),(9, 0)]
#devices = [(12, 1), (6, 1),(3, 0),(9, 0)]

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
#		print frame
		if len(frame) >= 24:
			rt.from_data(frame)

			dev = (rt.from_type, rt.from_addr)

			if True:
				# print response
				canid = (rt.from_type << 7) + rt.from_addr

				print "%03x: %s = %s" % (canid, el.var_name(rt.tgr_number), el.get_value(rt))
				if st.to_addr == rt.from_addr and st.to_type == rt.from_type and st.tgr_number == rt.tgr_number:
					link = vzlink % (get_value[get_value_idx]["uuid"], el.get_value(rt))
#					print link
					try:
						content = urllib2.urlopen(link).read()
#						print content
					except:
						print "unable to upload value"
					state = 2


	if state == 0:
		varidx = el.get_var_idx(get_value[get_value_idx]["var"])
		if varidx == False:
			raise Exception("such var does not exist %s" % get_value[get_value_idx])

		st.to_addr = get_value[get_value_idx]["dev_id"]
		st.to_type = get_value[get_value_idx]["dev_type"]
		st.tgr_type = TelegramType.READ
		st.tgr_number = varidx
	
#		print str(st)
#		break
		s.send(str(st) + '\n')

		state = 1
		timeout = 0
	elif state == 1:
		timeout = timeout + 1
		if timeout == 10:
			print "Unable to get value for variable %d" % (get_value_idx)

			# timeout, advance to next device
			state = 2
	elif state == 2:
		get_value_idx += 1
		if get_value_idx == len(get_value):
			# we are done
			s.close()
			break

		state = 0

	else:
		# send space, keepalive for server (gets dropped anyways)
		s.send(' ')

	
