import matplotlib.pyplot as plt 
import numpy as np
import json 

DIRNAME = "graphics/"

def get_metrics_game():
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

    plt.title("Tempo ação " + player)
    plt.xlabel("Tempo de execução")
    plt.ylabel("Partidas")

    fig.savefig(DIRNAME + f"{player}_execution_time.pdf", bbox_inches='tight')

def generate_mean_time_round_graphic(metrics, player):
    player_metrics = get_metrics_by_player(metrics, player)
    time_round_player = group_time_by_round(player_metrics)
    mean_time = [np.mean(time) for time in time_round_player]

    rounds = range(1, len(mean_time)+1)

    fig = generate_graphic(rounds, mean_time)

    plt.title("Tempo médio por rodada " + player)
    plt.xlabel("Rodadas")
    plt.ylabel("Tempo médio de execução")

    fig.savefig(DIRNAME + f"{player}_mean_time_round.pdf", bbox_inches='tight')

def main(): 
    players = ['PAB_3', 'MCTS_500']

    game_metrics = get_metrics_game()

    for player in players:
        generate_execute_time_graphic(game_metrics, player)
        generate_mean_time_round_graphic(game_metrics, player)

    
main() 