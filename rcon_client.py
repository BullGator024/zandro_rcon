#Done using python 3.8.5

from io import BytesIO
import hashlib
import huffman
import socket
from fixedcolors import get_color_less
from headers import svrc, clrc, protocol_ver, svrcu

h = huffman.HuffmanObject(huffman.SKULLTAG_FREQS)

class ZandronumError(Exception):

class rcon_client():
    ''' Instance of the rcon client for Zandronum 3.0 
        self.log = (List) Contains the current log
    '''
    def __init__(self):
        self.log = []
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def create_byte(self, byte: tuple):
        ''' Creates a byte and returns the huffman encoded packet
            byte = Byte type, found in headers.py
            Needs to be either a tuple or a single value
        '''
        z_byte = BytesIO()
        if type(byte) is tuple:
            for i in byte:
                z_byte.write(i)
        else:
            z_byte.write(byte)
        return h.encode(z_byte.getvalue())

    def decode_packet(self, packet):
        ''' Decodes a packet and returns the result '''
        return h.decode(packet)
    
    def add_to_log(self, entry: str):
        ''' Adds an entry to the "self.log" list '''
        self.log.append(entry)

    def disconnect_from_server(self):
        self.socket.sendto(self.create_byte(clrc['Disconnect']), self.address)
        self.socket.close()
        return
    
    def send_command(self, command: str):
        ''' Sends a command to the server '''
        self.socket.sendto(self.create_byte((clrc['Command'], command)))

    def packet_action(self, packet_id, packet_data):
        ''' Does an action depending on the packet's data and its ID '''
        pid = lambda compare: packet_id == compare

        if pid(svrc['OldProtocol']):
            raise ZandronumError('[!] Protocol version is old.')
        elif pid(svrc['Banned']):
            raise ZandronumError('[!] Your IP is banned from this server.')
        elif pid(svrc['Salt']):
            salt_pack = packet_data[0:32]
            md5_value = hashlib.md5(salt_pack + self.rcon.encode())
            md5_value = md5_value.hexdigest()
            password_pack = self.create_byte((clrc['Password'], md5_value.encode()))
            self.socket.sendto(password_pack, self.address)
        elif pid(svrc['LoggedIn']):
            print('[O] Logged in.')
        elif pid(svrc['InvalidPassword']):
            raise ZandronumError('[!] Invalid password.')
        elif pid(svrc['Message']):
            message = get_color_less(packet_data.decode())
            print(message)
        elif pid(svrc['Update']): pass
        elif pid(svrc['TabComplete']): pass
        elif pid(svrc['TooManyTabCompletes']): pass

    def connect_to_server(self, server_socket: tuple, rc_pass: str):
        ''' Establishes a connection to the server
            Must provide a socket (ip and a port in a tuple) as the second parameter
        '''
        try:
            self.socket.settimeout(4.0)
            connect_byte = self.create_byte((clrc['BeginConnection'], protocol_ver))
            self.socket.sendto(connect_byte, server_socket)
            self.address = server_socket
            s_data, addr = self.socket.recvfrom(4096)
        except socket.timeout:
            self.socket.close()
            raise ZandronumError('[!] Fail: Connection timed out.')

        # Attempt to log-in with the RCon
        print('[O] Server found. ', addr)
        self.rcon = rc_pass
        data = self.decode_packet(s_data)
        packet_id = data[0]
        self.packet_action(packet_id, data[1:])

        while True:
            try: 
                # Actions dependant to packet ID are enclosed in "ifs"
                # Can be seen in headers "svrc"
                data, addr = self.socket.recvfrom(4096)
                data = self.decode_packet(data)
                packet_id = data[0]
                self.packet_action(packet_id, data[1:])
            except socket.timeout:
                pong_packet = self.create_byte(clrc['Pong'])
                self.socket.sendto(pong_packet, self.address)
                self.socket.settimeout(4.0)

            # There was a problem somewhere, close the socket and the connection
            except ZandronumError as z_err:
                self.socket.sendto(self.create_byte(clrc['Disconnect']), self.address)
                self.socket.close()
                print('[!!!] Zandronum error: ', z_err.args)
                return

bot = rcon_client()
bot.connect_to_server(('127.0.0.1', 10666), 'megaman')
print('---- Finish ----')