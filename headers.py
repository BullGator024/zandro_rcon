protocol_ver = int(4).to_bytes(1, byteorder='little')

svrc = {
	'OldProtocol': 			int(32),
	'Banned': 				int(33),
	'Salt': 				int(34),
	'LoggedIn': 			int(35),
	'InvalidPassword': 		int(36),
	'Message': 				int(37),
	'Update': 				int(38),
	'TabComplete': 			int(39),
	'TooManyTabCompletes': 	int(38),
}

clrc = {
	'BeginConnection': 		int(52).to_bytes(1, byteorder='little'),
	'Password': 			int(53).to_bytes(1, byteorder='little'),
	'Command': 				int(54).to_bytes(1, byteorder='little'),
	'Pong': 				int(55).to_bytes(1, byteorder='little'),
	'Disconnect': 			int(56).to_bytes(1, byteorder='little'),
	'TabComplete': 			int(57).to_bytes(1, byteorder='little'),
}

svrcu = {
	'PlayerData':			int(0),
	'AdminCount': 			int(1),
	'Map': 					int(77),
}