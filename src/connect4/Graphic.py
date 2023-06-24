import Metrics
import matplotlib.pyplot as plt 
import json

DIRNAME = "graphics/"

class Generator:
    @staticmethod
    def effectiveness_table(results):
        names = list(results.keys())
        counts = list(results.values())
        plt.bar(names, counts)
        plt.xticks(rotation=90)
        plt.xlabel('Técnicas')
        plt.ylabel('Efetividade (%)')
        plt.title('Efetividade por técnica')

        plt.savefig(DIRNAME + 'efetividade.pdf', bbox_inches='tight')

    @staticmethod
    def save_result(result):
        with open(DIRNAME + 'resultado.json', 'w') as f:
            data = json.dumps(result)
            f.write(data)


def count_total_wins_player(matchups, player):
    count = 0
    for matchup in matchups:
        if matchup['winner'] == player:
            count += 1
    
    return count

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
    
    Generator.save_result(results)

def generate_effectiveness_table(players):
    matchups = Metrics.get_matchups_result(0)

    effectiveness = {}
    for player in players:
        matchups_player = get_matchups_of_player(matchups, player)
        match_total = len(matchups_player)
        total_wins = count_total_wins_player(matchups_player, player)

        effectiveness[player] = (total_wins / match_total) * 100

    Generator.effectiveness_table(effectiveness)
        
def main():
    set_idx = 1
    players = [player['name'] for player in Metrics.get_players()]

    print('Gerando a tabela de efetividade das tecnicas')
    # generate_effectiveness_table(players)

    matchups = Metrics.get_matchups_result(set_idx)

    print('Gerando o resultado vitorias/empate/derrota')
    generate_result_matchups(matchups, players)



main()