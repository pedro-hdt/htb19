import json
from collections import Counter
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

def make_auction_decision(past_auctions, bids):
    streak=[]
    for p in past_auctions:
        if p is not None:
            streak.append(superPowersDictionary[p])

    if len(streak)>=3:
       if not all(item == 0 for item in streak[-3:]) :
            return 'seer', bids[-1]/2
       else: return 'seer', bids[-1]*2
    else:
       return 'seer', 1

def auction(past_auctions, bids):
    l = True
    superPower, bid = make_auction_decision(past_auctions, bids)
    bids.append(bid)
    while (l):
        received = listen(SOCKET)
        print(pretty_json(received)) # print what happens
        if received["type"] == "auction":
            l = False
            token = received["token"]
        elif received["type"] == "auction_result":
            #past_auctions.append(received["superPower"])
            return

    auction_param = {'type': 'auction_response', 'token': token, 'superPower': superPower, "bid": bid}

    speak(SOCKET, auction_param)
    auction(past_auctions, bids)


def make_decision(status, super_power_card=None):

    cancheck = can_check(status)
    pocket = status['pocketCards']
    blind = status['blind']

    cards = list()
    cards.append(Card(pocket[0]['suit'], pocket[0]['rank']))
    cards.append(Card(pocket[1]['suit'], pocket[1]['rank']))
    if super_power_card is not None:
        community_cards = status['communityCards'].append(super_power_card)
    else: community_cards = status['communityCards']

    if community_cards is not None:
        stage = len(community_cards)
        for card in community_cards:
            cards.append(Card(card['suit'], card['rank']))
    else: stage = 0  # how many community cards


    if status['superPowers']['seer']>0 and stage!=5:
        status['superPowers']['seer']= status['superPowers']['seer'] -1
        return 'seer', None
    # Pre-flop
    if stage == 0:
        return preflop(cards, 2*blind, cancheck)

    # flop
    if stage == 3:
        if super_power_card is None:
            flopStrength= flop(cards)
            print("STRENGTH: "+str(flopStrength))

        else:
            flopStrength= flop(cards++super_power_card)
            print("STRENGTH: "+str(flopStrength))

        return strengthtoAction(flopStrength, blind, cancheck)

    # turn
    if stage == 4:
        if super_power_card is None:
            turnStrength=turn(cards)
            print("STRENGTH: "+ str(turnStrength))
        else:
            turnStrength=turn(cards++super_power_card)
            print("STRENGTH: "+ str(turnStrength))

        return strengthtoAction(turnStrength, blind, cancheck)

    # river
    if stage == 5:
        riverStrength=handStrength({computeHand(cards): 1})
        print("STRENGTH: "+str(riverStrength))
        return strengthtoAction(riverStrength, blind, cancheck)


def status(super_power_card=None, last_status=None):
    received=listen(SOCKET)

    while(received["type"]=="status"):
        last_status = received
        print("status: "+ pretty_json(received))
        received=listen(SOCKET)

    if received["type"]=="bet":
        token=received["token"]
        decision, stake = make_decision(last_status, super_power_card)
        print("DECISION: "+ decision)
        if stake:
            msg = {'type':'bet_response', 'token':token, 'action':decision, 'stake':stake, 'useReserve':False}
        else:
            msg = {'type':'bet_response', 'token':token, 'action':decision, 'useReserve':False}
        speak(SOCKET, msg)
        if msg["action"] in ['seer', 'spy', 'leech']:
            print(super_power_card)
            new_card=listen(SOCKET)
            print(pretty_json(new_card))
            super_power_card= new_card['card']

    elif received["type"]=="folded":
            print("folded: " + pretty_json(received))

    elif received["type"]=="summary":
        print("summary: " + pretty_json(received))
        return

    status(super_power_card, last_status)



if __name__ == '__main__':
    SOCKET.connect((TCP_IP, TCP_PORT))
    past_auctions=[]
    bids=[]
    while(True):
        print(pretty_json(login(tournament=False)))
        auction(past_auctions, bids)
        status()


    print(make_auction_decision(['seer', 'spy', 'null','null', 'null' ], [1,1,2, 4, 8 ]))
