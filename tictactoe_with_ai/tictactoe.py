from random import choice as random_choice
from typing import Dict, List, Tuple, Sequence


def output_board(board: Dict[int, str]) -> None:
    """
    Print current board marks.
    """
    board_figures = tuple(board.values())
    board_rows = (board_figures[i:i + 3] for i in range(0, 9, 3))
    output_rows = (['|'] + list(row) + ['|'] for row in board_rows)
    center = '\n'.join(' '.join(row) for row in output_rows)
    top = bottom = '---------'
    board_snapshot = '\n'.join((top, center, bottom))

    print(board_snapshot)


def validate_convert_coordinates(board: Dict[int, str], coordinates: str):
    """
    Accepts user coordinates and verify them.
    """
    try:
        x_str, y_str = coordinates.split()
    except ValueError:
        print('You should enter numbers!')
        return False

    if not x_str.isnumeric() and not y_str.isnumeric():
        print('You should enter numbers!')
        return False

    x, y = [int(n) for n in (x_str, y_str)]
    if not all((1 <= x <= 3, 1 <= y <= 3)):
        print('Coordinates should be from 1 to 3!')
        return False

    # Convert coordinates to key of board dict
    key = None
    if x == 1:
        if y == 1:
            key = 6
        elif y == 2:
            key = 3
        elif y == 3:
            key = 0
    elif x == 2:
        if y == 1:
            key = 7
        elif y == 2:
            key = 4
        elif y == 3:
            key = 1
    if x == 3:
        if y == 1:
            key = 8
        elif y == 2:
            key = 5
        elif y == 3:
            key = 2

    if key is None:
        raise SystemExit('Error while assigning coordinates in validate_convert_coordinates()')

    if board[key] != ' ':
        print('This cell is occupied! Choose another one!')
        return False

    return key


Cell = Tuple[int, str]
Line = Tuple[Cell, Cell, Cell]
Board_lines = Tuple[Line, Line, Line, Line, Line, Line, Line, Line]


def get_board_lines(board: Dict[int, str]) -> Board_lines:
    board_inline = tuple((k, v) for k, v in board.items())
    row1, row2, row3 = (board_inline[i:i+3] for i in range(0, 9, 3))
    col1, col2, col3 = ((board_inline[i], board_inline[i + 3], board_inline[i + 6]) for i in range(3))
    diag1 = (board_inline[0], board_inline[4], board_inline[8])
    diag2 = (board_inline[2], board_inline[4], board_inline[6])
    lines = (row1, row2, row3, col1, col2, col3, diag1, diag2)
    return lines


def get_empty_cells(board: Dict[int, str]) -> Sequence[int]:
    empty_cells = tuple(k for k, v in board.items() if v == ' ')

    return empty_cells


def mark_board(board: Dict[int, str], board_key: int, player_figure: str) -> None:
    """
    Mark board with user's figure.
    """
    board[board_key] = player_figure


def determine_result(board, player):
    """
    If there are the same figures in either any row, column or diagonal -- 'figure' wins.
    """
    board_lines = get_board_lines(board)  # chek for strike

    for line in board_lines:
        if [tt[1] for tt in line].count(player) == 3:
            # print(f"{figure} wins")
            return True


def get_coordinates(player_type: str, board: Dict[int, str], figure: str) -> int:

    def human_choice():
        user_input = input('Enter the coordinates:').strip()
        board_key = validate_convert_coordinates(board, user_input)
        if board_key is not False:
            return board_key
        else:
            return human_choice()

    def ai_easy(board):
        empty_cells = get_empty_cells(board)
        ai_choice = random_choice(empty_cells)

        return ai_choice

    def ai_medium(board, ai_figure, easy=ai_easy):
        lines = get_board_lines(board)

        # win in one move
        for line in lines:
            line_values = [tt[1] for tt in line]
            if line_values.count(ai_figure) == 2 and line_values.count(' ') == 1:
                ai_choice = [tt[0] for tt in line if tt[1] == ' '][0]
                return ai_choice

        # block opponent winning
        for line in lines:
            line_values = [tt[1] for tt in line]
            if line_values.count(ai_figure) == 0 and line_values.count(' ') == 1:
                ai_choice = [tt[0] for tt in line if tt[1] == ' '][0]
                return ai_choice

        return easy(board)

    def ai_hard(board, player_1, player_2):
        ...


    if player_type == 'user':
        return human_choice()
    elif player_type == 'easy':
        return ai_easy(board)
    elif player_type == 'medium':
        return ai_medium(board, figure)
    elif player_type == 'hard':
        return ai_hard


def play(player_1: str, player_2: str, game_started: bool = False) -> None:
    """
    Guide user through the game.
    """
    player_1_figure = 'X'
    player_2_figure = 'O'
    board = {int(n): ' ' for n in list('012345678')}

    if not game_started:  # show board once
        output_board(board)
        # game_started = True

    while True:
        position_to_mark = get_coordinates(player_1, board, player_1_figure)
        mark_board(board, position_to_mark, player_1_figure)
        output_board(board)

        if determine_result(board, player_1_figure):
            print(f"{player_1_figure} wins")
            break

        elif not get_empty_cells(board):
            print('Draw')
            break

        else:
            position_to_mark = get_coordinates(player_2, board, player_2_figure)
            mark_board(board, position_to_mark, player_2_figure)
            output_board(board)

            if determine_result(board, player_2_figure):
                print(f"{player_2_figure} wins")
                break

            elif not get_empty_cells(board):
                print('Draw')
                break
    print('Game finished!')


while True:

    command = input('Input command:').strip()

    if command == 'exit':
        break

    elif command.startswith('start'):
        # verify initial players
        player_a = player_b = None
        try:
            player_a, player_b = command.split()[1:3]
        except ValueError:
            print('Bad parameters!')

        if all((player_a, player_b)):
            
            play(player_a, player_b)

    else:
        print('Bad parameters!')
