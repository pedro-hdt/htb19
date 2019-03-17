import json
import socket
import utilites


# Server details
TCP_IP = '35.197.236.148'
TCP_PORT = 9877
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def speak(socket, msg):
    """Sends the given message (as python dict) to the game server"""
    json_msg = json.dumps(msg)
    encoded_msg = bytearray(len(json_msg).to_bytes(4, "little")) + bytearray(json_msg, 'utf-8')
    socket.send(encoded_msg)


def listen(socket):
    """Returns msgs from the server as JSON objects"""
    msg_len = socket.recv(4)  # check the size of msg
    BUFFER_SIZE = int.from_bytes(msg_len, byteorder='little')  # size buffer accordingly

    data = socket.recv(BUFFER_SIZE)

    return json.loads(data)


def login(tournament=False):
    """Log us into the game server """
    login_param = {"type": "login", "player": "moneymaker", "tournament": tournament}

    speak(SOCKET, login_param)
    return listen(SOCKET)


def pretty_json(data):
    """Converts JSON object to pretty str ready for printing"""
    return json.dumps(data, indent=4, separators=(',', ': '))


def auction():
    l = True
    while (l):
        received = listen(SOCKET)
        print(pretty_json(received)) # print what happens
        if received["type"] == "auction":
            l = False
            token = received["token"]
        elif received["type"] == "auction_result":
            return

    auction_param = {'type': 'auction_response', 'token': token, 'superPower': "seer", "bid": 30}

    speak(SOCKET, auction_param)
    auction()


def make_decision():

    if

    pass


def status():
    received=listen(SOCKET)

    while(received["type"]=="status"):
        print("status: "+ pretty_json(received))
        received=listen(SOCKET)

    if received["type"]=="bet":
        token=received["token"]
        decision, stake = make_decision()
        if stake:
            msg = {'type':'bet_response', 'token':token, 'action':decision, 'stake':stake, 'useReserve':False}
        else:
            msg = {'type':'bet_response', 'token':token, 'action':decision, 'useReserve':False}
        speak(SOCKET, msg)
        if msg["action"] in ['seer', 'spy', 'leech']:
            print("super power: "+ pretty_json(listen(SOCKET)))

    elif received["type"]=="folded":
            print("folded: " + pretty_json(received))

    elif received["type"]=="bankrupt":
            print("bankrupt: " + pretty_json(received))

    elif received["type"]=="summary":
        print("summary: " + pretty_json(received))
        return

    status()



if __name__ == '__main__':

    SOCKET.connect((TCP_IP, TCP_PORT))

    print(pretty_json(login()))
    auction()
    status()
    SOCKET.close()
