#!/usr/bin/env python

import random
import time


BOARD_STR = '''%(1)s|%(2)s|%(3)s\n-----\n%(4)s|%(5)s|%(6)s\n-----\n%(7)s|%(8)s|%(9)s'''
BOARD_KEY = '''1|2|3\n-----\n4|5|6\n-----\n7|8|9'''


class Board(object):

    def __init__(self):
        self.positions = {
            '1': ' ', '2': ' ', '3': ' ',
            '4': ' ', '5': ' ', '6': ' ',
            '7': ' ', '8': ' ', '9': ' ',
        }
        self.board = BOARD_STR % self.positions
        self.winning_positions = ((1, 2, 3),
                                  (4, 5, 6),
                                  (7, 8, 9),
                                  (1, 4, 7),
                                  (2, 5, 8),
                                  (3, 6, 9),
                                  (1, 5, 9),
                                  (3, 5, 7))

    def __str__(self):
        return self.board

    def update_board(self, positions):
        self.board = BOARD_STR % positions

    def update_positions(self, player, position):
        self.positions[str(position)] = player
        self.update_board(self.positions)
        winner = False
        for w in self.winning_positions:
            for i, d in enumerate(w):
                if self.positions[str(d)] != player:
                    break
                if i == (len(w) - 1):
                    winner = True
                    break
            if winner:
                break
        return winner


def generate_opponent_move(board, opponent):
    # TODO: Make opponent never lose.
    enemy = 'X' if opponent == 'O' else 'O'
    possible_moves = get_possible_moves(board)
    if len(possible_moves) > 0:
        possibly_good_moves = []
        for w in board.winning_positions:
            score = 0
            enemy_in_winning_pos = True if len(
                [x for x in w if board.positions[str(x)] == enemy]) > 0 else False
            if enemy_in_winning_pos:
                continue
            for i, d in enumerate(w):
                if board.positions[str(d)] == opponent:
                    score += 1
                if score >= 2:
                    for j in w:
                        if board.positions[
                                str(j)] == ' ' and str(j) in possible_moves:
                            return j
                elif score >= 1 and str(d) in possible_moves:
                    possibly_good_moves.append(d)
        for w in board.winning_positions:
            enemy_danger = []
            for i, d in enumerate(w):
                if board.positions[str(d)] == enemy:
                    enemy_danger.append([d, w])
            if len(enemy_danger) >= 2:
                for x in enemy_danger[0][1]:
                    if board.positions[
                            str(x)] == ' ' and str(x) in possible_moves:
                        return x
        if possibly_good_moves:
            return random.choice(possibly_good_moves)
        if str(5) in possible_moves:
            return 5
        return random.choice(possible_moves)


def get_possible_moves(board):
    possible_moves = []
    for k, v in board.positions.items():
        if v == ' ':
            possible_moves.append(k)
    return possible_moves


def play(board):
    print
    print('Welcome to Tic-tac-toe!')
    print
    response = raw_input('Would you like to play as X or O? ')
    while response not in ('x', 'X', 'o', 'O'):
        response = raw_input('Please enter either X or O. Try again: ')
    player = response.upper()
    opponent = 'X' if player == 'O' else 'O'
    print
    print(BOARD_KEY)
    print
    game_over = False
    winner = False
    loser = False
    while not game_over and not winner and not loser:
        possible_moves = get_possible_moves(board)
        if len(possible_moves) == 0:
            game_over = True
            break
        response = raw_input(
            'Please enter the appropriate number to make your move: ')
        while not response.isdigit() or not int(response) in range(1, 10):
            response = raw_input(
                'You must enter a digit between 1 and 9! '
                'Enter the appropriate number to make your move: ')
        while response not in get_possible_moves(board):
            response = raw_input('%s is already taken! Try again: ' % response)
        winner = board.update_positions(player, response)
        print
        print(board)
        print
        if winner or len(get_possible_moves(board)) == 0:
            break
        print('OK, my turn...\n')
        time.sleep(1)
        loser = board.update_positions(
            opponent,
            generate_opponent_move(
                board,
                opponent))
        print(board)
        print
        if loser or len(get_possible_moves(board)) == 0:
            break
    if winner:
        print("You're a winner!")
    elif loser:
        print('Oh noze! You lost!')
    else:
        print("It's a tie.")


def main():
    board = Board()
    try:
        play(board)
    except KeyboardInterrupt:
        print('\n\nBye!')


if __name__ == '__main__':
    main()
