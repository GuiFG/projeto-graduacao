import numpy as np
import copy 

P1 = 1
P2 = 2 

def verificaLinhas(tabuleiro):
    jogadores = [P1, P2]
    for linha in tabuleiro:    
        iguais = True 
        for jogador in jogadores:
            for posicao in linha: 
                if jogador != posicao: 
                    iguais = False 
                    break 
            if iguais: 
                return True, jogador 
            
    return False, None 

def verificaVencedor(tabuleiro):
    tab = lambda x : x 
    tranposta = lambda x : np.transpose(x) 
    diagonal_principal = lambda x : np.reshape(np.diag(x), (1, len(tabuleiro[0])))
    diagonal_secundaria = lambda x : np.reshape(np.diag(np.fliplr(x)), (1, len(tabuleiro[0])))

    functions = [tab, tranposta, diagonal_principal, diagonal_secundaria]
    for f in functions: 
        novo_tabuleiro = f(tabuleiro)
        existe_vencedor, jogador = verificaLinhas(novo_tabuleiro)

        if existe_vencedor:
            return jogador

    return None

def calculaPosicao(posicao):
    linha = int(posicao / 3) 
    coluna = int(posicao % 3) 

    return linha, coluna

def obtemPosicaoJogada(jogador_atual):
    posicao = 0
    while posicao <= 0 or posicao >= 10:
        posicao = input('posicao jogador ' + str(jogador_atual) + ': ')
        posicao = int(posicao) 
    
    return posicao - 1

def fimJogo(tabuleiro):
    vencedor = verificaVencedor(tabuleiro)

    if vencedor != None:
        return True 
    
    for linha in tabuleiro:
        if 0 in linha:
            return False 
    
    return True 

def atualizarTabuleiro(tabuleiro, posicao, jogador):
    linha, coluna = calculaPosicao(posicao - 1)

    tabuleiro[linha][coluna] = jogador

def resultado(tabuleiro, acao, jogador):
    resultado = copy.deepcopy(tabuleiro)

    atualizarTabuleiro(resultado, acao, jogador)

    return resultado 

def utilidade(tabuleiro, jogador):
    vencedor = verificaVencedor(tabuleiro)

    if vencedor == None: 
        return 0 
    
    if jogador == vencedor:
        return 1
    
    return -1

def adversario(jogador):
    return jogador if jogador == P2 else P2 

def _verificaAcao(valor, jogador):
    oponente = adversario(jogador)

    return valor != oponente and valor != jogador
        

def acoes(tabuleiro, jogador):
    posicoes = []

    total_colunas = len(tabuleiro[0])
    for linha in range(len(tabuleiro)):
        for coluna in range(total_colunas):
            if _verificaAcao(tabuleiro[linha][coluna], jogador):
                posicoes.append(linha * total_colunas + coluna + 1) 
    
    return posicoes 

def gerarTabuleiro():
    return np.zeros((3, 3))

def jogo():
    tabuleiro = gerarTabuleiro()

    vencedor = None 
    jogador_atual = P1
    while not vencedor:
        posicao = obtemPosicaoJogada(jogador_atual)

        atualizarTabuleiro(tabuleiro, posicao)

        vencedor = verificaVencedor(tabuleiro)

        jogador_atual = P1 if jogador_atual == P2 else P2 

        print(tabuleiro)
    
    print('vencedor', vencedor)


