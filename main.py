import json
import socket

# Server details
TCP_IP = '35.197.236.148'
TCP_PORT = 9877
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


"""Sends the given message to the game server"""
def speak(socket, msg):
    encoded_msg = bytearray(len(msg).to_bytes(4, "little")) + bytearray(msg, 'utf-8')
    socket.send(encoded_msg)


"""Returns msgs from the server as JSON objects"""
def listen(socket):

    msg_len = socket.recv(4)     # check the size of msg
    BUFFER_SIZE = int.from_bytes(msg_len, byteorder='little') # size buffer accordingly

    data = socket.recv(BUFFER_SIZE)

    return json.loads(data)



"""Log us into the game server """
def login(tournament=False):

    json_str = json.dumps({"type": "login", "player": "moneymaker", "tournament": tournament})

    speak(SOCKET, json_str)
    return listen(SOCKET)


"""Converts JSON object to pretty str ready for printing"""
def pretty_json(data):

     return json.dumps(data, indent=4, separators=(',', ': '))

def auction():
    listen=True
    while (listen):
        if listen(SOCKET)["type"]=="auction":
             listen=False
             token=listen(SOCKET)["token"]

    speak(SOCKET)

def play():
    # Game ends when the response message has type=summary

    auction()

    bet()




if __name__ == '__main__':

    SOCKET.connect((TCP_IP, TCP_PORT))

    print(pretty_json(login()))

    SOCKET.close()