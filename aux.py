def determine_action(status1, status2):
    """Given 2 statuses, returns the player and the action performed between them"""
    curr_player = status1['currentPlayer']
    curr_stake = status1['stake']

    for player in status2['activePlayers']:

        if player['playerId'] == curr_player:

            # Was there a fold?
            if player['folded']:
                return curr_player, 'fold'

            # Was there a call?
            new_stake = player['stake']
            if new_stake == curr_stake:
                return curr_player, 'call'

            # Was there a raise?
            else:
                return curr_player, 'raise'


def can_check(status):
    """Returns whether we can check (in which case we cannot call)"""
    for player in status['activePlayers']:

        if player['playerId'] == status['currentPlayer']:

            return status['stake'] == player['stake']


