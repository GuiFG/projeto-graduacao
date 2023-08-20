import Metrics
import matplotlib.pyplot as plt 
import json
import numpy as np
from copy import deepcopy

DIRNAME = "graphics/"

class Generator:
    @staticmethod
    def effectiveness_table(results, text_effectivenes):
        names = list(results.keys())
        counts = list(results.values())
        plt.bar(names, counts)
        plt.xticks(rotation=90)
        plt.xlabel('Técnicas')
        plt.ylabel('Efetividade (%)')
        plt.title('Efetividade por técnica')

        plt.savefig(DIRNAME + 'efetividade.pdf', bbox_inches='tight')

        with open('graphics/effectivenes.txt', 'w') as f:
            f.write(text_effectivenes)


    @staticmethod
    def save_result(result):
        with open(DIRNAME + 'resultado.json', 'w') as f:
            data = json.dumps(result)
            f.write(data)
    
    @staticmethod
    def boxplot_execution_time_by_player(data, player):
        fig = plt.figure(figsize=(10, 7))

        ax = fig.add_axes([0, 0, 1, 1])
        ax.boxplot(data)

        plt.title("Tempo execução nas partidas (s) " + player)
        plt.xlabel("Técnica")
        plt.ylabel("Tempo de execução")
        
        fig.savefig(DIRNAME + f"execution_time/{player}.pdf", bbox_inches='tight')
    
    @staticmethod
    def boxplot_execution_time(data):
        fig = plt.figure(figsize=(10, 7))

        names = list(data.keys())
        counts = list(data.values())
 

        ax = fig.add_axes([0, 0, 1, 1])
        ax.boxplot(counts)
        idx = list(range(1, len(names)+1))
        plt.xticks(idx, names)

        plt.title("Tempo execução nas partidas (s)")
        plt.xlabel("Técnicas")
        plt.ylabel("Tempo de execução")
        
        fig.savefig(DIRNAME + "execution_time_overall.pdf", bbox_inches='tight')
    
    @staticmethod
    def save_time_elapsed(time_tournment, time_random):
        with open('graphics/time_tournment.txt', 'w') as f:
            f.write(time_tournment)

        with open('graphics/time_random.txt', 'w') as f:
            f.write(time_random)
    
    @staticmethod
    def save_heat_map(data, players):
        fig = plt.figure(figsize=(8, 6))
        plt.imshow(data, cmap='coolwarm', interpolation='nearest')
        plt.colorbar(label='Número de Vitórias')

        for i in range(len(players)):
            for j in range(len(players)):
                plt.text(j, i, str(data[i][j]), ha='center', va='center', color='black')

        plt.xticks(np.arange(len(players)), players, rotation=45)
        plt.yticks(np.arange(len(players)), players)
        plt.title('Mapa de Calor - Confrontos entre as técnicas')
        plt.tight_layout()

        fig.savefig(DIRNAME + "heat_map.pdf", bbox_inches='tight')


def count_total_wins_player(matchups, player):
    count = 0
    for matchup in matchups:
        if matchup['winner'] == player:
            count += 1
    
    return count

def get_time_of_player(games, player):
    time = []
    for game in games:
        if game['player'] == player:
            time.append(game['time'])
    
    return time

def get_matchups_of_comb(matchups, combination):
    matchups_comb = []
    for matchup in matchups:
        if matchup['player1'] == combination[0] or matchup['player2'] == combination[0]:
            if matchup['player1'] == combination[1] or matchup['player2'] == combination[1]:
                matchups_comb.append(matchup)
    
    return matchups_comb

def get_matchups_of_player(matchups, player):
    matchups_player = []
    for matchup in matchups:
        if matchup['player1'] == player or matchup['player2'] == player:
            matchups_player.append(matchup)
    
    return matchups_player


def generate_execution_time(games, players):
    players_time = {}
    for player in players:
        player_time = get_time_of_player(games, player)
        
        Generator.boxplot_execution_time_by_player(player_time, player)

        players_time[player] = player_time 

    Generator.boxplot_execution_time(players_time)

def get_matchup_result(results, matchup):
    for result in results:
        player1 = matchup[0]
        player2 = matchup[1]
        if player1 in result and player2 in result: 
            return result

def generate_heat_map(matchups, players, results):
    size_matrix = len(players)
    matrix = []
    for i in range(size_matrix):
        lst = []
        for j in range(size_matrix):
            lst.append(0)
        matrix.append(lst)
    
    for matchup in matchups:
        player1 = matchup[0]
        player2 = matchup[1]

        idx1 = players.index(player1)
        idx2 = players.index(player2)

        result = get_matchup_result(results, matchup)
        
        matrix[idx1][idx2] = result[player1]
        matrix[idx2][idx1] = result[player2]

    Generator.save_heat_map(matrix, players)

def generate_result_matchups(matchups, players):
    player_combinations = Metrics.get_matchups(players, True, False)

    results = []
    for combination in player_combinations:
        matchups_combination = get_matchups_of_comb(matchups, combination)
        total = len(matchups_combination)

        player1 = combination[0]
        player2 = combination[1]
        player1_wins = count_total_wins_player(matchups_combination, player1)
        player2_wins = count_total_wins_player(matchups_combination, player2)
        draw = total - (player1_wins + player2_wins)

        results.append({player1: player1_wins, player2: player2_wins, 'draw' : draw, 'total' : total })
    
    generate_heat_map(player_combinations, players, results)

    Generator.save_result(results)

def generate_effectiveness_table(players):
    matchups = Metrics.get_matchups_result(False)
    qlearn_players = [p['name'] for p in Metrics.get_players(2)]
    qlearn_matchups = Metrics.get_json('metrics/qlearn_matchup.json')
    
    all_players = deepcopy(players)
    all_players.extend(qlearn_players)
    matchups.extend(qlearn_matchups)

    effectiveness = {}
    text_result = ''
    for player in all_players:
        matchups_player = get_matchups_of_player(matchups, player)
        match_total = len(matchups_player)
        
        total_wins = count_total_wins_player(matchups_player, player)

        effectiveness[player] = (total_wins / match_total) * 100
        text_result += f'{player}:{effectiveness[player]}\n'

    Generator.effectiveness_table(effectiveness, text_result)

def generate_time_elapsed(matchups):
    matchups_random = Metrics.get_matchups_result(False)

    calculate_time = lambda matchups: sum([matchup['time'] for matchup in matchups])

    time_tournment = calculate_time(matchups)
    time_random = calculate_time(matchups_random)

    time_tournment = Metrics.get_time_from_seconds(time_tournment)
    time_random = Metrics.get_time_from_seconds(time_random)

    Generator.save_time_elapsed(time_tournment, time_random)

def generate_results(tournment=True):
    players = [player['name'] for player in Metrics.get_players()]

    matchups_ids = Metrics.generate_matchups_ids(tournment)
    matchups = Metrics.get_matchups_result(tournment)
    matchups = Metrics.get_results_contains_id(matchups, matchups_ids)

    print('Gerar o tempo total do torneio e do teste de efetividade')
    generate_time_elapsed(matchups)
    
    print('Gerando a tabela de efetividade das tecnicas')
    generate_effectiveness_table(players)
    
    print('Gerando o resultado vitorias/empate/derrota')
    generate_result_matchups(matchups, players)
    
    games = Metrics.get_games_result(tournment)
    games = Metrics.get_results_contains_id(games, matchups_ids)

    print('Gerando boxplot do tempo de execucao de cada tecnica')
    generate_execution_time(games, players)

def main():
    generate_results()
    
main()