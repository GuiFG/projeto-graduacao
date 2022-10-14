import tictactoe

def valor_maximo(estado, jogador_atual):
    if tictactoe.fimJogo(estado):
        return tictactoe.utilidade(estado, jogador_atual), None
    
    acoes = tictactoe.acoes(estado, jogador_atual)
    utilidade_final = float('-inf')
    melhor_acao = 0
    for acao in acoes:
        novo_estado = tictactoe.resultado(estado, acao, jogador_atual)
        adversario = tictactoe.adversario(jogador_atual)
        utilidade, movimento = valor_minimo(novo_estado, adversario)

        if utilidade > utilidade_final:
            utilidade_final = utilidade
            melhor_acao = acao 
        
    return utilidade_final, melhor_acao

def valor_minimo(estado, jogador_atual):
    if tictactoe.fimJogo(estado):
        return tictactoe.utilidade(estado, jogador_atual), None 
    
    acoes = tictactoe.acoes(estado, jogador_atual)

    utilidade_final = float('inf')
    melhor_acao = 0
    for acao in acoes:
        novo_estado = tictactoe.resultado(estado, acao, jogador_atual)
        adversario = tictactoe.adversario(jogador_atual)
        utilidade, movimento = valor_maximo(novo_estado, adversario)

        if utilidade < utilidade_final:
            utilidade_final = utilidade 
            melhor_acao = acao  
    
    return utilidade_final, melhor_acao


def main():
    tabuleiro = tictactoe.gerarTabuleiro()

    print('calculando o valor maximo')
    vm = valor_maximo(tabuleiro, tictactoe.P1)

    print(vm)



main() 