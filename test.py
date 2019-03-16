import json
import socket

# Server details
TCP_IP = '35.197.236.148'
TCP_PORT = 9877


"""Sends the given message to the game server and returns the response as a JSON object"""
def speak(msg):

    encoded_msg= bytearray(len(msg).to_bytes(4, "little")) + bytearray(msg, 'utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_IP, TCP_PORT))
        s.send(encoded_msg)
        response_len = s.recv(4)
        BUFFER_SIZE = int.from_bytes(response_len, byteorder='little')
        data = s.recv(BUFFER_SIZE)

    return json.loads(data)


"""Log us into the game server """
def login(tournament=False):

    json_str = json.dumps({"type": "login", "player": "moneymaker", "tournament": tournament})

    return speak(json_str)


"""Converts JSON object to pretty str ready for printing"""
def pretty_json(data):

     return json.dumps(data, indent=4, separators=(',', ': '))


print(pretty_json(login()))