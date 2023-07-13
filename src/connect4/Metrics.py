import json
import itertools
import os
import copy
from os import listdir
from os.path import isfile, join

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

def divmod(value, divisor):
    quocient = value // divisor
    remainder = value % divisor

    return int(quocient), int(remainder)

def get_time_from_seconds(seconds_time):
    minutes, seconds = divmod(seconds_time, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return f'{days}d:{hours}h:{minutes}m:{seconds}s\n{seconds_time}'

def save_train_time(time, idx):
    seconds = time.total_seconds()
    train_time = get_time_from_seconds(seconds)
    
    with open(f'metrics/qtrain_{idx}.txt', 'w') as f:
        f.write(train_time)

def get_matchups_result(tournment=True):
    return get_result_json('matchup', tournment)
    
def get_games_result(tournment=True):
    return get_result_json('game', tournment)

def get_result_json(type, tournment):
    folder = 'metrics'
    if not tournment:
        return get_json(folder + f'/{type}_random.json')

    check = lambda f: isfile(join(folder, f)) and type in f and 'random' not in f

    onlyfiles = [f for f in listdir(folder) if check(f)]
    
    matchups = []
    for file in onlyfiles:
        json = get_json(folder + '/' + file)
        
        matchups.extend(json)
    
    return matchups

def generate_matchups_ids(tournment=True, game_total=50):
    players = get_players()
    matchups = get_matchups(players, tournment)

    matchups_id = []
    for i in range(len(matchups)):
        matchup = matchups[i]
        for j in range(game_total):
            matchup_id = f'{i+1}/{len(matchups)}{matchup[0]["name"]}_X_{matchup[1]["name"]}_{j+1}'
            
            matchups_id.append(matchup_id)

            if matchup[0]['type'] == 'ALFA_BETA' and matchup[1]['type'] == 'ALFA_BETA':
                break
    
    return matchups_id

def exists_id(list, id):
    for item in list: 
        if item['id'] == id: 
            return True 
    
    return False

def get_results_contains_id(results, ids):
    final_result = []

    for result in results:
        id_result = result['id'] 
        if id_result in ids:
            if not exists_id(final_result, id_result):
                final_result.append(result)
                
    return final_result

def get_players(idx=0):
    file_name = f'data/players_{idx}.json' if idx != 0 else 'data/players.json'

    f = open(file_name)
    data = json.load(f)
    f.close()

    return data 