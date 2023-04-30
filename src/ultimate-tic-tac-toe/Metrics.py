import json
import itertools

DIRNAME = 'metrics/'

def save_content(file_name, content):
    with open(DIRNAME + file_name, 'w') as f:
        f.write(content)

def get_players():
	f = open('players.json')
	data = json.load(f)
	f.close()

	return data 

def get_matchups(players):
    combinations = list(itertools.combinations(players, 2))

    matchups = []
    for comb in combinations:
        player1 = comb[0]
        player2 = comb[1]

        if player1['type'] == player2['type']:
            continue 

        matchups.append(comb)
        revert = (comb[1], comb[0])
        matchups.append(revert)
    
    return matchups

def get_game_metrics(id, player, round):
	return { 'id' : id, 'player': player, 'time': 0, 'round': round }

def get_match_metrics(game_counter, player1, player2, match_number):
    return { 'id' : game_counter, 'time' : 0, 'winner': '', 'player1': player1, 'player2': player2, 'match_number': match_number }

def save_matchup_metrics(metrics_matchup):
    content = json.dumps(metrics_matchup)
    save_content('matchup.json', content)

def save_game_metrics(metric_game):
    content = json.dumps(metric_game)
    save_content('game.json', content)
