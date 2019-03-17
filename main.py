import json
import socket
from utilities import *
from aux import *

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

    auction_param = {'type': 'auction_response', 'token': token, 'superPower': "seer", "bid": 1}

    speak(SOCKET, auction_param)
    auction()


def make_decision(status):

    cancheck = can_check(status)
    pocket = status['pocketCards']
    blind = status['blind']

    cards = list()
    cards.append(Card(pocket[0]['suit'], pocket[0]['rank']))
    cards.append(Card(pocket[1]['suit'], pocket[1]['rank']))

    community_cards = status['communityCards']
    stage = len(community_cards)  # how many community cards
    for card in community_cards:
        cards.append(Card(card['suit'], card['rank']))

    # Pre-flop
    if stage == 0:
        return preflop(cards, 2*blind, cancheck)

    # flop
    if stage == 3:
        flopStrength= flop(cards)
        print("STRENGTH: "+str(flopStrength))
        return strengthtoAction(flopStrength, blind, cancheck)

    # turn
    if stage == 4:
        turnStrength=turn(cards)
        print("STRENGTH: "+ str(turnStrength))
        return strengthtoAction(turnStrength, blind, cancheck)

    # river
    if stage == 5:
        riverStrength=handStrength({computeHand(cards): 1})
        print("STRENGTH: "+str(riverStrength))
        return strengthtoAction(riverStrength, blind, cancheck)


def status():
    received=listen(SOCKET)

    while(received["type"]=="status"):
        last_status = received
        print("status: "+ pretty_json(received))
        received=listen(SOCKET)

    if received["type"]=="bet":
        token=received["token"]
        decision, stake = make_decision(last_status)
        print("DECISION: "+ decision)
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
    #print(preflop([Card( 'spades','queen'), Card( 'hearts','queen')], 2.0, True ))
    SOCKET.close()
