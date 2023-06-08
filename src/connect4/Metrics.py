import json
import itertools

def get_json(file_name):
    data = None 
    with open(file_name, 'r') as f:
        data = json.load(f) 

    return data

def get_matchups(players, double=True):
    combinations = list(itertools.combinations(players, 2))

    matchups = []
    for comb in combinations:
        player1 = comb[0]
        player2 = comb[1]

        if player1['type'] == player2['type']:
            continue 

        matchups.append(comb)
        if double:
            revert = (comb[1], comb[0])
            matchups.append(revert)
    
    return matchups

def get_metrics_match(id, player1, player2, count):
    return { 'id' : id, 'time' : 0, 'winner': '', 'player1': player1['name'], 'player2': player2['name'], 'count': count, 'empty_cells' : 0 }

def get_metrics_game(id, round):
	return { 'id' : id, 'player': '', 'time': 0, 'empty_cells': 0, 'round': round }

def save_content(file_name, content):
    with open('metrics/' + file_name, 'w') as f:
        f.write(content)

def save_metrics_matchup(metrics_matchup, idx):
    content = json.dumps(metrics_matchup)
    save_content(f'matchup_{idx}.json', content)

def save_metrics_game(metric_game, idx):
    content = json.dumps(metric_game)
    save_content(f'game_{idx}.json', content)

def get_players(idx=0):
    file_name = f'data/players_{idx}.json' if idx != 0 else 'data/players.json'

    f = open(file_name)
    data = json.load(f)
    f.close()

    return data 