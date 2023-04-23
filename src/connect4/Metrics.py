import json

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

def save_csv(file_name, csv):
    with open(file_name, 'w') as f:
        f.write(csv)


def get_players():
	f = open('players.json')
	data = json.load(f)
	f.close()

	return data 

def get_metrics_game(id):
	return { 'id' : id, 'player': '', 'time': 0, 'empty_cells': 0, 'round': 0 }

def save_metrics_matchup(metrics_matchup):
    csv = generate_csv(metrics_matchup)
    save_csv('matchup.csv', csv)
		
def save_metrics_game(metric_game):
    csv = generate_csv(metric_game)
    save_csv('game.csv', csv)
		
		
