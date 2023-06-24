import Metrics
import matplotlib.pyplot as plt 

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


def count_total_wins_player(matchups, player):
    count = 0
    for matchup in matchups:
        if matchup['winner'] == player:
            count += 1
    
    return count

def get_matchups_of_player(matchups, player):
    matchups_player = []
    for matchup in matchups:
        if matchup['player1'] == player or matchup['player2'] == player:
            matchups_player.append(matchup)
    
    return matchups_player

def generate_effectiveness_table(matchups, players):

    effectiveness = {}
    for player in players:
        matchups_player = get_matchups_of_player(matchups, player)
        match_total = len(matchups_player)
        total_wins = count_total_wins_player(matchups_player, player)

        effectiveness[player] = (total_wins / match_total) * 100

    Generator.effectiveness_table(effectiveness)
        
def main():
    set_idx = 0

    players = [player['name'] for player in Metrics.get_players()]
    matchups = Metrics.get_matchups_result(set_idx)

    print('Gerando a tabela de efetividade das tecnicas')
    generate_effectiveness_table(matchups, players)


main()