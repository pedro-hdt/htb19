import json
import socket

# Server details
TCP_IP = '35.197.236.148'
TCP_PORT = 9877
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


"""Sends the given message to the game server"""
def speak(socket, msg):
    msg=json.dumps(msg)
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
    l=True
    while (l):
        received=listen(SOCKET)
        print("a "+ pretty_json(received))
        if received["type"]=="auction":
             l=False
             token=received["token"]
        elif received["type"]=="auction_result":
                return

    msg=json.dumps({'type':'auction_response', 'token':token, 'superPower':"seer", "bid":30})

    speak(SOCKET, msg)
    auction()

def status():
    received=listen(SOCKET)
    if received["type"]=="status":
        print("status: "+ pretty_json(received))
    elif received["type"]=="bet":
        token=received["token"]
        msg ={'type':'bet_response', 'token':token, 'action':'seer', 'useReserve':False}
        speak(SOCKET, msg)
        if msg["action"] in ['seer', 'spy', 'leech']:
            print("super power: "+ pretty_json(received))
    elif received["type"]=="summary":
        print("summary: " + pretty_json(received))
        return

    status()



def play():
    # Game ends when the response message has type=summary
    return




if __name__ == '__main__':
    SOCKET.connect((TCP_IP, TCP_PORT))

    print(pretty_json(login()))
    auction()
    status()
    SOCKET.close()
