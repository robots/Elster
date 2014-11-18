from Telegram import Telegram
import ModuleType
import struct


tg = Telegram()
#tg.from_data("0300060679fe010000000187")
#tg.show()
#tg.test()
tg.from_addr = 0
tg.from_type = 0x0d
tg.to_addr = 0x04 #scan_busaddr
tg.to_type = 0x05 #scan_modules[scan_module_idx]
tg.tgr_type = 1
tg.tgr_number = 0x0b

print tg.to_data()
print ModuleType.ModuleType.to_string(10)
print repr(tg)
