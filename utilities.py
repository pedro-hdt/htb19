class Card:
    rank, suit = "", ""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def equals(self, otherCard):
        return (otherCard.rank == self.rank and otherCard.suit == self.suit)


rankDictionary = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, '10':8, 'jack':9, 'queen':10, 'king':11, 'ace':12}
suitDictionary = {'spades':0, 'hearts':1, 'diamonds':2, 'clubs':3}


def inList(newCard, cards):
    result = False
    for card in cards:
        if newCard.equals(card):
            return True
    return False


def computeHand(allCards):
    threes_index = None
    count_twos = 0
    twos_index = None
    fstStraight = None
    sndStraight = None

    # onePair, twoPair, threeOfAKind, straight, flush, fullHouse, straightFlush, royalFlush
    # bestCombination = [False]*9
    # check for royalFlush

    # [two, three, four, five, six, seven, eight, nine, ten, jack, queen, king, ace]
    ranks = [0] * 13

    # [spades, hearts, diamonds, clubs]
    suits = [0] * 4

    for card in allCards:
        ranks[rankDictionary[card.rank]] += 1
        suits[suitDictionary[card.suit]] += 1

    # check Royal Flush
    if ranks[12] >= 1 and ranks[11] >= 1 and ranks[10] >= 1 and ranks[9] >= 1 and ranks[8] >= 1 and (max(suits) >= 5):
        return 'royalFlush', None, None

    # check Straight Flush
    for index in range(len(ranks) - 4):
        if (ranks[index] >= 1) and (ranks[index + 1] >= 1) and (ranks[index + 2] >= 1) and (ranks[index + 3] >= 1) and (
                ranks[index + 4] >= 1):
            fstStraight = index
            sndStraight = index + 4
            if max(suits) >= 5:
                return 'straightFlush', index, index + 4

    # check 4 of a kind
    for i in range(len(ranks)):
        if ranks[i] >= 4:
            return 'fourOfAKind', i, None
        elif ranks[i] >= 3:
            threes_index = i
        elif ranks[i] >= 2:
            count_twos += 1
            twos_index = i

    # check if full house
    if threes_index and twos_index:
        return 'fullHouse', threes_index, twos_index

    # check if flush
    if max(suits) >= 5:
        return 'flush', None, None

    # check if straight
    if fstStraight != None and sndStraight != None:
        return 'straight', fstStraight, sndStraight

    # check if three of a kind
    if threes_index:
        return 'threeOfAKind', threes_index, None

    # check if two_pair
    if count_twos >= 2:
        index = len(ranks) - 1
        fstTwoPair = None
        while index >= 0:
            if ranks[index] >= 2:
                if fstTwoPair:
                    return 'twoPair', fstTwoPair, index
                else:
                    fstTwoPair = index
            index += -1

    # check if pair
    if count_twos >= 1:
        index = len(ranks) - 1
        while index >= 0:
            if ranks[index] >= 2:
                return 'onePair', index, None
            index += -1

    # get High Card
    index = len(ranks) - 1
    while index >= 0:
        if ranks[index] >= 1:
            return 'highCard', index, None
        index += -1


def flop(cardsSeen):
    outcomes = dict({'highCard': 0, 'onePair': 0, 'twoPair': 0, 'threeOfAKind': 0, 'straight': 0,
                     'flush': 0, 'fullHouse': 0, 'fourOfAKind': 0, 'straightFlush': 0, 'royalFlush': 0})

    for rank1 in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']:
        for suit1 in ['hearts', 'clubs', 'spades', 'diamonds']:
            card1 = Card(suit1, rank1)
            if not inList(card1, cardsSeen):
                l1Cards = cardsSeen + [card1]
                for rank2 in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']:
                    for suit2 in ['hearts', 'clubs', 'spades', 'diamonds']:
                        card2 = Card(suit2, rank2)
                        if not inList(card2, l1Cards):
                            l2Cards = l1Cards + [card2]
                            outcome, _, __ = computeHand(l2Cards)
                            outcomes[outcome] += 1

    total = 0
    for outcome in outcomes.keys():
        total += outcomes[outcome]

    for outcome in outcomes.keys():
        print(str(outcome) + ' with probability ' + str(outcomes[outcome] / total))


def turn(cardsSeen):
    outcomes = dict({'highCard': 0, 'onePair': 0, 'twoPair': 0, 'threeOfAKind': 0, 'straight': 0,
                     'flush': 0
                        , 'fullHouse': 0, 'fourOfAKind': 0, 'straightFlush': 0, 'royalFlush': 0})
    for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']:
        for suit in ['hearts', 'clubs', 'spades', 'diamonds']:
            newCard = Card(suit, rank)
            if not inList(newCard, cardsSeen):
                l1Cards = cardsSeen + [newCard]
                outcome, _, __ = computeHand(l1Cards)
                outcomes[outcome] += 1

    total = 0
    for outcome in outcomes.keys():
        total += outcomes[outcome]

    for outcome in outcomes.keys():
        print(str(outcome) + ' with probability ' + str(outcomes[outcome] / total))
