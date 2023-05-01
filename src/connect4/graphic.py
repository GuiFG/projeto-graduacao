import matplotlib.pyplot as plt 
import numpy as np
import json 
from Metrics import get_matchups, get_players

DIRNAME = "graphics/"

def get_matchup_metric(idx):
    with open(f'metrics/matchup_{idx}.json', 'r') as f:
        content = f.read()
    
    return json.loads(content)

def get_game_metric(idx):
    with open(f'metrics/game_{idx}.json', 'r') as f:
        content = f.read()
    
    return json.loads(content)

def get_last_id(metric):
    return metric[len(metric) - 1]['id']

def update_id(metric, offset):
    for m in metric:
        m['id'] += offset

def merge_game_metrics(total):
    game_data = []
    last_id = 0
    for i in range(total):
        game_metric = get_game_metric(i + 1)
        update_id(game_metric, last_id)
        last_id = get_last_id(game_metric)
        
        game_data.extend(game_metric)

    return game_data

def merge_matchup_metrics(total):
    matchup_data = []
    last_id = 0
    for i in range(total):
        matchup_metric = get_matchup_metric(i + 1)
        update_id(matchup_metric, last_id)
        last_id = get_last_id(matchup_metric)
        
        matchup_data.extend(matchup_metric)

    return matchup_data

def get_game_metrics():
    with open('metrics/game.json', 'r') as f:
        content = f.read()

    return json.loads(content)

def generate_graphic(x_values, y_values):
    xpoints = np.array(x_values)
    ypoints = np.array(y_values)

    fig = plt.figure(figsize=(10, 7))
    plt.plot(xpoints, ypoints)

    return fig

def generate_boxplot_graphic(data, player):
    fig = plt.figure(figsize=(10, 7))

    ax = fig.add_axes([0, 0, 1, 1])
    ax.boxplot(data)

    plt.title("Tempo execução por partidas (s)" + player)
    plt.xlabel("Partidas")
    plt.ylabel("Tempo de execução")
    return fig 

def get_metrics_by_player(metrics, player):
    return [y for y in metrics if y['player']==player]

def group_time_by_id(metrics):
    values = set(map(lambda x: x['id'], metrics))
    return [[m['time'] for m in metrics if m['id']==x] for x in values]

def group_time_by_round(metrics):
    values = set(map(lambda x: x['round'], metrics))
    return [[m['time'] for m in metrics if m['round']==x] for x in values]

def generate_execute_time_graphic(metrics, player):
    player_metrics = get_metrics_by_player(metrics, player)
    time_player = group_time_by_id(player_metrics)

    fig = generate_boxplot_graphic(time_player, player)

    fig.savefig(DIRNAME + f"execution_time/{player}.pdf", bbox_inches='tight')

def generate_mean_time_round_graphic(metrics, player):
    player_metrics = get_metrics_by_player(metrics, player)
    time_round_player = group_time_by_round(player_metrics)
    mean_time = [np.mean(time) for time in time_round_player]

    rounds = range(1, len(mean_time)+1)

    fig = generate_graphic(rounds, mean_time)

    plt.title("Tempo médio por rodada (s)" + player)
    plt.xlabel("Rodadas")
    plt.ylabel("Tempo médio de execução")

    fig.savefig(DIRNAME + f"mean_time_round/{player}.pdf", bbox_inches='tight')

def get_matchups_names(players):
    m1 = get_matchups(players, False)
    
    matchups = []
    for m in m1:
        matchup = []
        for i in range(len(m)):
            if '10000' not in m[i]['name']:
                matchup.append(m[i]['name'])
        
        if len(matchup) == 2:
            matchups.append(matchup)
    
    return matchups

def get_metrics_from_matchup(metrics, matchup):
    results = []
    for metric in metrics:
        player1 = matchup[0]
        player2 = matchup[1]

        if player1 == metric['player1'] and player2 == metric['player2']:
            results.append(metric)
            continue 

        if player1 == metric['player2'] and player2 == metric['player1']:
            results.append(metric)
    
    return results 

def get_total_wins_by_player(metrics, player):
    total = 0
    for metric in metrics:
        if metric['winner'] == player:
            total += 1
    
    return total
        
def get_results_from_matchups(metrics, matchups):
    results = []
    for matchup in matchups:
        results_matchup = get_metrics_from_matchup(metrics, matchup)
        
        player1 = get_total_wins_by_player(results_matchup, matchup[0])
        player2 = get_total_wins_by_player(results_matchup, matchup[1])
        
        result = { matchup[0]: player1, matchup[1]: player2, 'draw': len(results_matchup) - player1 - player2 }

        results.append(result)

    return results
        
def generate_table_result(metrics, players):
    matchups = get_matchups_names(players)

    results = get_results_from_matchups(metrics, matchups)

    with open('graphics/results.json', 'w') as f:
        content = json.dumps(results)
        f.write(content)

    # TODO: montar figura da tabela de resultado

def main(): 
    players = get_players()
    players_names = [player['name'] for player in players]

    game_metrics = merge_game_metrics(4)
    matchup_metrics = merge_matchup_metrics(4)

    generate_table_result(matchup_metrics, players)
    for player in players_names:
        generate_execute_time_graphic(game_metrics, player)
        generate_mean_time_round_graphic(game_metrics, player)
        
    
main() 