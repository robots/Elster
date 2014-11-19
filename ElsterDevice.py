
from ModuleType import ModuleType
from TelegramType import TelegramType
from Telegram import Telegram
import Elster

import time

class ElsterDevice:

	my_type = ModuleType.BEDIEN
	my_addr = 2

	_params = {
		0x0009: 0x2611,
		0x000a: 0x120b,
		0x000b: 0xc305,
		0x0010: 0x0051,
		0x0011: 0x00c3,
		0x002b: 0x6400,
		0x0075: 0x0015,
	}

	last_self = 0
	last_master = 0

	def get_param(self, param):
		if param not in self._params.keys():
			return 0x8000

		return self._params[param]

	def set_param(self, param, value):
		if param not in self._params.keys():
			return False

		self._params[param] = value
		return True

	def create_init_tgr(self):
		st = Telegram()

		st.to_addr = self.my_addr
		st.to_type = self.my_type
		st.from_type = self.my_type
		st.from_addr = self.my_addr
		st.tgr_type = TelegramType.SYSTEM
		st.tgr_number = 0xfd
		st.value = 0x8

		return st

	def process_tgr(self, tgr):
		if not (tgr.to_type == self.my_type and tgr.to_addr == self.my_addr):
			return False

		st = Telegram()

		st.from_type = self.my_type
		st.from_addr = self.my_addr
		st.to_type = tgr.from_type
		st.to_addr = tgr.from_addr

		print repr(tgr)
		if tgr.tgr_type == TelegramType.READ:
			st.tgr_type = TelegramType.RESPOND

			idx = tgr.tgr_number
			st.tgr_number = idx
			st.value = self.get_param(idx)
			
		elif tgr.tgr_type == TelegramType.WRITE:
			self.set_param(tgr.tgr_number, tgr.value)
		else:
			return False

		print repr(st)
		return st
	
	def periodic(self):
		ts = time.time()

		return
		if ts - self.last_self  > 4: #420
			self.last_self = ts

			st = Telegram()

			st.from_type = self.my_type
			st.from_addr = self.my_addr
			st.to_addr = 0x79
			st.to_type = 0x6
			st.tgr_type = TelegramType.SYSTEM
			st.tgr_number = 0xfe
			st.value = 0x100

			return st
		if ts - self.last_master > 5:
			self.last_master = ts

			st = Telegram()

			st.from_addr = self.my_addr
			st.from_type = self.my_type
			st.to_type = 0x0a
			st.to_addr = 0x79
			st.tgr_type = TelegramType.SYSTEM
			st.tgr_number = 0xfe
			st.value = 0x100

			return st


		return False
