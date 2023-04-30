import matplotlib.pyplot as plt 
import numpy as np
import json 

DIRNAME = "graphics/"

def get_game_metrics():
    with open('metrics/game.json', 'r') as f:
        content = f.read()

    return json.loads(content)

def generate_random_graphic():
    np.random.seed(10)

    data_1 = np.random.normal(100, 10, 200)
    data_2 = np.random.normal(90, 20, 200)
    data_3 = np.random.normal(80, 30, 200)
    data_4 = np.random.normal(70, 40, 200)
    data = [data_1, data_2, data_3, data_4]

    fig = plt.figure(figsize=(10, 7))

    ax = fig.add_axes([0, 0, 1, 1])

    ax.boxplot(data)

    fig.savefig(DIRNAME + "foo.pdf", bbox_inches='tight')


def generate_graphic(data, player):
    fig = plt.figure(figsize=(10, 7))

    ax = fig.add_axes([0, 0, 1, 1])
    ax.boxplot(data)

    plt.title("Tempo ação " + player)
    plt.xlabel("Tempo de execução")
    plt.ylabel("Partidas")

    return fig 

def get_metrics_by_player(metrics, player):
    return [y for y in metrics if y['player']==player]

def group_time_by_id(metrics):
    values = set(map(lambda x: x['id'], metrics))
    return [[m['time'] for m in metrics if m['id']==x] for x in values]

def generate_execute_time_graphic(metrics, player):
    player_metrics = get_metrics_by_player(metrics, player)
    time_player = group_time_by_id(player_metrics)

    fig = generate_graphic(time_player, player)

    fig.savefig(DIRNAME + f"{player}.pdf", bbox_inches='tight')
    

def main(): 
    players = ['PAB_6', 'MCTS_10000']

    game_metrics = get_game_metrics()

    for player in players:
        generate_execute_time_graphic(game_metrics, player)

    
main() 