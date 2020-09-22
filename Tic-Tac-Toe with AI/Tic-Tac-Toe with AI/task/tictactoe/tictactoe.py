import random

MEANINGFUL_POSITIONS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def print_field(state):
    print('---------')
    print('|', state[0], state[1], state[2], '|')
    print('|', state[3], state[4], state[5], '|')
    print('|', state[6], state[7], state[8], '|')
    print('---------')
    

def position(coordinates):
    return 9 - 3 * (int(coordinates[1]) - 1) - (4 - int(coordinates[0]))
    

def state_analyze(state):
    wins = ''
    for pos in MEANINGFUL_POSITIONS:
        if state[pos[0]] == state[pos[1]] == state[pos[2]] and state[pos[0]] != ' ':
            wins += state[pos[0]]
    if wins == '' and ' ' in state:
        return 'Game not finished'
    elif wins == '' and ' ' not in state:
        return 'Draw'
    elif wins == 'X':
        return 'X wins'
    elif wins == 'O':
        return 'O wins'
    else:
        return 'Wrong state!'
        

def validate_input(x_y, state):
    if x_y[0].isdigit() and x_y[1].isdigit:
        if 0 < int(x_y[0]) < 4 and 0 < int(x_y[1]) < 4:
            if state[position(x_y)] == ' ':
                return True
            else:
                print('This cell is occupied! Choose another one!')
        else:
            print('Coordinates should be from 1 to 3!')
    else:
        print('You should enter numbers!')
    return False
    

def easy(state):
    print('Making move level "easy"')
    empty_cell_list = [i for i, item in enumerate(state) if item == ' ']
    state[random.choice(empty_cell_list)] = x_or_o(state)
    return state


def medium(state):
    print('Making move level "medium"')
    xo = x_or_o(state)
    ox = 'X' if xo == 'O' else 'O'
    if is_winning(state, xo):
        state[int(is_winning(state, xo))] = xo
        return state
    elif is_winning(state, ox):
        state[int(is_winning(state, ox))] = xo
        return state
    empty_cell_list = [i for i, item in enumerate(state) if item == ' ']
    state[random.choice(empty_cell_list)] = xo
    return state
    

def hard(state):
    print('Making move level "hard"')
    xo = x_or_o(state)
    new_state = state[:]
    moves = {}
    for idx in empty_indexes(state):
        new_state[idx] = xo
        moves[idx] = min_max(new_state, xo)
        new_state[idx] = ' '
    best_move = [-10, -10]
    for move in moves:
        if moves[move] > best_move[1]:
            best_move[0] = move
            best_move[1] = moves[move]
    print(moves, best_move)
    state[best_move[0]] = xo
    return state


def min_max(state, sign):
    xo = x_or_o(state)
    if len(empty_indexes(state)) == 0:
        return 0
    win = min_max_win(state, sign)
    if win:
        return win
    scores = []
    new_state = state[:]
    for idx in empty_indexes(state):
        new_state[idx] = xo
        scores.append(min_max(new_state, sign))
        new_state[idx] = ' '
    return max(scores) if xo == sign else min(scores)


def min_max_win(state, sign):
    for pos in MEANINGFUL_POSITIONS:
        if state[pos[0]] == state[pos[1]] == state[pos[2]]:
            if state[pos[0]] == sign:
                return 1
            elif state[pos[0]] != ' ':
                return -1
            return False


def empty_indexes(state):
    return [i for i, idx in enumerate(state) if idx == ' ']


def is_winning(state, xo):
    for pos in MEANINGFUL_POSITIONS:
        line = state[pos[0]] + state[pos[1]] + state[pos[2]]
        if line.count(xo) == 2 and ' ' in line:
            print('ага', pos[line.index(' ')])
            return str(pos[line.index(' ')])
    return 
    

def user(state):
    while True:
        x_y = input('Enter the coordinates: ').split()
        if validate_input(x_y, state):
            state[position(x_y)] = x_or_o(state)
            return state
    

def x_or_o(state):
    if state.count('X') == state.count('O'):
        return 'X'
    elif state.count('X') > state.count('O'):
        return 'O'
    

def main():
    possible_players = {'user': user, 'easy': easy, 'medium': medium, 'hard': hard}
    while True:
        command = input('Input command: ').split()
        if command[0] == 'start' and command[1] in possible_players and command[2] in possible_players:
            state = [' '] * 9
            while True:
                state = possible_players[command[1]](state)
                print_field(state)
                print()
                if state_analyze(state) != 'Game not finished':
                    print(state_analyze(state))
                    break
                state = possible_players[command[2]](state)
                print_field(state)
                print()
                if state_analyze(state) != 'Game not finished':
                    print(state_analyze(state))
                    break
        elif command[0] == 'exit':
            break
        else:
            print('Bad parameters!')

main()

