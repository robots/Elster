

from TelegramType import TelegramType
import ModuleType

import struct
from Elster import Elster


class Telegram(object):

	_data = [0] * 12 

#	def __init__(self):
#		print "ahoj"
	
	def __init__(self, from_addr=0x00, from_type=0x0d, to_addr = 0, to_type = 0x00, tgr_type = 0, tgr_number = 0):
		self.from_type = from_type
		self.from_addr = from_addr
		self.to_type= to_type
		self.tgr_type = tgr_type
		self.to_addr = to_addr
		self.tgr_number = tgr_number

	def _chksum(self):
		s = sum(self._data[:10])

		self._data[10] = (s >> 8)
		self._data[11] = (s & 0xff)

	def to_data(self):
		self._chksum()

		out = ""
		for i in range(0, 12):
			out += "%02x" % self._data[i]

		return out

	def from_data(self, data):
		if not len(data) == 12*2:
			raise Exception("Data len error")

		d = []
		for i in range(0, 12):
			d.append(int(data[i*2:i*2+2], 16))

		s = sum(d[:10])

		if d[10] == (s >> 8) and d[11] == (s & 0xff):
			self._data = d
			return True

		raise Exception("Checksum error")


	@property
	def to_addr(self):
		return self._data[4]
	
	@to_addr.setter
	def to_addr(self, to_addr):
#		print "setting toaddr", to_addr
#		if to_addr < 0 or to_addr > 0x0f:
#			raise Exception("Out of range")

		self._data[4] = to_addr
	
	@property
	def to_type(self):
		return self._data[2]
	
	@to_type.setter
	def to_type(self, to_type):
		if to_type >= 255:
			raise Exception("Out of range")

		self._data[2] = to_type
	
	@property
	def from_type(self):
		return self._data[0]

	@from_type.setter
	def from_type(self, from_type):
		self._data[0] = from_type

	@property
	def from_addr(self):
		return self._data[1]

	@from_addr.setter
	def from_addr(self, from_addr):
		self._data[1] = from_addr

	@property
	def tgr_type(self):
		return self._data[3]
	
	@tgr_type.setter
	def tgr_type(self, nr):
		if nr > 7:
			raise Exception("Out of range")

		self._data[3] = nr

	@property
	def tgr_number(self):
		nr = self._data[5]
		if self._data[5] == 250:
			nr = (self._data[6] << 8) + self._data[7]
			
		return nr

	@tgr_number.setter
	def tgr_number(self, nr):
		if nr == 250:
			raise Exception("250 is not allowed")
		elif nr > 255:
			self._data[5] = 250
			self._data[6] = (nr >> 8) & 0xff
			self._data[7] = nr & 0xff
		else:
			self._data[5] = nr

	@property
	def value(self):
		return self.get_data_short()

	@value.setter
	def value(self, data):
		self.set_data_short(data)

	def set_data_short(self, short):
		idx = 6
		if self._data[5] == 250:
			idx = 8
		self._data[idx+1] = short & 0xff 
		self._data[idx+0] = (short >> 8) & 0xff 

	def get_data_short(self):
		idx = 6
		if self._data[5] == 250:
			idx = 8
		return self._data[idx+1] | (self._data[idx+0] << 8)

	def get_data_long(self):
		return self._data[6] | (self._data[7] << 8) | (self._data[8] << 16) | (self._data[9] << 24)

	def is_response(self, tg):
		#FIXME: READ -> ACK? is that correct?
		if self.to_addr == tg.from_addr and self.to_type == tg.from_type and self.tgr_number == tg.tgr_number:
			if self.tgr_type == TelegramType.READ and (tg.tgr_type == TelegramType.RESPOND or tg.tgr_type == TelegramType.ACKNOWLEDGE):
				return True
			if self.tgr_type == TelegramType.WRITE and (tg.tgr_type == TelegramType.WRITE_RESPOND or tg.tgr_type == TelegramType.WRITE_ACKNOWLEDGE):
				return True
			if self.tgr_type == TelegramType.SYSTEM and tg.tgr_type == TelegramType.RESPONDSYSTEM:
				return True

		return False

	def __repr__(self):
		canid_from = (self.from_type << 7) + self.from_addr
		canid_to = (self.to_type << 7) + self.to_addr
		el = Elster()

		if self.tgr_type == TelegramType.READ:
			s = "0x%03x -> 0x%03x (%s) %s" % (canid_from, canid_to, TelegramType.to_string(self.tgr_type), el.var_name(self.tgr_number))
		else:
			s = "0x%03x -> 0x%03x (%s) %s = %s" % (canid_from, canid_to, TelegramType.to_string(self.tgr_type), el.var_name(self.tgr_number), el.get_value(self))

		return s

	def __str__(self):
		return self.to_data()

	def show(self):
		print "%02d:%02d -> %02d:%02d (%02d, %02d)" % (self.from_type, self.from_addr, self.to_type, self.to_addr, self.tgr_type, self.tgr_number)
