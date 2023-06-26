import json
import itertools
import os
import copy

def get_json(file_name):
    if not os.path.isfile(file_name):
        return None 

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

def update_game_metrics(game_metrics, game_metric, idx):
    for gm in game_metric:
        if idx >= len(game_metrics):
            break

        m = game_metrics[idx]

        if m['id'] == gm['id']:
            game_metrics[idx] = copy.deepcopy(gm)

        idx += 1

def metric_exist(metrics, metric):
    idx = 0
    for m in metrics: 
        if m['id'] == metric['id']:
            return True, idx

        idx += 1

    return False, idx


def save_game_metrics(game_metric, idx):
    game_metrics = get_json(f'metrics/game_{idx}.json')
    if game_metrics is None: 
        game_metrics = []
    
    exist, idx_metric = metric_exist(game_metrics, game_metric[0])
    if exist:
        update_game_metrics(game_metrics, game_metric, idx_metric)
    else: 
        game_metrics.extend(game_metric)

    content = json.dumps(game_metrics)

    save_content(f'game_{idx}.json', content)

def save_matchup_metrics(matchup_metric, idx):
    matchup_metrics = get_json(f'metrics/matchup_{idx}.json')
    if matchup_metrics is None: 
        matchup_metrics = []

    exist, idx_metric = metric_exist(matchup_metrics, matchup_metric)
    if exist:
        matchup_metrics[idx_metric] = matchup_metric
    else: 
        matchup_metrics.append(matchup_metric)
    
    content = json.dumps(matchup_metrics)

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