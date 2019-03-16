import json
import socket

json_str = json.dumps({"type":"login", "player":"moneymaker", "tournament":False})

TCP_IP = '35.197.236.148'
TCP_PORT = 9877
BUFFER_SIZE = 1024
MESSAGE = bytearray(len(json_str).to_bytes(4, "little")) + bytearray(json_str, 'utf-8')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print("received data:", data)
