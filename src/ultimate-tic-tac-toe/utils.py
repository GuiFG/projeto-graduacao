from smallBoard import SmallBoard

def opponent_player(player):
    return 'O' if player == 'X' else 'X'

def is_terminal_node(board):
    curState = board.getState()

    return curState[0] == 'W' or curState[0] == 'D'

def get_valid_moves(board, prevMove):
    return board.getValidMoves(prevMove)[0]

def count_player(line, player):
    count = 0
    for cell in line:
        if cell == player:
            count += 1
    
    return count

def get_current_small_board(bigBoard, prevMove):
    smallBoardInd = [prevMove[0]%3, prevMove[1]%3]

    return bigBoard.board[smallBoardInd[0]][smallBoardInd[1]]

def get_score_big_board(bigBoard, player):
    smallVer = SmallBoard()
    for i in range(3):
        for j in range(3):
            curState = bigBoard.board[i][j].getState()

            if curState[0] == 'W':
                smallVer.board[i][j] = curState[1]
               
    score = evaluation_small_board(smallVer.board, player)

    return score 

def evaluation_small_board(board, player):
    score = 0
    op = opponent_player(player)

    # verifica a contagem nas linhas
    for row in board:
        count = count_player(row, player)
        op_count = count_player(row, op)

        score += get_score_by_count(count, op_count)

    # verifica a contagem nas colunas
    for col in range(3):
        column = [board[row][col] for row in range(3)]

        count = count_player(column, player)
        op_count = count_player(column, op)

        score += get_score_by_count(count, op_count)

    # verifica a contagem nas diagonais
    diagonal1 = [board[i][i] for i in range(3)]
    diagonal2 = [board[i][2-i] for i in range(3)]

    count = count_player(diagonal1, player)
    op_count = count_player(diagonal1, op)
    score += get_score_by_count(count, op_count)

    count = count_player(diagonal2, player)
    op_count = count_player(diagonal2, op)
    score += get_score_by_count(count, op_count)

    return score
    
    
def get_score_by_count(count, op_count):
    score = 0
    if count == 3:
        score += 100
    elif count == 2 and op_count == 0:
        score += 10
    elif count == 1 and op_count == 0:
        score += 1
    elif op_count == 3:
        score -= 100
    elif count == 0 and op_count == 2:
        score -= 10
    elif count == 0 and op_count == 1:
        score -= 1
    
    return score

def flatten_board(board):
    flattened = [cell for row in board for cell in row]
    return ''.join(flattened) 