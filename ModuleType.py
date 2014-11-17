
class ModuleType:
	DIRECT = 0
	KESSEL = 3
	BEDIEN = 6
	RAUM_FERNSTELLER = 8
	MANAGER = 9
	HEIZMODUL = 0x0a
	MISCHER = 0x0c
	PC = 0x0d
	FREMDGERAET = 0x0e 
	DCF_MODUL = 0x0f

	@staticmethod
	def to_string(modid):
		strings = {
			0: "Direct",
			3: "Kessel",
			6: "Bedien",
			8: "Raum fernsteller",
			9: "Manager",
			10: "Heizmodul",
			12: "Mischer",
			13: "PC",
			14: "Fremdgeraet",
			15: "DCF",
		}

		return strings[modid]

