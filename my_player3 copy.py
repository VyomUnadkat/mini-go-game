import random
import sys
from read import readInput
from write import writeOutput
from copy import deepcopy
import timeit
import math
import argparse
from collections import Counter
from copy import deepcopy

from host import GO



def get_input(go, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''        
    possible_placements = []
    for i in range(go.size):
        for j in range(go.size):
            if go.valid_place_check(i, j, piece_type, test_check = True):
                possible_placements.append((i,j))

    if not possible_placements:
        return "PASS"
    else:
        return random.choice(possible_placements)


N = 5
piece_type, previous_board, board = readInput(N)
set_board(piece_type, previous_board, board)
player = RandomPlayer()
action = player.get_input(go, piece_type)
writeOutput(action)