import json
import itertools

def get_json(file_name):
    data = None 
    with open(file_name, 'r') as f:
        data = json.load(f) 

    return data

def get_matchups(players, is_tournament, double=True):
    matchups = []
    if is_tournament: 
        combinations = list(itertools.combinations(players, 2))

        for comb in combinations:
            matchups.append(comb)
            if double:
                revert = (comb[1], comb[0])
                matchups.append(revert)
        
        return matchups

    random_player = get_random_player()
    for player in players:
        matchups.append([player, random_player])
        if double:
            matchups.append([random_player, player])
    
    return matchups

def get_random_player():
    return {"id" : 0, "type": "RANDOM", "name": "RANDOM"}

def get_match_metrics(id, player1, player2, count):
    return { 'id' : id, 'time' : 0, 'winner': '', 'player1': player1['name'], 'player2': player2['name'], 'count': count, 'empty_cells' : 0 }

def get_game_metrics(id, round):
	return { 'id' : id, 'player': '', 'time': 0, 'empty_cells': 0, 'round': round }

def save_content(file_name, content):
    with open('metrics/' + file_name, 'w') as f:
        f.write(content)

def save_game_metrics(metric_game, idx):
    content = json.dumps(metric_game)
    save_content(f'game_{idx}.json', content)

def save_matchup_metrics(metrics_matchup, idx):
    content = json.dumps(metrics_matchup)
    save_content(f'matchup_{idx}.json', content)

def get_matchups_result(idx):
    return get_json(f'metrics/matchup_{idx}.json')

def get_games_result(idx):
    return get_json(f'metrics/game_{idx}.json')


def get_players(idx=0):
    file_name = f'data/players_{idx}.json' if idx != 0 else 'data/players.json'

    f = open(file_name)
    data = json.load(f)
    f.close()

    return data 