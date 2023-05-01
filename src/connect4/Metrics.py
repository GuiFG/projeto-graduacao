import json
import itertools

DIRNAME = 'metrics/'

def get_json(file_name):
    data = None 
    with open(file_name, 'r') as f:
        data = json.load(f) 

    return data
    
def generate_csv(list_json):
    headers = []
    for key in list_json[0].keys():
        headers.append(key)

    values = []
    for item in list_json:
        csv = ''
        for key, value in item.items():
            if key == 'time':
                value = str(value).replace('.', ',')

            csv += f'{value};'
        csv = csv[:len(csv)-1]
        values.append(csv)
    
    result = ';'.join(headers) + '\n'
    result += '\n'.join(values)

    return result

def save_content(file_name, content):
    with open(DIRNAME + file_name, 'w') as f:
        f.write(content)

def save_csv(file_name, csv):
    with open(file_name, 'w') as f:
        f.write(csv)

def get_players(idx=0):
    file_name = f'data/players_{idx}.json' if idx != 0 else 'data/players.json'

    f = open(file_name)
    data = json.load(f)
    f.close()

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

def get_metrics_game(id):
	return { 'id' : id, 'player': '', 'time': 0, 'empty_cells': 0, 'round': 0 }

def save_metrics_matchup(metrics_matchup, idx):
    content = json.dumps(metrics_matchup)
    save_content(f'matchup_{idx}.json', content)

def save_metrics_game(metric_game, idx):
    content = json.dumps(metric_game)
    save_content(f'game_{idx}.json', content)

def save_metrics_matchup_csv(metrics_matchup):
    csv = generate_csv(metrics_matchup)
    save_csv('matchup.csv', csv)
		
def save_metrics_game_csv(metric_game):
    csv = generate_csv(metric_game)
    save_csv('game.csv', csv)

def save_boards(boards):
    data = json.dumps(boards)
    with open('boards', 'w') as f:
        f.write(data)
