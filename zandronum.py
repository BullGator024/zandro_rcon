from io import BytesIO

import hashlib
import huffman
import socket
from fixedcolors import purifystring
from headers import svrc, clrc, protocol_ver, svrcu

h = huffman.HuffmanObject(huffman.SKULLTAG_FREQS)


class Zandronum(object):
    def __init__(self, addr: 'str', prt: 'int', password: 'str'):
        # General
        self.state = '---'
        self.skip_log = False
        self.do_chat = False
        self.rcon = password
        self.debug = False

        self.currentLog = []
        self.map = ''

        # Socket
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Ip and port
        self.ip = addr
        self.port = prt
        self.address = (str(self.ip), int(self.port))

    def encode_p(self, data):
        return h.encode(data.getvalue())

    def decode_p(self, data):
        return h.decode(data)

    def connect(self):
        print(f'Connecting to {self.ip}:{self.port}...')
        self.socket.settimeout(5)
        connect_tries = 5

        while 1:
            connect_tries -= 1
            if connect_tries == 0:
                self.state = 'Fail'
                break
            try:
                b = BytesIO()
                b.write(clrc['BeginConnection'])
                b.write(protocol_ver)
                self.socket.sendto(self.encode_p(b), self.address)
                self.__main__()
            except socket.timeout:
                self.socket.settimeout(4)
            except Exception as e:
                print(e)

    def __main__(self):
        p, address = [0, 0]
        while True:
            try:
                self.socket.settimeout(5)
                p, address = self.socket.recvfrom(4096)
                if self.debug:
                    print(f'Received from {p}:{address}')
            except socket.timeout:
                b = BytesIO()
                b.write(clrc['Pong'])
                self.socket.sendto(self.encode_p(b), self.address)
                self.socket.settimeout(4)
            except Exception as e:
                print(e)

            i = 0
            d = ''
            if p is not None:
                d = self.decode_p(p)

                i = d[0]
                d = d[1:]

            if i == svrc['Salt']:
                salt = d[0:32]
                md = hashlib.md5(salt + self.rcon.encode())
                md_final = md.hexdigest()
                b = BytesIO()
                b.write(clrc['Password'])
                b.write(md_final.encode())
                self.socket.sendto(self.encode_p(b), self.address)
            elif i == svrc['LoggedIn']:
                self.state = 'Connected'
                self.currentLog.append('Connected and logged in.')
            elif i == svrc['InvalidPassword']:
                self.state = 'Invalid'

            elif i == svrc['Message']:
                message = d.decode()
                cleaned_string = purifystring(message)
                toprint = cleaned_string.rstrip('\0')
                try:
                    self.currentLog.append(toprint)
                except Exception as err:
                    self.currentLog.append(err)
            elif i == svrc['Update']:
                print(f'Received "Update" of type: {d[1]}')
                if d[1] == svrcu['Map']:
                    self.change_map(d[1:].decode('latin-1'))

            p = None
            i = 0

    def disconnect(self):
        b = BytesIO()
        b.write(clrc['Disconnect'])
        self.socket.sendto(self.encode_p(b), self.address)
        self.state = 'Disconnected'

    def send_command(self, command: 'str'):
        b = BytesIO()
        b.write(clrc['Command'])
        b.write(command.encode())
        self.socket.sendto(self.encode_p(b), self.address)

    def change_map(self, new_map: 'str'):
        if self.map == '':
            print(f'Map changed to {new_map}')
            self.currentLog.append(f'Map changed to {new_map}')
            self.map = new_map
        else:
            print(f'Map changed from {self.map} to {new_map}')
            self.currentLog.append(f'Map changed from {self.map} to {new_map}')
            self.map = new_map
