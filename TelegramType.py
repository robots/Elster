
class TelegramType:
	WRITE = 0
	READ = 1
	RESPOND = 2
	ACKNOWLEDGE = 3
	WRITE_ACKNOWLEDGE = 4
	WRITE_RESPOND = 5
	SYSTEM = 6
	RESPONDSYSTEM = 7
	WRITE_LARGE = 32
	READ_LARGE = 33

	@staticmethod
	def to_string(modid):
		strings = {
			TelegramType.WRITE: "write",
			TelegramType.READ: "read",
			TelegramType.RESPOND: "respond",
			TelegramType.ACKNOWLEDGE: "ack",
			TelegramType.WRITE_ACKNOWLEDGE: "write ack",
			TelegramType.WRITE_RESPOND: "write respond",
			TelegramType.SYSTEM: "system",
			TelegramType.RESPONDSYSTEM: "system respond",
			TelegramType.WRITE_LARGE: "write large",
			TelegramType.READ_LARGE: "read large",
		}

		return strings[modid]

